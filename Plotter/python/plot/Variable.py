# -*- coding: utf-8 -*-
# Author: Izaak Neutelings (2017)
import re
from array import array
from math import floor
from copy import copy, deepcopy
from ROOT import TH1D, TH2D
from TauFW.Plotter.plot.string import *
from TauFW.Plotter.plot.Context import getcontext
from TauFW.Plotter.plot.utils import LOG, isnumber, islist, ensurelist, unpacklistargs


class Variable(object):
  """
  Variable class to:
   - hold all relevant information of a variable that will be plotted;
       var name, filename friendly name, LaTeX friendly title, binning, ...
   - allow for variable binning into TH1
   - allow for contextual binning, i.e. depending on channel/selection/...
   - easy string conversions: filename, LaTeX, ...
   - analysis-specific operations: applying variations, ...
   
  Initialize as
    var = Variable('x',100,0,200)
    var = Variable('x','x title',100,0,200)
    var = Variable('x',[0,10,50,100,200])   # pass bin edges for variable binning
    ...
  """
  
  def __init__(self, name, *args, **kwargs):
    strings, bins     = [ ], [ ]
    for arg in args:
      if isinstance(arg,str): strings.append(arg)
      else: bins.append(arg)
    self.name         = name # variable name: branch in tree or mathematical expression of branch(es), to be used in draw command
    self._name        = name # backup for addoverflow
    self.title        = strings[0] if strings else self.name
    filename          = strings[1] if len(strings)>=2 else makefilename(self.name.replace('/','_')) # file-safe name
    self.title        = kwargs.get('title',       self.title     ) # for plot axes
    self.filename     = kwargs.get('fname',       filename       ) # file-friendly name for files & histograms
    self.filename     = kwargs.get('filename',    self.filename  ) # alias
    self.filename     = self.filename.replace('$NAME',self.name).replace('$VAR',filename).replace(
                                              '[','-').replace(']','').replace('.','p') #.replace('$FILE',self.filename)
    self.tag          = kwargs.get('tag',         ""             )
    self.units        = kwargs.get('units',       True           ) # for plot axes
    self.latex        = kwargs.get('latex',       True           ) # for plot axes
    self.nbins        = None
    self.min          = None
    self.max          = None
    self.edges        = None # bin edges
    self.cut          = kwargs.get('cut',         ""             ) # extra cut when filling histograms
    self.weight       = kwargs.get('weight',      ""             ) # extra weight when filling histograms (MC only)
    self.dataweight   = kwargs.get('dataweight',  ""             ) # extra weight when filling histograms for data
    self.setbins(*bins)
    self.dividebins   = kwargs.get('dividebins',  self.hasvariablebins() ) # divide each histogram bins by it bin size (done in Plot.draw)
    self.data         = kwargs.get('data',        True           ) # also draw this variable for observed data
    self.flag         = kwargs.get('flag',        ""             ) # flag, e.g. 'up', 'down', ...
    self.binlabels    = kwargs.get('labs',        [ ]            ) # alias
    self.binlabels    = kwargs.get('labels',      self.binlabels ) # bin labels for x axis
    self.ymin         = kwargs.get('ymin',        None           )
    self.ymax         = kwargs.get('ymax',        None           )
    self.rmin         = kwargs.get('rmin',        None           )
    self.rmax         = kwargs.get('rmax',        None           )
    self.ratiorange   = kwargs.get('rrange',      None           )
    self.logx         = kwargs.get('logx',        False          )
    self.logy         = kwargs.get('logy',        False          )
    self.ymargin      = kwargs.get('ymarg'  ,     None           ) # margin between hist maximum and plot's top
    self.ymargin      = kwargs.get('ymargin',     self.ymargin   ) # margin between hist maximum and plot's top
    self.logyrange    = kwargs.get('logyrange',   None           ) # log(y) range from hist maximum to ymin
    self.position     = kwargs.get('pos',         ""             ) # legend position
    self.position     = kwargs.get('position',    self.position  ) # legend position
    self.ncols        = kwargs.get('ncol',        None           ) # number of legend columns
    self.ncols        = kwargs.get('ncols',       self.ncols     ) # number of legend columns
    #self.plot         = kwargs.get('plots',       True           )
    self.opts         = kwargs.get('opts',        { }            ) # general dictionary of extra user options
    self.only         = kwargs.get('only',        [ ]            ) # only plot for these patterns
    self.veto         = kwargs.get('veto',        [ ]            ) # do not plot for these patterns
    self.blindcuts    = kwargs.get('blind',       ""             ) # string for blind cuts to blind data
    self._addoverflow = kwargs.get('addof',       False          ) # add overflow to last bin
    self._addoverflow = kwargs.get('addoverflow', self._addoverflow ) # add overflow to last bin
    if self.latex:
      self.title = makelatex(self.title,units=self.units)
      if 'ctitle' in kwargs:
        for ckey, title in kwargs['ctitle'].items():
          kwargs['ctitle'][ckey] = makelatex(title,units=self.units)
    if self.only:
      self.only = ensurelist(self.only)
    if self.veto:
      self.veto = ensurelist(self.veto)
    if self.binlabels and len(self.binlabels)<self.nbins:
      LOG.warn("Variable.init: len(binlabels)=%d < %d=nbins"%(len(self.binlabels),self.nbins))
    if self._addoverflow:
      self.addoverflow()
    if islist(self.blindcuts): # assume tuple of pair of floats: (lower cut, upper cut)
      LOG.insist(len(self.blindcuts)==2,"Variable.init: blind cuts must be a string, or a pair of floats! Got: %s"%(self.blindcuts,))
      self.blindcuts = self.blind(*self.blindcuts)
    self.ctxtitle    = getcontext(kwargs, self.title,     key='ctitle',   regex=True ) # context-dependent title
    self.ctxbins     = getcontext(kwargs, args,           key='cbins',    regex=True ) # context-dependent binning
    self.ctxposition = getcontext(kwargs, self.position,  key='cpos',     regex=True ) # context-dependent position
    self.ctxncols    = getcontext(kwargs, self.ncols,     key='cncols',   regex=True ) # context-dependent ncols
    self.ctxblind    = getcontext(kwargs, self.blindcuts, key='cblind',   regex=True ) # context-dependent blind limits
    self.ctxymargin  = getcontext(kwargs, self.ymargin,   key='cymargin', regex=True ) # context-dependent ymargin
    self.ctxcut      = getcontext(kwargs, self.cut,       key='ccut',     regex=True ) # context-dependent cuts
    self.ctxweight   = getcontext(kwargs, self.weight,    key='cweight',  regex=True ) # context-dependent cuts
      
  
  @property
  def xmin(self): return self.min
  @xmin.setter
  def xmin(self,value): self.xmin = value
  
  @property
  def xmax(self): return self.max
  @xmax.setter
  def xmax(self,value): self.xmax = value
  
  def __str__(self):
    """Returns string representation of Variable object."""
    return self.name
  
  def __repr__(self):
    """Returns string representation of Variable object."""
    #return '<%s.%s("%s","%s",%s,%s,%s)>'%(self.__class__.__module__,self.__class__.__name__,self.name,self.title,self.nbins,self.xmin,self.xmax)
    return '<%s(%r,%r,%s,%s,%s) at %s>'%(self.__class__.__name__,self.name,self.title,self.nbins,self.xmin,self.xmax,hex(id(self)))
  
  def __iter__(self):
    """Start iteration over variable information."""
    for i in [self.name,self.nbins,self.min,self.max]:
      yield i
  
  def __gt__(self,ovar):
    """Order alphabetically."""
    return self.filename > ovar.filename
  
  def clone(self,*args,**kwargs):
    """Shallow copy."""
    verbosity = LOG.getverbosity(self,kwargs)
    strargs = tuple([a for a in args if isinstance(a,str)]) # string arguments: name, title
    binargs = tuple([a for a in args if not isinstance(a,str)])
    if verbosity>=2:
      print(">>> Variable.clone: Old strargs=%r, binargs=%r, kwargs=%r"%(strargs,binargs,kwargs))
    if not strargs:
      strargs = (kwargs.pop('name',self.name),kwargs.pop('title',self.title)) # default name
    if len(strargs)==1:
      strargs += (kwargs.pop('title',self.title),) # default title
    if not binargs: # get binning
      binargs = self.getbins()
      cut = kwargs.get('cut',None)
      if cut and self.ctxbins: # change context based on extra cut
        bins = self.ctxbins.getcontext(cut) # get bins in this context
        if binargs!=bins and verbosity>=2:
          print(">>> Variable.clone: Changing binning %r -> %r because of context %r"%(binargs,bins,cut))
        binargs = bins
      if isinstance(binargs,list): # assume list is bin edges
        binargs = (binargs,) # force list in tuple
    newdict = self.__dict__.copy()
    if 'fname' in kwargs:
      kwargs['filename'] = kwargs['fname']
    if 'filename' in kwargs:
      kwargs['filename'] = kwargs['filename'].replace('$FILE',self.filename)
    if 'tag' in kwargs:
      kwargs['filename'] = kwargs.get('filename',self.filename)+kwargs['tag']
    if kwargs.get('combine',True) and 'weight' in kwargs and self.weight:
      kwargs['weight'] = joinweights(kwargs['weight'],self.weight)
    for key in list(kwargs.keys())+['name','title','nbins','min','max','bins']: # prevent overwrite: set via newargs
      newdict.pop(key,None)
    if 'cbins' in kwargs:
      newdict.pop('ctxbins')
    elif self.ctxbins:
      newdict['ctxbins'] = self.ctxbins.clone() # create new dictionary
      newdict['ctxbins'].default = binargs # change default context
    newargs = strargs+binargs
    if verbosity>=2:
      print(">>> Variable.clone: New args=%r, kwargs=%r"%(newargs,kwargs))
    newvar = Variable(*newargs,**kwargs)
    newvar.__dict__.update(newdict)
    if verbosity>=2:
      print(">>> Variable.clone: Cloned %r -> %r"%(self,newvar))
    return newvar
  
  def issame(self,ovar,**kwargs):
    """Compare Variable objects."""
    return self.name==ovar.name and self.getbins()==ovar.getbins()
  
  def printbins(self,filename=False):
    """Print the variable name with the binning."""
    if filename:
      return '%s(%s,%s,%s)'%(self.filename,self.nbins,self.xmin,self.xmax)
    else:
      return '%s(%s,%s,%s)'%(self.name,self.nbins,self.xmin,self.xmax)
  
  def setbins(self,*args):
    """Set binning: (N,min,max), or bins if it is set"""
    LOG.verb('Variable.setbins: setting binning to %s'%(args,),level=2)
    numbers = [a for a in args if isnumber(a)]
    bins    = [a for a in args if islist(a)] #and all(isinstance(x,(int,float)) for x in a)
    if len(numbers)==3:
      self.nbins = numbers[0]
      self.min   = numbers[1]
      self.max   = numbers[2]
      self.edges = None
    elif len(bins)>0:
      edges      = list(bins[0])
      if any(x<edges[i] for i, x in enumerate(edges[1:])): # check sorting
        LOG.warn("Variable.setbins: Bin edges for %r are not sorted: edges=%r"%(self.name,edges))
      if len(edges)!=len(set(edges)): # check for duplicates
        LOG.warn("Variable.setbins: Bin edges for %r has duplicate values: edges=%r"%(self.name,edges))
      self.nbins = len(edges)-1
      self.min   = edges[0]
      self.max   = edges[-1]
      self.edges = edges
    else:
      LOG.throw(IOError,'Variable: bad arguments "%s" for binning!'%(args,))
  
  def getbins(self,full=False):
    """Get binning: (N,xmin,xmax), or bins if it is set"""
    if self.hasvariablebins():
      return self.edges
    elif full: # get binedges
      return [self.min+i*(self.max-self.min)/self.nbins for i in range(self.nbins+1)]
    else:
      return (self.nbins,self.min,self.max)
  
  def getedge(self,i):
    """Get edge. 0=first edge, nbins+1=last edge"""
    LOG.insist(i>=0,"getedge: Number of bin edge has to be >= 0! Got: %s"%(i))
    LOG.insist(i<=self.nbins+1,"getedge: Number of bin edge has to be <= %d! Got: %s"%(self.nbins+1,i))
    if self.hasvariablebins():
      return self.edges[i]
    return self.min+i*(self.max-self.min)/self.nbins
  
  def hasvariablebins(self):
    """True if bins is set."""
    return self.edges!=None
  
  def hasintbins(self):
    """True if binning is integer."""
    width = (self.max-self.min)/self.nbins
    return self.edges==None and int(self.min)==self.min and int(self.max)==self.max and width==1
  
  def match(self, *terms, **kwargs):
    """Match search terms to the variable's name and title."""
    return match(terms,[self.name,self.title])
  
  def changecontext(self,*args,**kwargs):
    """Change the contextual title, binning or position for a set of arguments, if it is available"""
    verbosity = LOG.getverbosity(self,kwargs)
    if self.ctxtitle:
      title = self.ctxtitle.getcontext(*args)
      if title!=None:
        if verbosity>=3:
          print(">>> Variable.changecontext: ctxtitle=%s, args=%r"%(self.ctxtitle.context,args))
          print(">>> Variable.changecontext: title=%r -> %r"%(self.title,title))
        self.title = title
      elif verbosity>=3:
        print(">>> Variable.changecontext: ctxtitle=%s, args=%r, title=%r (no change)"%(self.ctxtitle.context,args,self.title))
    if self.ctxbins:
      bins = self.ctxbins.getcontext(*args)
      if isinstance(bins,list):
        bins = (bins,)
      if bins!=None:
        if verbosity>=3:
          print(">>> Variable.changecontext: ctxbins=%s, args=%r"%(self.ctxbins.context,args))
          print(">>> Variable.changecontext: bins=%r -> %r"%(self.edges,bins))
        elif verbosity>=3:
          print(">>> Variable.changecontext: ctxbins=%s, args=%r, bins=%r (no change)"%(self.ctxbins.context,args,self.edges))
        self.setbins(*bins)
      if self._addoverflow:
        self.addoverflow() # in case the last bin changed
      self.dividebybinsize = kwargs.get('dividebybinsize',self.hasvariablebins())
    if self.ctxposition:
      position = self.ctxposition.getcontext(*args)
      if position!=None:
        self.position = position
    if self.ctxncols:
      ncols = self.ctxncols.getcontext(*args)
      if ncols!=None:
        self.ncols = ncols
    if self.ctxymargin:
      ymargin = self.ctxymargin.getcontext(*args)
      if ymargin!=None:
        self.ymargin = ymargin
    if self.ctxcut:
      cut = self.ctxcut.getcontext(*args)
      if cut!=None:
        if verbosity>=3:
          print(">>> Variable.changecontext: ctxcut=%s, args=%r"%(self.ctxcut.context,args))
          print(">>> Variable.changecontext: cut=%r -> %r"%(self.cut,cut))
        self.cut = cut
      elif verbosity>=3:
        print(">>> Variable.changecontext: ctxcut=%s, args=%r, cut=%r (no change)"%(self.ctxcut.context,args,self.cut))
    if self.ctxweight:
      weight = self.ctxweight.getcontext(*args)
      if weight!=None:
        self.weight = weight
  
  def plotfor(self,*strings,**kwargs):
    """Check if given string is filtered (with 'only') or vetoed (with 'veto') for this variable."""
    verbosity = LOG.getverbosity(self,kwargs)
    strings   = list(strings)
    LOG.verbose('Variable.plotfor: strings=%s, veto=%s, only=%s'%(strings,self.veto,self.only),verbosity,level=2)
    if not self.data and kwargs.get('data',False):
      LOG.verbose('Variable.plotfor: Do not draw "%r" for data'%(self.name),verbosity,level=2)
      return False # do not draw for data
    for i, string in enumerate(strings):
      if string.__class__.__name__=='Selection':
        string     = string.selection
        strings[i] = string
      for searchterm in self.veto:
        if re.search(searchterm,string):
          LOG.verbose('Variable.plotfor: Regex match of string "%s" to "%s"'%(string,searchterm),verbosity,level=2)
          return False
    if len(self.only)==0:
      return True
    for i, string in enumerate(strings):
      for searchterm in self.only:
        if re.search(searchterm,string):
          LOG.verbose('Variable.plotfor: Regex match of string "%s" to "%s"'%(string,searchterm),verbosity,level=2)
          return True
    return False
  
  def unpack(self):
    return (self.name,self.nbins,self.min,self.max)
  
  def getnametitle(self,name=None,title=None,tag=None):
    """Help function to create name and title."""
    if tag and tag[0]!='_':
      tag   = '_'+tag
    if name==None:
      name  = self.filename+tag
    if title==None:
      title = self.title
    name = name.replace('(','').replace(')','').replace('[','').replace(']','').replace(',','-').replace('.','p')
    return name, title
  
  def gethistmodel(self,name=None,title=None,tag=None):
    """Create arguments for initiation TH1D (useful for RDataFrame.Histo1D)."""
    # https://root.cern/doc/master/structROOT_1_1RDF_1_1TH1DModel.html
    name, title = self.getnametitle(name,title,tag)
    if self.hasvariablebins(): # variable bin width
      model = (name,title,self.nbins,array('d',list(self.edges)))
    else: # constant/fixed bin width
      model = (name,title,self.nbins,self.min,self.max)
    return model
  
  def gethistmodel2D(self,yvariable,name=None,title=None,tag=None):
    """Create arguments for initiation TH2D (useful for RDataFrame.Histo2D)."""
    # https://root.cern/doc/master/structROOT_1_1RDF_1_1TH1DModel.html
    model = self.gethistmodel(name,title,tag)
    if yvariable.hasvariablebins(): # variable bin width
      model += (yvariable.nbins,array('d',list(yvariable.edges)))
    else: # constant/fixed bin width
      model += (yvariable.nbins,yvariable.min,yvariable.max)
    return model
  
  def gethist(self,name=None,title=None,tag=None,**kwargs):
    """Create a 1D histogram."""
    poisson = kwargs.get('poisson', False       )
    sumw2   = kwargs.get('sumw2',   not poisson )
    xtitle  = kwargs.get('xtitle',  self.title  )
    ytitle  = kwargs.get('ytitle',  None        )
    hist    = TH1D(*self.gethistmodel(name,title,tag))
    if poisson:
      hist.SetBinErrorOption(TH1D.kPoisson)
    elif sumw2:
      hist.Sumw2()
    hist.GetXaxis().SetTitle(xtitle)
    if ytitle:
      hist.GetYaxis().SetTitle(ytitle)
    #hist.SetDirectory(0)
    return hist
  
  def gethist2D(self,yvariable,name=None,title=None,tag=None,**kwargs):
    """Create a 2D histogram where xvar=self."""
    poisson = kwargs.get('poisson', False           )
    sumw2   = kwargs.get('sumw2',   not poisson     )
    xtitle  = kwargs.get('xtitle',  self.title      )
    ytitle  = kwargs.get('ytitle',  yvariable.title )
    ztitle  = kwargs.get('ztitle',  None            )
    doption = kwargs.get('option',  'COLZ'          ) # draw option
    hist    = TH2D(*self.gethistmodel2D(yvariable,name,title,tag))
    if poisson: # for observed data (asymmetric uncertainty bars)
      hist.SetBinErrorOption(TH2D.kPoisson)
    elif sumw2: # for weighted MC events
      hist.Sumw2()
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    if ztitle:
      hist.GetZaxis().SetTitle(ztitle)
    hist.SetOption(doption) # default drawing option
    return hist
  
  def drawcmd(self,name=None,tag="",bins=False,**kwargs):
    """Create variable expression for the Tree.Draw method."""
    histname, title = self.getnametitle(name,None,tag)
    varname = self.name
    if kwargs.get('undoshift',False): # remove up/down tags from varname
      varname = undoshift(varname)
    if bins:
      dcmd = "%s >> %s(%d,%s,%s)"%(varname,histname,self.nbins,self.min,self.max)
    else:
      dcmd = "%s >> %s"%(varname,histname)
    return dcmd
  
  def drawcmd2D(self,yvar,name=None,tag="",bins=False):
    """Create variable expression for the Tree.Draw method."""
    histname, title = self.getnametitle(name,None,tag)
    if bins:
      dcmd = "%s:%s >> %s(%d,%s,%s,%d,%s,%s)"%(yvar.name,self.name,histname,self.nbins,self.min,self.max,yvar.nbins,yvar.min,yvar.max)
    else:
      dcmd = "%s:%s >> %s"%(yvar.name,self.name,histname)
    return dcmd
  
  def draw(self,tree,cut,name=None,title=None,**kwargs):
    """Create and fill histogram from tree."""
    hist   = self.gethist(name,title,**kwargs)
    option = kwargs.get('option','gOff')
    dcmd   = self.drawcmd(name,**kwargs)
    tree.Draw(dcmd,cut,option)
    return hist
  
  def shift(self,vshift,vars=None,**kwargs):
    """Create new variable with a shift tag added to its name."""
    if len(vshift)>0 and vshift[0]!='_':
      vshift = '_'+vshift
    if vars: # shift only the variables in this list
      newname = shift(self.name,vshift,vars,**kwargs)
    else: # simply add shift at the end
      newname = self.name+vshift
    newvar = deepcopy(self)
    newvar.name = newname # overwrite name
    if not kwargs.get('keepfile',False) and self.name!=newname:
      newvar.filename += vshift # overwrite file name
    return newvar
  
  def shiftjme(self,jshift,title=None,**kwargs):
    """Create new variable with a shift tag added to its name."""
    verbosity = LOG.getverbosity(self,kwargs)
    if len(jshift)>0 and jshift[0]!='_':
      jshift = '_'+jshift
    newname  = shiftjme(self.name,jshift,**kwargs)
    newvar   = deepcopy(self)
    LOG.verb("Variable.shiftjme: name = %r -> %r"%(self.name,newname),verbosity,2)
    newvar.name = newname # overwrite name
    if title:
      newvar.title = title
    elif self.title[-1] in [']',')']: # insert shift tag into title before units
      newvar.title = re.sub(r"^(.*\s*)([[(][^()\[\]]+[)\]])$",r"\1%s \2"%(jshift.strip('_')),self.title)
    else: # add shift tag to title
      newvar.title += ' '+jshift.strip('_')
    LOG.verb("Variable.shiftjme: title = %r -> %r"%(self.title,newvar.title),verbosity,2)
    if not kwargs.get('keepfile',False) and self.name!=newname:
      newvar.filename += jshift # overwrite file name
      LOG.verb("Variable.shiftjme: filename = %r -> %r"%(self.filename,newvar.filename),verbosity,2)
    if newvar.cut:
      newvar.cut = shiftjme(newvar.cut,jshift,**kwargs)
      LOG.verb("Variable.shiftjme: extra cut = %r -> %r"%(self.cut,newvar.cut),verbosity,2)
    if newvar.ctxcut:
      for key, cut in newvar.ctxcut.context.items():
        newvar.ctxcut.context[key] = shiftjme(cut,jshift,**kwargs)
      newvar.ctxcut.default = shiftjme(newvar.ctxcut.default,jshift,**kwargs)
    return newvar
  
  def shiftname(self,vshift,**kwargs):
    """Shift name and return string only (without creating new Variable object)."""
    return shift(self.name,vshift,**kwargs)
  
  def blind(self,bmin=None,bmax=None,blinddict=None,**kwargs):
    """Return selection string that blinds some window (bmin,bmax),
    making sure the cuts match the bin edges of some (nbins,xmin,xmax) binning."""
    verbosity = LOG.getverbosity(self,kwargs)
    if isinstance(blinddict,dict) and self._name in blinddict:
      bmin, bmax = blinddict[self._name]
    if bmin==None or bmax==None: # use own blinding cut strings
      return self.blindcuts
    if bmax<bmin:
      bmax, bmin = bmin, bmax
    LOG.insist(bmax>bmin,'Variable.blind: %r has window a = %s <= %s = b !'%(self._name,bmin,bmax))
    blindcut = ""
    xlow, xhigh = bmin, bmax
    nbins, xmin, xmax = self.nbins, self.min, self.max
    if self.hasvariablebins(): # variable bin width
      edges = self.edges
      for xval in edges:
        if xval>bmin: break # edge above lower cut
        xlow = xval
      for xval in reversed(edges):
        if xval<bmax: break # edge below upper cut
        xhigh = xval
    else: # fixed bin width
      binwidth = float(xmax-xmin)/nbins
      if xmin<bmin<xmax:
        bin, rem = divmod(bmin-xmin,binwidth)
        xlow = bin*binwidth # first edge below or equal to lower cut
      if xmin<bmax<xmax:
        bin, rem = divmod(bmax-xmin,binwidth)
        if rem>0:
          bin += 1
        xhigh = bin*binwidth # first edge above or equal to lower cut
    blindcut = "(%s<%s || %s<%s)"%(self.name,xlow,xhigh,self.name)
    LOG.verb('Variable.blind: blindcut = %r for a (%s,%s) window and (%s,%s,%s) binning'%(blindcut,bmin,bmax,nbins,xmin,xmax),verbosity,2) 
    return blindcut
  
  def addoverflow(self,frac=0.90,**kwargs):
    """Modify variable name in order to add the overflow to the last bin."""
    verbosity = LOG.getverbosity(self,kwargs)
    if self.hasvariablebins():
      xmax  = self.edges[-1]
      width = xmax-self.edges[-2]
    else:
      xmax  = self.max
      width = (xmax-self.min)/float(self.nbins)
    thres = xmax - (1.-frac)*width # threshold for minimum min(x,threshold)
    # NOTE: the min(x,thres) function causes errors in RDataFrame when x and thres are different data types,
    # The ternary operation (x<xmax?x:thres) should not affect performance unless x is a complicated expression
    ###self.name = "min(%s,%s)"%(self._name,thres) # causes errors
    self.name = "%s<%s?%s:%s"%(self._name,xmax,self._name,thres) # (x<xmax?x:thres)
    LOG.verb("Variable.addoverflow: %r -> %r for binning '%s'"%(self._name,self.name,self.getbins()),verbosity,2)
    return self.name
  
