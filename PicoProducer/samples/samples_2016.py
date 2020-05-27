from TauFW.PicoProducer.storage.Sample import MC as M
from TauFW.PicoProducer.storage.Sample import Data as D
storage  = None #"/eos/user/i/ineuteli/samples/nano/$ERA/$PATH"
url      = None #"root://cms-xrd-global.cern.ch/"
filelist = None #"samples/files/2016/$SAMPLE.txt"
samples  = [
  
  # DRELL-YAN
  M('DY','DYJetsToLL_M-50',
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
    #"/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext2-v1/NANOAODSIM",
    store=storage,url=url,file=filelist,
  ),
#   M('DY','DY1JetsToLL_M-50',
#     "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY2JetsToLL_M-50',
#     "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY3JetsToLL_M-50',
#     "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY4JetsToLL_M-50',
#     "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DYJetsToLL_M-10to50',
#     "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY1JetsToLL_M-10to50',
#     "/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY2JetsToLL_M-10to50',
#     "/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY3JetsToLL_M-10to50',
#     "/DY3JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('DY','DY4JetsToLL_M-10to50',
#     "/DY4JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
  
  # TTBAR
  M('TT','TT',
    "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v2/NANOAODSIM",
    store=storage,url=url,file=filelist,
  ),
  
  # W+JETS
#   M('WJ','WJetsToLNu',
#     "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext2-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('WJ','W1JetsToLNu',
#     "/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('WJ','W2JetsToLNu',
#     "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('WJ','W3JetsToLNu',
#     "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('WJ','W4JetsToLNu',
#     "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#     "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext2-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
  
  # SINGLE TOP
#   M('ST','ST_tW_antitop',
#     "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('ST','ST_tW_top',
#     "/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('ST','ST_t-channel_antitop',
#     "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('ST','ST_t-channel_top',
#     "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
  
  # DIBOSON
#   M('VV','WW',
#     "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('VV','WZ',
#     "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
#   M('VV','ZZ',
#     "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM",
#     "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#     store=storage,url=url,file=filelist,
#   ),
  
  # SINGLE MUON
#   D('Data','SingleMuon_Run2016B', "/SingleMuon/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
  D('Data','SingleMuon_Run2016C', "/SingleMuon/Run2016C-Nano25Oct2019-v1/NANOAOD",
    store=storage,url=url,file=filelist,
  ),
#   D('Data','SingleMuon_Run2016D', "/SingleMuon/Run2016D-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleMuon_Run2016E', "/SingleMuon/Run2016E-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleMuon_Run2016F', "/SingleMuon/Run2016F-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleMuon_Run2016G', "/SingleMuon/Run2016G-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleMuon_Run2016H', "/SingleMuon/Run2016H-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
  
  # SINGLE ELECTRON
#   D('Data','SingleElectron_Run2016B', "/SingleElectron/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleElectron_Run2016C', "/SingleElectron/Run2016C-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleElectron_Run2016D', "/SingleElectron/Run2016D-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleElectron_Run2016E', "/SingleElectron/Run2016E-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleElectron_Run2016F', "/SingleElectron/Run2016F-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleElectron_Run2016G', "/SingleElectron/Run2016G-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','SingleElectron_Run2016H', "/SingleElectron/Run2016H-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
  
  # TAU
#   D('Data','Tau_Run2016B', "/Tau/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','Tau_Run2016C', "/Tau/Run2016C-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   )
#   D('Data','Tau_Run2016D', "/Tau/Run2016D-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','Tau_Run2016E', "/Tau/Run2016E-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','Tau_Run2016F', "/Tau/Run2016F-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','Tau_Run2016G', "/Tau/Run2016G-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
#   D('Data','Tau_Run2016H', "/Tau/Run2016H-Nano25Oct2019-v1/NANOAOD",
#     store=storage,url=url,file=filelist,
#   ),
  
  # LQ
#   M('LQ','VLQ_single_M1100',
#    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/NANOAODSIM",
#    #"/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext2-v1/NANOAODSIM",
#    store=storage,url=url,file=filelist,
#   ),
  
]
