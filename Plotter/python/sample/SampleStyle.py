# -*- coding: utf-8 -*-
# Author: Izaak Neutelings (July 2020)
import os, re
from collections import OrderedDict
from tabnanny import verbose
from TauFW.Plotter.sample.utils import LOG
from TauFW.Plotter.plot.string import makelatex
from ROOT import TColor, kBlack, kWhite, kGray, kAzure, kBlue, kCyan,\
                 kGreen, kSpring, kTeal, kYellow,\
                 kOrange, kRed, kPink, kMagenta, kViolet

sample_titles = {
  'DY':         "Drell-Yan", # Z + jets
  'DY_M50':     "Drell-Yan, M > 50 GeV",
  'DY_M10to50': "Drell-Yan, 10 GeV < M < 50 GeV ",
  'ZMM':        "Z -> mumu",
  'ZTT':        "Z -> tau_{l}tau_{h}",
  'ZTT_DM0':    "Z -> tau_{l}tau_{h}, h^{#pm}",
  'ZTT_DM1':    "Z -> tau_{l}tau_{h}, h^{#pm}#pi^{0}",
  'ZTT_DM10':   "Z -> tau_{l}tau_{h}, h^{#pm}h^{#mp}h^{#pm}",
  'ZTT_DM11':   "Z -> tau_{l}tau_{h}, h^{#pm}h^{#mp}h^{#pm}#pi^{0}",
  'ZTT_other':  "Z -> tau_{l}tau_{h}, other",
  'ZL':         "Z -> ll, l -> tau_h", #"Drell-Yan with l -> tau_h",
  'ZJ':         "Drell-Yan, j -> tau_h",
  'Top':        "ttbar and single t",
  'TopT':       "ttbar and single t, real tau_h",
  'TopJ':       "ttbar and single t other",
  'TT':         "ttbar",
  'TTT':        "ttbar, real tau_h",
  'TTJ':        "ttbar other",
  'TTL':        "ttbar, l -> tau_h",
  'ST':         "Single t",
  'STT':        "Single t, real tau_h",
  'STL':        "Single t, l -> tau_h",
  'STJ':        "Single t other",
  'EWK':        "Electroweak",
  'EWKT':       "Electroweak, real tau_h",
  'EWKJ':       "Electroweak",
  'VV':         "Diboson",
  'VVT':        "Diboson, real tau_h",
  'VVJ':        "Diboson other",
  'W':          "W + jets",
  'WMu':         "WToMuNu",
  'WTau':        "WToTauNu",
  'WJ':         "W + jets",
  'JTF':        "j -> tau_h fakes",
  'QCD':        "QCD multijet",
  'Data':       "Observed",
  'data_obs':   "Observed",
}

sample_colors = {
  'DY':        kAzure+5, #kOrange-4,
  'ZL':        kAzure+5, #TColor.GetColor(100,182,232), #kAzure+5,
  'ZJ':        kGreen-6,
  'ZMM':       kAzure+5,
  'ZTT':       kOrange-4,
  'ZTT_DM0':   kOrange+5,
  'ZTT_DM1':   kOrange-4, #kOrange,
  'ZTT_DM10':  kYellow-9,
  'ZTT_DM11':  kOrange-6,
  'ZTT_other': kOrange-10,
  'DY10':      kOrange-4, #TColor.GetColor(240,175,60), #TColor.GetColor(222,90,106)
  'TT':        kBlue-8,
  'TTT':       kAzure-9,
  'TTL':       kBlue-8,
  'TTJ':       kGreen-8, #kViolet-8, #kGreen-2,
  'ST':        38, #TColor.GetColor(140,180,220),
  'STL':       kMagenta-3,
  'STJ':       kMagenta-8,
  'VV':        45, #TColor.GetColor(222,140,106),
  'VVT':       kOrange+5, #TColor.GetColor(222,140,106),
  'VVJ':       kOrange-6, #TColor.GetColor(222,140,106),
  'WMu':       400,
  'WTau':      416,
  'WJ':        50,
  'QCD':       kMagenta-10,
  'Data':      kBlack,
}


