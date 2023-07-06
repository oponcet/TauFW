  
#! /usr/bin/env python
# Author: P.Mastrapasqua, O. Poncet (May 2023)
# Usage: python TauES_ID/createJSON_poi.py -y UL2018 -c ./TauES_ID/config/FitSetup_mutau_9pt_40-200.yml
'''This script makes pt-dependants poi json/root files from config file.'''
import ROOT
import os, sys,yaml
from array import array
from argparse import ArgumentParser
from collections import OrderedDict
from ROOT import gROOT, gPad, gStyle, TFile, TCanvas, TLegend, TLatex, TF1, TGraph, TGraph2D, TPolyMarker3D, TGraphAsymmErrors, TLine,kBlack, kBlue, kRed, kGreen, kYellow, kOrange, kMagenta, kTeal, kAzure, TMath
#from TauFW.Plotter.sample.utils import CMSStyle
# import correctionlib.schemav2 as cs
# import rich

def load_pt_values(setup,**kwargs):
    poi          = kwargs.get('poi',       ""              )
    pt_avg_list = []
    pt_error_list  = []
    bins_order = setup["plottingOrder"]
    for ibin, ptregion in enumerate(bins_order):
        # print("region = %s" %(ptregion))
        # print("region = %s" %(ptregion))
        if poi == 'poi': 
          print(poi)
          title = setup["poiRegions"][ptregion]["title"]
        else:
            title = setup["tid_poiRegions"][ptregion]["title"]
        str_pt_lo = title.split("<")[0].split(" ")[-1]
        str_pt_hi = title.split("<")[-1].split(" ")[0]
        pt_hi = float(str_pt_hi)
        pt_lo = float(str_pt_lo)
        pt_avg = (pt_hi + pt_lo) / 2.0
        pt_error = pt_avg - pt_lo
        pt_avg_list.append(pt_avg)
        pt_error_list.append(pt_error)
        # print("pt average = %f and pt error = %s" %(pt_avg, pt_error))

    return pt_avg_list, pt_error_list

def load_edges(setup,**kwargs):
    poi          = kwargs.get('poi',       ""              )
    edg  = []
    bins_order = setup["plottingOrder"]
    for ibin, ptregion in enumerate(bins_order):
        # print("region = %s" %(ptregion))
        if poi == 'poi': 
          print(poi)
          title = setup["poiRegions"][ptregion]["title"]
        else:
            title = setup["tid_poiRegions"][ptregion]["title"]       
        str_pt_lo = title.split("<")[0].split(" ")[-1]
        str_pt_hi = title.split("<")[-1].split(" ")[0]
        #print("ibin")
        #print(str_pt_lo)
        #print(str_pt_hi)
        pt_hi = float(str_pt_hi)
        pt_lo = float(str_pt_lo)
        edg.append(pt_lo)
    #print(pt_hi)
    edg.append(pt_hi)
    return edg

# Load the id poi measurement from measurement_poi_.txt file produced with plotParabola_POI_region.py
def load_poi_measurements(setup,year,**kwargs):

  indir   = kwargs.get('indir',       "plots_%s"%year )
  tag     = kwargs.get('tag',         ""              )

  region = []
  poi = []
  poi_errhi = []
  poi_errlo = []
  #inputfilename = "%s/measurement_poi_mt_v10_2p5%s_DeepTau.txt" %(indir,tag)
  inputfilename = "./plots_UL2018_v10/_mutau_mt65_DM_Dt2p5_rangev1/measurement_poi_mt_mutau_mt65_DM_Dt2p5_rangev1_DeepTau_fit_asymm.txt"
  with open(inputfilename, 'r') as file:
      next(file)
      for line in file:
        cols = line.strip().split()
        region.append(str(cols[0]))
        poi.append(float(cols[1]))
        poi_errhi.append(float(cols[3]))
        poi_errlo.append(float(cols[2]))
  #Print the lists
  # print(region)
  # print(poi)
  # print(poi_errhi)
  # print(poi_errlo)
  return region, poi, poi_errhi, poi_errlo


