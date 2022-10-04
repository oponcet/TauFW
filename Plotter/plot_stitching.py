#! /usr/bin/env python
# Author: Izaak Neutelings (May 2022)
# Description: Compare distributions in pico analysis tuples to test stitching
# Sources:
#   https://twiki.cern.ch/twiki/bin/viewauth/CMS/MCStitching
import os
import TauFW.Plotter.plot.Plot as _Plot
from TauFW.Plotter.plot.Plot import Plot, deletehist
from TauFW.Plotter.plot.Plot import LOG as PLOG
from TauFW.Plotter.sample.utils import LOG, STYLE, ensuredir, ensurelist, setera,\
                                       Sel, Var, MC, SampleSet, getmcsample, stitch


def getbaseline(channel):
  if 'tautau' in channel:
    cuts_iso  = "idDeepTau2017v2p1VSjet_1>=16 && idDeepTau2017v2p1VSjet_2>=16"
    antilep   = "idDeepTau2017v2p1VSe_1>=2 && idDeepTau2017v2p1VSmu_1>=1 && idDeepTau2017v2p1VSe_2>=2 && idDeepTau2017v2p1VSmu_2>=1"
    baseline  = "q_1*q_2<0 && idDecayModeNewDMs_1 && idDecayModeNewDMs_2 && %s && %s && !lepton_vetos_noTau && metfilter"%(antilep,cuts_iso)
  elif 'mutau' in channel:
    idiso1   = "iso_1<0.15 && idMedium_1"
    idiso2   = "idDecayModeNewDMs_2 && idDeepTau2017v2p1VSjet_2>=16 && idDeepTau2017v2p1VSe_2>=2 && idDeepTau2017v2p1VSmu_2>=8"
    baseline = "q_1*q_2<0 && %s && %s && !lepton_vetoes_notau && metfilter"%(idiso1,idiso2)
  return baseline
  