Var = Variable # shortened alias


def wrapvariable(*args,**kwargs):
  """Help function to wrap variable arguments into a Variable object."""
  if len(args)==4 or len(args)==5:
    return Variable(args) # (xvar,nxbins,xmin,xmax)
  elif len(args)==1 and isinstance(args[0],Variable):
    return args[0]
  LOG.warn('wrapvariable: Could not unpack arguments %r to a Variable object. Returning None.'%args)
  return None
  

def unpack_variable_bins(*args,**kwargs):
  """Help function to unpack variable arguments to return variable name, number of bins,
  minumum and maximum x axis value."""
  if len(args)==4:
    return args # (xvar,nxbins,xmin,xmax)
  elif len(args)==1 and isintance(args[0],Variable):
    return args[0].unpack()
  LOG.throw(IOError,'unpack_variable_bins: Could not unpack arguments "%s" to a Variable object.'%args)
  

def ensurevar(*args,**kwargs):
  """Help function to ensure arguments are one Variable object:
      - xvar, nxbins, xmin, xmax (str, int, float, float)
      - xvar, xbins (str, list)
      - var (str)
  """
  args = unpacklistargs(args)
  if len(args)==4:
    return Variable(*args) # (xvar,nxbins,xmin,xmax)
  elif len(args)==2 and islist(args[1]):
    return Variable(*args)  # (xvar,xbins)
  elif len(args)==1 and isinstance(args[0],Variable):
    return args[0]
  else:
    LOG.throw(IOError,'unpack_variable_args: Could not unpack arguments %s, len(args)=%d. Returning None.'%(args,len(args)))
  
