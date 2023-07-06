import ROOT

import os, sys, re, glob, time
import numpy, copy
from array import array
from argparse import ArgumentParser
import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import gROOT, gPad, gStyle, Double, TFile, TCanvas, TLegend, TLatex, TF1, TGraph, TGraph2D, TPolyMarker3D, TGraphAsymmErrors, TLine,\
                 kBlack, kBlue, kRed, kGreen, kYellow, kOrange, kMagenta, kTeal, kAzure, TMath
from TauFW.Plotter.sample.utils import CMSStyle
from itertools import combinations
from math import sqrt, log, ceil, floor

import yaml


gROOT.SetBatch(True)
#gROOT.SetBatch(False)
gStyle.SetOptTitle(0)

# CMS style
CMSStyle.setTDRStyle()



def findz_min(g):
    n = g.GetN()
    z = g.GetZ()
    locmin = ROOT.TMath.LocMin(n, z)
    z_min = z[locmin]
    return z_min

def findtes_min(g):
    n = g.GetN()
    z = g.GetZ()
    y = g.GetY()
    locmin = ROOT.TMath.LocMin(n, z)
    tes_min = y[locmin]
    return tes_min

def findtid_min(g):
    n = g.GetN()
    z = g.GetZ()
    x = g.GetX()
    locmin = ROOT.TMath.LocMin(n, z)
    tid_min = x[locmin]
    return tid_min

def plot2D_Scan(setup,region,year,**kwargs):

    # Retrieve optional arguments or set default values
    indir        = kwargs.get('indir',       "output_%s"%year )
    outdir       = kwargs.get('outdir',      "plots_%s"%year  )
    tag          = kwargs.get('tag',         ""               )
    poi1         = kwargs.get('poi1',        ""               ) #tes 
    poi2         = kwargs.get('poi2',        ""               ) #tid_SF
    era          = "%s-13TeV"%year
    channel      = setup["channel"].replace("mu","m").replace("tau","t")


    # Construct the name of the canvas
    canvasname = "%s/contour_%s_%s_%s_m_vis-%s%s%s"%(outdir,poi1,poi2,channel,region,tag)
    ensureDirectory(outdir)

    # Construct the name of the input file
    filename = '%s/higgsCombine.%s_%m_vis-%s%s-%s.MultiDimFit.mH90.root'%(indir,channel,region,tag,era)
    print('>>>   file "%s"'%(filename))
    file = ensureTFile(filename)


    # Get the tree in the input file 
    tree = file.Get('limit')
    print("poi1 = %s and poi2= %s" %(poi1,poi2))

    poi1_name = "%s_%s"%(poi1,region)
    poi2_name = "%s_%s"%(poi2,region)

    # Create the canvas 
    canvas = ROOT.TCanvas("c", canvasname, 25, 25, 800, 800 )
 
    # Graph
    tree.Draw("2*deltaNLL:%s:%s>>h(51,0.97,1.03,51,0.4,1.6)", "2*deltaNLL<10", "prof colz" %(poi1_name,poi2_name))

    n = tree.Draw("%s:%s", "quantileExpected == -1", "P same" %(poi1_name,poi2_name))

    g = ROOT.TGraph(n, tree.GetV1(), tree.GetV2())
    g.SetTitle("Combinedfit ;%s;%s" %(poi1_name,poi2_name))

    g.Draw("p same")

    CMSStyle.setCMSLumiStyle(canvas,0)
   

    # Save the canvas
    canvas.Modified()
    canvas.Update()
    canvas.SaveAs(canvasname+".png")
    canvas.SaveAs(canvasname+".root")


