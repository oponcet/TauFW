#! /usr/bin/env python
# Author: Izaak Neutelings (January 2021)
# Description: Script to measure Z pt reweighting based on dimuon events
#   ./measureZpt.py -y 2018
#   ./validateZpt.py -y 2018
from config.samples import *
from TauFW.Plotter.plot.utils import LOG as PLOG
from TauFW.common.tools.math import frange
from ROOT import gROOT, gSystem
gROOT.Macro('weights/zptweight.C+')
from ROOT import loadZptWeights

baseline = "q_1*q_2<0 && pt_2>20 && iso_1<0.15 && iso_2<0.15 && idMedium_1 && idMedium_2 && !extraelec_veto && !extramuon_veto && metfilter && m_ll>20"
#baseline = "q_1*q_2<0 && pfRelIso04_all_1<0.15 && pfRelIso04_all_2<0.15 && !extraelec_veto && !extramuon_veto && m_vis>20" # old
ptitle   = "p_{T}(#mu#mu)" # [GeV]"
mtitle   = "m_{#mu#mu}" # [GeV]"
pgtitle  = "Z p_{T}"
mgtitle  = "m_{Z}"
Zmbins0  = [20,30,40,50,60,70,80,85,88,89,89.5,90,90.5,91,91.5,92,93,94,95,100,110,120,180,500,1000]
Zmbins1  = [0,50,70,91,110,150,200,400,800,1500]
ptbins0  = [0,5,10,15,20,25,30,35,40,45,50,60,70,100,140,200,300,500,1000]
ptbins1  = [0,5,15,30,50,100,200,500,1000]
dRbins   = [0,0.4,1.0,1.5,2.0]+frange(2.2,5.61,0.2)+[6.0]


