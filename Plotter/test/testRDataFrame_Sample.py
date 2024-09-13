#! /usr/bin/env python3
# Author: Izaak Neutelings (November 2023)
# Description: Unit tests of RDataFrame implementation in Sample
import os, re
import time
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True # to avoid conflict with argparse
from TauFW.common.tools.file import ensuredir
from TauFW.common.tools.string import took
from TauFW.Plotter.sample.ResultDict import ResultDict, RDF # for containing RDataFRame RResultPtr
from TauFW.Plotter.sample.SampleSet import SampleSet
from TauFW.Plotter.sample.utils import join
from TauFW.Plotter.plot.utils import LOG
from TauFW.Plotter.plot.Plot import Plot, Var
from TauFW.Plotter.plot.Plot2D import Plot2D
from TauFW.Plotter.plot.Stack import Stack
from TauFW.Plotter.plot.Selection import Sel
from pseudoSamples import getsamples


# CUSTUM FUNCTIONs to mimic C++ macro
ROOT.gInterpreter.Declare("""
  Float_t dmmap(Int_t dm) {
    return dm==0 ? 0 : (dm==1 || dm==2) ? 1 : dm==10 ? 2 : dm==11 ? 3 : 4;
  };
""")
def dmmap(dm='dm_2'): # python version
  return f"{dm}==0 ? 0 : ({dm}==1 || {dm}==2) ? 1 : {dm}==10 ? 2 : {dm}==11 ? 3 : 4"


###def test_SampleSet_MultiDraw(sampleset,variables,selections,outdir="plots/test",split=False,tag="",method=None,parallel=True,verb=0):
###  """Test SampleSet.gethists with MultiDraw for comparison. NOTE: SampleSet.gethists removed in this branch."""
###  LOG.header("test_SampleSet_MultiDraw")
###  
###  # GET HISTS
###  if sampleset.datasample:
###    start  = time.time(), time.process_time() # wall-clock & CPU time
###    stacks = { } # { selection : { variable: Stack } }
###    nhists = 0
###    for selection in selections:
###      start2 = time.time(), time.process_time() # wall-clock & CPU time
###      results = sampleset.getstack(variables,selection,method=method,split=split,parallel=parallel,verb=verb)
###      print(f">>> test_SampleSet_MultiDraw: Running of {len(results)} results with MultiDraw for one selection took {took(*start2)} with {ROOT.GetThreadPoolSize()} threads")
###      stacks[selection] = results # add nested dictionary
###      nhists += sum(len(s.exphists)+(1 if s.datahist else 0) for s in results)
###    print(f">>> test_SampleSet_MultiDraw: Running of {nhists} results with MultiDraw for all selections took {took(*start)} with {ROOT.GetThreadPoolSize()} threads")
###    
###    # PLOT
###    for selection in selections:
###      for stack in stacks[selection]:
###        #stack = stacks[selection][variable].getstack()
###        stack.draw(ratio=True)
###        stack.drawlegend()
###        stack.drawtext("Test SampleSet.getstack MultiDraw",selection.title)
###        stack.saveas(f"{outdir}/testRDF_stack_$VAR_{selection.filename}{tag}_MultiDraw.png")
###        stack.close(keep=parallel) # avoid segmentation fault for parallel
###    
###  else: # no stack
###    start  = time.time(), time.process_time() # wall-clock & CPU time
###    hists  = { } # { selection : { variable: HistSet.exp } }
###    nhists = 0
###    for selection in selections:
###      variables_ = [ ] 
###      for variable in variables:
###        if variable.plotfor(selection) and selection.plotfor(variable):
###          variable.changecontext(selection.selection)
###          variables_.append(variable)
###      start2 = time.time(), time.process_time() # wall-clock & CPU time
###      results = sampleset.gethists(variables_,selection,split=split,parallel=parallel,verb=verb)
###      print(f">>> test_SampleSet_MultiDraw: Running of {len(results)} results with MultiDraw for one selection took {took(*start2)} with {ROOT.GetThreadPoolSize()} threads")
###      hists[selection] = { v: results[v].exp for v in results} # add nested dictionary
###      nhists += sum(len(results[v].exp) for v in results)
###    print(f">>> test_SampleSet_MultiDraw: Running of {nhists} results with MultiDraw for all selections took {took(*start)} with {ROOT.GetThreadPoolSize()} threads")
###    
###    # PLOT
###    for selection in selections:
###      for variable in hists[selection]:
###        variable.changecontext(selection.selection)
###        plot = Plot(variable,hists[selection][variable]) # create Plot object
###        plot.draw(ratio=True)
###        plot.drawlegend()
###        plot.drawtext("Test SampleSet.gethists MultiDraw",selection.title)
###        plot.saveas(f"{outdir}/testRDF_plot_{variable.filename}_{selection.filename}{tag}_MultiDraw.png")
###        plot.close()


