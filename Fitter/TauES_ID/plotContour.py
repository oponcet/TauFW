#! /usr/bin/env python
# Author: Izaak Neutelings (January 2018)
# Modification May 2022

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


def plotContour(setup,var,region,year,**kwargs):
    print green("plot 2D contour for %s, %s" % (region, var), pre="\n>>> ")
    
    # Retrieve optional arguments or set default values
    indir        = kwargs.get('indir',       "output_%s"%year )
    outdir       = kwargs.get('outdir',      "plots_%s"%year  )
    tag          = kwargs.get('tag',         ""               )
    plottag      = kwargs.get('plottag',     ""               )
    ctext        = kwargs.get('ctext',       [ ]              )
    poi1         = kwargs.get('poi1',        ""               )
    poi2         = kwargs.get('poi2',        ""               )
    era          = "%s-13TeV"%year
    channel      = setup["channel"].replace("mu","m").replace("tau","t")


    # Construct the name of the canvas
    canvasname = "%s/contour_%s_%s_%s_%s-%s%s%s"%(outdir,poi1,poi2,channel,var,region,tag,plottag)
    ensureDirectory(outdir)

    # Construct the name of the input file
    filename     = '%s/higgsCombine.%s_%s-%s%s-%s.MultiDimFit.mH90.root'%(indir,channel,var,region,tag,era)
    print('>>>   file "%s"'%(filename))
    file = ensureTFile(filename)
    tree = file.Get('limit')
    print("poi1 = %s and poi2= %s" %(poi1,poi2))

    # Process the tree to obtain DeltaNLL values and the corresponding parameter values
    list_nll = [ ]
    list_poi1 = [ ]
    list_poi2 = [ ]
    for i, event in enumerate(tree):
      if i==0: continue
      if tree.quantileExpected<0: continue
      if tree.deltaNLL == 0: continue
      #if tree.poi < 0.97: continue
      poi1_name = "%s_%s"%(poi1,region)
      poi2_name = "%s_%s"%(poi2,region)

      #list_poi.append(tree.poi)
      list_poi1.append(getattr(tree,poi1_name)) 
      list_poi2.append(getattr(tree,poi2_name)) 
      list_nll.append(2*tree.deltaNLL)
    file.Close()

    # Calculate minimum and DeltaNLL values
    nllmin    = min(list_nll)
    print(nllmin)
    list_dnll = map(lambda n: n-nllmin, list_nll) # DeltaNLL 
    # MINIMUM
    dnllmin         = min(list_dnll) # should be 0.0 by definition
    print("dnllmin = %f" %dnllmin)
    min_index       = list_dnll.index(dnllmin)
    list_dnll_left  = list_dnll[:min_index]
    list_poi1_left   = list_poi1[:min_index]
    list_poi2_left   = list_poi2[:min_index]
    list_dnll_right = list_dnll[min_index:]
    list_poi1_right  = list_poi1[min_index:]
    list_poi2_right  = list_poi2[min_index:]
    #print ">>> min   = %d , min_index = %d"%(dnllmin, min_index)
    if len(list_dnll_left)==0 or len(list_dnll_right)==0 : 
      print "ERROR! Parabola does not have minimum within given range !!!"
      exit(1)
  
    tmin1_left = -1
    tmin1_right = -1
    tmin2_left = -1
    tmin2_right = -1
    
    # FIND crossings of 1 sigma line
    # |-----<---min---------|
    for i, val in reversed(list(enumerate(list_dnll_left))):
      if val > (dnllmin+1):
          tmin1_left = list_poi1_left[i]
          tmin2_left = list_poi2_left[i]
          break
    # |---------min--->-----|
    for i, val in enumerate(list_dnll_right):
      if val > (dnllmin+1):
          tmin1_right = list_poi1_right[i]
          tmin2_right = list_poi2_right[i]
          break
    
    poi1_val = round(list_poi1[min_index],4)
    poi2_val = round(list_poi2[min_index],4)


    poi1_errDown = round((poi1_val-tmin1_left)*10000)/10000
    poi1_errUp   = round((tmin1_right-poi1_val)*10000)/10000
    shift1       = (list_poi1[min_index]-1)*100

    poi2_errDown = round((poi2_val-tmin2_left)*10000)/10000
    poi2_errUp   = round((tmin2_right-poi2_val)*10000)/10000
    shift2       = (list_poi2[min_index]-1)*100
    
    # GRAPHS
    graph       = createContourFromLists(list_poi1,list_poi2,list_dnll)
    graphs_bd   = [ ]
    colors_bd   = [kRed, kBlue, kGreen]
    poi_bbb, poi_stat = -1., -1.
    
    # DRAW
    canvas = TCanvas('canvas','canvas',100,100,700,600)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetTopMargin(  0.07 ); canvas.SetBottomMargin( 0.12 )
    canvas.SetLeftMargin( 0.12 ); canvas.SetRightMargin(  0.04 )
    canvas.cd()
    
    xmin, xmax   = 0.95, 1.05
    ymin, ymax   = 0.0,  10.
    fontsize     = 0.044
    lineheight   = 0.05
    xtext, ytext = 0.90, 0.405
    frame = canvas.DrawFrame(xmin,ymin,xmax,ymax)
    frame.GetYaxis().SetTitleSize(0.055)
    frame.GetXaxis().SetTitleSize(0.055)
    frame.GetXaxis().SetLabelSize(0.050)
    frame.GetYaxis().SetLabelSize(0.050)
    frame.GetXaxis().SetLabelOffset(0.010)
    frame.GetXaxis().SetTitleOffset(1.04)
    frame.GetYaxis().SetTitleOffset(1.02)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetXaxis().SetTitle(poi1)
    frame.GetYaxis().SetTitle(poi2)
    frame.GetZaxis().SetTitle('-2#Deltaln(L)')
    
    # GRAPH
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.4)
    graph.Draw('colz')
    
   
    # RESULTS
    latex = TLatex()
    lines = [ ]
    for i,y in [(1,1),(2,4)]:
      line = TLine(xmin, dnllmin+y, xmax, dnllmin+y)
      #line.SetLineWidth(1)
      line.SetLineStyle(7)
      line.Draw('SAME')
      latex.SetTextSize(0.050)
      latex.SetTextAlign(11)
      latex.SetTextFont(42)
      latex.DrawLatex(xmin+0.04*(xmax-xmin),y+0.02*(ymax-ymin),"%d#sigma"%i)
      lines.append(line)
    
    for tmin1 in [tmin1_left,tmin1_right]:
      line1 = TLine(tmin1, dnllmin, tmin1, dnllmin+1)
      line1.SetLineStyle(2)
      line1.Draw('SAME')
      lines.append(line1)

    for tmin2 in [tmin2_left,tmin2_right]:
      line2 = TLine(tmin2, dnllmin, tmin2, dnllmin+1)
      line2.SetLineStyle(2)
      line2.Draw('SAME')
      lines.append(line2)
    
    # LEGEND
    legend = None
    if ctext:
      ctext = writeText(ctext,position='topright',textsize=0.80*fontsize)
    
    # Print the results
    print ">>> poi %7.3f - %-5.3f + %-5.3f"%(poi1_val,poi1_errDown,poi1_errUp)
    print ">>> shift  %7.3f - %-5.3f + %-5.3f %%"%(shift1,poi1_errDown*100,poi1_errUp*100)
    print ">>> poi %7.3f - %-5.3f + %-5.3f"%(poi2_val,poi2_errDown,poi2_errUp)
    print ">>> shift  %7.3f - %-5.3f + %-5.3f %%"%(shift2,poi2_errDown*100,poi2_errUp*100)

    # Draw the text and legend
    text = TLatex()
    text.SetTextSize(fontsize)
    text.SetTextAlign(31)
    text.SetTextFont(42)
    text.SetNDC(True)
    if "title" in setup["observables"][var]:
        text.DrawLatex(xtext,ytext, "%s"%(setup["observables"][var]["title"]))
    else:
        text.DrawLatex(xtext,ytext, "%s"%(var))
    text.DrawLatex(xtext,ytext-lineheight,     "%s"%(region))
    text.DrawLatex(xtext,ytext-2.0*lineheight, "%7.3f_{-%5.3f}^{+%5.3f}"%(poi1_val,poi1_errDown,poi1_errUp))
    text.DrawLatex(xtext,ytext-2.2*lineheight, "%7.3f_{-%5.3f}^{+%5.3f}"%(poi2_val,poi2_errDown,poi2_errUp))


    CMSStyle.setCMSLumiStyle(canvas,0)
    #canvas.SetTicks(1,1)

    # Save the canvas
    canvas.Modified()
    canvas.Update()
    canvas.SaveAs(canvasname+".png")
    canvas.SaveAs(canvasname+".root")
    canvas.Close()
    
    return poi1_val, poi1_errDown, poi1_errUp,poi2_val, poi2_errDown, poi2_errUp
    

