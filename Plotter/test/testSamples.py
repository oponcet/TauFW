#! /usr/bin/env python3
# Author: Izaak Neutelings (July 2020)
# Description: Test the Sample class
#   test/testSamples.py -v2
from TauFW.Plotter.sample.utils import LOG, STYLE, setera, CMSStyle, ensuredir,\
                                       Sample, MergedSample, SampleSet
#import TauFW.Plotter.sample.SampleStyle as STYLE
#from TauFW.Plotter.sample.SampleStyle import getcolor, sample_colors
#from TauFW.Plotter.sample.Sample import Sample
#from TauFW.Plotter.sample.MergedSample import MergedSample
#from TauFW.Plotter.sample.SampleSet import SampleSet
from TauFW.Plotter.plot.Variable import Variable #as Var
from TauFW.Plotter.plot.Stack import Stack
from TauFW.Plotter.plot.Stack import LOG as PLOG
from pseudoSamples import getsamples

selections = [
  ('pt_1>30 && pt_2>30 && abs(eta_1)<2.4 && abs(eta_2)<2.4', 'weight'),
]
variables = [
  Variable('m_vis',            32,  0, 160, blind=(120,130)),
  ###Variable('m_vis',            [0,20,40,50,60,65,70,75,80,85,90,95,100,110,130,160,200]),
  Variable('pt_1',             40,  0, 120),
  Variable('pt_2',             40,  0, 120),
  Variable('pt_1+pt_2',        40,  0, 200),
  Variable('eta_1',            30, -3,   3, ymargin=1.65),
  Variable('eta_2',            30, -3,   3, ymargin=1.65),
  Variable('min(eta_1,eta_2)', 30, -3,   3, fname="minetas"),
  Variable('njets',            10,  0,  10),
]
variables2D = [
  (Variable('pt_1',  50,  0, 100), Variable('pt_2',  50,  0, 100)),
  (Variable('pt_1',  50,  0, 100), Variable('eta_1', 50, -3,   3)),
  #(Variable('pt_2',  50,  0, 100), Variable('eta_2', 50, -3,   3)),
  #(Variable('eta_1', 50, -3,   3), Variable('eta_1', 50, -3,   3)),
  #(Variable('pt_1',  50,  0, 100), Variable('m_vis', 50,  0, 150)),
  #(Variable('pt_2',  50,  0, 100), Variable('m_vis', 50,  0, 150)),
]
text     = "#mu#tau_{h} baseline"
position = 'topright'


def plotsamples_stack(datasample,expsamples,outdir="plots/test",tag=""):
  """Test Sample.gethist method and plot data/MC comparison."""
  LOG.header("plotsamples_stack")
  
  # MAKE 1D HISTS
  ensuredir(outdir)
  fname = "%s/testSamples_$VAR%s.png"%(outdir,tag)
  for selection, weight in selections:
    histdict = { }
    for sample in [datasample]+expsamples:
      hists = sample.gethist(variables,selection)
      histdict[sample] = hists
      print(">>> %r: %s"%(sample.name,[repr(h.GetName()) for h in hists]))
    
    # PLOT
    for i, variable in enumerate(variables):
      #LOG.header(variable)
      datahist = histdict[datasample][i]
      exphists = [histdict[s][i] for s in expsamples]
      plot = Stack(variable,datahist,exphists)
      plot.draw(ratio=True)
      plot.drawlegend(position=position)
      plot.drawtext(text)
      plot.saveas(fname)
      plot.close()
  

def plotsamples2D(datasample,expsamples):
  """Test Sample.gethist2D method."""
  LOG.header("plotsamples2D")
  for selection, weight in selections:
    histdict = { }
    for sample in [datasample]+expsamples:
      hists = sample.gethist2D(variables2D,selection)
      histdict[sample] = hists
      print(">>> %r: %s"%(sample.name,[repr(h.GetName()) for h in hists]))
  

def testMergedSamples(datasample,expsamples):
  """Test MergedSample class: join samples, print out, and plot."""
  LOG.header("testMergedSamples")
  print(">>> Joining samples %s"%(expsamples))
  #color      = expsamples[0].fillcolor
  STYLE.sample_colors['Exp'] = STYLE.kOrange
  STYLE.sample_colors['Bkg'] = STYLE.kOrange
  bkgsample  = MergedSample("Bkg","Background",expsamples[1:]) #,color=color)
  expsamples = [expsamples[0],bkgsample]
  expsample  = MergedSample("Exp","Expected",expsamples) #,color=color)
  print(">>> ")
  expsample.printheader()
  expsample.printrow()
  expsample.printobjs()
  print(">>> ")
  plotsamples_stack(datasample,[expsample],tag='_merged')
  

def main(args):
  LOG.header("Prepare samples")
  sampleset = [
    ('ZTT',  "Z -> #tau_{mu}#tau_{h}", 1.00),
    ('WJ',   "W + jets",               0.40),
    ('QCD',  "QCD multijet",           0.30),
    ('TT',   "t#bar{t}",               0.15),
    ('Data', "Observed",                -1 ),
  ]
  lumi = 10 # [fb-1] to cancel xsec [pb]
  #CMSStyle.setCMSEra(2018)
  setera(2018,lumi)
  datasample, expsamples = getsamples(sampleset,nevts=args.nevts,reuse=args.reuse,lumi=lumi,verb=args.verbosity+1)
  plotsamples_stack(datasample,expsamples)
  plotsamples2D(datasample,expsamples)
  testMergedSamples(datasample,expsamples)
  

if __name__ == "__main__":
  from argparse import ArgumentParser
  description = """Test the Sample class"""
  parser = ArgumentParser(prog="testSamples",description=description,epilog="Good luck!")
  parser.add_argument('-n', '--nevts',   type=int, default=50000, action='store',
                                         help="number of events to generate per sample" )
  parser.add_argument('-r', '--reuse',   action='store_true',
                                         help="reuse previously generated pseudo samples" )
  parser.add_argument('-v', '--verbose', dest='verbosity', type=int, nargs='?', const=1, default=0, action='store',
                                         help="set verbosity" )
  args = parser.parse_args()
  LOG.verbosity = args.verbosity
  PLOG.verbosity = args.verbosity-1
  main(args)
  print(">>>\n>>> Done.")
  