def test_SampleSet_RDF(sampleset,variables,selections,outdir="plots/test",method=None,split=False,tag="",verb=0):
  """Test SampleSet.gethists with RDataFrame."""
  LOG.header("test_SampleSet_RDF")
  
  # GET HISTS
  dot = f"{outdir}/graph_$NAME.dot"
  sampleset.addalias('ptsum',"pt_1+pt_2",verb=verb+1) # test alias / AddRDFColumn
  hists = sampleset.gethists(variables,selections,method=method,split=split,dot=dot,verb=verb)
  
  # PLOT
  for selection in hists:
    for variable in hists[selection]:
      variable.changecontext(selection.selection)
      if sampleset.datasample:
        #stack = Stack(variable,hists[selection][variable].data,hists[selection][variable].exp)
        stack = hists[selection][variable].getstack(context=selection,verb=verb-2) # create Stack object
        stack.draw(ratio=True)
        stack.drawlegend()
        stack.drawtext("Test SampleSet.gethists RDataFrame",selection.title)
        stack.saveas(f"{outdir}/testRDF_stack_{variable.filename}_{selection.filename}{tag}_RDF.png")
        stack.close()
      else:
        plot = Plot(variable,hists[selection][variable].exp) # create Plot object
        plot.draw(ratio=True)
        plot.drawlegend()
        plot.drawtext("Test SampleSet.gethists RDataFrame",selection.title)
        plot.saveas(f"{outdir}/testRDF_plot_{variable.filename}_{selection.filename}{tag}_RDF.png")
        plot.close()
  

def test_getrdframe(samples,variables,selections,outdir="plots/test",split=False,tag="",rungraphs=True,verb=0):
  """Test Sample.getrdframe."""
  LOG.header("test_getrdframe")
  
  # PREPARE RDataFrames
  start    = time.time(), time.process_time() # wall-clock & CPU time
  res_dict = ResultDict()
  rdf_dict = { }
  for sample in samples:
    res_dict += sample.getrdframe(variables,selections,split=split,rdf_dict=rdf_dict,verb=verb+1)
  print(f">>> test_getrdframe: Booking of {len(res_dict)} results took {took(*start)}")
  if verb>=2:
    print(f">>> test_getrdframe: Got res_dict:")
    res_dict.display()
  
  # RUN RDataFrame events loops to fill histograms
  # NOTE: RDataFrame parallelizes over TTree clusters
  # The pseudo samples may only have a single clusters per file,
  # so the gain will be small: check tree->Print("clusters")
  dot = f"{outdir}/graph_$NAME.dot"
  res_dict.run(graphs=rungraphs,rdf_dict=rdf_dict,dot=dot,verb=verb+1)
  
  # PLOT
  for selection, variable, samples, hists in res_dict.iterhists():
    plot = Plot(variable,hists)
    plot.draw(ratio=True)
    plot.drawlegend()
    plot.drawtext("Test Sample.getrdframe",selection.title)
    plot.saveas(f"{outdir}/testRDF_plot_{variable.filename}_{selection.filename}{tag}.png")
    plot.close()
  

def test_getrdframe2D(sample,variables,selections,outdir="plots/test",split=False,tag="",rungraphs=True,verb=0):
  """Test Sample.getrdframe for 2D."""
  LOG.header("test_getrdframe2D")
  
  # PREPARE RDataFrames
  start    = time.time(), time.process_time() # wall-clock & CPU time
  rdf_dict = { }
  res_dict = sample.getrdframe(variables,selections,rdf_dict=rdf_dict,split=split,verb=verb+1)
  print(f">>> test_getrdframe2D: Booking of {len(res_dict)} results took {took(*start)}")
  if verb>=2:
    print(f">>> test_getrdframe2D: Got res_dict:")
    res_dict.display()
  dot = f"{outdir}/graph2d_$NAME.dot"
  res_dict.run(graphs=rungraphs,rdf_dict=rdf_dict,dot=dot,verb=verb+1)
  
  # PLOT
  for selection, variable, samples, hists in res_dict.iterhists():
    #print(variable,hists)
    #hist = hists.gethists(single=True)
    xvar, yvar = variable
    plot = Plot2D(xvar,yvar,hists[0])
    plot.draw()
    plot.drawtext("Test Sample.getrdframe 2D",selection.title)
    plot.saveas(f"{outdir}/testRDF_plot2D_{yvar.filename}_vs_{xvar.filename}_{selection.filename}_{sample.name}{tag}.png")
    plot.close()
    