def plot_dm_graph(setup,year,form,**kwargs):

  indir   = kwargs.get('indir',       "plots_%s"%year )
  outdir  = kwargs.get('outdir',      "plots_%s"%year )
  tag     = kwargs.get('tag',         ""              )

  pt_avg_list, pt_error_list = load_pt_values(setup)
  pt_edges = load_edges(setup)
  region, poi, poi_errhi, poi_errlo = load_poi_measurements(setup, year, tag=tag, indir=indir)
  
  # loop over DMs
  print(">>> DM exclusive ")
  # define the DM order
  dm_order = ["DM0_", "DM1_", "DM10_", "DM11_"]

  # create a dictionary to store poi data
  poi_dict = {}
  # loop over DMs
  for dm in dm_order:
      print(">>>>>>>>>>>> %s:" %(dm))
      # filter elements with current DM
      dm_list = [elem for elem in region if dm in elem]
      print("Elements with %s:" %(dm_list))
      # get values for current DM
      print(">>>>>> INPUT FOR JSON")
      dm_poi = [poi[region.index(elem)] for elem in dm_list]
      print("poi for : %s" %(dm_poi))
      dm_pt_edges = [pt_edges[region.index(elem)] for elem in dm_list]
      dm_pt_edges.append(pt_edges[-1])
      print("pt_edges for : %s" %(dm_pt_edges))

      dm_poi_errhi = [poi_errhi[region.index(elem)] for elem in dm_list]
      print("poi_errhi :  %s" %(dm_poi_errhi))
      dm_poi_errlo = [poi_errlo[region.index(elem)] for elem in dm_list]
      print("poi_errlo :  %s" %(dm_poi_errlo))
   
      dm_poi_up = [sum(x) for x in zip(dm_poi,dm_poi_errhi)] 
      print("poi_up for : %s" %(dm_poi_up))
      dm_poi_errlo_neg = [-x for x in dm_poi_errlo]
      dm_poi_down = [sum(x) for x in zip(dm_poi,dm_poi_errlo_neg)]
      print("poi_down for : %s" %(dm_poi_down))

      poi_dict[dm.replace("DM", "").replace("_","")] = {"edges": dm_pt_edges, "content":dm_poi, "up": dm_poi_up, "down": dm_poi_down}
      print("poi dictionary")
      print(poi_dict)
  
  if form=='root':
      poifile = TFile("poi_DeepTau2018v2p5VSjet_%s.root"%year, 'recreate')
      #loop on DMs
      for kdm in poi_dict:
          funcstr = '(x<=20)*0'
          funcstr_up = '(x<=20)*0'
          funcstr_down = '(x<=20)*0'
          for ip in range(0, len(poi_dict[kdm]["content"])):
              funcstr += '+ ( x > ' + str(poi_dict[kdm]["edges"][ip]) + ' && x <=' + str(poi_dict[kdm]["edges"][ip+1]) + ')*' + str(poi_dict[kdm]["content"][ip])
              funcstr_up += '+ ( x > ' + str(poi_dict[kdm]["edges"][ip]) + ' && x <=' + str(poi_dict[kdm]["edges"][ip+1]) + ')*' + str(poi_dict[kdm]["up"][ip])
              funcstr_down += '+ ( x > ' + str(poi_dict[kdm]["edges"][ip]) + ' && x <=' + str(poi_dict[kdm]["edges"][ip+1]) + ')*' + str(poi_dict[kdm]["down"][ip])
          funcstr +='+ ( x > 200)*1.0'
          funcstr_up +='+ ( x > 200)*1.0'
          funcstr_down +='+ ( x > 200)*1.0'
          print("DM"+kdm)
          print(funcstr)
          func_poi      = TF1('Medium_DM' + kdm + '_cent', funcstr,     0,200)
          func_poi.Write()
          func_poi_up   = TF1('Medium_DM' + kdm + '_up', funcstr_up,     0,200)
          func_poi_up.Write()
          func_poi_down = TF1('Medium_DM' + kdm + '_down', funcstr_down,     0,200)
          func_poi_down.Write()
      poifile.Write()
      poifile.Close()
  
