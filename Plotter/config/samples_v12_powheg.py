# Description: Common configuration file for creating pico sample set plotting scripts
import re
from TauFW.Plotter.sample.utils import LOG, STYLE, ensuredir, repkey, joincuts, joinweights, ensurelist,\
                                       setera, getyear, loadmacro, Sel, Var
from TauFW.Plotter.sample.utils import getsampleset as _getsampleset
import json
# f = open("/afs/cern.ch/user/o/oponcet/private/TauPOG_run3/CMSSW_12_4_8/src/TauFW/PicoProducer/samples/nanoaod_sumw_2022_postEE.json")
# nevts_json = json.load(f)

def getsampleset(channel,era,**kwargs):
  verbosity = LOG.getverbosity(kwargs)
  year     = getyear(era) # get integer year
  fname    = kwargs.get('fname', "$PICODIR/$SAMPLE_$CHANNEL$TAG.root" ) # file name pattern of pico files
  split    = kwargs.get('split',    ['DY'] if 'tau' in channel else [ ] ) # split samples (e.g. DY) into genmatch components
  join     = kwargs.get('join',     ['VV','Top'] ) # join samples (e.g. VV, top)
  rmsfs    = ensurelist(kwargs.get('rmsf', [ ])) # remove the tau ID SF, e.g. rmsf=['idweight_2','ltfweight_2']
  addsfs   = ensurelist(kwargs.get('addsf', [ ])) # add extra weight to all samples
  weight   = kwargs.get('weight',   None         ) # weight for all MC samples
  dyweight = kwargs.get('dyweight', 'zptweight'  ) # weight for DY samples
  ttweight = kwargs.get('ttweight', 'ttptweight' ) # weight for ttbar samples
  filter   = kwargs.get('filter',   None         ) # only include these MC samples
  vetoes   = kwargs.get('vetoes',   None         ) # veto these MC samples
  #tag      = kwargs.get('tag',      ""           ) # extra tag for sample file names
  table    = kwargs.get('table',    True         ) # print sample set table
  setera(era,cme=13.6) # set era for plot style and lumi-xsec normalization
  if 'TT' in split and 'Top' in join: # don't join TT & ST
    join.remove('Top')
    join += ['TT','ST']
  
  # SM BACKGROUND MC SAMPLES
  if '2022_preEE' in era or '2022_postEE' in era: # so far same samples and cross sections are used for preEE and postEE, if event numbers are set elsewhere then we don't need to add seperate numbers for both eras
    # for now nevts is set to 1 so it isn't taken into account in the scaling of the samples as this will be done elsewhere
    
    kfactor_dy= 6282.6/6731.99 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV [https://twiki.cern.ch/twiki/bin/viewauth/CMS/MATRIXCrossSectionsat13p6TeV]
    kfactor_wj=63425.1/55300 # LO->NNLO+NLO_EW k-factor computed for 13.6 TeV
    kfactor_ttbar=923.6/762.1 # NLO->NNLO k-factor computed for 13.6 TeV
    kfactor_ww=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
    kfactor_zz=1.524 # LO->NNLO+NLO_EW computed for 13.6 TeV
    kfactor_wz=1.414 # LO->NNLO+NLO_EW computed for 13.6 TeV 


    cme=13.6
    if '2022_preEE' in era:
      expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP NAME                     TITLE                 XSEC      EXTRA OPTIONS
        ( 'DY', "DYto2Tau_MLL_10to50_powheg",   "Drell-Yan 10 to 50",       6744.0*1.0, {'extraweight': dyweight, 'nevts': 1459245, 'sumw':1338709.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_50to120_powheg",  "Drell-Yan 50 to 120",      2219*kfactor_dy, {'extraweight': dyweight, 'nevts': 2967285, 'sumw':2907117.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_120to200_powheg", "Drell-Yan 120 to 200",     21.65*kfactor_dy, {'extraweight': dyweight, 'nevts': 1498536, 'sumw':1483110.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_200to400_powheg", "Drell-Yan 200 to 400",     3.058*kfactor_dy, {'extraweight': dyweight, 'nevts': 876608, 'sumw': 872968.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_400to800_powheg", "Drell-Yan 400 to 800",     0.2691*kfactor_dy, {'extraweight': dyweight, 'nevts': 898556, 'sumw':897512.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_800to1500_powheg", "Drell-Yan 800 to 1500",   0.01915*kfactor_dy, {'extraweight': dyweight, 'nevts': 581254, 'sumw':581124.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_1500to2500_powheg", "Drell-Yan 1500 to 2500", 0.001111*kfactor_dy, {'extraweight': dyweight, 'nevts': 600000, 'sumw':599982.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_2500to4000_powheg", "Drell-Yan 2500 to 4000", 0.00005949*kfactor_dy, {'extraweight': dyweight, 'nevts': 300000, 'sumw':299996.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_4000to6000_powheg", "Drell-Yan 4000 to 6000", 0.000001558*kfactor_dy, {'extraweight': dyweight, 'nevts': 300000, 'sumw':299998.0} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_6000_powheg",      "Drell-Yan 6000",          3.519e-8*kfactor_dy, {'extraweight': dyweight, 'nevts': 146995, 'sumw':146995.0} ), # LO times kfactor

        ( 'DY', "DYto2Mu_MLL_10to50_powheg",   "Drell-Yan 10 to 50",       6744*1.0, {'extraweight': dyweight, 'nevts': 1418050, 'sumw':1301142} ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_50to120_powheg",  "Drell-Yan 50 to 120",      2219*kfactor_dy, {'extraweight': dyweight, 'nevts': 2820937, 'sumw':2763691.0} ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_120to200_powheg", "Drell-Yan 120 to 200",     21.65*kfactor_dy, {'extraweight': dyweight, 'nevts': 1453748, 'sumw':1438952.0}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_200to400_powheg", "Drell-Yan 200 to 400",     3.058*kfactor_dy, {'extraweight': dyweight, 'nevts': 853443, 'sumw':849855.0}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_400to800_powheg", "Drell-Yan 400 to 800",     0.2691*kfactor_dy, {'extraweight': dyweight, 'nevts': 874240, 'sumw':873292.0}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_800to1500_powheg", "Drell-Yan 800 to 1500",   0.01915*kfactor_dy, {'extraweight': dyweight, 'nevts': 579560, 'sumw': 579456.0}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_1500to2500_powheg", "Drell-Yan 1500 to 2500", 0.001111*kfactor_dy, {'extraweight': dyweight,'nevts': 590523, 'sumw':590493.0}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_2500to4000_powheg", "Drell-Yan 2500 to 4000", 0.00005949*kfactor_dy, {'extraweight': dyweight,'nevts': 299278, 'sumw':299274.0} ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_4000to6000_powheg", "Drell-Yan 4000 to 6000", 0.000001558*kfactor_dy, {'extraweight': dyweight, 'nevts': 289200, 'sumw':289198.0}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_6000_powheg",      "Drell-Yan 6000",           3.519e-8*kfactor_dy, {'extraweight': dyweight ,'nevts': 145002, 'sumw':145002.0}  ), # LO times kfactor

        ( 'DY', "DYto2E_MLL_10to50_powheg",   "Drell-Yan 10 to 50",       6744*1.0, {'extraweight': dyweight,'nevts': 1477950, 'sumw':1356076.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_50to120_powheg",  "Drell-Yan 50 to 120",      2219*kfactor_dy, {'extraweight': dyweight,'nevts': 2918148, 'sumw':2859284.0} ), # LO times kfactor  
        ( 'DY', "DYto2E_MLL_120to200_powheg", "Drell-Yan 120 to 200",     21.65*kfactor_dy, {'extraweight': dyweight,'nevts': 1497870, 'sumw':1482424.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_200to400_powheg", "Drell-Yan 200 to 400",     3.058*kfactor_dy, {'extraweight': dyweight,'nevts': 867524, 'sumw':864092.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_400to800_powheg", "Drell-Yan 400 to 800",     0.2691*kfactor_dy, {'extraweight': dyweight,'nevts': 891121, 'sumw':890161.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_800to1500_powheg", "Drell-Yan 800 to 1500",   0.01915*kfactor_dy, {'extraweight': dyweight,'nevts': 600000, 'sumw':599902.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_1500to2500_powheg", "Drell-Yan 1500 to 2500", 0.001111*kfactor_dy, {'extraweight': dyweight,'nevts': 586690, 'sumw':586670.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_2500to4000_powheg", "Drell-Yan 2500 to 4000", 0.00005949*kfactor_dy, {'extraweight': dyweight,'nevts': 290480, 'sumw':290470.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_4000to6000_powheg", "Drell-Yan 4000 to 6000", 0.000001558*kfactor_dy, {'extraweight': dyweight,'nevts': 298948, 'sumw':298946.0} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_6000_powheg",      "Drell-Yan 6000",           3.519e-8*kfactor_dy, {'extraweight': dyweight,'nevts': 145094, 'sumw':145094.0} ), # LO times kfactor
        

        ( 'WJ', "WtoLNu-4Jets" ,            "W + jets",           55300.0*kfactor_wj, {"nevts":183585526.0, "sumw":183585526}), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_1J",           "W + 1J",              9128.0*kfactor_wj, {"nevts":11896625.0, "sumw":11896625} ), # LO times kfactor # currently not available
        ( 'WJ', "WJetstoLNu-4Jets_2J",           "W + 2J",              2922.0*kfactor_wj, {"nevts":9283334.0, "sumw":9283334} ), # LO times kfactor # currently not available
        ( 'WJ', "WJetstoLNu-4Jets_3J",           "W + 3J",               861.3*kfactor_wj, {"nevts":8221862.0, "sumw":8221862}  ), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_4J",           "W + 4J",               415.4*kfactor_wj, {"nevts":1463885.0, "sumw":1463885} ), # LO times kfactor
     
        ( 'VV', "WW",             "WW",                    80.23*kfactor_ww, {"nevts":15405496, "sumw":15405496}), # LO times kfactor
        ( 'VV', "WZ",             "WZ",                    29.1*kfactor_wz, {"nevts":7479528, "sumw":7479528}), # LO times kfactor
        ( 'VV', "ZZ",             "ZZ",                    12.75*kfactor_zz, {"nevts":1181750, "sumw":1181750} ), # LO times kfactor

        ( 'TT', "TTto2L2Nu",             "ttbar 2l2#nu",          80.9*kfactor_ttbar, {'extraweight': ttweight, "nevts":47887413, "sumw":47500385.0} ), # NLO times BR times kfactor
        ( 'TT', "TTto4Q",                "ttbar hadronic",       346.4*kfactor_ttbar, {'extraweight': ttweight, "nevts":105888577, "sumw":105030029.0} ), # NLO times BR times kfactor
        ( 'TT', "TTtoLNu2Q",             "ttbar semileptonic",   334.8*kfactor_ttbar, {'extraweight': ttweight, "nevts":156612890, "sumw":155346152.0} ), # NLO times BR times kfactor
        ( 'ST', "ST_t_channel_top_4f_InclusiveDecays",      "ST t-channel t",       123.8, {"nevts":2973675, "sumw":2737505.0}), # NLO
        ( 'ST', "ST_t_channel_antitop_4f_InclusiveDecays",  "ST t-channel at",       75.47, {"nevts":1325389, "sumw":1325389.0} ), # NLO
        ( 'ST', "ST_tW_antitop_LNu2Q",             "ST tW semileptonic",                 15.8 , {"nevts":1433215, "sumw":9183029} ), # NLO (36.0) times LNu2Q BR
        ( 'ST', "ST_tW_top_2L2Nu",             "ST tW 2l2#nu",                 3.8, {"nevts":4886868, "sumw":4887056} ), # NLO (36.0) times 2L2Nu BR
        ( 'ST', "ST_tW_top_LNu2Q",         "ST atW semileptonic",          15.9, {"nevts":9644321, "sumw":9643983.0}), # NLO (36.1) times LNu2Q BR
        ( 'ST', "ST_tW_antitop_2L2Nu",         "ST atW 2l2#nu",                3.8, {"nevts":4763425, "sumw":4763261.0}), # NLO (36.1) times 2L2Nu BR
      ]
     # if 'mutau' in channel:
     #   expsamples.append(('DY',"DYto2TautoMuTauh_M-50","Drell-Yan 50 -> tautau -> mu+tauh",5455.0*kfactor_dy,{'extraweight': dyweight})) # LO (using same cross section as inclusive samples), apply correct normalization in stitching
     #   # the cross section for this exact samples is 1885.0 which is ~ 1/3 the total DY->LL cross section (expected since it only selects taus and not electrons and muons)
     #   # the filter efficiency for this sample (due to tau BRs + kinematic cuts on tau decay products) is 2.865e-02 
    if '2022_postEE' in era:
       expsamples = [ # table of MC samples to be converted to Sample objects
        # GROUP NAME                     TITLE                 XSEC      EXTRA OPTIONS
        ( 'DY', "DYto2Tau_MLL_10to50_powheg",   "Drell-Yan 10 to 50",       6744.0*1.0, {'extraweight': dyweight, 'nevts': 5249261, 'sumw':4815253} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_50to120_powheg",  "Drell-Yan 50 to 120",      2219*kfactor_dy, {'extraweight': dyweight, 'nevts': 10167136, 'sumw':9961938} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_120to200_powheg", "Drell-Yan 120 to 200",     21.65*kfactor_dy, {'extraweight': dyweight, 'nevts': 5249271, 'sumw':5194901} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_200to400_powheg", "Drell-Yan 200 to 400",     3.058*kfactor_dy, {'extraweight': dyweight, 'nevts': 3021840, 'sumw': 3009278} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_400to800_powheg", "Drell-Yan 400 to 800",     0.2691*kfactor_dy, {'extraweight': dyweight, 'nevts': 3110408, 'sumw':3106940} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_800to1500_powheg", "Drell-Yan 800 to 1500",   0.01915*kfactor_dy, {'extraweight': dyweight, 'nevts': 2078460, 'sumw':2078006} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_1500to2500_powheg", "Drell-Yan 1500 to 2500", 0.001111*kfactor_dy, {'extraweight': dyweight, 'nevts': 1995777, 'sumw':1995673} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_2500to4000_powheg", "Drell-Yan 2500 to 4000", 0.00005949*kfactor_dy, {'extraweight': dyweight, 'nevts': 1050000, 'sumw':1049992} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_4000to6000_powheg", "Drell-Yan 4000 to 6000", 0.000001558*kfactor_dy, {'extraweight': dyweight, 'nevts': 1047456, 'sumw':1047456} ), # LO times kfactor
        ( 'DY', "DYto2Tau_MLL_6000_powheg",      "Drell-Yan 6000",          3.519e-8*kfactor_dy, {'extraweight': dyweight, 'nevts': 523113, 'sumw':523113} ), # LO times kfactor

        ( 'DY', "DYto2Mu_MLL_10to50_powheg",   "Drell-Yan 10 to 50",       6744*1.0, {'extraweight': dyweight, 'nevts': 5010800, 'sumw':4597120} ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_50to120_powheg",  "Drell-Yan 50 to 120",      2219*kfactor_dy, {'extraweight': dyweight, 'nevts': 9869280, 'sumw':9669500} ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_120to200_powheg", "Drell-Yan 120 to 200",     21.65*kfactor_dy, {'extraweight': dyweight, 'nevts': 4909820, 'sumw':4859532}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_200to400_powheg", "Drell-Yan 200 to 400",     3.058*kfactor_dy, {'extraweight': dyweight, 'nevts': 3051242, 'sumw':3038276}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_400to800_powheg", "Drell-Yan 400 to 800",     0.2691*kfactor_dy, {'extraweight': dyweight, 'nevts': 2930748, 'sumw':2927264}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_800to1500_powheg", "Drell-Yan 800 to 1500",   0.01915*kfactor_dy, {'extraweight': dyweight, 'nevts': 2088496, 'sumw':2088078}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_1500to2500_powheg", "Drell-Yan 1500 to 2500", 0.001111*kfactor_dy, {'extraweight': dyweight,'nevts': 2006688, 'sumw':2006612}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_2500to4000_powheg", "Drell-Yan 2500 to 4000", 0.00005949*kfactor_dy, {'extraweight': dyweight,'nevts': 1000182, 'sumw':1000170} ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_4000to6000_powheg", "Drell-Yan 4000 to 6000", 0.000001558*kfactor_dy, {'extraweight': dyweight, 'nevts': 994900, 'sumw':994896}  ), # LO times kfactor
        ( 'DY', "DYto2Mu_MLL_6000_powheg",      "Drell-Yan 6000",           3.519e-8*kfactor_dy, {'extraweight': dyweight ,'nevts': 503888, 'sumw':503888}  ), # LO times kfactor

        ( 'DY', "DYto2E_MLL_10to50_powheg",   "Drell-Yan 10 to 50",       6744*1.0, {'extraweight': dyweight,'nevts': 5193138, 'sumw':4764222} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_50to120_powheg",  "Drell-Yan 50 to 120",      2219*kfactor_dy, {'extraweight': dyweight,'nevts': 10403118, 'sumw':10192192} ), # LO times kfactor  
        ( 'DY', "DYto2E_MLL_120to200_powheg", "Drell-Yan 120 to 200",     21.65*kfactor_dy, {'extraweight': dyweight,'nevts': 5238528, 'sumw':5184446} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_200to400_powheg", "Drell-Yan 200 to 400",     3.058*kfactor_dy, {'extraweight': dyweight,'nevts': 3147891, 'sumw':3134891} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_400to800_powheg", "Drell-Yan 400 to 800",     0.2691*kfactor_dy, {'extraweight': dyweight,'nevts': 2975850, 'sumw':2972468} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_800to1500_powheg", "Drell-Yan 800 to 1500",   0.01915*kfactor_dy, {'extraweight': dyweight,'nevts': 2004300, 'sumw':2003864} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_1500to2500_powheg", "Drell-Yan 1500 to 2500", 0.001111*kfactor_dy, {'extraweight': dyweight,'nevts': 2053944, 'sumw':2053882} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_2500to4000_powheg", "Drell-Yan 2500 to 4000", 0.00005949*kfactor_dy, {'extraweight': dyweight,'nevts': 986496, 'sumw':986486} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_4000to6000_powheg", "Drell-Yan 4000 to 6000", 0.000001558*kfactor_dy, {'extraweight': dyweight,'nevts': 1027656, 'sumw':1027654} ), # LO times kfactor
        ( 'DY', "DYto2E_MLL_6000_powheg",      "Drell-Yan 6000",           3.519e-8*kfactor_dy, {'extraweight': dyweight,'nevts': 525000, 'sumw':525000} ), # LO times kfactor
        

        ( 'WJ', "WtoLNu-4Jets" ,            "W + jets",                 55300.0*kfactor_wj, {"nevts":683448011, "sumw":683448011}), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_1J",           "W + 1J",              9128.0*kfactor_wj, {"nevts":42695566, "sumw":42695566} ), # LO times kfactor # currently not available
        ( 'WJ', "WJetstoLNu-4Jets_2J",           "W + 2J",              2922.0*kfactor_wj, {"nevts":36349344, "sumw":36349344} ), # LO times kfactor # currently not available
        ( 'WJ', "WJetstoLNu-4Jets_3J",           "W + 3J",               861.3*kfactor_wj, {"nevts":27828446, "sumw":27828446}  ), # LO times kfactor
        ( 'WJ', "WJetstoLNu-4Jets_4J",           "W + 4J",               415.4*kfactor_wj, {"nevts":4906634, "sumw":4906634} ), # LO times kfactor
     
        ( 'VV', "WW",             "WW",                    80.23*kfactor_ww, {"nevts":53112080, "sumw":53112080.0}), # LO times kfactor
        ( 'VV', "WZ",             "WZ",                    29.1*kfactor_wz, {"nevts":26722782, "sumw":26722782.0}), # LO times kfactor
        ( 'VV', "ZZ",             "ZZ",                    12.75*kfactor_zz, {"nevts":4043040, "sumw":4043040} ), # LO times kfactor

        ( 'TT', "TTto2L2Nu",             "ttbar 2l2#nu",          80.9*kfactor_ttbar, {'extraweight': ttweight, "nevts":169050774, "sumw":167682796.0} ), # NLO times BR times kfactor
        ( 'TT', "TTto4Q",                "ttbar hadronic",       346.4*kfactor_ttbar, {'extraweight': ttweight, "nevts":366376610, "sumw":363409416.0} ), # NLO times BR times kfactor
        ( 'TT', "TTtoLNu2Q",             "ttbar semileptonic",   334.8*kfactor_ttbar, {'extraweight': ttweight, "nevts":542269521, "sumw":537883189.0} ), # NLO times BR times kfactor
        ( 'ST', "ST_t_channel_top_4f_InclusiveDecays",      "ST t-channel t",       123.8, {"nevts":4363850, "sumw":2685976.0}), # NLO
        ( 'ST', "ST_t_channel_antitop_4f_InclusiveDecays",  "ST t-channel at",       75.47, {"nevts":2762668, "sumw":1700756.0} ), # NLO
        ( 'ST', "ST_tW_antitop_LNu2Q",             "ST tW semileptonic",                 15.8 , {"nevts":33758259, "sumw":33757009.0} ), # NLO (36.0) times LNu2Q BR
        ( 'ST', "ST_tW_top_2L2Nu",             "ST tW 2l2#nu",                 3.8, {"nevts":16575934, "sumw":16575338.0} ), # NLO (36.0) times 2L2Nu BR
        ( 'ST', "ST_tW_top_LNu2Q",         "ST atW semileptonic",          15.9, {"nevts":32513048, "sumw":32511808.0}), # NLO (36.1) times LNu2Q BR
        ( 'ST', "ST_tW_antitop_2L2Nu",         "ST atW 2l2#nu",                3.8, {"nevts":16782809, "sumw":16782203.0}), # NLO (36.1) times 2L2Nu BR
      ]
     # if 'mutau' in channel:
     #   expsamples.append(('DY',"DYto2TautoMuTauh_M-50","Drell-Yan 50 -> tautau -> mu+tauh",5455.0*kfactor_dy,{'extraweight': dyweight})) # LO (using same cross section as inclusive samples), apply correct normalization in stitching
     #   # the cross section for this exact samples is 1885.0 which is ~ 1/3 the total DY->LL cross section (expected since it only selects taus and not electrons and muons)
     #   # the filter efficiency for this sample (due to tau BRs + kinematic cuts on tau decay products) is 2.865e-02 
  else:
    LOG.throw(IOError,"Did not recognize era %r!"%(era))
  
  # OBSERVED DATA SAMPLES
  if   'tautau' in channel: dataset = "Tau_Run%d?"%year
  elif 'mutau'  in channel:
    if era=='2022_preEE':
      dataset = "*Muon_Run%d?"%year
      print("dataset = ", dataset) 
      #dataset = "SingleMuon_Run%d?"%year # need this one as well for C
      # TODO: need to somehow handle that we need SingleMuonC, MuonC, and MuonD for preEE
    elif era=='2022_postEE': dataset = "Muon_Run%d?"%year
    # Muon_Run2022F and Muon_Run2022G for prEE 
    # elif era=='2022_postEE': dataset = "Muon_Run%d[F-G]"%year
    else: dataset = "SingleMuon_Run%d?"%year
  elif 'etau'   in channel: dataset = "EGamma_Run%d?"%year if (year==2018 or year==2022) else "SingleElectron_Run%d?"%year
  elif 'mumu'   in channel:
    if era=='2022_preEE':        
      dataset = "*Muon_Run%d?"%year
    elif era=='2022_postEE': dataset = "Muon_Run%d?"%year
    else: dataset = "SingleMuon_Run%d?"%year       
  elif 'emu'    in channel: dataset = "SingleMuon_Run%d?"%year
  elif 'ee'     in channel: dataset = "EGamma_Run%d?"%year if year==2018 else "SingleElectron_Run%d?"%year
  else:
    LOG.throw(IOError,"Did not recognize channel %r!"%(channel))
  datasample = ('Data',dataset) # GROUP, NAME
  print("datasample = ", datasample)
  
  # FILTER
  if filter:
    expsamples = [s for s in expsamples if any(f in s[0] for f in filter)]
  if vetoes:
    expsamples = [s for s in expsamples if not any(v in s[0] for v in vetoes)]
  
  # SAMPLE SET
  if weight=="":
    weight = ""
  #elif channel in ['mutau','etau']:
  if 'mutau' in channel or 'etau' in channel:
    weight = "sign(genweight)*trigweight*puweight*idisoweight_1*idweight_2*ltfweight_2"
  elif channel in ['tautau','ditau']:
    weight = "genweight*trigweight*puweight*idweight_1*idweight_2*ltfweight_1*ltfweight_2"
  else: # mumu, emu, ...
    weight = "sign(genweight)*trigweight*puweight*idisoweight_1*idisoweight_2"
  for sf in rmsfs: # remove (old) SFs, e.g. for SF measurement
    weight = weight.replace(sf,"").replace("**","*").strip('*')
  for sf in addsfs:  # add extra SFs, e.g. for SF measurement
    weight = joinweights(weight,sf)
  kwargs.setdefault('weight',weight) # common weight for MC
  kwargs.setdefault('fname', fname)  # default filename pattern
  print(expsamples)
  sampleset = _getsampleset(datasample,expsamples,channel=channel,era=era,**kwargs)
  LOG.verb("weight = %r"%(weight),verbosity,1)

  # for expsamples in sampleset.expsamples:
    # print all information about the sample
    # print("Sample: %s, title: %s, xsec: %s, nevts: %s, weight: %s"%(expsamples.name, expsamples.title, expsamples.xsec, expsamples, expsamples.weight))
  
  # STITCH
  # Note: titles are set via STYLE.sample_titles
  if era=='2022_postEE':     
    sampleset.stitch("W*4Jets*",    incl='WtoLNu-4Jets',  name='WJ', cme=cme) # W + jets 2022_postEE
    # sampleset.stitch("WJetstoLNu-4Jets*J",    incl='WtoLNu-4Jets',  name='WJ', cme=cme) # W + jets 2022_postEE
  elif era=='2022_preEE':     
    sampleset.stitch("W*4Jets*",    incl='WtoLNu-4Jets',  name='WJ', cme=cme) # W + jets 2022_postEE
  # sampleset.stitch("DYto2L-4Jets_MLL-50*", incl='DYto2L-4Jets_MLL-50', name="DY_M50", cme=cme) # Drell-Yan, M > 50 GeV
  
  # JOIN
  sampleset.join('DY', name='DY' ) # Drell-Yan, M < 50 GeV + M > 50 GeV
  if 'VV' in join:
    sampleset.join('VV','WZ','WW','ZZ', name='VV' ) # Diboson
  if 'TT' in join and era!='year':
    sampleset.join('TT', name='TT' ) # ttbar
  if 'ST' in join:
    sampleset.join('ST', name='ST' ) # single top
  if 'Top' in join:
    sampleset.join('TT','ST', name='Top' ) # ttbar + single top
  
  # SPLIT
  # Note: titles are set via STYLE.sample_titles
  if split and channel.count('tau')==1:
    ZTT = STYLE.sample_titles.get('ZTT',"Z -> %s"%channel) # title
    if channel.count('tau')==1:
      ZTT = ZTT.replace("{l}","{mu}" if "mu" in channel else "{e}")
      GMR = "genmatch_2==5"
      GML = "genmatch_2>0 && genmatch_2<5"
      GMJ = "genmatch_2==0"
      GMF = "genmatch_2<5"
    elif channel.count('tau')==2:
      ZTT = ZTT.replace("{l}","{h}")
      GMR = "genmatch_1==5 && genmatch_2==5"
      GML = "(genmatch_1<5 || genmatch_2<5) && genmatch_1>0 && genmatch_2>0"
      GMJ = "(genmatch_1==0 || genmatch_2==0)"
      GMF = "(genmatch_1<5 || genmatch_2<5)"
    else:
      LOG.throw(IOError,"Did not recognize channel %r!"%(channel))
    if 'DM' in split: # split DY by decay modes
      samples.split('DY', [('ZTTDM0', ZTT+", h^{#pm}",                   GMR+" && dm_2==0"),
                           ('ZTTDM1', ZTT+", h^{#pm}h^{0}",              GMR+" && dm_2==1"),
                           ('ZTTDM10',ZTT+", h^{#pm}h^{#mp}h^{#pm}",     GMR+" && dm_2==10"),
                           ('ZTTDM11',ZTT+", h^{#pm}h^{#mp}h^{#pm}h^{0}",GMR+" && dm_2==11"),
                           ('ZL',GML),('ZJ',GMJ),])
    elif 'DY' in split:
      sampleset.split('DY',[('ZTT',ZTT,GMR),('ZL',GML),('ZJ',GMJ),])
    if 'TT' in split:
      sampleset.split('TT',[('TTT',GMR),('TTJ',GMF),('TTL',"genmatch_2>0 && genmatch_2<5")])
    if 'ST' in split:
      sampleset.split('ST',[('TTT',"genmatch_2==5 && genmatch_2<5"),('STJ',"genmatch_2<5")])
    # if 'TT' in split:
    #   sampleset.split('TT',[('TTT',GMR),('TTJ',GMF),])
  
  if table:
    sampleset.printtable(merged=True,split=True)
  print(">>> common weight: %r"%(weight))
  return sampleset
  