def test_getsumw(sample,selections,split=False,rungraphs=True,verb=0):
  """Test Sample.getsumw."""
  LOG.header("test_getsumw")
  res_dict = sample.getsumw(selections,split=split,verb=verb)
  #print(res_dict)
  if split:
    TAB = LOG.table("%15.2f  %-10s   %r")
    TAB.printheader("Sum-of-weights","Sample","Selection"+' '*50)
    for selection in res_dict:
      for sample in res_dict[selection]:
        TAB.printrow(res_dict[selection][sample],sample.name,selection.selection)
  else:
    TAB = LOG.table("%15.2f   %r")
    TAB.printheader("Sum-of-weights","Selection"+' '*50)
    for selection in res_dict:
      TAB.printrow(res_dict[selection],selection.selection)
    

def test_getmean(sample,variables,selections,split=False,sumw=False,rungraphs=True,verb=0):
  """Test Sample.getmean."""
  LOG.header("test_getmean")
  res_dict = sample.getmean(variables,selections,split=split,sumw=sumw,verb=verb)
  #print(res_dict)
  if split:
    TAB = LOG.table("%15.4f  %-10r %-10s   %r")
    TAB.printheader("Mean","Variable","Sample","Selection"+' '*50)
    for selection in res_dict:
      for variable in res_dict[selection]:
        vstr = variable if isinstance(variable,str) else variable.name
        for sample in res_dict[selection][variable]:
          TAB.printrow(res_dict[selection][variable][sample],vstr,sample.name,selection.selection)
  else:
    TAB = LOG.table("%15.4f  %-10s   %r")
    TAB.printheader("Mean","Variable","Selection"+' '*50)
    for selection in res_dict:
      for variable in res_dict[selection]:
        vstr = variable if isinstance(variable,str) else variable.name
        TAB.printrow(res_dict[selection][variable],vstr,selection.selection)
  

def test_gethist(sample,variables,selections,outdir="plots/test",split=False,tag="",verb=0):
  """Test Sample.gethist."""
  LOG.header("test_gethist")
  hist_dict = sample.gethist(variables,selections,split=split,verb=verb)
  #hist_dict = sample.gethist(variables,selections,split=split,alias={'ptsum':"pt_1+pt_2"},verb=verb)
  for selection in hist_dict:
    for variable in hist_dict[selection]:
      if split: # convert dict { sample: hist } to list of histograms
        hists = list(hist_dict[selection][variable].values())
      else: # retrieve single histogram
        hists = hist_dict[selection][variable]
      plot = Plot(variable,hists)
      plot.draw(ratio=True)
      plot.drawlegend()
      plot.drawtext("Test Sample.gethist RDataFrame",selection.title)
      plot.saveas(f"{outdir}/testRDF_plot_{variable.filename}_{selection.filename}_{sample.name}{tag}.png")
      plot.close()
  

def test_gethist2D(sample,variables,selections,outdir="plots/test",split=False,tag="",verb=0):
  """Test Sample.gethist2D."""
  LOG.header("test_gethist2D")
  hist_dict = sample.gethist2D(variables,selections,split=split,verb=verb)
  #hist_dict = sample.gethist2D(variables,selections,split=split,alias={'ptsum':"pt_1+pt_2"},verb=verb)
  for selection in hist_dict:
    for varpair in hist_dict[selection]:
      xvar, yvar = varpair
      if split: # convert dict { sample: hist } to list of histograms
        hist = list(hist_dict[selection][varpair].values())[0]
      else: # retrieve single histogram
        hist = hist_dict[selection][varpair]
      plot = Plot2D(xvar,yvar,hist)
      plot.draw()
      plot.drawtext("Test Sample.gethist2D RDataFrame",selection.title)
      plot.saveas(f"{outdir}/testRDF_plot2D_{yvar.filename}_vs_{xvar.filename}_{selection.filename}_{sample.name}{tag}.png")
      plot.close()
  

