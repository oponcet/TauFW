  
#! /usr/bin/env python
# Author: P.Mastrapasqua, O. Poncet (May 2023)
# Usage: python TauES_ID/createJSON_idSF.py -y UL2018 -c ./TauES_ID/config/FitSetup_mutau_9pt_40-200.yml
'''This script makes pt-dependants id SF json/root files from config file.'''
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
    pt_avg_list = []
    pt_error_list  = []
    bins_order = setup["plottingOrder"]
    for ibin, ptregion in enumerate(bins_order):
        # print("region = %s" %(ptregion))
        title = setup["tid_SFRegions"][ptregion]["title"]
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
    edg  = []
    bins_order = setup["plottingOrder"]
    for ibin, ptregion in enumerate(bins_order):
        # print("region = %s" %(ptregion))
        title = setup["tid_SFRegions"][ptregion]["title"]
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

# Load the id SF measurement from measurement_poi_.txt file produced with plotParabola_POI_region.py
def load_sf_measurements(setup,year,**kwargs):

  indir   = kwargs.get('indir',       "plots_%s"%year )
  tag     = kwargs.get('tag',         ""              )

  region = []
  id_SFs = []
  id_SFs_errhi = []
  id_SFs_errlo = []
  #inputfilename = "%s/measurement_poi_mt_v10_2p5%s_DeepTau.txt" %(indir,tag)
  inputfilename = "./plots_UL2018_v10/_mutau_mt65_DM_pt_Dt2p5_v2/opt2/measurement_poi_mt_mutau_mt65_DM_pt_Dt2p5_v2_DeepTau.txt"
  with open(inputfilename, 'r') as file:
      next(file)
      for line in file:
          cols = line.strip().split()
          region.append(str(cols[0]))
          id_SFs.append(float(cols[1]))
          id_SFs_errhi.append(float(cols[3]))
          id_SFs_errlo.append(float(cols[2]))
  #Print the lists
  # print(region)
  # print(id_SFs)
  # print(id_SFs_errhi)
  # print(id_SFs_errlo)
  return region, id_SFs, id_SFs_errhi, id_SFs_errlo


def plot_dm_graph(setup,year,form,**kwargs):

  indir   = kwargs.get('indir',       "plots_%s"%year )
  outdir  = kwargs.get('outdir',      "plots_%s"%year )
  tag     = kwargs.get('tag',         ""              )

  pt_avg_list, pt_error_list = load_pt_values(setup)
  pt_edges = load_edges(setup)
  region, id_SFs, id_SFs_errhi, id_SFs_errlo = load_sf_measurements(setup, year, tag=tag, indir=indir)
  
  # loop over DMs
  print(">>> DM exclusive ")
  # define the DM order
  dm_order = ["DM0_", "DM1_", "DM10_", "DM11_"]

  # create a dictionary to store sf data
  sf_dict = {}
  # loop over DMs
  for dm in dm_order:
      print(">>>>>>>>>>>> %s:" %(dm))
      # filter elements with current DM
      dm_list = [elem for elem in region if dm in elem]
      print("Elements with %s:" %(dm_list))
      # get values for current DM
      print(">>>>>> INPUT FOR JSON")
      dm_id_SFs = [id_SFs[region.index(elem)] for elem in dm_list]
      print("id_SFs for : %s" %(dm_id_SFs))
      dm_pt_edges = [pt_edges[region.index(elem)] for elem in dm_list]
      dm_pt_edges.append(pt_edges[-1])
      print("pt_edges for : %s" %(dm_pt_edges))

      dm_id_SFs_errhi = [id_SFs_errhi[region.index(elem)] for elem in dm_list]
      print("id_SFs_errhi :  %s" %(dm_id_SFs_errhi))
      dm_id_SFs_errlo = [id_SFs_errlo[region.index(elem)] for elem in dm_list]
      print("id_SFs_errlo :  %s" %(dm_id_SFs_errlo))
   
      dm_id_SFs_up = [sum(x) for x in zip(dm_id_SFs,dm_id_SFs_errhi)] 
      print("id_SFs_up for : %s" %(dm_id_SFs_up))
      dm_id_SFs_errlo_neg = [-x for x in dm_id_SFs_errlo]
      dm_id_SFs_down = [sum(x) for x in zip(dm_id_SFs,dm_id_SFs_errlo_neg)]
      print("id_SFs_down for : %s" %(dm_id_SFs_down))

      sf_dict[dm.replace("DM", "").replace("_","")] = {"edges": dm_pt_edges, "content":dm_id_SFs, "up": dm_id_SFs_up, "down": dm_id_SFs_down}
      print("SF dictionary")
      print(sf_dict)
  
  if form=='root':
      sfile = TFile("id_SF_DeepTau2018v2p5VSjet_%s.root"%year, 'recreate')
      #loop on DMs
      for kdm in sf_dict:
          funcstr = '(x<=20)*0'
          funcstr_up = '(x<=20)*0'
          funcstr_down = '(x<=20)*0'
          for ip in range(0, len(sf_dict[kdm]["content"])):
              funcstr += '+ ( x > ' + str(sf_dict[kdm]["edges"][ip]) + ' && x <=' + str(sf_dict[kdm]["edges"][ip+1]) + ')*' + str(sf_dict[kdm]["content"][ip])
              funcstr_up += '+ ( x > ' + str(sf_dict[kdm]["edges"][ip]) + ' && x <=' + str(sf_dict[kdm]["edges"][ip+1]) + ')*' + str(sf_dict[kdm]["up"][ip])
              funcstr_down += '+ ( x > ' + str(sf_dict[kdm]["edges"][ip]) + ' && x <=' + str(sf_dict[kdm]["edges"][ip+1]) + ')*' + str(sf_dict[kdm]["down"][ip])
          funcstr +='+ ( x > 200)*1.0'
          funcstr_up +='+ ( x > 200)*1.0'
          funcstr_down +='+ ( x > 200)*1.0'
          print("DM"+kdm)
          print(funcstr)
          func_SF      = TF1('Medium_DM' + kdm + '_cent', funcstr,     0,200)
          func_SF.Write()
          func_SF_up   = TF1('Medium_DM' + kdm + '_up', funcstr_up,     0,200)
          func_SF_up.Write()
          func_SF_down = TF1('Medium_DM' + kdm + '_down', funcstr_down,     0,200)
          func_SF_down.Write()
      sfile.Write()
      sfile.Close()
  
