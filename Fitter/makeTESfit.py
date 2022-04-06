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
FIT_OPTS="--robustFit=1 --points=201  --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=2 --setRobustFitTolerance=0.001" #--preFitValue=1. 
# POI_OPTS="-P tes --setParameterRanges tes=${RANGE} -m 90 --setParameters r=1 --freezeParameters r  " 
POI_OPTS="-P tes --setParameterRanges tes=%s -m 90 --setParameters r=1,tes=1 --freezeParameters r " %(RANGE)
XRTD_OPTS="--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND" #--X-rtd FITTER_DYN_STEP
CMIN_OPTS="--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan" # --cminPreFit 1 --cminOldRobustMinimize 

os.system("./TauES/harvestDatacards_TES.py -y %s -c %s -e %s"%(args.era,args.config,EXTRATAG))

for v in setup["observables"]:
    print v
    variable = setup["observables"][v]

    for r in variable["fitRegions"]:
        print r
        region = setup["regions"][r]

        BINLABEL="mt_"+v+"-"+r+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
        os.system("text2workspace.py output_%s/ztt_%s.txt"%(args.era,BINLABEL))

        WORKSPACE="output_"+args.era+"/ztt_"+BINLABEL+".root" 
        os.system("combine -M MultiDimFit -t -1 --saveToys --fastScan %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all"%(WORKSPACE,ALGO,POI_OPTS,BINLABEL,FIT_OPTS,XRTD_OPTS,CMIN_OPTS))
        #os.system("combine -M GenerateOnly -t -1 --saveToys --setParameterRanges tes=%s -m 90 --setParameters r=1,tes=1 --freezeParameters r --freezeNuisanceGroups=all %s -n .%s "%(RANGE,WORKSPACE,BINLABEL))

        
        #Add save toy to save Asimov dataset 
        #-t -1 --saveToys  -toysFile --points=41 --freezeNuisanceGroups=sys --fastScan
        print("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root")
        os.rename("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root", "higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")
        #os.rename("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.GenerateOnly.mH90.123456.root", "higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")


        ##Impact
        # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s --doInitialFit"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS))
        # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s --doFits --parallel 4"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS))
        # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s -o postfit/impacts_%s.json"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS, BINLABEL))
        # os.system("plotImpacts.py -i postfit/impacts_%s.json -o postfit/impacts_%s.json"%(BINLABEL,BINLABEL))
        #os.system("convert -density 160 -trim postfit/impacts_%s.json.pdf[0] -quality 100 postfit/impacts_%s.png"%(BINLABEL,BINLABEL))


os.system("mv higgsCombine*root output_%s"%args.era)


os.system("./TauES/plotParabola_TES.py -y %s -e %s -r %s,%s -s -a -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))
os.system("./TauES/plotPostFitScan_TES.py -y %s -e %s -r %s,%s -c %s"%(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))