#   if form=='json': 
#       ###############################################################
#       ## create JSON file with pois (following correctionlib rules)
#       corr = cs.Correction(
#          name="TauIdpoi",
#          version=1,
#          description="Tau Id poi, pT binned divided by DM",
#          inputs= [
#                  cs.Variable(name="genmatch", type="int", description="Tau genmatch, poi only on real taus (genmatch 5) "),
#                  cs.Variable(name="DM", type="int", description="Tau decay mode (0,1,10,11)"),
#                  cs.Variable(name="pT", type="real", description="Tau transverse momentum"),
#                  ], 
#          output={'name': "poi", 'type': "real", 'description': "Tau Id scale factor"},
#          data=cs.Category(
#               nodetype="category",
#               input="genmatch",
#               content=[
#                       cs.CategoryItem(key=1,value=1.0),
#                       cs.CategoryItem(key=2,value=1.0),
#                       cs.CategoryItem(key=3,value=1.0),
#                       cs.CategoryItem(key=4,value=1.0),
#                       cs.CategoryItem(key=5,
#                                       value=cs.Category(
#                                             nodetype="category",
#                                             input="DM",
#                                             content=[
#                                                     cs.CategoryItem(key=0,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=poi_dict["0"]["edges"],
#                                                           content=poi_dict["0"]["content"] ,
#                                                           flow="clamp"
#                                                           )), 
#                                                     cs.CategoryItem(key=1,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=poi_dict["1"]["edges"],
#                                                           content=poi_dict["1"]["content"] ,
#                                                           flow="clamp"
#                                                           )),
#                                                     cs.CategoryItem(key=10,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=poi_dict["10"]["edges"],
#                                                           content=poi_dict["10"]["content"] ,
#                                                           flow="clamp"
#                                                           )),
#                                                     cs.CategoryItem(key=11,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=poi_dict["11"]["edges"],
#                                                           content=poi_dict["11"]["content"] ,
#                                                           flow="clamp"
#                                                           )),
#                                                     ]
#                                                     )),
#                       cs.CategoryItem(key=6,value=1.0),
#                       cs.CategoryItem(key=0,value=1.0)
#                       ]
#                       )
#              )

    #   print("Evaluate a point: ")
    #   print(corr.to_evaluator().evaluate(5,11,300.))
    #   rich.print(corr)
    #   cset = cs.CorrectionSet(
    #          schema_version=2,
    #          description="Tau pois",
    #          corrections=[
    #                       corr
    #                      ],
    #          )
    #   with open("poi_DeepTau2018v2p5VSjet_%s.json"%year, "w") as fout:
    #        print(">>>Writing JSON!")
    #        fout.write(cset.json())


def ensureDirectory(dirname):
  """Make directory if it does not exist."""
  if not os.path.exists(dirname):
      os.makedirs(dirname)
      print(">>> made directory %s"%dirname)


def main(args):
    
  print("Using configuration file: %s"%args.config)
  with open(args.config, 'r') as file:
      setup = yaml.safe_load(file)

  tag           = setup["tag"] if "tag" in setup else ""
  year          = args.year
  form          = args.form
  poi           = args.poi
  indir         = "plots_%s"%year
  outdir        = "plots_%s"%year
  ensureDirectory(outdir)
  #CMSStyle.setCMSEra(year)

  plot_dm_graph(setup,year,form,indir=indir,outdir=outdir,tag=tag)


if __name__ == '__main__':

    description = '''This script makes plot of pt-dependants id poi measurments from txt file and config file.'''
    parser = ArgumentParser(prog="plot_id_poi",description=description,epilog="Success!")
    parser.add_argument('-y', '--year', dest='year', choices=['2016','2017','2018','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018','UL2018_v10'], type=str, default='UL2018', action='store', help="select year")
    parser.add_argument('-c', '--config', dest='config', type=str, default='TauES_ID/config/FitSetuppoi_mutau_nopoi_pt_DM.yml', action='store', help="set config file")
    parser.add_argument('-f', '--form', dest='form', choices=['json', 'root'], type=str, default='root', action='store', help="select format")
    parser.add_argument('-p', '--poi', dest='poi', default='tid_poi', type=str, action='store', help='use this parameter of interest')
    args = parser.parse_args()
    main(args)
    print(">>>\n>>> done\n")