def createContourFromLists(list_x, list_y, list_dnll):
    """Create TGraph2D of DeltaNLL contour vs. x and y from lists."""
    npoints = len(list_dnll)
    graph = TGraph2D(npoints)
    for i in range(npoints):
        x = list_x[i]
        y = list_y[i]
        dnll = list_dnll[i]
        graph.SetPoint(i, x, y, dnll)
    return graph


def createContour(filename, poi, region):
    """Create TGraph2D of DeltaNLL contour vs. x and y from MultiDimFit file."""
    file = ensureTFile(filename)
    tree = file.Get('limit')
    poi1, poi2, dnll = [], [], []
    for i, event in enumerate(tree):
        if i == 0:
            continue
        # poi.append(tree.poi)
        poi1_name = "%s_%s"%(poi1,region) #combine DM 
        poi2_name = "%s_%s"%(poi2,region) #combine DM 
        poi1.append(getattr(tree,poi1_name))  # modify to get x coordinate from the tree
        poi2.append(getattr(tree, poi2_name))  # modify to get y coordinate from the tree
        dnll.append(2 * tree.deltaNLL)
    file.Close()
    minnll = min(dnll)
    minx = x[dnll.index(minnll)]
    miny = y[dnll.index(minnll)]
    dnll = list(map(lambda val: val - minnll, dnll))  # DeltaNLL
    graph = TGraph2D(len(x), array('d', x), array('d', y), array('d', dnll))
    return graph, minx, miny

   
