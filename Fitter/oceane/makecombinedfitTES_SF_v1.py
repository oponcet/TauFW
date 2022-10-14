"""
Date : May 2022 
Description :
 - fit of tes_DM with others parameters free (option 1),
 - fit of tid_SF_DM with other parameters free (option 2) 
 - combined fit of tes_DM and tid_SF_DM with other parameters free (option 3)
 - fit of tes_DM in simultaneous DM (option 4)
 - Scan of tid_SF_pt for combined fit of tes_DM and tid_SF_pt (option 5)
 - Scan of tes_DM for combined fit of tes_DM and tid_SF_pt (option 6)
 - 2D Scan of tid_SF_pt et tes_DM for combined fit of tes_DM and tid_SF_pt (option 7)   
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
parser = ArgumentParser(
    prog="makeTESfit", description="execute all steps to run TES fit")
parser.add_argument('-y', '--era', dest='era', choices=['2016', '2017', '2018', 'UL2016_preVFP',
                                                        'UL2016_postVFP', 'UL2017', 'UL2018'], default=['UL2018'], action='store', help="set era")
parser.add_argument('-c', '--config', dest='config', type=str, default='TauES_ID/config/defaultFitSetupTES_mutau.yml',
                    action='store', help="set config file containing sample & fit setup")
parser.add_argument('-o', '--option', dest='option', choices=['1', '2', '3', '4', '5','6','7'], default='1', action='store',
                    help="set option : fit of tes_DM(-o 1) ; fit of tid_SF_DM (-o 2) ; combined fit of tes_DM and tid_SF_DM (-o 3) \
                        ; fit of tes_DM in simultaneous DM (-o 4) ; combine fit of on region scan ID SF (-o 5); combine fit of on region scan TES (-o 6)\
                        ; combine fit of on region 2D scan TES and tid SF (-o 7) ")
args = parser.parse_args()

with open(args.config, 'r') as file:
    setup = yaml.safe_load(file)

# MORE GLOBAL VARIABLES
RANGE = "0.970,1.030"  # Range of tes_DM
EXTRATAG = "_DeepTau"
ALGO = "--algo=grid --alignEdges=1 --saveFitResult "  # --saveWorkspace
# --preFitValue=1.
FIT_OPTS = "--robustFit=1 --points=31  --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=2 --setRobustFitTolerance=0.001"
# --X-rtd FITTER_DYN_STEPCMIN_OPTS="--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan" # --cminPreFit 1 --cminOldRobustMinimize
XRTD_OPTS = "--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"
# --cminPreFit 1 --cminOldRobustMinimize
CMIN_OPTS = "--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan"

if args.option == '4': #combined the datacards
    LABEL = setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
    os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis- DM0=DM0%s.txt DM1=DM1%s.txt DM10=DM10%s.txt DM11=DM11%s.txt >output_%s/combinecards.txt" % (args.era, LABEL, LABEL, LABEL, LABEL, args.era))
    os.system("text2workspace.py output_%s/combinecards.txt" % (args.era))


# elif args.option == '7': #generate the datacards and do the fit
#     os.system("./TauES_ID/harvestDatacards_TES_idSF_bin_pt.py -y %s -c %s -e %s " %(args.era, args.config, EXTRATAG))  # Generating the datacards for option 5 

#     v = "m_vis"
#     LABEL = setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
#     #Combining the datacards
#     os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis-  DM0_pt1=DM0_pt1%s.txt DM0_pt2=DM0_pt2%s.txt DM0_pt3=DM0_pt3%s.txt \
#                 DM0_pt4=DM0_pt4%s.txt DM0_pt5=DM0_pt5%s.txt DM0_pt6=DM0_pt6%s.txt DM0_pt7=DM0_pt7%s.txt DM1_pt1=DM1_pt1%s.txt \
#                 DM1_pt2=DM1_pt2%s.txt DM1_pt3=DM1_pt3%s.txt DM1_pt4=DM1_pt4%s.txt DM1_pt5=DM1_pt5%s.txt DM1_pt6=DM1_pt6%s.txt \
#                 DM1_pt7=DM1_pt7%s.txt DM10_pt1=DM10_pt1%s.txt DM10_pt2=DM10_pt2%s.txt DM10_pt3=DM10_pt3%s.txt DM10_pt4=DM10_pt4%s.txt\
#                 DM10_pt5=DM10_pt5%s.txt DM10_pt6=DM10_pt6%s.txt DM10_pt7=DM10_pt7%s.txt DM11_pt1=DM11_pt1%s.txt DM11_pt2=DM11_pt2%s.txt\
#                 DM11_pt3=DM11_pt3%s.txt DM11_pt4=DM11_pt4%s.txt DM11_pt5=DM11_pt5%s.txt DM11_pt6=DM11_pt6%s.txt DM11_pt7=DM11_pt7%s.txt\
#                 >output_%s/combinecards.txt" % (args.era, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL,LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, args.era))
#     os.system("text2workspace.py output_%s/combinecards.txt" % (args.era))
#     #for each decay mode
#     for r in ["pt1","pt2","pt3","pt4","pt5","pt6","pt7"]: #["DM0","DM1","DM10","DM11"]
#         for dm in ["DM0","DM1","DM10","DM11"]:
#             BINLABEL = "mt_"+v+"-"+r+dm+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
#             WORKSPACE = "output_"+args.era+"/ztt_"+BINLABEL+".root"
#             print("Region : "+r)
#             print(">>>>>>> simultaneous fit of tes_" +r + " in pt bins and tes_"+r + "in DM")
#             POI_OPTS = "-P tid_SF_%s -P tes_%s --setParameterRanges tid_SF_pt1=0.7,1.2:tid_SF_pt2=0.7,1.2:tid_SF_pt3=0.7,1.2:tid_SF_pt4=0.7,1.2:tid_SF_pt5=0.7,1.2:tid_SF_pt6=0.7,1.2:tid_SF_pt7=0.7,1.2:tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s \
#                     -m 90 --setParameters r=1 --freezeParameters r" %(r,dm, RANGE, RANGE, RANGE, RANGE)
#             WORKSPACE = "output_"+args.era+"/combinecards.root"
#             os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all" %(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS))

# # TID SF scan in simultanoeus region and combien fit of TES and TID SF : TID SF in p_T bins
# elif args.option == '5': #generate the datacards and do the fit
#     os.system("./TauES_ID/harvestDatacards_TES_idSF_bin_pt.py -y %s -c %s -e %s " %(args.era, args.config, EXTRATAG))  # Generating the datacards for option 5 

#     v = "m_vis"
#     LABEL = setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
#     #Combining the datacards
#     os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis-  DM0_pt1=DM0_pt1%s.txt DM0_pt2=DM0_pt2%s.txt DM0_pt3=DM0_pt3%s.txt \
#                 DM0_pt4=DM0_pt4%s.txt DM0_pt5=DM0_pt5%s.txt DM0_pt6=DM0_pt6%s.txt DM0_pt7=DM0_pt7%s.txt DM1_pt1=DM1_pt1%s.txt \
#                 DM1_pt2=DM1_pt2%s.txt DM1_pt3=DM1_pt3%s.txt DM1_pt4=DM1_pt4%s.txt DM1_pt5=DM1_pt5%s.txt DM1_pt6=DM1_pt6%s.txt \
#                 DM1_pt7=DM1_pt7%s.txt DM10_pt1=DM10_pt1%s.txt DM10_pt2=DM10_pt2%s.txt DM10_pt3=DM10_pt3%s.txt DM10_pt4=DM10_pt4%s.txt\
#                 DM10_pt5=DM10_pt5%s.txt DM10_pt6=DM10_pt6%s.txt DM10_pt7=DM10_pt7%s.txt DM11_pt1=DM11_pt1%s.txt DM11_pt2=DM11_pt2%s.txt\
#                 DM11_pt3=DM11_pt3%s.txt DM11_pt4=DM11_pt4%s.txt DM11_pt5=DM11_pt5%s.txt DM11_pt6=DM11_pt6%s.txt DM11_pt7=DM11_pt7%s.txt\
#                 >output_%s/combinecards.txt" % (args.era, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL,LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, args.era))
#     os.system("text2workspace.py output_%s/combinecards.txt" % (args.era))
#     ## for each decay mode
#     for r in ["pt1","pt2","pt3","pt4","pt5","pt6","pt7"]: #["DM0","DM1","DM10","DM11"]
#         BINLABEL = "mt_"+v+"-"+r+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
#         WORKSPACE = "output_"+args.era+"/ztt_"+BINLABEL+".root"
#         print("Region : "+r)
#         POI_OPTS = "-P tid_SF_%s  --setParameterRanges tid_SF_pt1=0.7,1.2:tid_SF_pt2=0.7,1.2:tid_SF_pt3=0.7,1.2:tid_SF_pt4=0.7,1.2:tid_SF_pt5=0.7,1.2:tid_SF_pt6=0.7,1.2:tid_SF_pt7=0.7,1.2:tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s \
#                 -m 90 --setParameters r=1,tes_DM0=1,tes_DM1=1,tes_DM10=1,tes_DM11=1,tid_SF_pt1=1,tid_SF_pt2=1,tid_SF_pt3=1,tid_SF_pt4=1,tid_SF_pt5=1,tid_SF_pt6=1,tid_SF_pt7=1 --freezeParameters r" %(r, RANGE, RANGE, RANGE, RANGE)
#         WORKSPACE = "output_"+args.era+"/combinecards.root"
#         os.system("combine -M MultiDimFit -t -1 %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all" %(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS))

elif args.option == '6': #generate the datacards and do the fit
    os.system("./TauES_ID/harvestDatacards_TES_idSF_bin_pt.py -y %s -c %s -e %s " %(args.era, args.config, EXTRATAG))  # Generating the datacards for option 5 

    v = "m_vis"
    LABEL = setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
    ##Combining the datacards
    os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis-  DM0_pt1=DM0_pt1%s.txt DM0_pt2=DM0_pt2%s.txt DM0_pt3=DM0_pt3%s.txt \
                DM0_pt4=DM0_pt4%s.txt DM0_pt5=DM0_pt5%s.txt DM0_pt6=DM0_pt6%s.txt DM0_pt7=DM0_pt7%s.txt DM1_pt1=DM1_pt1%s.txt \
                DM1_pt2=DM1_pt2%s.txt DM1_pt3=DM1_pt3%s.txt DM1_pt4=DM1_pt4%s.txt DM1_pt5=DM1_pt5%s.txt DM1_pt6=DM1_pt6%s.txt \
                DM1_pt7=DM1_pt7%s.txt DM10_pt1=DM10_pt1%s.txt DM10_pt2=DM10_pt2%s.txt DM10_pt3=DM10_pt3%s.txt DM10_pt4=DM10_pt4%s.txt\
                DM10_pt5=DM10_pt5%s.txt DM10_pt6=DM10_pt6%s.txt DM10_pt7=DM10_pt7%s.txt DM11_pt1=DM11_pt1%s.txt DM11_pt2=DM11_pt2%s.txt\
                DM11_pt3=DM11_pt3%s.txt DM11_pt4=DM11_pt4%s.txt DM11_pt5=DM11_pt5%s.txt DM11_pt6=DM11_pt6%s.txt DM11_pt7=DM11_pt7%s.txt\
                >output_%s/combinecards.txt" % (args.era, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL,LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, LABEL, args.era))
    os.system("text2workspace.py output_%s/combinecards.txt" % (args.era))
    #for each decay mode
    for r in ["DM0","DM1","DM10","DM11"]: #
        BINLABEL = "mt_"+v+"-"+r+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
        WORKSPACE = "output_"+args.era+"/ztt_"+BINLABEL+".root"
        print("Region : "+r)
        print(">>>>>>> simultaneous fit of tes_" +r + " in pt bins and tes_"+r + "in DM")
        POI_OPTS = "-P tes_%s  --setParameterRanges tid_SF_pt1=0.7,1.2:tid_SF_pt2=0.7,1.2:tid_SF_pt3=0.7,1.2:tid_SF_pt4=0.7,1.2:tid_SF_pt5=0.7,1.2:tid_SF_pt6=0.7,1.2:tid_SF_pt7=0.7,1.2:tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s \
                -m 90 --setParameters r=1,tes_DM0=1,tes_DM1=1,tes_DM10=1,tes_DM11=1,tid_SF_pt1=1,tid_SF_pt2=1,tid_SF_pt3=1,tid_SF_pt4=1,tid_SF_pt5=1,tid_SF_pt6=1,tid_SF_pt7=1 \
                --freezeParameters r" %(r, RANGE, RANGE, RANGE, RANGE)
        WORKSPACE = "output_"+args.era+"/combinecards.root"
        os.system("combine -M MultiDimFit -t -1 %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all" %(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS))
        #os.system("python plot1D_Scan.py output_UL2018/higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root --y-cut 10 --y-max 10 --output plots/plots_"+args.era+"/plot1D_tes_%s --POI tes_%s  --main-label  tid_SF_%s --logo '' --logo-sub '' "%(r,r,r))

# # TES scan in simultanoeus region and combien fit of TES and TID SF : TES in DM
# elif args.option < '5'   :
#     # Generating datacards
#     os.system("./TauES_ID/harvestDatacards_TES_idSF.py -y %s -c %s -e %s "%(args.era,args.config,EXTRATAG)) # Generating the datacards
#     #os.system("./TauES_ID/harvestDatacards_TES_idSF_bin.py -y %s -c %s -e %s "%(args.era,args.config,EXTRATAG)) # Generating the datacards
#     for v in setup["observables"]:
#         print("Observable : "+v)
#         variable = setup["observables"][v]

#         for r in variable["fitRegions"]:
#             print("Region : "+r)

#             region = setup["regions"][r]

#             BINLABEL = "mt_"+v+"-"+r+setup["tag"]+EXTRATAG+"-"+args.era+"-13TeV"
#             WORKSPACE = "output_"+args.era+"/ztt_"+BINLABEL+".root"

#             if args.option == '1':  # fit of tes_DM
#                 POI = "tes_%s" % (r)
#                 print(">>>>>>>"+POI+" fit")
#                 POI_OPTS = "-P %s  --setParameterRanges %s=%s:tid_SF_%s=0.9,1.1 -m 90 --setParameters r=1,%s=1 --freezeParameters r " % (POI, POI, RANGE, r, POI)  # tes_DM
#                 os.system("text2workspace.py output_%s/ztt_%s.txt" %(args.era, BINLABEL))
#                 os.system("combine -M MultiDimFit  %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all --trackParameters tid_SF_%s" %(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS, r))

#             elif args.option == '2':  # fit of tid_SF_DM
#                 POI = "tid_SF_%s" % (r)
#                 print(">>>>>>> tid_"+r+" fit")
#                 POI_OPTS = "-P %s --setParameterRanges tes_%s=%s:%s=0.7,1.2 -m 90 --setParameters r=1,%s=1,tes_%s=1 --freezeParameters r " % (POI, r, RANGE, POI, POI, r)  # tid_SF
#                 os.system("text2workspace.py output_%s/ztt_%s.txt" %(args.era, BINLABEL))
#                 os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all --trackParameters tes_%s" %(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS, r))
#                 #os.system("python plot1D_Scan.py higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root --y-cut 10 --y-max 10 --output plots_"+args.era+"/plot1D_tid_SF_%s --POI tid_SF_%s  --main-label  tid_SF_%s --logo '' --logo-sub '' "%(r,r,r))

#             elif args.option == '3':  # combined fit of tes_DM and tid_SF_DM
#                 print(">>>>>>> combine fit of tid_"+r+" and tes_"+r)
#                 POI1 = "tid_SF_%s" % (r)
#                 POI2 = "tes_%s" % (r)
#                 POI_OPTS = "-P %s -P %s --setParameterRanges %s=%s:%s=0.7,1.2 -m 90 --setParameters r=1,%s=1,%s=1 --freezeParameters r " % (POI2, POI1, POI2, RANGE, POI1, POI2, POI1)
#                 os.system("text2workspace.py output_%s/ztt_%s.txt" %(args.era, BINLABEL))
#                 os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all " %(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS))

#             elif args.option == '4':  # simultaneous fit in DM
#                 print(">>>>>>> simultaneous fit of tes_"+r)
#                 POI_OPTS = "-P tes_%s  --setParameterRanges tid_SF_DM0=0.9:tid_SF_DM1=0.9,1.1:tid_SF_DM10=0.9:tid_SF_DM11=0.9:tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s -m 90 \
#                             --setParameters r=1,tes_%s=1,tid_SF_%s=1 --freezeParameters r " % (r, RANGE, RANGE, RANGE, RANGE, r, r)
#                 WORKSPACE = "output_"+args.era+"/combinecards.root"
#                 os.system("combine -M MultiDimFit  %s %s %s -n .%s %s %s %s --saveNLL --saveSpecifiedNuis all"%(WORKSPACE, ALGO, POI_OPTS, BINLABEL, FIT_OPTS, XRTD_OPTS, CMIN_OPTS))

#             else:
#                 continue

#             # Add this when addind -saveToys option to combine
#             # print("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root")
#             # os.rename("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.123456.root", "higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")
#             # os.rename("higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.GenerateOnly.mH90.123456.root", "higgsCombine.mt_"+v+"-"+r+setup["tag"]+"_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root")

            # # ##Impact plot
            # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s --doInitialFit"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS))
            # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s --doFits --parallel 4"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS))
            # os.system("combineTool.py -M Impacts -t -1 -n %s -d %s %s  --redefineSignalPOIs tes %s %s %s -o postfit/impacts_%s.json"%(BINLABEL, WORKSPACE, FIT_OPTS, POI_OPTS, XRTD_OPTS, CMIN_OPTS, BINLABEL))
            # os.system("plotImpacts.py -i postfit/impacts_%s.json -o postfit/impacts_%s.json"%(BINLABEL,BINLABEL))
            # os.system("convert -density 160 -trim postfit/impacts_%s.json.pdf[0] -quality 100 postfit/impacts_%s.png"%(BINLABEL,BINLABEL))




# os.system("mv higgsCombine*root output_%s" % args.era)


# if args.option == '2' :
#     os.system("./TauES_ID/plotParabola_POI_region.py -p tid_SF -y %s -e %s -r %s,%s -s -a -c %s"% (args.era, EXTRATAG, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), args.config))


# if args.option == '1' or args.option == '4' :
#     os.system("./TauES/plotParabola_TES.py -y %s -e %s -r %s,%s -s -a -c %s" % (args.era, EXTRATAG,min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), args.config))
# #    os.system("./TauES/plotPostFitScan_TES.py -y %s -e %s -r %s,%s -c %s" %(args.era,EXTRATAG,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]),args.config))

# if args.option == '6' :
#     os.system("./TauES_ID/plotParabola_POI_region.py -p tes -y %s -e %s -r %s,%s -s -a -c %s"% (args.era, EXTRATAG, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), args.config))

# if args.option == '5' :
#     os.system("./TauES_ID/plotParabola_POI_region.py -p tid_SF -y %s -e %s -r %s,%s -s -a -c %s"% (args.era, EXTRATAG, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), args.config))
