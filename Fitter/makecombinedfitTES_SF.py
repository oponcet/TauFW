"""
Date : May 2022 
Description :
 - fit of tes_DM with others parameters free (option 1),
 - fit of tid_SF_DM with other parameters free (option 2) 
 - combined fit of tes_DM and tid_SF_DM with other parameters free (option 3)
 - fit of tes_DM in simultaneous DM (option 4)
Add the option -t -1 to MultiDimFit to realize the fit with an asimov dataset
and add the option -saveToys to save the asimovdataset in higgsCombine*.root file. 
Note that the name of the generated file will be changed with this option 
(seed will be added at the end of the file name) -> use os.rename line 
Add the option --fastScan to do a fit without any systemetic
Add the option --freezeNuisanceGroups=group to do a fit a group of nuisance parameters
frozen, the groups are defined in harvestDatacards_TES_idSF.py
"""
import sys
import os
import yaml
from argparse import ArgumentParser

argv = sys.argv
parser = ArgumentParser(prog="makeTESfit",description="execute all steps to run TES fit")
parser.add_argument('-y', '--era', dest='era', choices=['2016','2017','2018','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018'], default=['UL2018'], action='store', help="set era" )
parser.add_argument('-c', '--config', dest='config', type=str, default='TauES/config/defaultFitSetupTES_mutau.yml', action='store', help="set config file containing sample & fit setup" )
parser.add_argument('-o', '--option', dest='option', choices=['1','2','3','4'], default='1', action='store', help="set option : fit of tes_DM(-o 1) ; fit of tid_SF_DM (-o 2) ; combined fit of tes_DM and tid_SF_DM (-o 3) ; fit of tes_DM in simultaneous DM (-o 4)")
args = parser.parse_args()

with open(args.config, 'r') as file:
    setup = yaml.safe_load(file)

# MORE GLOBAL VARIABLES
RANGE="0.950,1.050" # Range of tes_DM
EXTRATAG="_DeepTau"
ALGO="--algo=grid --alignEdges=1 --saveFitResult " # --saveWorkspace 
FIT_OPTS="--robustFit=1 --points=51  --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=2 --setRobustFitTolerance=0.001" #--preFitValue=1. 
XRTD_OPTS="--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND" #--X-rtd FITTER_DYN_STEPCMIN_OPTS="--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan" # --cminPreFit 1 --cminOldRobustMinimize 
CMIN_OPTS="--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan" # --cminPreFit 1 --cminOldRobustMinimize 


# Generating datacards
os.system("./TauES/harvestDatacards_TES_idSF.py -y %s -c %s -e %s "%(args.era,args.config,EXTRATAG)) # Generating the datacards

if args.option == '4': 
    LABEL=setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
    os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis- DM0=DM0%s.txt DM1=DM1%s.txt DM10=DM10%s.txt DM11=DM11%s.txt >output_%s/combinecards.txt"%(args.era,LABEL,LABEL,LABEL,LABEL,args.era))
    os.system("text2workspace.py output_%s/combinecards.txt"%(args.era))


# for v in setup["observables"]:
#     print("Observable : "+v)
#     variable = setup["observables"][v]

#     for r in variable["fitRegions"]:
#         print("Region : "+r)

#         region = setup["regions"][r]

#         BINLABEL="mt_"+v+"-"+r+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
#         WORKSPACE="output_"+args.era+"/ztt_"+BINLABEL+".root"

#         if args.option == '1': ### fit of tes_DM
#             POI = "tes_%s"%(r)
#             print(">>>>>>> tes_"+r+" fit")
#             POI_OPTS="-P %s  --setParameterRanges %s=%s:tid_SF_%s=0.9,1.1 -m 90 --setParameters r=1,%s=1 --freezeParameters r " %(POI,POI,RANGE,r,POI) ##tes_DM
#             os.system("text2workspace.py output_%s/ztt_%s.txt"%(args.era,BINLABEL))
#             os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all --trackParameters tid_SF_%s"%(WORKSPACE,ALGO,POI_OPTS,BINLABEL,FIT_OPTS,XRTD_OPTS,CMIN_OPTS,r))