def plot(era,channel,weight="",tag="",title="",outdir="plots",parallel=True,pdf=False,dy='jets',verb=0):
  """Test plotting of SampleSet class for data/MC comparison."""
  LOG.header("plot %s"%(tag.strip('_')))
  global Zmbins1, ptbins1
  
  # ERA
  fname     = "$PICODIR/$SAMPLE_$CHANNEL$TAG.root"
  dyweight  = weight #"zptweight"
  #sampleset = getsampleset('mutau','UL2018',fname=fname,dyweight=weight,dy="") # check stitching
  #sampleset = getsampleset(channel,era,fname=fname,dyweight="") # no Z pt reweighting
  sampleset = getsampleset(channel,era,fname=fname,dyweight=weight,dy=dy)
  #sampleset = getsampleset(channel,era,fname=fname,dyweight=dyweight)
  
  # SELECTIONS
  selections = [
    Sel('baseline',                   baseline),
    #Sel('baseline, met<50 GeV',       baseline+" && met<50", fname="baseline-metlt50"),
    #Sel('m_{mumu} > 110 GeV',         baseline+" && pt_1>50 && pt_2>50 && m_vis>110", fname="mgt110"),
    #Sel('m_{mumu} > 200 GeV',         baseline+" && pt_1>50 && pt_2>50 && m_vis>200", fname="mgt200"),
    #Sel('0j, m_{mumu} > 200 GeV',     baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && njets50==0", fname="0j-mgt200"),
    #Sel('0cj, m_{mumu} > 200 GeV',    baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && ncjets50==0", fname="0cj-mgt200"),
    #Sel('0j, 200 GeV < m_{mumu} < 400 GeV',        baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && m_vis<400 && njets50==0", fname="0j-mgt200-400"),
    #Sel('0cj, 200 GeV < m_{mumu} < 400 GeV',       baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && m_vis<400 && ncjets50==0", fname="0cj-mgt200-400"),
    #Sel('m_{mumu} > 200 GeV, #LT#eta#GT<1.1',      baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && (eta_1+eta_2)/2<1.1 && deta_ll<3", fname="mgt200-etalt1p1"),
    #Sel('0j, m_{mumu} > 200 GeV, #LT#eta#GT<1.1',  baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && (eta_1+eta_2)/2<1.1 && deta_ll<3 && njets50==0", fname="0j-mgt200-etalt1p1"),
    #Sel('0cj, m_{mumu} > 200 GeV, #LT#eta#GT<1.1', baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && (eta_1+eta_2)/2<1.1 && deta_ll<3 && ncjets50==0", fname="0cj-mgt200-etalt1p1"),
    #Sel('0j, 200 GeV < m_{mumu} < 400 GeV, (eta_1+eta_2)<2.2',  baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && m_vis<400 && njets50==0", fname="0j-mgt200-400-etalt1p1"),
    #Sel('0cj, 200 GeV < m_{mumu} < 400 GeV, (eta_1+eta_2)<2.2', baseline+" && pt_1>50 && pt_2>50 && m_vis>200 && m_vis<400 && ncjets50==0", fname="0cj-mgt200-400-etalt1p1"),
  ]
  
  # VARIABLES
  if dy=='mass':
    Zmbins1     = [110,150,200,400,600,1500]
    ptbins1     = [0,3,5,7,11,15,30,50,100,200,500,1000]
  nurbins  = (len(Zmbins1)-1)*(len(ptbins1)-1) # number of 2D bins (excl. under-/overflow)
  urbins0  = (nurbins,1,1+nurbins) # unrolled
  urlabels1 = [str(i) if i%(len(ptbins1)-1)==1 or i in [nurbins] else " " for i in range(1,nurbins+1)]
  urlabels2 = [str(i) if i%(len(Zmbins1)-1)==1 or i in [nurbins] else " " for i in range(1,nurbins+1)]
  variables = [
    Var('pt_1',  "Leading muon pt",     40,  0,  120, cbins={"m_vis>200":(25,20,270)} ),
    Var('pt_2',  "Subleading muon pt",  40,  0,  120, cbins={"m_vis>200":(25,20,270)} ),
    Var('eta_1', "Leading muon eta",    30, -3,    3, ymargin=1.6, pos='T', ncols=2),
    Var('eta_2', "Subleading muon eta", 30, -3,    3, ymargin=1.6, pos='T', ncols=2),
    Var('m_ll',  "m_mumu",              40,  0,  200, fname="$VAR", cbins={"m_vis>":(36,100,1000),"m_vis>200":(40,200,1000)}), # alias: m_ll alias of m_vis
    Var('m_ll',  "m_mumu",              40,  0,  200, fname="$VAR_log", logy=True, ymin=1e2, cbins={"m_vis>":(36,100,1000),"m_vis>200":(30,200,1000)} ),
    Var('m_ll',  "m_mumu",              40, 70,  110, fname="$VAR_Zmass", veto=["m_vis>110","m_vis>200"] ),
    Var('m_ll',  "m_mumu",              Zmbins1,      fname="$VAR_tail", logy=True, ymin=1e-1, logyrange=6 ), #cbins={"m_vis>200":Zmbins3}
    #Var('mt_1',  "mt(mu,MET)", 40,  0, 200),
    Var("jpt_1",    29,   10,  300, veto=[r"njets\w*==0"]),
    Var("jpt_2",    29,   10,  300, veto=[r"njets\w*==0"]),
    Var("jeta_1",   53, -5.4,  5.2, ymargin=1.6,pos='T',ncols=2,veto=[r"njets\w*==0"]),
    Var("jeta_2",   53, -5.4,  5.2, ymargin=1.6,pos='T',ncols=2,veto=[r"njets\w*==0"]),
    Var('njets',     8,  0,   8),
    Var('njets50',   8,  0,   8),
    Var('ncjets',    8,  0,   8),
    Var('ncjets50',  8,  0,   8),
    Var('met',      50,  0, 150),
    Var('pt_ll',   "pt(mumu)",    25, 0, 200, cbins={"m_vis>200":ptbins0}),
    Var('pt_ll',   "pt(mumu)",    25, 0, 200, fname="$VAR_log", logy=True, logx=True, ymin=1e2, pos='RR', cbins={"m_vis>200":ptbins0}),
    Var('pt_ll',   "pt(mumu)",    50, 0, 500, fname="$VAR_500", logy=True, ymin=5e1, pos='RR'),
    Var('dR_ll',   "DR(mumu)",    30, 0, 6.0 ),
    Var('dR_ll',   "DR(mumu)",    dRbins, fname="$VAR_log", logy=True, pos='Ly=0.88', logyrange=7, ymargin=1.6),
    Var('deta_ll', "deta(mumu)",  20, 0, 6.0, logy=True, pos='TRR'), #, ymargin=8, logyrange=2.6
    #Var('dzeta',  56, -180, 100, pos='L;y=0.88',units='GeV'),
    #Var("pzetavis", 50,    0, 200 ),
    #Var('npv',    40,    0,  80 ),
    Var('Unroll::GetBin(pt_ll,m_ll,0,1)',"Reconstructed ptmumu bin",*urbins0,fname="pt_ll_unrolled",units=False,logy=True,ymin=1e-2,labels=urlabels1), # unroll bin number
    Var('Unroll::GetBin(pt_ll,m_ll,1,1)',"Reconstructed m_mumu bin",*urbins0,fname="m_ll_unrolled",units=False,logy=True,ymin=1e-2,labels=urlabels2), # unroll bin number, transposed
  ]
  
  # UNROLL
  gROOT.ProcessLine(".L ../../Plotter/python/macros/Unroll.cxx+O")
  from ROOT import Unroll
  xvar = Var('pt_ll', ptbins1,"Reconstructed ptmumu")
  yvar = Var('m_ll',  Zmbins1,"Reconstructed m_mumu")
  hist2D = xvar.gethist2D(yvar,"h2_unroll_axes") # get pt_ll vs. m_ll TH2
  Unroll.SetBins(hist2D,verb) # set bin axes for Unroll.GetBin
  
  # PLOT
  outdir   = ensuredir(repkey(outdir,CHANNEL=channel,ERA=era))
  exts     = ['png','pdf'] if pdf else ['png'] # extensions
  for selection in selections:
    if 'mgt200' in tag and 'm_vis>' not in selection.selection: continue
    stacks = sampleset.getstack(variables,selection,method='QCD_OSSS',parallel=parallel)
    fname  = "%s/$VAR_%s-%s-%s$TAG"%(outdir,channel.replace('mu',"m"),selection.filename,era)
    text   = "%s: %s"%(channel.replace('mu',"#mu").replace('tau',"#tau_{h}"),selection.title)
    if title:
      text += ", "+title
    for stack, variable in stacks.iteritems():
      #position = "" #variable.position or 'topright'
      if "Unroll" in variable.name:
        yt = 0.91 # lower corner text for bin text
        lpos = 'RR;y=0.91'
        kwargs = {
          'width': 1200, 'xlabelsize': 0.072, 'labeloption': 'h',
        }
      else:
        yt = None
        lpos = None
        kwargs = { }
      stack.draw(**kwargs)
      if "Unroll::GetBin(pt_ll,m_ll,0" in variable.name:
        stack.drawbins(yvar,y=0.96,size=0.035,text="m_{#mu#mu}",addoverflow=True)
      elif "Unroll::GetBin(pt_ll,m_ll,1" in variable.name: # transposed
        stack.drawbins(xvar,y=0.96,size=0.035,text="p_{T}^{#mu#mu}",addoverflow=True)
      stack.drawlegend(lpos)
      stack.drawtext(text,y=yt)
      stack.saveas(fname,ext=exts,tag=tag)
      stack.close()
  
  sampleset.close()
  

