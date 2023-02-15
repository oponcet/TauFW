  
# this script takes the fit result and converts it into a set of TGraphAsymmErrors objects

import ROOT
from array import array
from argparse import ArgumentParser
import yaml
from collections import OrderedDict


# HI
description = '''This script makes plot of pt-dependants id SF measurments from txt file and config file.'''
parser = ArgumentParser(prog="plot_it_SF",description=description,epilog="Success!")
parser.add_argument('-c', '--config', dest='config', type=str, default='TauES_ID/config/FitSetupTES_mutau_noSF_pt_DM.yml', action='store', help="set config file")
parser.add_argument('--dm-bins', dest='dm_bins', default=False, action='store_true', help="if specified then the mu+tauh channel fits are also split by tau decay-mode")
args = parser.parse_args()
dm_bins=args.dm_bins


print "Using configuration file: %s"%args.config
with open(args.config, 'r') as file:
  setup = yaml.safe_load(file)

  pt_avg_list = []
  pt_error_list  = []

  # Need this because dictionaries are unordered collections
  binsOrder = setup["plottingOrder"] 

  for ibin,ptregion in enumerate(binsOrder):
    #print("region = %s" %(ptregion))
    # pt width and average value 
    title = setup["tid_SFRegions"][ptregion]["title"]
    str_pt_lo = title.split("<")[0].split(" ")[-1]
    str_pt_hi = title.split("<")[-1].split(" ")[0]
    pt_hi = float(str_pt_hi)
    pt_lo = float(str_pt_lo)
    pt_avg = (pt_hi + pt_lo) / 2.0
    pt_error = pt_avg - pt_lo
    #print("pt average = %f and pt error = %s" %(pt_avg, pt_error))
    pt_avg_list.append(pt_avg)
    pt_error_list.append(pt_error)


# Open the file
with open('plots_UL2018/measurement_poi_mt_mtlt65_noSF_DMpt_DeepTau.txt', 'r') as file:

  # Skip the first line whcihc contains the date and info of the file 
  next(file)

  # Create empty lists for each column
  region = []
  id_SFs = []
  id_SFs_errhi = []
  id_SFs_errlo = []

  # Loop through each line in the file
  for line in file:

      # Split the line into columns using whitespace as the delimiter
      cols = line.strip().split()

      # Append the values from each column to the corresponding list
      region.append(str(cols[0]))
      id_SFs.append(float(cols[1]))
      id_SFs_errhi.append(float(cols[2]))
      id_SFs_errlo.append(float(cols[3]))

#Print the lists
# print(region)
# print(id_SFs)
# print(id_SFs_errhi)
# print(id_SFs_errlo)
# print(pt_avg_list)
# print(pt_error_list)


# define the DM order
dm_order = ["DM0_", "DM1_", "DM10_", "DM11_"]

# create a dictionary to store the TGraphAsymmErrors objects
graphs_dict = {}

# loop over DMs
for dm in dm_order:
  print(">>>>>>>>>>>> %s:" %(dm))
  # filter elements with current DM
  dm_list = [elem for elem in region if dm in elem]
  print("Elements with %s:" %(dm_list))
  # get values for current DM
  dm_id_SFs = [id_SFs[region.index(elem)] for elem in dm_list]
  print("id_SFs for : %s" %(dm_id_SFs))
  dm_id_SFs_errhi = [id_SFs_errhi[region.index(elem)] for elem in dm_list]
  print("id_SFs_errhi :  %s" %(dm_id_SFs_errhi))
  dm_id_SFs_errlo = [id_SFs_errlo[region.index(elem)] for elem in dm_list]
  print("id_SFs_errlo :  %s" %(dm_id_SFs_errlo))
  dm_pt_avg_list = [pt_avg_list[region.index(elem)] for elem in dm_list]
  print("pt_avg_list : %s" %(dm_pt_avg_list))
  dm_pt_error_list = [pt_error_list[region.index(elem)] for elem in dm_list]
  print("pt_error_list : %s" %(dm_pt_error_list))
  
  # create a TGraphAsymmErrors object for the current DM
  graph = ROOT.TGraphAsymmErrors(len(dm_pt_avg_list),
                                  array("d", dm_pt_avg_list),
                                  array("d", dm_id_SFs),
                                  array("d", dm_pt_error_list),
                                  array("d", dm_pt_error_list),
                                  array("d", dm_id_SFs_errlo),
                                  array("d", dm_id_SFs_errhi))
  
  # set the title and axis labels for the graph
  graph.SetTitle("ID Scale Factors vs. pT for %s" % dm)
  graph.GetXaxis().SetTitle("pT [GeV]")
  graph.GetYaxis().SetTitle("ID Scale Factors")
  graph.GetYaxis().SetRangeUser(0.65, 1.1)
  
  # add the graph to the dictionary
  graphs_dict[dm] = graph
  
  # disable the canvas drawing
  ROOT.gROOT.SetBatch(True)
  
  # draw the graph
  outdir = "plots_UL2018"
  canvasname = "%s/id_SF_ptplot_%s" %(outdir,dm)
  canvas = ROOT.TCanvas(canvasname, canvasname, 800, 600)
  graph.Draw("AP")
  canvas.Draw()
  canvas.SaveAs(canvasname+".root")
  canvas.Close()