def main(args):
  verbosity = args.verbosity
  reuse     = args.reuse
  ncores    = args.ncores
  parallel  = ncores>=2
  outdir    = ensuredir('plots/test')
  rungraphs = True #and False # RDF.RunGraphs should be faster
  merge     = [ # to test MergedSample.getrdframe
    'DY',  # = sum(DY*Jets)
    #'JTF', # = WJ + QCD
    #'nonDY', # = JTF + TT (to test MergedSample of MergedSample objects)
  ]
  obssample, expsamples = getsamples(nevts=args.nevts,split=True,merge=merge,veto='QCD',reuse=reuse,verb=verbosity)
  sampleset = SampleSet(obssample,expsamples) # data + exp
  sampleset_exp = SampleSet(None,expsamples) # only expected
  
  selections = [
    ###Sel('pT > 30', 'pt_1>30 && pt_2>30', fname="ptgt30" ),
    ###Sel('pT > 50', 'pt_1>50 && pt_2>50', fname="ptgt50" ),
    ###Sel('pT > 30, |eta|<2.4',
    ###    'pt_1>30 && pt_2>30 && abs(eta_1)<2.4 && abs(eta_2)<2.4', fname="ptgt30", only=['m_vis']),
#     Sel('pT > 30, |eta|<2.4, SS',
#         'pt_1>30 && pt_2>30 && abs(eta_1)<2.4 && abs(eta_2)<2.4 && q_1*q_2>0', fname="ss-ptgt30"),
    Sel('pT > 30, |eta|<2.4, OS',
        'pt_1>30 && pt_2>30 && abs(eta_1)<2.4 && abs(eta_2)<2.4 && q_1*q_2<0', fname="os-ptgt30"),
#     Sel('pT > 30, |eta|<2.4, OS (weighted)', # to test propagation of Selection.weight
#         'pt_1>30 && pt_2>30 && abs(eta_1)<2.4 && abs(eta_2)<2.4 && q_1*q_2<0', fname="os-ptgt30_wgt", weight="10", only=['m_vis']),
#     Sel('pT > 30, |eta|<2.4, OS, ptsum > 100',
#         'pt_1>30 && pt_2>30 && abs(eta_1)<2.4 && abs(eta_2)<2.4 && ptsum>100 && q_1*q_2<0', fname="os-ptgt30-ptsumgt100", only=['pt.*']),
  ]
  variables = [
    Var('m_vis',            20,  0, 140, fname='mvis', cbins={'q_1\*q_2>0': (20,0,200)}, ymarg=1.28),
    Var('m_vis', [40,50,60,65,70,75,80,85,90,95,100,110,130,160,200], fname='mvis_rebin', ymarg=1.28, cut="m_vis>40",blind=(120,130)),
    Var('pt_1',             40,  0, 120, cbins={'ptsum>100': (50,0,250)}),
    Var('pt_2',             40,  0, 120, cbins={'ptsum>100': (50,0,250)}),
#     Var('pt_1+pt_2',        40,  50,300), #, cut="pt_1>30 && pt_2>30"
#     Var('ptsum',            40, 50, 250),
#     Var('eta_1',            20, -4,   4, ymarg=1.4),
#     ###Var('eta_2',            20, -4,   4, ymarg=1.4),
#     Var('min(eta_1,eta_2)', 30, -3,   3, fname='mineta'),
#     Var('njets',            10,  0,  10),
#     Var('njets',            10,  0,  10, fname='njets_wgt', weight="2"), # test weighting
#     Var('dm_2',             12,  0,  12, only='q_1\*q_2<0'), # test conditional (bool?x:y) expression
#     Var(dmmap(),             6,  0,   6, fname='dm_2_map1', title="dm_2", only='q_1\*q_2<0'), # test conditional (bool?x:y) expression
#     Var('dmmap(dm_2)',       6,  0,   6, fname='dm_2_map2', title="dm_2", only='q_1\*q_2<0'), # test C++ macro
  ]
  variables2D = [
    (Var('m_vis',20,0,140,fname='mvis'),
     Var('pt_1', 40,0,120)),
    (Var('q_1',"q_{#mu}", 3,-1,2,fname='q1'),
     Var('q_2',"q_{#tau}",3,-1,2,fname='q2')),
    (Var('q_1>0?0:1',"q_{#mu}", 2,0,2,fname='q1_lab',labs=['#minus1','+1']),
     Var('q_2>0?0:1',"q_{#tau}",2,0,2,fname='q2',labs=['#minus1','+1'])),
  ]
  
  # TO RUN PARALLEL
  if ncores>=2:
    #ROOT.DisableImplicitMT() # turn off to overwrite previous setting
    #ROOT.EnableImplicitMT(ncores) # number of threads to run parallel
    RDF.SetNumberOfThreads(ncores,verb=verbosity)
  
  # TEST Sample.getrdframe