def set_sample_colors(coldict):
  global sample_colors
  sample_colors = OrderedDict([ # order matters: first match to key is used
    ('ZTT_DM11',         coldict['ZTT_DM11']),
    ('ZTT_DM10',         coldict['ZTT_DM10']),
    ('ZTT_DM1',          coldict['ZTT_DM1']),
    ('ZTT_DM0',          coldict['ZTT_DM0']),
    ('ZTT_DMother',      coldict['ZTT_other']),
    #('Z*tau*h*pm',       coldict['ZTT_DM0']),
    #('Z*tau*h*pm*h*0',   coldict['ZTT_DM1']),
    #('Z*tau*h*h*h',      coldict['ZTT_DM10']),
    #('Z*tau*h*h*h*h*0',  coldict['ZTT_DM11']),
    #('Z*tau*other',      coldict['DY10']),
    ('ZTT',              coldict['ZTT']),
    ('ZMM',              coldict['ZMM']),
    ('ZL',               coldict['ZL']),
    ('ZJ',               coldict['ZJ']),
    ('Z*tau',            coldict['DY']),
    ('Z*ll',             coldict['ZL']),
    ('D*Y*j*tau',        coldict['ZJ']),
    ('D*Y*l*tau',        coldict['ZL']),
    ('D*Y*other',        coldict['ZJ']), #kSpring+3, kPink-2
    ('D*Y*10*50',        coldict['DY10']),
    ('DY',               coldict['DY']),
    ('Drel*Yan',         coldict['DY']),
    ('Embedded',         coldict['DY']),
    ('EWKT',             coldict['VV']),
    ('EWKJ',             coldict['WJ']),
    ('EWK',              coldict['WJ']),
    ('WToMuNu',          coldict['WMu']),
    ('WToTauNu',         coldict['WTau']),
    ('W*jets',           coldict['WJ']),
    ('W*J',              coldict['WJ']),
    ('W',                coldict['WJ']),
    ('WW',               coldict['VV']),
    ('WZ',               coldict['VV']),
    ('ZZ',               coldict['VV']),
    ('VVT',              coldict['VVT']),
    ('VVJ',              coldict['VVJ']),
    ('VV',               coldict['VV']),
    ('Diboson',          coldict['VV']),
    ('Electroweak',      coldict['WJ']),
    ('STT',              coldict['ST']),
    ('STJ',              coldict['STJ']),
    ('STL',              coldict['STL']),
    ('ST',               coldict['ST']),
    #('Single*top':       coldict['ST']),
    #('Single*top*real',  coldict['ST']),
    #('Single*top*other', coldict['STJ'],
    ('TTT',              coldict['TTT']),
    ('TTL',              coldict['TTL']),
    ('TTJ',              coldict['TTJ']),
    ('TT',               coldict['TT']),
    #('ttbar*real*tau',   coldict['TTT']),
    #('ttbar*l',          coldict['TTL']),
    #('ttbar*j',          coldict['TTJ']),
    #('ttbar*other',      coldict['TTJ']),
    #('ttbar*single',     coldict['TT']),
    ('ttbar',            coldict['TT']),
    ('TopT',             coldict['TTT']),
    ('TopJ',             coldict['TTJ']),
    ('Top',              coldict['TT']),
    ('QCD',              coldict['QCD']),
    ('JTF',              coldict['QCD']),
    ('Fake*rate',        coldict['QCD']),
    ('j*tau*fake',       coldict['QCD']),
    ('Data',             coldict['Data']),
    ('Observed',         coldict['Data']),
    ('data_obs',         coldict['Data']),
  ])
set_sample_colors(sample_colors)


def getcolor(sample,color=kWhite,**kwargs):
  """Get color for some sample name."""
  if hasattr(sample,'name'):
    sample = sample.name
  for key in sample_colors: #sorted(sample_colors,key=lambda x: len(x),reverse=True)
    if re.findall(key.replace('*',".*"),sample): # glob -> regex wildcard
      LOG.verb("SampleStyle.getcolor: Found color %s for %r from search term %r!"%(sample_colors[key],sample,key),kwargs,level=3)
      #print("SampleStyle.getcolor: Found color %s for %r from search term %r!"%(sample_colors[key],sample,key))
      #print(kwargs)
      color = sample_colors[key]
      break
  else:
    LOG.warning("SampleStyle.getcolor: Could not find color for %r! Returning %s..."%(sample,color))
  return color
  

def gettitle(sample,default=None,**kwargs):
  """Get title for some sample name."""
  if sample in sample_titles:
    LOG.verb("SampleStyle.gettitle: Found title %s for %r!"%(sample_titles[sample],sample),kwargs,level=3)
    sample = sample_titles[sample]
  elif default:
    sample = default
  else:
    LOG.warning("SampleStyle.gettitle: Could not find title for %r! Returning %r..."%(sample,sample))
  if kwargs.get('latex',False):
    sample = makelatex(sample)
  return sample
  