#         if args.option == '2': ### fit of tid_SF_DM
#             POI = "tid_SF_%s"%(r)
#             print(">>>>>>> tid_"+r+" fit")
#             POI_OPTS="-P %s --setParameterRanges tes_%s=%s:%s=0.7,1.2 -m 90 --setParameters r=1,%s=1,tes_%s=1 --freezeParameters r " %(POI,r,RANGE,POI,POI,r) ##tid_SF
#             os.system("text2workspace.py output_%s/ztt_%s.txt"%(args.era,BINLABEL))
#             os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all --trackParameters tes_%s"%(WORKSPACE,ALGO,POI_OPTS,BINLABEL,FIT_OPTS,XRTD_OPTS,CMIN_OPTS,r))
#             #os.system("python plot1D_Scan.py higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root --y-cut 10 --y-max 10 --output plots_"+args.era+"/plot1D_tid_SF_%s --POI tid_SF_%s  --main-label  tid_SF_%s --logo '' --logo-sub '' "%(r,r,r))

#         if args.option == '3': ### combined fit of tes_DM and tid_SF_DM
#             print(">>>>>>> combine fit of tid_"+r+" and tes_"+r)
#             POI1 = "tid_SF_%s"%(r)
#             POI2 = "tes_%s"%(r)
#             POI_OPTS="-P %s -P %s --setParameterRanges %s=%s:%s=0.7,1.3 -m 90 --setParameters r=1,%s=1,%s=1 --freezeParameters r " %(POI2,POI1,POI2,RANGE,POI1,POI2,POI1)
#             os.system("text2workspace.py output_%s/ztt_%s.txt"%(args.era,BINLABEL))
#             os.system("combine -M MultiDimFit -t -1 %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all "%(WORKSPACE,ALGO,POI_OPTS,BINLABEL,FIT_OPTS,XRTD_OPTS,CMIN_OPTS))
        
#         if args.option == '4': ### simultaneous fit in DM
#             print(">>>>>>> simultaneous fit of tes_"+r)
#             POI_OPTS="-P tid_SF_%s  --setParameterRanges tid_SF_%s=0.7,1.2:tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s -m 90 --setParameters r=1,tes_%s=1,tid_SF_%s=1 --freezeParameters r " %(r,r,RANGE,RANGE,RANGE,RANGE,r,r) 
#             WORKSPACE="output_"+args.era+"/combinecards.root" 
#             os.system("combine -M MultiDimFit  %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all"%(WORKSPACE,ALGO,POI_OPTS,BINLABEL,FIT_OPTS,XRTD_OPTS,CMIN_OPTS))


#         else:
#             continue


#         # Add this when addind -saveToys option to combine
#         # print("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root")
#         # os.rename("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root", "higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")
#         # os.rename("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.GenerateOnly.mH90.123456.root", "higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")

#         # # ##Impact plot
#         # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s --doInitialFit"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS))
#         # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s --doFits --parallel 4"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS))
#         # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s -o postfit/impacts_%s.json"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS, BINLABEL))
#         # os.system("plotImpacts.py -i postfit/impacts_%s.json -o postfit/impacts_%s.json"%(BINLABEL,BINLABEL))
#         # os.system("convert -density 160 -trim postfit/impacts_%s.json.pdf[0] -quality 100 postfit/impacts_%s.png"%(BINLABEL,BINLABEL))


# os.system("mv higgsCombine*root output_%s"%args.era)


# if args.option == '4' :
#     os.system("./TauES/plotParabola_POI.py -p tid_SF -y %s -e %s -r %s,%s -s -a -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))


# if args.option == '1' or args.option == '4' :
#     os.system("./TauES/plotParabola_TES.py -y %s -e %s -r %s,%s -s -a -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))
# #    os.system("./TauES/plotPostFitScan_TES.py -y %s -e %s -r %s,%s -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))