#   if form=='json': 
#       ###############################################################
#       ## create JSON file with SFs (following correctionlib rules)
#       corr = cs.Correction(
#          name="TauIdSF",
#          version=1,
#          description="Tau Id SF, pT binned divided by DM",
#          inputs= [
#                  cs.Variable(name="genmatch", type="int", description="Tau genmatch, sf only on real taus (genmatch 5) "),
#                  cs.Variable(name="DM", type="int", description="Tau decay mode (0,1,10,11)"),
#                  cs.Variable(name="pT", type="real", description="Tau transverse momentum"),
#                  ], 
#          output={'name': "sf", 'type': "real", 'description': "Tau Id scale factor"},
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
#                                                           edges=sf_dict["0"]["edges"],
#                                                           content=sf_dict["0"]["content"] ,
#                                                           flow="clamp"
#                                                           )), 
#                                                     cs.CategoryItem(key=1,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=sf_dict["1"]["edges"],
#                                                           content=sf_dict["1"]["content"] ,
#                                                           flow="clamp"
#                                                           )),
#                                                     cs.CategoryItem(key=10,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=sf_dict["10"]["edges"],
#                                                           content=sf_dict["10"]["content"] ,
#                                                           flow="clamp"
#                                                           )),
#                                                     cs.CategoryItem(key=11,
#                                                     value=cs.Binning(
#                                                           nodetype="binning",
#                                                           input="pT",
#                                                           edges=sf_dict["11"]["edges"],
#                                                           content=sf_dict["11"]["content"] ,
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
    #          description="Tau SFs",
    #          corrections=[
    #                       corr
    #                      ],
    #          )
    #   with open("tes_DeepTau2018v2p5VSjet_%s.json"%year, "w") as fout:
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
  indir         = "plots_%s"%year
  outdir        = "plots_%s"%year
  ensureDirectory(outdir)
  #CMSStyle.setCMSEra(year)

  plot_dm_graph(setup,year,form,indir=indir,outdir=outdir,tag=tag)





if __name__ == '__main__':

  description = '''This script makes plot of pt-dependants id SF measurments from txt file and config file.'''
  parser = ArgumentParser(prog="plot_it_SF",description=description,epilog="Success!")
  parser.add_argument('-y', '--year', dest='year', choices=['2016','2017','2018','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018','UL2018_v10'], type=str, default='UL2018', action='store', help="select year")
  parser.add_argument('-c', '--config', dest='config', type=str, default='TauES_ID/config/FitSetupTES_mutau_noSF_pt_DM.yml', action='store', help="set config file")
  parser.add_argument('-f', '--form', dest='form', choices=['json', 'root'], type=str, default='root', action='store', help="select format")
  args = parser.parse_args()
  main(args)
  print(">>>\n>>> done\n")