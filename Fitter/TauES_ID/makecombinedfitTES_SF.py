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
from distutils import filelist
from distutils.command.config import config
import sys
import os
import yaml
from argparse import ArgumentParser


### Fitting fnction using combine tool
def combinedfit(setup, option, **kwargs):
    tes_range    = kwargs.get('tes_range',    "0.970,1.030"                                                                                  )
    tid_SF_range = kwargs.get('tid_SF_range', "0.7,1.2"                                                                                      )
    extratag     = kwargs.get('extratag',     "_DeepTau"                                                                                     )
    algo         = kwargs.get('algo',         "--algo=grid --alignEdges=1 --saveFitResult "                                                  )# --saveWorkspace
    fit_opts     = kwargs.get('fit_opts',     "--robustFit=1 --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=2 --setRobustFitTolerance=0.1")
    npts_fit     = kwargs.get('npts_fit',     "--points=51"                                                                                  )
    xrtd_opts    = kwargs.get('xrtd_opts',    "--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"           )
    cmin_opts    = kwargs.get('cmin_opts',    "--cminFallbackAlgo Minuit2,Migrad,0:0.5 --cminFallbackAlgo Minuit2,Migrad,0:1.0 --cminPreScan")
    save_opts    = kwargs.get('save_opts',     "--saveNLL --saveSpecifiedNuis all"                                                            )
    era          = kwargs.get('era',          ""                                                                                             )
    config       = kwargs.get('config',       ""                                                                                             )

    ### DM regions : tes and tid_SF
    if option < '5':
    # Generating datacards
        #os.system("./TauES_ID/harvestDatacards_TES_idSF.py -y %s -c %s -e %s "%(era,config,extratag))
        os.system("./TauES_ID/harvestDatacards_TES_idSF_bin.py -v -y %s -c %s -e %s "%(era,config,extratag)) # Generating the datacards with one statistics uncertianties for all processes
    
    # Simultaneous fit require to combine the datacards 
    elif option == '4':
        LABEL = setup["tag"]+extratag+"-"+era+"-13TeV"
        os.system("combineCards.py --prefix=output_%s/ztt_mt_m_vis- DM0=DM0%s.txt DM1=DM1%s.txt DM10=DM10%s.txt DM11=DM11%s.txt >output_%s/combinecards.txt" % (era, LABEL, LABEL, LABEL, LABEL, era))
        os.system("text2workspace.py output_%s/combinecards.txt" % (era))
    
    ## Fit of tid_SF in pt regions with tes_DM and other tid_SF_pt as nuisance parameters  
    elif option == '5' or option == '6' : 
        # generate the datacards and do the fit
        #os.system("./TauES_ID/harvestDatacards_TES_idSF_bin_pt.py -y %s -c %s -e %s " %(era, config, extratag))
        print(" ok ")
    else:
        print("This option does not exist... try --help")


    # Variable like m_vis 
    for v in setup["observables"]:
        variable = setup["observables"][v]
        print("Observable : "+v)

        # #Combining the datacards to do the fit simultaneously with all the parameters
        # if  option == '5' or option == '6' : 
        #     LABEL = setup["tag"]+extratag+"-"+era+"-13TeV"
        #     filelist = "" # List of the datacard files to merge in one file combinecards.txt
        #     for region in variable["fitRegions"]:
        #         filelist += "output_"+era+"/ztt_mt_m_vis-"+region+LABEL+".txt "
        # #print("filelist : %s") %(filelist) 
        # os.system("combineCards.py %s >output_%s/combinecards.txt" % (filelist, era))
        # os.system("text2workspace.py output_%s/combinecards.txt" % (era))

        ## For each region defined in scanRegions in the config file 
        for r in variable["scanRegions"]:
            print("Region : "+r)

            # Global variables
            BINLABEL = "mt_"+v+"-"+r+setup["tag"]+extratag+"-"+era+"-13TeV"
            WORKSPACE = "output_"+era+"/ztt_"+BINLABEL+".root"

            # Fit of tes_DM by DM with tid_SF as a nuisance parameter 
            if option == '1':
                POI = "tes_%s" % (r)
                print(">>>>>>>"+POI+" fit")
                POI_OPTS = "-P %s --setParameterRanges %s=%s:tid_SF_%s=%s -m 90 --setParameters r=1,{.*tes.*}=1 --freezeParameters r " % (POI, POI, tes_range, r,tid_SF_range)  # tes_DM
                os.system("text2workspace.py output_%s/ztt_%s.txt" %(era, BINLABEL))
                os.system("combine -M MultiDimFit  %s %s %s -n .%s %s %s %s %s --trackParameters tid_SF_%s" %(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts, r))

            # Fit of tid_SF_DM by DM with tes as a nuisance parameter
            elif option == '2':
                POI = "tid_SF_%s" % (r)
                print(">>>>>>> tid_"+r+" fit")
                POI_OPTS = "-P %s --setParameterRanges %s=%s:tid_SF_%s=%s -m 90 --setParameters r=1,{.*tes.*}=1 --freezeParameters r " % (POI, POI, tes_range, r,tid_SF_range, POI)  # tes_DM
                os.system("text2workspace.py output_%s/ztt_%s.txt" %(era, BINLABEL))
                os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s 5s --trackParameters tes_%s" %(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts, r))

            # Fit of tes_DM and tid_SF_DM by DM, both are pois
            elif option == '3':  
                print(">>>>>>> Fit of tid_"+r+" and tes_"+r)
                POI1 = "tid_SF_%s" % (r)
                POI2 = "tes_%s" % (r)
                POI_OPTS = "-P %s -P %s --setParameterRanges %s=%s:%s=%s -m 90 --setParameters r=1,%s=1,%s=1 --freezeParameters r " % (POI2, POI1, POI2, tes_range, tid_SF_range, POI1, POI2, POI1)
                os.system("text2workspace.py output_%s/ztt_%s.txt" %(era, BINLABEL))
                os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s %s " %(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts))

            # Fit of tes_DM with other tes_DM and id_SF as nuisance parameter 
            elif option == '4':
                print(">>>>>>> Simultaneous fit of tes_"+r)
                POI_OPTS = "-P tes_%s  --setParameterRanges tid_SF_DM0=%s:tid_SF_DM1=%s:tid_SF_DM10=%s:tid_SF_DM11=%s:tes_DM0=%s:tes_DM1=%s:tes_DM10=%s:tes_DM11=%s -m 90 \
                            --setParameters r=1,tes_%s=1,tid_SF_%s=1 --freezeParameters r " % (r, tid_SF_range, tid_SF_range, tid_SF_range,tid_SF_range, tes_range, tes_range, tes_range, tes_range, r, r)
                WORKSPACE = "output_"+era+"/combinecards.root"
                os.system("combine -M MultiDimFit  %s %s %s -n .%s %s %s %s %s "%(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts))

            ## Fit of tid_SF in pt regions with tes_DM and other tid_SF_pt as nuisance parameters  
            elif option == '5': 
                print(">>>>>>> Fit of tid_SF_"+r)
                POI_OPTS = "-P tid_SF_%s --setParameterRanges rgx{.*tid.*}=%s:rgx{.*tes.*}=%s -m 90 --setParameters r=1,rgx{.*tes.*}=1,rgx{.*tid.*}=1 --freezeParameters r" %(r, tid_SF_range, tes_range)
                WORKSPACE = "output_"+era+"_lastworkingversion/combinecards.root"
                os.system("combine -M MultiDimFit -v 1 %s %s %s -n .%s %s %s %s %s" %(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts))

            ## Fit of tes in DM regions with tid_SF and other tes_DM as nuisance parameters  
            elif option == "6":
                print(">>>>>>> simultaneous fit of tid_SF in pt bins and tes_"+r + " in DM")
                POI_OPTS = "-P tes_%s --setParameterRanges rgx{.*tid.*}=%s:rgx{.*tes.*}=%s -m 90 --setParameters r=1,rgx{.*tes.*}=1,rgx{.*tid.*}=1 --freezeParameters r" %(r, tid_SF_range, tes_range)
                WORKSPACE = "output_"+era+"_lastworkingversion/combinecards.root"
                os.system("combine -M MultiDimFit -t -1 %s %s %s -n .%s %s %s %s %s" %(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts))

            else:
                continue


    os.system("mv higgsCombine*root output_%s"%era)

    ### Plot 

    if option == '2' :
      os.system("./TauES_ID/plotParabola_POI_region.py -p tid_SF -y %s -e %s -r %s,%s -s -a -c %s"% (era, extratag, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), config))
    
    elif option == '1' or option == '4' :
        os.system("./TauES_ID/plotParabola_POI_region.py -p tes -y %s -e %s -r %s,%s -s -a -c %s" % (era, extratag, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), config))
    #    os.system("./TauES/plotPostFitScan_TES.py -y %s -e %s -r %s,%s -c %s" %(era,extratag,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]), config))

    elif option == '6' :
        os.system("./TauES_ID/plotParabola_POI_region.py -p tes -y %s -e %s -r %s,%s -s -a -c %s"% (era, extratag, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), config))

    elif option == '5' :
        os.system("./TauES_ID/plotParabola_POI_region.py -p tid_SF -y %s -e %s -r %s,%s -s -a -c %s"% (era, extratag, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), config))
    
    else:
        print(" No output...")
      

      # ## 2D Fit of tes_DM and tid_SF in DM and pt regions with others tid_SF and tes_DM as nuisance parameter
    # elif option == '7':
    #     os.system("./TauES_ID/harvestDatacards_TES_idSF_bin_pt.py -y %s -c %s -e %s " %(era, config, extratag))

    #     v = "m_vis"
    #     LABEL = setup["tag"]+extratag+"-"+era+"-13TeV"
    #        #Combining the datacards to do the fit simultaneously with all the parameters
    #     filelist = "" # List of the datacard files to merge in one file combinecards.txt
    #     for file in setup['fitRegions']:
    #         filelist += "output_"+era+"/ztt_mt_m_vis-"+file+LABEL+".txt "
    #     #print("filelist : %s") %(filelist) 
    #     os.system("combineCards.py %s >output_%s/combinecards.txt" % (filelist, era))
    #     os.system("text2workspace.py output_%s/combinecards.txt" % (era))
    #     #for each decay mode
    #     for r in ["pt1","pt2","pt3","pt4","pt5","pt6","pt7"]: #["DM0","DM1","DM10","DM11"]
    #         for dm in ["DM0","DM1","DM10","DM11"]:
    #             BINLABEL = "mt_"+v+"-"+r+dm+setup["tag"]+extratag+"-"+era+"-13TeV"
    #             print("Region : "+r)
    #             print(">>>>>>> simultaneous fit of tes_" +r + " in pt bins and tes_"+r + "in DM")
    #             POI_OPTS = "-P tid_SF_%s -P tes_%s --setParameterRanges rgx{.*tid.*}=%s:rgx{.*tes.*}=%s -m 90 --setParameters r=1 --freezeParameters r" %(r,dm, tid_SF_range, tes_range)
    #             WORKSPACE = "output_"+era+"/combinecards.root"
    #             os.system("combine -M MultiDimFit %s %s %s -n .%s %s %s %s %s " %(WORKSPACE, algo, POI_OPTS, BINLABEL, fit_opts, xrtd_opts, cmin_opts, save_opts))