def writeText(*text,**kwargs):
    """Write text on plot."""
    
    position = kwargs.get('position',     'topleft'       ).lower()
    textsize = kwargs.get('textsize',     0.040           )
    font     = 62 if kwargs.get('bold',   False           ) else 42
    align    = 13
    if len(text)==1 and isinstance(text[0],list):
      text = text[0]
    else:
      text     = ensureList(text)
    if not text or not any(t!="" for t in text):
      return None
    L, R     = gPad.GetLeftMargin(), gPad.GetRightMargin()
    T, B     = gPad.GetTopMargin(),  gPad.GetBottomMargin()
    
    if 'right' in position:
      x, align = 0.96, 30
    else:
      x, align = 0.04, 10
    if 'bottom' in position:
      y = 0.05; align += 1
    else:
      y = 0.95; align += 3
    x = L + (1-L-R)*x
    y = B + (1-T-B)*y

    latex = TLatex()
    latex.SetTextSize(textsize)
    latex.SetTextAlign(align)
    latex.SetTextFont(font)
    #latex.SetTextColor(kRed)
    latex.SetNDC(True)
    for i, line in enumerate(text):
      latex.DrawLatex(x,y-i*1.2*textsize,line)
    
    return latex
    


def stringWidth(*strings0):
    """Make educated guess on the maximum length of a string."""
    strings = list(strings0)
    for string in strings0:
      matches = re.search(r"#splitline\{(.*?)\}\{(.*?)\}",string) # check splitline
      if matches:
        while string in strings: strings.pop(strings.index(string))
        strings.extend([matches.group(1),matches.group(2)])
      matches = re.search(r"[_^]\{(.*?)\}",string) # check subscript/superscript
      if matches:
        while string in strings: strings.pop(strings.index(string))
        strings.append(matches.group(1))
      string = string.replace('#','')
    return max([len(s) for s in strings])
    
def marginCenter(canvas,axis,side='left',shift=0,margin=None):
    """Calculate the center of the right margin in units of a given axis"""
    range    = axis.GetXmax() - axis.GetXmin()
    rangeNDC = 1 - canvas.GetRightMargin() - canvas.GetLeftMargin()
    if side=='right':
      if margin==None: margin = canvas.GetRightMargin()
      center = axis.GetXmax() + margin*range/rangeNDC/2.
    else:
      if margin==None: margin = canvas.GetLeftMargin()
      center = axis.GetXmin() - margin*range/rangeNDC/2.
    if shift:
        if center>0: center*=(1+shift/100.0)
        else:        center*=(1-shift/100.0)
    return center
    
def green(string,**kwargs):
  return kwargs.get('pre',"")+"\x1b[0;32;40m%s\033[0m"%(string)
  
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

def ensureFile(filename):
  if not os.path.isfile(filename):
    error('File "%s" does not exist!'%(filename))
  return filename
  
def ensureList(arg):
  return arg if (isinstance(arg,list) or isinstance(arg,tuple)) else [arg]