def plot3D_Scan(tag, channel, observable):
    print(f"filename = ./output_UL2018/higgsCombine.mt_{observable}-{channel}{tag}_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")
    f = ROOT.TFile(f"./output_UL2018_v10/higgsCombine.mt_{observable}-{channel}{tag}_DeepTau-UL2018_v10-13TeV.MultiDimFit.mH90.root")
    tree = f.Get("limit")

    c = ROOT.TCanvas("c", "tid_SF", 25, 25, 800, 800)

    # Graph
    n = tree.Draw(f"tid_SF_{channel}:tes_{channel}:2*deltaNLL", "2*deltaNLL<20 && (tid_SF_{channel}>0.7 && tid_SF_{channel}<1.2 && tes_{channel}>0.95 && tes_{channel}<1.05)", "gOff")

    g = ROOT.TGraph2D(n, tree.GetV1(), tree.GetV2(), tree.GetV3())
    g.SetTitle(f"Combinedfit ;tid_SF_{channel};tes_{channel}")

    nThere seems to be some missing parts of the code that are not provided. Specifically, the header files and libraries such as `TROOT.h`, `TObject.h`, `TMath.h`, `TGraph.h`, `TString.h`, `TFile.h`, `RooRealVar.h`, `RooDataSet.h`, `RooGaussian.h`, `TCanvas.h`, `RooPlot.h`, `TAxis.h`, `RooStats/ModelConfig.h`, and `<fstream>`. Without these dependencies, the code won't compile or run.

def warning(string,**kwargs):
  print ">>> \x1b[1;33;40m%sWarning!\x1b[0;33;40m %s\033[0m"%(kwargs.get('pre',""),string)
    
def error(string,**kwargs):
  print ">>> \x1b[1;31;40m%sERROR!\x1b[0;31;40m %s\033[0m"%(kwargs.get('pre',""),string)
  exit(1)
  

def ensureDirectory(dirname):
  """Make directory if it does not exist."""
  if not os.path.exists(dirname):
      os.makedirs(dirname)
      print ">>> made directory %s"%dirname


def ensureTFile(filename,option='READ',**kwargs):
  """Open TFile and make sure if that it exists."""
  pre  = kwargs.get('pre',  ""   )
  stop = kwargs.get('exit', True )
  if not os.path.isfile(filename):
    error('ensureTFile: File in path "%s" does not exist'%(filename),pre=pre)
  file = TFile(filename,option)
  if not file or file.IsZombie():
    if stop:
      error('ensureTFile: Could not open file by name "%s"'%(filename),pre=pre)
    else:
      warning('ensureTFile: Could not open file by name "%s"'%(filename),pre=pre)
  return file

def main(args):
    
    print("Using configuration file: %s"%args.config)
    with open(args.config, 'r') as file:
        setup = yaml.safe_load(file)

    channel       = setup["channel"].replace("mu","m").replace("tau","t")
    tag           = setup["tag"] if "tag" in setup else ""
    verbosity     = args.verbose
    poi1          = args.poi1
    poi2          = args.poi2
    year          = args.year
    lumi          = 36.5 if year=='2016' else 41.4 if (year=='2017' or year=='UL2017') else 59.5 if (year=='2018' or year=='UL2018') else 19.5 if year=='UL2016_preVFP' else 16.8
    indir         = "output_%s"%year
    outdir        = "plots_%s"%year
    ensureDirectory(outdir)

    CMSStyle.setCMSEra(year)

    for region in setup["regions"]:
       plot2D_Scan(setup,region,year,indir=indir,tag=tag,poi1=poi1,poi2=poi2)




if __name__ == '__main__':
     
    
    argv = sys.argv
    description = '''Plot 2d contours.'''
    parser = ArgumentParser(prog="plot2dContour",description=description,epilog="Succes!")
    parser.add_argument('-y', '--year',        dest='year', choices=['2016','2017','2018','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018', 'UL2018_v10'], type=str, default='2017', action='store', help="select year")
    parser.add_argument('-c', '--config', dest='config', type=str, default='TauES/config/defaultFitSetuppoi_mutau.yml', action='store', help="set config file containing sample & fit setup" )
    parser.add_argument('-v', '--verbose',     dest='verbose',  default=False, action='store_true', help="set verbose")
    parser.add_argument('-p1', '--poi1',     dest='poi1', default='tes', type=str, action='store', help='use this parameter of interest')
    parser.add_argument('-p2', '--poi2',     dest='poi2', default='tid_SF', type=str, action='store', help='use this parameter of interest')

    args = parser.parse_args()
    
    main(args)
    print ">>>\n>>> done\n"
    