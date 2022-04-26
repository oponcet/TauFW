import sys
import os
import yaml
from argparse import ArgumentParser

argv = sys.argv
parser = ArgumentParser(prog="makeTESfit",description="execute all steps to run TES fit")
parser.add_argument('-y', '--era', dest='era', choices=['2016','2017','2018','UL2016_preVFP','UL2016_postVFP','UL2017','UL2018'], default=['UL2018'], action='store', help="set era" )
parser.add_argument('-c', '--config', dest='config', type=str, default='TauES/config/defaultFitSetupTES_mutau.yml', action='store', help="set config file containing sample & fit setup" )
args = parser.parse_args()

with open(args.config, 'r') as file:
    setup = yaml.safe_load(file)

# MORE GLOBAL VARIABLES
RANGE="0.970,1.030"
EXTRATAG="_DeepTau"
ALGO="--algo=grid --alignEdges=1 --saveFitResult " # --saveWorkspace 
FIT_OPTS="--robustFit=1 --points=10000 --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=2 --setRobustFitTolerance=0.001" #--preFitValue=1. 
# POI_OPTS="-P tes --setParameterRanges tes=${RANGE} -m 90 --setParameters r=1 --freezeParameters r " 
POI_OPTS="-P tes_DM0 -P tes_DM1 -P tes_DM10 -P tes_DM11 --setParameterRanges tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s -m 90 --setParameters r=1,tes_DM0=1,tes_DM1=1,tes_DM10=1,tes_DM11=1 --freezeParameters r"%(RANGE,RANGE,RANGE,RANGE)
XRTD_OPTS="--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND" #--X-rtd FITTER_DYN_STEP
CMIN_OPTS="--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan" # --cminPreFit 1 --cminOldRobustMinimize 

os.system("./TauES/harvestDatacards_TES.py -M -y %s -c %s -e %s"%(args.era,args.config,EXTRATAG))

LABEL=setup["tag"]+EXTRATAG+"_MDF-"+args.era+"-13TeV"
os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis- DM0=DM0%s.txt DM1=DM1%s.txt DM10=DM10%s.txt DM11=DM11%s.txt >output_%s/combinecards.txt"%(args.era,LABEL,LABEL,LABEL,LABEL,args.era))
    
os.system("text2workspace.py output_%s/combinecards.txt"%(args.era))

for v in setup["observables"]:
    print v
    variable = setup["observables"][v]

    BINLABEL="mt_"+v+"-MDF"+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
    WORKSPACE="output_"+args.era+"/combinecards.root" 
    os.system("combine -M MultiDimFit -t -1 --saveToys -v 1 %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all"%(WORKSPACE,ALGO,POI_OPTS,BINLABEL,FIT_OPTS,XRTD_OPTS,CMIN_OPTS))

        #Add save toy to save Asimov dataset 
        #-t -1 --saveToys  -toysFile --points=41 --cminInitialHesse=1 --robustHesse=1
        #print("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root")
        # os.system("hadd -a higgsCombine.mt_"+v+"-MDF"+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root ")

    os.rename("higgsCombine.mt_"+v+"-MDF"+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root", "higgsCombine.mt_"+v+"-MDF"+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")

        # #Impact
        # os.system("combineTool.py -M Impacts -n %s -d %s %s  %s %s %s --redefineSignalPOIs tes_%s  -P tes_%s --setParameterRanges tes_%s=%s -m 90 --setParameters r=1,tes_%s=1 --doInitialFit"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS,r,r,r,RANGE,r))
        # os.system("combineTool.py -M Impacts -n %s -d %s %s  %s %s %s --redefineSignalPOIs tes_%s  -P tes_%s --setParameterRanges tes_%s=%s -m 90 --setParameters r=1,tes_%s=1 --doFits --parallel 4"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS,r,r,r,RANGE,r))
        # os.system("combineTool.py -M Impacts -n %s -d %s %s  %s %s %s --redefineSignalPOIs tes_%s -P tes_%s --setParameterRanges tes_%s=%s -m 90 --setParameters r=1,tes_%s=1 -o postfit/impacts_%s.json"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS,r,r,r,RANGE,r,BINLABEL))
        # os.system("plotImpacts.py -i postfit/impacts_%s.json -o postfit/impacts_%s.json"%(BINLABEL,BINLABEL))
    
os.system("mv higgsCombine*root output_%s"%args.era)


os.system("./TauES/plotParabola_TES.py -M -y %s -e %s -r %s,%s -s -a -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))
#os.system("./TauES/plotPostFitScan_TES.py -y %s -e %s -r %s,%s -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))