### main function
def main(args):

    print("Using configuration file: %s")%(args.config)
    with open(args.config, 'r') as file:
        setup = yaml.safe_load(file)

    era    = args.era
    config = args.config
    option = args.option

    combinedfit(setup, era=era, config=config, option=option)

###
if __name__ == '__main__':
    print

    argv = sys.argv
    parser = ArgumentParser(prog="makeTESfit", description="execute all steps to run TES fit")
    parser.add_argument('-y', '--era', dest='era', choices=['2016', '2017', '2018', 'UL2016_preVFP','UL2016_postVFP', 'UL2017', 'UL2018'], default=['UL2018'], action='store', help="set era")
    parser.add_argument('-c', '--config', dest='config', type=str, default='TauES_ID/config/defaultFitSetupTES_mutau.yml', action='store', help="set config file containing sample & fit setup")
    parser.add_argument('-o', '--option', dest='option', choices=['1', '2', '3', '4', '5','6','7'], default='1', action='store',
                        help="set option : fit of tes_DM(-o 1) ; fit of tid_SF_DM (-o 2) ; combined fit of tes_DM and tid_SF_DM (-o 3) \
                        ; fit of tes_DM in simultaneous DM (-o 4) ; combined fit of on region scan ID SF (-o 5); combine fit of on region scan TES (-o 6)\
                        ; combine fit of on region 2D scan TES and tid SF (-o 7) ")
   
    args = parser.parse_args()

    main(args)
    print ">>>\n>>> done\n"




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