#   test_getrdframe(expsamples,variables,selections,outdir,rungraphs=rungraphs,split=False,tag="_nosplit",verb=verbosity)
#   test_getrdframe(expsamples,variables,selections,outdir,rungraphs=rungraphs,split=True, tag="_split",  verb=verbosity)
  
  # TEST Sample.getrdframe2d
#   test_getrdframe2D(expsamples[1],variables2D,selections,outdir,rungraphs=rungraphs,split=False,tag="_nosplit",verb=verbosity) # single
#   test_getrdframe2D(expsamples[0],variables2D,selections,outdir,rungraphs=rungraphs,split=False,tag="_nosplit",verb=verbosity) # merged
  
  # TEST Sample.getsumw
#   test_getsumw(expsamples[1],selections,split=False,verb=verbosity) # single
#   test_getsumw(expsamples[0],selections,split=False,verb=verbosity) # merged
#   test_getsumw(expsamples[0],selections,split=True, verb=verbosity) # merged, split
  
  # TEST Sample.getmean
#   test_getmean(expsamples[1],variables,selections,split=False,verb=verbosity) # single
#   test_getmean(expsamples[0],variables,selections,split=False,verb=verbosity) # merged
#   test_getmean(expsamples[0],variables,selections,split=True, verb=verbosity) # merged, split
  
  # TEST Sample.gethist
#   test_gethist(expsamples[1],variables,selections,outdir,split=False,tag="_nosplit",verb=verbosity) # single
#   test_gethist(expsamples[0],variables,selections,outdir,split=False,tag="_nosplit",verb=verbosity) # merged
#   test_gethist(expsamples[0],variables,selections,outdir,split=True, tag="_split",verb=verbosity)   # merged, split
  
  # TEST Sample.gethist2D
  test_gethist2D(expsamples[0],variables2D,selections,outdir,split=False,tag="_nosplit",verb=verbosity) # single
  test_gethist2D(expsamples[0],variables2D,selections,outdir,split=True, tag="_split",  verb=verbosity) # merged
  test_gethist2D(expsamples[1],variables2D,selections,outdir,split=False,tag="_nosplit",verb=verbosity) # merged, split
  
  # TEST SampleSet.gethists
  ###test_SampleSet_MultiDraw(sampleset_exp,variables,selections,outdir,parallel=parallel,split=True,tag="_split",verb=verbosity) # deprecated
  test_SampleSet_RDF(sampleset_exp,variables,selections,outdir,split=True,tag="_split",verb=verbosity)
  
  # TEST SampleSet.getstack to test QCD
  ###test_SampleSet_MultiDraw(sampleset,variables,selections,outdir,parallel=parallel,split=True,tag="_split",method='QCD_OSSS',verb=verbosity) # deprecated
  test_SampleSet_RDF(sampleset,variables,selections,outdir,split=True,tag="_split",method='QCD_OSSS',verb=verbosity)
  

if __name__ == "__main__":
  from argparse import ArgumentParser
  description = """Test RDataFrame."""
  parser = ArgumentParser(description=description,epilog="Good luck!")
  parser.add_argument('-i', '--fnames',   nargs='+', help="input files" )
  parser.add_argument('-t', '--tag',      default="", help="extra tag for output" )
  parser.add_argument('-r', '--reuse',    action='store_true',
                                          help="reuse previously generated pseudo samples" )
  parser.add_argument('-n', '--nevts',    type=int, default=50000, action='store',
                                          help="number of events to generate per sample" )
  parser.add_argument('-c', '--ncores',   default=8, type=int, help="number of cores/threads, default=%(default)s" )
  parser.add_argument('-v', '--verbose',  dest='verbosity', type=int, nargs='?', const=1, default=0, action='store',
                                          help="set verbosity" )
  args = parser.parse_args()
  main(args)
  print("\n>>> Done!")
  