def compare_mutaufilter(channel,era,tag="",**kwargs):
  """Compare list of samples."""
  LOG.header("compare_samples",pre=">>>")
  outdir   = kwargs.get('outdir',   "plots/stitch" )
  parallel = kwargs.get('parallel', True          ) #and False
  norms    = kwargs.get('norm',     [False,True]  )
  #entries  = kwargs.get('entries', [str(e) for e in eras] ) # for legend
  exts     = kwargs.get('exts',     ['png']       ) # figure file extensions
  verb     = kwargs.get('verb',     0             )
  ensuredir(outdir)
  norms    = ensurelist(norms)
  setera(era) # set era for plot style and lumi-xsec normalization
  
  xs_excl = 1.834e+03*0.0257
  samples = {
    'DY':    getmcsample('DY',"DYJetsToLL_M-50",    "DYJetsToLL",     5343.0,channel,era,verb=verb),
    #'DY1J':  getmcsample('DY',"DY1JetsToLL_M-50",   "DY1JetsToLL",     877.8,channel,era,verb=verb),
    #'DY2J':  getmcsample('DY',"DY2JetsToLL_M-50",   "DY2JetsToLL",     304.4,channel,era,verb=verb),
    #'DY3J':  getmcsample('DY',"DY3JetsToLL_M-50",   "DY3JetsToLL",     111.5,channel,era,verb=verb),
    #'DY4J':  getmcsample('DY',"DY4JetsToLL_M-50",   "DY4JetsToLL",     44.05,channel,era,verb=verb),
    'DY_mt': getmcsample('DY',"DYJetsToMuTauh_M-50","DYJetsToMuTauh",xs_excl,channel,era,verb=verb),
    'DY_S19':    getmcsample('DY',"DYJetsToLL_M-50",    "DYJetsToLL Summer19",    5343.0,channel,era,verb=verb),
    'DY_mt_S19': getmcsample('DY',"DYJetsToMuTauh_M-50","DYJetsToMuTauh Summer19",xs_excl,channel,era,verb=verb),
    'DY_mt_S20': getmcsample('DY',"DYJetsToMuTauh_M-50_Summer20","DYJetsToMuTauh Summer20",xs_excl,channel,era,verb=verb),
  }
  #dysamples = [samples['DY'],samples['DY1J'],samples['DY2J'],samples['DY3J'],samples['DY4J']]
  #samples['DY*J'] = stitch(dysamples,'DY',incl='DYJ',name="DY_M50",npart='NUP')
  
  # SAMPLE SETS
  samplesets = {
    'DY': [samples['DY'],samples['DY_mt']],
    'DY_Summer20': [samples['DY_S19'],samples['DY_mt_S19'],samples['DY_mt_S20']],
    #'DY-all': [samples['DY'],samples['DY1J'],samples['DY2J'],samples['DY3J'],samples['DY4J'],samples['DY_mt']],
  }
  
  # SELECTIONS
  baseline   = getbaseline(channel)
  selections = [
    Sel('gen. mutaufilter', "mutaufilter", fname="nocuts-genfilter"),
    #Sel('baseline', baseline),
    Sel('baseline, gen. mutaufilter', baseline+" && mutaufilter", fname="baseline-genfilter"),
  ]
  
  # VARIABLES
  ptbins  = range(10,50,2) + range(50,70,4) + range(70,100,10) + [100,120,140]
  Zptbins = range(0,60,3) + range(60,100,10) + range(100,140,20) + [140,170,200]
  variables = [
    Var('mutaufilter', 4, 0, 4, "Generator mutauh filter (pt > 18 GeV, |eta|<2.5)", labels=['Fail','Pass','','']),
    Var('m_vis',   50, 0, 150, fname="mvis"),
    Var('m_vis',   50, 0, 150, fname="mvis_log",logy=True),
    Var('dR_ll',   50, 0,   4, fname="dR",pos='L'),
    Var('dR_ll',   50, 0,   4, fname="dR_log",logy=True,pos='L',ymarg=1.3),
    Var('pt_1',    60,10, 130, "Muon pt", fname="$VAR" ),
    Var('pt_1',        ptbins, "Muon pt", fname="$VAR_coarse" ),
    Var('pt_2',    60,10, 130, "tau_h pt", fname="$VAR" ),
    Var('pt_2',        ptbins, "tau_h pt", fname="$VAR_coarse" ),
    Var('eta_1',   20,-3,   5, "Muon eta" ),
    Var('eta_2',   20,-3,   5, "tau_h eta" ),
    Var('q_1',      6,-2,   4, "Muon charge", labels=['','#minus1','','#plus1','',''],ymarg=1.3),
    Var('q_2',      6,-2,   4, "tau_h charge", labels=['','#minus1','','+1','',''],ymarg=1.3),
    Var('jpt_1',   18, 0, 270 ),
    Var('jpt_2',   18, 0, 270 ),
    Var('met',     20, 0, 300 ),
    Var('njets',    5, 0,   5, logy=True,logyrange=2),
    Var('NUP',      5, 0,   5, "Number of partons (at LHE level)", logy=True,logyrange=2.2),
    Var('genvistaupt_2', 60,10, 130, "Generator visible tau_h pt", fname="$VAR" ),
    Var('genvistaupt_2',     ptbins, "Generator visible tau_h pt", fname="$VAR_coarse" ),
    Var('genmatch_1',    10, 0,  10, "Generator match muon",  logy=True,logyrange=2.4),
    Var('genmatch_2',    10, 0,  10, "Generator match tau_h", logy=True),
    Var('m_moth',  50, 0, 150, "Generator Z boson mass", pos='Ly=0.83'),
    Var('m_moth',  50, 0, 150, "Generator Z boson mass", pos='Ly=0.83', fname="$VAR_log",logy=True,logyrange=3.8),
    Var('pt_moth', 50, 0, 150, "Generator Z boson pt", pos='y=0.78'),
    Var('pt_moth', 50, 0, 150, "Generator Z boson pt", pos='y=0.78',fname="$VAR_log",logy=True,logyrange=2.4),
    Var('pt_moth',    Zptbins, "Generator Z boson pt", pos='y=0.78',fname="$VAR_coarse",logy=True,logyrange=2.4),
    #Var('rawDeepTau2017v2p1VSe_2',   "rawDeepTau2017v2p1VSe",   30, 0.70, 1, fname="$VAR_zoom",logy=True,pos='L;y=0.85'),
    #Var('rawDeepTau2017v2p1VSmu_2',  "rawDeepTau2017v2p1VSmu",  20, 0.80, 1, fname="$VAR_zoom",logy=True,logyrange=4,pos='L;y=0.85'),
    #Var('rawDeepTau2017v2p1VSjet_2', "rawDeepTau2017v2p1VSjet", 100, 0.0, 1, pos='L;y=0.85',logy=True,ymargin=2.5),
    #Var('rawDeepTau2017v2p1VSjet_2', "rawDeepTau2017v2p1VSjet", 20, 0.80, 1, fname="$VAR_zoom",pos='L;y=0.85'),
  ]
  
  # PLOT
  for sname, samplelist in samplesets.items():
    sampleset = SampleSet(samplelist)
    sampleset.printtable()
    header = "" #samplelist[0].title
    for selection in selections:
      print ">>> %s: %r"%(selection,selection.selection)
      hdict = { }
      text  = "%s: %s"%(channel.replace("tau","tau_{#lower[-0.2]{h}}"),selection.title)
      fname = "%s/compare_stitch_$VAR_%s_%s%s$TAG"%(outdir,sname,selection.filename,tag)
      for sample in samplelist:
        vars  = [v for v in variables if v.data or not sample.isdata]
        hists = sample.gethist(vars,selection,parallel=parallel)
        for variable, hist in zip(variables,hists):
          hdict.setdefault(variable,[ ]).append(hist)
      for variable, hists in hdict.iteritems():
        for norm in norms:
          ntag  = '_norm' if norm else "_lumi"
          lsize = _Plot._lsize*(1.55 if variable.name.startswith('q_') else 1)
          style = [1,1,2,1,1,1]
          plot  = Plot(variable,hists,norm=norm,clone=True)
          plot.draw(ratio=True,style=style,xlabelsize=lsize)
          plot.drawlegend(header=header) #,entries=entries)
          plot.drawtext(text)
          plot.saveas(fname,ext=['png'],tag=ntag) #,'pdf'
          plot.close()
        deletehist(hists)
    print ">>> "
  