def main(args):
  channels  = args.channels
  eras      = args.eras
  parallel  = args.parallel
  pdf       = args.pdf
  dytype    = args.dytype
  outdir    = "plots/$ERA"
  verbosity = args.verbosity
  tag       = ""
  for era in eras:
    setera(era) # set era for plot style and lumi-xsec normalization
    for channel in channels:
      plot(era,channel,weight="",title="no reweighting",tag="_noweight",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
      if dytype=='mass': # mass-binned samples
        fname1D = "weights/zpt_weights_mgt110_%s.root"%(era) # m_mumu > 110
        #fname1D = "weights/zpt_weights_mgt200_%s.root"%(era) # m_mumu > 200
        fname2D = "weights/zptmass_weights_mgt110_%s.root"%(era)
        loadZptWeights(fname1D,"zpt_weight")
        plot(era,channel,weight="getZptWeight(pt_moth)",title="unfolded 1D weight",tag="_weight1D_mgt110",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
        loadZptWeights(fname2D,"zptmass_weight")
        plot(era,channel,weight="getZptWeight(pt_moth,m_moth)",title="unfolded 2D weight",tag="_weight2D_mgt110",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
        ###loadZptWeights("weights/zptnjets_weights_mgt200_%s.root"%(era),"zptnjets_weight")
        ###plot(era,channel,weight="getZptWeight(pt_moth,njets)",title="unfolded 2D weight",tag="_weight2D_njets",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
      else: # jet-binned samples
        fname1D = "weights/zpt_weights_%s.root"%(era)
        fname2D = "weights/zptmass_weights_%s.root"%(era)
        ###loadZptWeights(fname1D,"zpt_weight_reco")
        ###plot(era,channel,weight="getZptWeight(pt_ll)",title="reco. 1D weight",tag="_recoweight1D",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
        loadZptWeights(fname1D,"zpt_weight")
        plot(era,channel,weight="getZptWeight(pt_moth)",title="unfolded 1D weight",tag="_weight1D",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
        loadZptWeights(fname2D,"zptmass_weight")
        plot(era,channel,weight="getZptWeight(pt_moth,m_moth)",title="unfolded 2D weight",tag="_weight2D",outdir=outdir,parallel=parallel,pdf=pdf,dy=dytype,verb=verbosity)
    

if __name__ == "__main__":
  from argparse import ArgumentParser
  description = """Simple plotting script for pico analysis tuples"""
  parser = ArgumentParser(description=description,epilog="Good luck!")
  parser.add_argument('-y', '--era',     dest='eras', nargs='*', default=['2017'], action='store', #, choices=['2016','2017','2018','UL2017']
                                         help="set era" )
  parser.add_argument('-c', '--channel', dest='channels', nargs='*', choices=['mumu'], default=['mumu'], action='store',
                                         help="set channel" )
  parser.add_argument(      '--dy',      dest='dytype', type=str, default='jet', action='store',
                                         help="DY type: 'jet' (default), 'mass'" )
  parser.add_argument('-s', '--serial',  dest='parallel', action='store_false',
                                         help="run Tree::MultiDraw serial instead of in parallel" )
  parser.add_argument('-p', '--pdf',     dest='pdf', action='store_true',
                                         help="create pdf version of each plot" )
  parser.add_argument('-v', '--verbose', dest='verbosity', type=int, nargs='?', const=1, default=0, action='store',
                                         help="set verbosity" )
  args = parser.parse_args()
  LOG.verbosity = args.verbosity
  PLOG.verbosity = args.verbosity
  main(args)
  print("\n>>> Done.")
  
