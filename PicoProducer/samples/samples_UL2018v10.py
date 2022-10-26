from TauFW.PicoProducer.storage.Sample import MC as M
from TauFW.PicoProducer.storage.Sample import Data as D
storage  = "/eos/cms/store/group/phys_tau/TauFW/nanoV10/Run2_2018/$DAS" #"/eos/cms/store/group/phys_tau/TauFW/nano/UL2018/$DAS"
url      = None #"root://eosuser.cern.ch/"
filelist = None #"samples/files/UL2018/$SAMPLE.txt"
samples  = [
  
  #DRELL-YAN
  M('DY','DYJetsToLL_M-10to50',
    "/DYJetsToLL_M-10to50-madgraphMLM",
    store=storage,url=url,files=filelist,opts="useT1=False,zpt=True"),
  M('DY','DYJetsToLL_M-50',
    "DYJetsToLL_M-50-madgraphMLM",
    "/DYJetsToLL_M-50-madgraphMLM_ext1",
    store=storage,url=url,files=filelist,opts="useT1=False,zpt=True"),
  M('DY','DY1JetsToLL_M-50',
    "/DY1JetsToLL_M-50_MatchEWPDG20_TuneCP5_13TeV-madgraphMLM-pythia8",
    store=storage,url=url,files=filelist,opts="useT1=False,zpt=True"),
  M('DY','DY2JetsToLL_M-50',
    "DY2JetsToLL_M-50-madgraphMLM",
    store=storage,url=url,files=filelist,opts="useT1=False,zpt=True"),
  M('DY','DY3JetsToLL_M-50',
    "/DY3JetsToLL_M-50_MatchEWPDG20_TuneCP5_13TeV-madgraphMLM-pythia8",
    store=storage,url=url,files=filelist,opts="useT1=False,zpt=True"),
  M('DY','DY4JetsToLL_M-50',
    "/DY4JetsToLL_M-50_MatchEWPDG20_TuneCP5_13TeV-madgraphMLM-pythia8",
    store=storage,url=url,files=filelist,opts="useT1=False,zpt=True"),
  # ############# M('DY','DYJetsToMuTauh_M-50',
  #   "/DYJetsToTauTauToMuTauh_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
  #   store=storage,url=url,files=filelist,opts="useT1=True,zpt=True",channels=["skim*",'*mutau*']),
  
  # TTBAR
  M('TT','TTTo2L2Nu',
    ###"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM", # BUGGY Summer19
    "/TTTo2L2Nu",
    store=storage,url=url,files=filelist,opts="useT1=False,toppt=True"),
  M('TT','TTToSemiLeptonic',
    ###"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM", # BUGGY Summer19
  "/TTToSemiLeptonic",
    store=storage,url=url,files=filelist,opts="useT1=False,toppt=True"),
  M('TT','TTToHadronic',
    ###"/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM", # BUGGY Summer19
    "/TTToHadronic",
    store=storage,url=url,files=filelist,opts="useT1=False,toppt=True"),
  
  # W+JETS
  M('WJ','WJetsToLNu',
    "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('WJ','W1JetsToLNu',
    "/W1JetsToLNu",
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('WJ','W2JetsToLNu',
    "/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('WJ','W3JetsToLNu',
    "/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('WJ','W4JetsToLNu',
    "/W4JetsToLNu", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  
  # SINGLE TOP
  M('ST','ST_tW_antitop',
    "/ST_tW_antitop_5f_NoFullyHadronicDecays", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('ST','ST_tW_top',
    "/ST_tW_top_5f_NoFullyHadronicDecays", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('ST','ST_t-channel_antitop',
    "/ST_t-channel_antitop_4f_InclusiveDecays", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('ST','ST_t-channel_top',
    "/ST_t-channel_top_4f_InclusiveDecays", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  
  # DIBOSON
  M('VV','WW',
    "/WW",
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('VV','WZ',
    "/WZ", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  M('VV','ZZ',
    "/ZZ", # BUGGY Summer19
    store=storage,url=url,files=filelist,opts="useT1=False"),
  
  # SINGLE MUON
  D('Data','SingleMuon_Run2018A',"/SingleMuon_Run2018A",
   store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'mutau','mumu','emu']),
  D('Data','SingleMuon_Run2018B',"/SingleMuon_Run2018B",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'mutau','mumu','emu']),
  D('Data','SingleMuon_Run2018C',"/SingleMuon_Run2018C",
   store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'mutau','mumu','emu']),
  D('Data','SingleMuon_Run2018D',"/SingleMuon_Run2018D",
   store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'mutau','mumu','emu']),
  
  # SINGLE ELECTRON
  D('Data','EGamma_Run2018A',"/EGamma_Run2018A",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'etau','ee']),
  D('Data','EGamma_Run2018B',"/EGamma_Run2018B",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'etau','ee']),
  D('Data','EGamma_Run2018C',"/EGamma_Run2018C",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'etau','ee']),
  D('Data','EGamma_Run2018D',"/EGamma_Run2018D",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'etau','ee']),
  
  # TAU
  D('Data','Tau_Run2018A',"/Tau_Run2018A",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'tautau']),
  D('Data','Tau_Run2018B',"/Tau_Run2018B",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'tautau']),
  D('Data','Tau_Run2018C',"/Tau_Run2018C",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'tautau']),
  D('Data','Tau_Run2018D',"/Tau_Run2018D",
    store=storage,url=url,files=filelist,opts="useT1=False",channels=["skim*",'tautau']),
  
]