def main(args):
  fname    = None #"$PICODIR/$SAMPLE_$CHANNEL.root" # fname pattern
  channels  = args.channels
  eras      = args.eras
  parallel  = args.parallel
  varfilter = args.varfilter
  selfilter = args.selfilter
  pdf       = args.pdf
  outdir    = "plots/stitch"
  fname     = "$PICODIR/$SAMPLE_$CHANNEL$TAG.root"
  tag       = args.tag
  
  for era in eras:
    for channel in channels:
      compare_mutaufilter(channel,era,tag=tag,outdir=outdir)
  

if __name__ == "__main__":
  import sys
  from argparse import ArgumentParser
  argv = sys.argv
  description = """Simple plotting script to compare distributions in pico analysis tuples"""
  parser = ArgumentParser(prog="plot_compare",description=description,epilog="Good luck!")
  parser.add_argument('-y', '--era',     dest='eras', nargs='*', default=['UL2018'],
                                         help="set era" )
  parser.add_argument('-c', '--channel', dest='channels', type=str, nargs='+', default=['mutau'], action='store',
                                         help="set channel, default=%(default)r" )
  parser.add_argument('-V', '--var',     dest='varfilter', nargs='+',
                                         help="only plot the variables passing this filter (glob patterns allowed)" )
  parser.add_argument('-S', '--sel',     dest='selfilter', nargs='+',
                                         help="only plot the selection passing this filter (glob patterns allowed)" )
  parser.add_argument('-s', '--serial',  dest='parallel', action='store_false',
                                         help="run Tree::MultiDraw serial instead of in parallel" )
  parser.add_argument('-p', '--pdf',     dest='pdf', action='store_true',
                                         help="create pdf version of each plot" )
  parser.add_argument('-t', '--tag',     default="", help="extra tag for output" )
  parser.add_argument('-v', '--verbose', dest='verbosity', type=int, nargs='?', const=1, default=0, action='store',
                                         help="set verbosity" )
  args = parser.parse_args()
  LOG.verbosity = args.verbosity
  PLOG.verbosity = args.verbosity
  main(args)
  print "\n>>> Done."
  