def main(args):
    
    print "Using configuration file: %s"%args.config
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
    multiDimFit   = args.multiDimFit
    summary       = args.summary
    parabola      = args.parabola
    customSummary = args.customSummary
    ensureDirectory(outdir)

    CMSStyle.setCMSEra(year)
    
    fittag  =  "_fit"
    tag += args.extratag
    
    # LOOP over tags, channels, variables
    print "parabola %i"%parabola
    if parabola:
        points, points_fit = [ ], [ ]

        allObs = []
        allObsTitles = []
        allRegions = []
        for v in setup["observables"]:
            print v
            var = setup["observables"][v]
            if not v in allObs:
                allObs.append(v)
                if "title" in var:
                    allObsTitles.append(var["title"])
                else:
                    allObsTitles.append(v)
        for r in setup["regions"]:
            print r
            isUsedInFit = True #change to true
            for v in setup["observables"]:
                if r in setup["observables"][v]["fitRegions"]:
                    isUsedInFit = True
                    break
            if isUsedInFit and not r in allRegions:
                allRegions.append(r)

        for var in setup["observables"]:
            variable = setup["observables"][var]
            
            # MULTIDIMFIT
            slices = { }
         
            print allRegions
            # LOOP over regions
            for i, region in enumerate(allRegions):
                if not region in variable["fitRegions"]:
                    if len(points)<=i: points.append([ ]); points_fit.append([ ])
                    points[i].append(None); points_fit[i].append(None)
                    continue
      
                # PARABOLA
               
                poi1_val,poi1Down,poi1Up,poi2_val,poi2Down,poi2Up = plotContour(setup,var,region,year,indir=indir,tag=tag,poi1=poi1,poi2=poi2)
              
                # SAVE points
                if len(points)<=i: points.append([ ]); points_fit.append([ ])
                points[i].append((poi1_val,poi1Down,poi1Up))
                points[i].append((poi2_val,poi2Down,poi2Up))
          
            if len(points)>1 :
                print green("write results to file",pre="\n>>> ")
                filename = "%s/measurement_poi_%s%s"%(outdir,channel,tag)
                # writeMeasurement(filename,allRegions,points)
            
    
    # SUMMARY plot
    if summary:
        print green("make summary plot for %s"%(tag),pre="\n>>> ")
        ftags = [ tag ]
        for ftag in ftags:
            canvas = "%s/measurement_poi_%s%s"%(outdir,channel,ftag)
            # measurements = readMeasurement(canvas)

            #plotMeasurements(setup, measurements, (setup["plottingOrder"] if "plottingOrder" in setup else allRegions) ,canvas=canvas,xtitle="tau energy scale",xmin=min(setup["TESvariations"]["values"]),xmax=max(setup["TESvariations"]["values"]),L=0.20, position="out",entries=allObsTitles,emargin=0.14,cposition='topright',exts=['png','pdf'])
            # plotMeasurements(setup, measurements, (setup["plottingOrder"] if "plottingOrder" in setup else allRegions) ,canvas=canvas,xtitle="tau energy scale",xmin=0.95,xmax=1.05,L=0.20, position="out",entries=allObsTitles,emargin=0.14,cposition='topright',exts=['png','pdf'])

       


if __name__ == '__main__':
     
    
    argv = sys.argv
    description = '''Plot parabolas.'''
    parser = ArgumentParser(prog="plotParabola",description=description,epilog="Succes!")
    parser.add_argument('-y', '--year',        dest='year', choices=['2016','2017','2018','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018', 'UL2018_v10'], type=str, default='2017', action='store', help="select year")
    parser.add_argument('-c', '--config', dest='config', type=str, default='TauES/config/defaultFitSetuppoi_mutau.yml', action='store', help="set config file containing sample & fit setup" )
    parser.add_argument('-e', '--extra-tag',   dest='extratag', type=str, default="", action='store', metavar='TAG', help="extra tag for output files")
    parser.add_argument('-r', '--shift-range', dest='shiftRange', type=str, default="0.940,1.060", action='store', metavar='RANGE',       help="range of poi shifts")
    parser.add_argument('-M', '--multiDimFit', dest='multiDimFit',  default=False, action='store_true', help="assume multidimensional fit with a POI for each DM")
    parser.add_argument('-n', '--no-para',     dest='parabola', default=True, action='store_false', help="make summary of measurements")
    parser.add_argument('-s', '--summary',     dest='summary', default=False, action='store_true', help="make summary of measurements")
    parser.add_argument(      '--custom',      dest='customSummary', nargs='*', default=False, action='store',help="make custom summary of measurements")
    parser.add_argument('-v', '--verbose',     dest='verbose',  default=False, action='store_true', help="set verbose")
    parser.add_argument('-p1', '--poi1',     dest='poi1', default='tes', type=str, action='store', help='use this parameter of interest')
    parser.add_argument('-p2', '--poi2',     dest='poi2', default='tid_SF', type=str, action='store', help='use this parameter of interest')

    args = parser.parse_args()
    
    main(args)
    print ">>>\n>>> done\n"
    

