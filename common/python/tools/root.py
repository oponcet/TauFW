# Author: Izaak Neutelings (July 2023)
from __future__ import print_function # for python3 compatibility
from past.builtins import basestring # for python2 compatibility
import os, re
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import gROOT, gSystem, TFile, TNamed, TH2
from TauFW.common.tools.log import LOG
from TauFW.common.tools.utils import unpacklistargs, islist
TNamed.__repr__ = lambda o: "<%s(%r,%r) at %s>"%(o.__class__.__name__,o.GetName(),o.GetTitle(),hex(id(o))) # overwrite default representation
#TH1.__repr__ = lambda o: "<%s(%r,%r,%g,%g,%g) at %s>"%(o.__class__.__name__,o.GetName(),o.GetTitle(),o.GetXaxis().GetNbins(),o.GetXaxis().GetXmin(),o.GetXaxis().GetXmax(),id(o))


def rootname(*args):
  """Convert list of TNamed objects to list of names."""
  if len(args)==1 and not islist(args[0]):
    obj   = args[0]
    names = obj.GetName() if hasattr(obj,'GetName') else str(obj) # return string
  else:
    args = unpacklistargs(args)
    names = [getname(o) for o in args ] # return list of strings
  return names
  

def rootrepr(*args,**kwargs):
  """Create representation string for ROOT objects."""
  if len(args)==1 and not islist(args[0]):
    obj   = args[0]
    if hasattr(obj,'GetName') and hasattr(obj,'GetTitle'):
      name = "%r,%r"%(obj.GetName(),obj.GetTitle())
      if kwargs.get('bins',False) and hasattr(obj,'GetXaxis'): # include histogram binning
        name += "%g,%g,%g"%(obj.GetXaxis().GetNbins(),obj.GetXaxis().GetXmin(),obj.GetXaxis().GetXmax())
        if isinstance(obj,TH2): # add y axis binning
          name += "%g,%g,%g"%(obj.GetYaxis().GetNbins(),obj.GetYaxis().GetXmin(),obj.GetYaxis().GetXmax())
      if kwargs.get('id',False): # include hex id
        names = "<%s(%s) at %s>"%(obj.__class__.__name__,name,hex(id(obj)))
      else:
        names = "%s(%s)"%(obj.__class__.__name__,name)
    else: # default representation
      names = repr(obj)
  else: # list of objects
    args = unpacklistargs(args)
    names = [rootrepr(o) for o in args ] # return list of strings
    if kwargs.get('join',True):
      names = '['+', '.join(names)+']' # return string of list
  return names
  

def ensureTFile(filename,option='READ',compress=None,verb=0):
  """Open TFile, checking if the file in the given path exists."""
  if isinstance(filename,basestring):
    if option=='READ' and ':' not in filename and not os.path.isfile(filename):
      LOG.throw(IOError,'File in path "%s" does not exist!'%(filename))
      exit(1)
    if compress==None:
      file = ROOT.TFile.Open(filename,option,filename)
    else:
      compresslevel, compressalgo = parsecompression(compress)
      file = ROOT.TFile.Open(filename,option,filename,compresslevel)
      if compressalgo!=None:
        file.SetCompressionAlgorithm(compressalgo)
      LOG.verb("ensureTFile: Using compression algorithm %s with level %s"%(compressalgo,compresslevel),verb+2,1)
    if not file or file.IsZombie():
      LOG.throw(IOError,'Could not open file by name %r!'%(filename))
    LOG.verb("Opened file %s..."%(filename),verb,1)
  else:
    file = filename
    if not file or (hasattr(file,'IsZombie') and file.IsZombie()):
      LOG.throw(IOError,'Could not open file %r!'%(file))
  return file
  

def parsecompression(compression='LZMA:9'):
  # https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/framework/postprocessor.py
  level = 0    # ROOT.RCompressionSetting.EDefaults.EValues.kUseCompiledDefault
  algo  = None # ROOT.RCompressionSetting.EAlgorithm.kUseGlobal
  if compression!=None:
    if isinstance(compression,int):
      level = compression
    elif isinstance(compression,str) and compression.isdigit():
      level = int(compression)
    elif isinstance(compression,str) and compression.count(':')==1:
      #ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
      (algo, level) = compression.split(":")
      level = int(level)
      if 'LZMA' in algo:
        algo = ROOT.ROOT.kLZMA
      elif 'ZLIB' in algo:
        algo = ROOT.ROOT.kZLIB
      elif 'LZ4' in algo:
        algo = ROOT.ROOT.kLZ4
      else:
        raise RuntimeError("Unsupported compression %s"%algo)
    else:
      LOG.error("Compression setting must be a string of the form 'algo:level', e.g. 'LZMA:9'. "
                "Got %r"%(compression))
  return level, algo
  

def ensureTDirectory(file,dirname,cd=True,split=True,verb=0):
  """Make TDirectory in a file (or other TDirectory) if it does not yet exist."""
  if split and '/' in dirname: # split subdirectory structure to ensure they exist recursively
    dirs = dirname.strip('/').split('/')
    topdir = '/'.join(dirs[:-1])
    dirname = dirs[-1]
    file = ensureTDirectory(file,topdir,cd=False,verb=verb) # create top dirs recursively
  directory = file.GetDirectory(dirname)
  if not directory:
    directory = file.mkdir(dirname)
    if verb>=1:
      print(">>> Created directory %s in %s"%(dirname,file.GetPath()))
  if cd:
    directory.cd()
  return directory
  

def gethist(file,histname,setdir=True,close=None,retfile=False,fatal=True,warn=True):
  """Get histogram from a given file."""
  if isinstance(file,basestring): # open TFile
    file = ensureTFile(file)
    if close==None:
      close = not retfile
  if not file or file.IsZombie():
    LOG.throw(IOError,"Could not open file by name %r"%(filename))
  hist = file.Get(histname)
  if not hist:
    if fatal:
      LOG.throw(IOError,"Did not find histogram %r in file %r!"%(histname,file.GetPath()))
    elif warn:
      LOG.warn("Did not find histogram %r in file %r!"%(histname,file.GetPath()))
  if (close or setdir) and isinstance(hist,ROOT.TH1):
    hist.SetDirectory(0)
  if close: # close TFile
    file.Close()
  if retfile:
    return file, hist
  return hist
  

def loadmacro(macro,fast=False,opt='+O',verb=0):
  """Load C++ macro via ROOT."""
  if fast: # try to fast load library, assuming it is already exist and the macro is unchanged
    # NOTE! If you changed the macro, you should set fast=False, or remove the old library
    macrolib = re.sub(r"(\w+)\.([Cc][CcXx]{0,2})$",r"\1_\2.so",macro)
    if os.path.exists(macrolib):
      try:
        LOG.verb("loadmacro: Loading library %s..."%(macrolib),verb,1)
        return gSystem.Load(macrolib) # faster than compiling each time
      except: # loading library failed => compile
        LOG.warn("loadmacro: Failed to loading library %s for %s... Will try to compile from scratch..."%(macrolib,macro))
    elif verb>=1:
      print(">>> loadmacro: Could not find library %s! Will try to compile from scratch..."%(macrolib))
  line = ".L %s%s"%(macro,opt)
  if verb>=2:
    print(">>> loadmacro: Compiling macro %s (processing %r)..."%(macro,line))
  elif verb>=1:
    print(">>> loadmacro: Compiling macro %s..."%(macro))
  return gROOT.ProcessLine(line)
  
