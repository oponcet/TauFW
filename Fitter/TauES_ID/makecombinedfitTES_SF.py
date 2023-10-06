#! /usr/bin/env python
"""
Date : July 2023 
Author : @oponcet 
Description :
 - Scan of tes and tid SF is implemented as a rateParamer wich is profiled. Ex usage : Scan by DM (option 1)
 - Scan of tid SF and tes need to be set as POI with redefineSignalPOIs to include it in the fit. Ex usage : Scan by DM (option 2) 
 - 2D scan of tes and tid SF. Ex usage : Scan by DM (option 3)
 - Scan of tid SF, tid SF and tes of other regions are profiled POIs. Ex usage : Fit tes by DM and tid SF by pt (option 4)
 - Scan of tes, tid SF and tes of other regions are profiled POIs. Ex usage : Fit tes by DM and tid SF by pt (option 5)
 - 2D scan of tes and tid SF and tes of other regions are profiled POIs. Ex usage : Fit tes by DM and tid SF by pt (option 6) 
"""

from distutils import filelist
from distutils.command.config import config
import sys
import os
import yaml
from argparse import ArgumentParser

# Generating the datacards for mutau channel
def generate_datacards_mutau(era, config, extratag):
    print(' >>>>>> Generating datacards for mutau channel')
    os.system("./TauES_ID/harvestDatacards_TES_idSF_MCStat.py -y %s -c %s -e %s "%(era,config,extratag)) 

# Generating the datacards for mumu channel
def generate_datacards_mumu(era, config_mumu, extratag):
    print(' >>>>>> Generating datacards for mumu channel')
    os.system("TauES_ID/harvestDatacards_zmm.py -y %s -c %s -e %s "%(era,config_mumu,extratag)) # Generating the datacards with one statistics uncertianties for all processes

# Merge the datacards between regions for combine fit and return the name of the combined datacard file
def merge_datacards_regions(setup, setup_mumu, config_mumu, era, extratag):
    # Variable of the fit (usually mvis)
    variable = "m_vis"
    print("Observable : "+variable)
    # LABEL used for datacard file
    LABEL = setup["tag"]+extratag+"-"+era+"-13TeV"
    filelist = "" # List of the datacard files to merge in one file combinecards.txt
    # Name of the combined datacard file
    outcombinedfile = "combinecards%s" %(setup["tag"])
    for region in setup["observables"]["m_vis"]["fitRegions"]:
        filelist += region + "=output_"+era+"/ztt_mt_m_vis-"+region+LABEL+".txt "
        os.system("combineCards.py %s >output_%s/%s.txt" % (filelist, era,outcombinedfile))
    #print("filelist : %s") %(filelist) 
    # Add the CR datacard file to the lsit of file to merge if there is CR option
    if str(config_mumu) != 'None':
        LABEL_mumu = setup_mumu["tag"]+extratag+"-"+era+"-13TeV"
        filelist +=  "zmm=output_"+era+"/ztt_mm_m_vis-baseline"+LABEL_mumu+".txt "
        outcombinedfile += "CR"
        os.system("combineCards.py %s >output_%s/%s.txt" % (filelist, era,outcombinedfile))
        print(">>>>>>>>> merging datacards is done ")
    return outcombinedfile



# Merge the datacards between mt regions and Zmm when using Zmm CR and return the name of the CR + region datacard file
def merge_datacards_ZmmCR(setup, setup_mumu, era,extratag,region):
    # datacard of the region to be merged
    datacardfile_region = "ztt_mt_m_vis-"+region+setup["tag"]+extratag+"-"+era+"-13TeV.txt"
    filelist = "%s=output_%s/%s" %(region,era, datacardfile_region)
    LABEL_mumu = setup_mumu["tag"]+extratag+"-"+era+"-13TeV"
    filelist += " Zmm=output_"+era+"/ztt_mm_m_vis-baseline"+LABEL_mumu+".txt "
    print(filelist)
    # Name of the CR + region datacard file
    outCRfile = "ztt_mt_m_vis-%s_zmmCR" %(region)
    os.system("combineCards.py %s >output_%s/%s.txt" % (filelist, era,outCRfile))
    return outCRfile
    
def run_combined_fit(setup, setup_mumu, option, **kwargs):
    #tes_range    = kwargs.get('tes_range',    "0.970,1.030")
    tes_range    = kwargs.get('tes_range',    "%s,%s" %(min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]))                         )
    tid_SF_range = kwargs.get('tid_SF_range', "0.7,1.3")
    extratag     = kwargs.get('extratag',     "_DeepTau")
    algo         = kwargs.get('algo',         "--algo=grid --alignEdges=1 --saveFitResult ")
    npts_fit     = kwargs.get('npts_fit',     "--points=101")
    fit_opts     = kwargs.get('fit_opts',     "--robustFit=1 --setRobustFitAlgo=Minuit2 --setRobustFitStrategy=2 --setRobustFitTolerance=0.001 %s" %(npts_fit))
    xrtd_opts    = kwargs.get('xrtd_opts',    "--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NE")
    cmin_opts    = kwargs.get('cmin_opts',    "--cminFallbackAlgo Minuit2,Migrad,0:0.0001 --cminPreScan"                                                 )
    save_opts    = kwargs.get('save_opts',    "--saveNLL --saveSpecifiedNuis all "                                                                           )
    era          = kwargs.get('era',          "")
    config_mumu  = kwargs.get('config_mumu',  "")
    workspace = ""

    # Create the workspace for combined fit
    if int(option) > 3:
        # merge datacards regions
        datacardfile = merge_datacards_regions(setup,setup_mumu, config_mumu, era, extratag)
        print("datacard file for combined fit = %s" %(datacardfile)) 
        # Create workspace 
        os.system("text2workspace.py output_%s/%s.txt" %(era, datacardfile))
        workspace = "output_%s/%s.root" %(era, datacardfile)
   
    # Variable of the fit (usually mvis)
    variable = "m_vis"
    ## For each region defined in scanRegions in the config file 
    for r in setup["observables"]["m_vis"]["scanRegions"]:
        print("Region : "+r)

        # Binelabel for output file of the fit
        BINLABELoutput = "mt_"+variable+"-"+r+setup["tag"]+extratag+"-"+era+"-13TeV"

        # For fit by region create the datacards and the workspace here
        if int(option) <= 3 :
            # For CR Zmumu 
            print("config_mumu = %s"  %(config_mumu))
            if str(config_mumu) != 'None':
                # merge datacards regions and CR
                datacardfile = merge_datacards_ZmmCR(setup, setup_mumu, era, extratag, r)
                print("datacard file for fit by region with additionnal CR = %s" %(datacardfile)) 

            else:
                datacardfile = "ztt_mt_m_vis-"+r+setup["tag"]+extratag+"-"+era+"-13TeV"
                print("datacard file for fit by region = %s" %(datacardfile)) 
            # Create workspace 
            os.system("text2workspace.py output_%s/%s.txt" %(era, datacardfile))
            workspace = "output_%s/%s.root" %(era, datacardfile)
            print("Datacard workspace has been created")

        ## FIT ##

        # Fit of tes_DM by DM with tid_SF as a nuisance parameter 
        if option == '1':
            POI = "tes_%s" % (r)
            NP = "rgx{.*tid.*}"
            print(">>>>>>> "+POI+" fit")
            #POI_OPTS = "-P %s --redefineSignalPOIs %s,tid_SF_%s --setParameterRanges %s=%s:tid_SF_%s=%s -m 90 --setParameters r=1,rgx{.*tes.*}=1,rgx{.*tid.*}=1 --freezeParameters r " % (POI, POI, r, POI, tes_range, r,tid_SF_range)  # tes_DM
            POI_OPTS = "-P %s --redefineSignalPOIs %s --setParameterRanges %s=%s -m 90 --setParameters r=1,tes_%s=1,tid_SF_%s=1 --freezeParameters r " % (POI, POI, POI, tes_range, r, r)  # tes_DM
            MultiDimFit_opts = " %s %s %s -n .%s %s %s %s %s --trackParameters %s,rgx{.**.},rgx{.*sf_W_*.}" %(workspace, algo, POI_OPTS, BINLABELoutput, fit_opts, xrtd_opts, cmin_opts, save_opts,NP)
            # Fit with combine
            os.system("combine -M MultiDimFit  %s" %(MultiDimFit_opts))
            # ##Impact plot
            #POI_OPTS_I = "-P %s --setParameterRanges %s=%s:tid_SF_%s=%s -m 90 --setParameters r=1,rgx{.*tes.*}=1,rgx{.*tid.*}=1 --freezeParameters r " % (POI, POI, tes_range, r,tid_SF_range)
            # os.system("combineTool.py -M Impacts -v 2 -n %s -d %s  %s %s %s %s  --doInitialFit"%(BINLABELoutput, workspace,fit_opts, POI_OPTS, xrtd_opts, cmin_opts))
            # os.system("combineTool.py -M Impacts -v 2 -n %s -d %s %s %s %s %s --doFits --parallel 4"%(BINLABELoutput, workspace,fit_opts, POI_OPTS, xrtd_opts, cmin_opts))
            # os.system("combineTool.py -M Impacts -v 2 -n %s -d %s  %s %s %s %s -o postfit/impacts_%s.json"%(BINLABELoutput, workspace, fit_opts, POI_OPTS, xrtd_opts, cmin_opts, BINLABELoutput))
            # os.system("plotImpacts.py -i postfit/impacts_%s.json -o postfit/impacts_%s.json"%(BINLABELoutput,BINLABELoutput))
            # os.system("convert -density 160 -trim postfit/impacts_%s.json.pdf[0] -quality 100 postfit/impacts_%s.png"%(BINLABELoutput,BINLABELoutput))
                
                
        # Fit of tid_SF_DM by DM with tes as a nuisance parameter
        elif option == '2':
            POI = "tid_SF_%s" % (r)
            NP = "rgx{.*tid.*}" 
            print(">>>>>>> Scan of "+POI)
            POI_OPTS = "-P %s --redefineSignalPOIs tes_%s,%s --setParameterRanges %s=%s:tes_%s=%s -m 90 --setParameters r=1,rgx{.*tid.*}=1,rgx{.*tes.*}=1 --freezeParameters r --floatOtherPOIs=1" % (POI,r,POI, POI, tid_SF_range, r,tes_range)  # tes_DM
            MultiDimFit_opts = " %s %s %s -n .%s %s %s %s %s --trackParameters rgx{.*tid.*},rgx{.*W.*},rgx{.*dy.*} --saveInactivePOI=1 " %(workspace, algo, POI_OPTS, BINLABELoutput, fit_opts, xrtd_opts, cmin_opts, save_opts)
            os.system("combine -M MultiDimFit %s " %(MultiDimFit_opts))

        # 2D Fit of tes_DM and tid_SF_DM by DM, both are pois
        elif option == '3':  
            print(">>>>>>> Fit of tid_SF_"+r+" and tes_"+r)
            POI1 = "tid_SF_%s" % (r)
            POI2 = "tes_%s" % (r)
            POI_OPTS = "-P %s -P %s --setParameterRanges %s=%s:%s=%s  --setParameters r=1,%s=1,%s=1 --freezeParameters r " % (POI2, POI1, POI2, tes_range, POI1,tid_SF_range, POI2, POI1)
            MultiDimFit_opts = " -m 90 %s %s %s -n .%s %s %s %s %s --trackParameters rgx{.*tid.*},rgx{.*W.*},rgx{.*dy.*}" %(workspace, algo, POI_OPTS, BINLABELoutput, fit_opts, xrtd_opts, cmin_opts, save_opts)
            os.system("combine -M MultiDimFit  %s " %(MultiDimFit_opts))

        ### Fit with combined datacards  tes_DM0,tes_DM1,tes_DM10,tes_DM11 
        ## Fit of tid_SF in its regions with tes_region and other tid_SF_regions as nuisance parameters    tes_DM0,tes_DM1,tes_DM10,tes_DM11
        elif option == '4': 
            print(">>>>>>> Fit of tid_SF_"+r)
            POI_OPTS = "-P tid_SF_%s --redefineSignalPOIs tes_DM0_pt1,tes_DM0_pt2,tes_DM1_pt1,tes_DM1_pt2,tes_DM10_pt1,tes_DM10_pt2,tes_DM11_pt1,tes_DM11_pt2  --setParameterRanges rgx{.*tid.*}=%s:rgx{.*tes.*}=%s -m 90 --setParameters r=1,rgx{.*tes.*}=1 --freezeParameters r --floatOtherPOIs=1 " %(r, tid_SF_range,tes_range)
            MultiDimFit_opts = "%s %s %s -n .%s %s %s %s %s  --trackParameters rgx{.*tid.*},rgx{.*W.*},rgx{.*dy.*} --saveInactivePOI=1" %(workspace, algo, POI_OPTS, BINLABELoutput, fit_opts, xrtd_opts, cmin_opts, save_opts)
            os.system("combine -M MultiDimFit %s" %(MultiDimFit_opts))

        ## Fit of tes in DM regions with tid_SF and other tes_DM as nuisance parameters  
        elif option == '5':
            print(">>>>>>> simultaneous fit of tid_SF in pt bins and tes_"+r + " in DM")
            POI_OPTS = "-P tes_%s --redefineSignalPOIs tes_DM0_pt1,tes_DM0_pt2,tes_DM1_pt1,tes_DM1_pt2,tes_DM10_pt1,tes_DM10_pt2,tes_DM11_pt1,tes_DM11_pt2 --setParameterRanges rgx{.*tid.*}=%s:rgx{.*tes.*}=%s -m 90 --setParameters r=1,rgx{.*tes.*}=1,rgx{.*tid.*}=1 --freezeParameters r,rgx{.*tid.*} --floatOtherPOIs=1" %(r, tid_SF_range, tes_range)
            MultiDimFit_opts = "%s %s %s -n .%s %s %s %s %s --trackParameters rgx{.*tid.*} --saveInactivePOI=1"  %(workspace, algo, POI_OPTS, BINLABELoutput, fit_opts, xrtd_opts, cmin_opts, save_opts)
            os.system("combine -M MultiDimFit %s " %(MultiDimFit_opts))

        ### 2D Fit of tes_DM and tid_SF in DM and pt regions with others tid_SF and tes_DM as nuisance parameter
        elif option == '6':
            #for each decay mode
            for r in setup['tidRegions']: #["DM0","DM1","DM10","DM11"]
                for dm in setup['tesRegions']:
                    print("Region : "+r)
                    print(">>>>>>> simultaneous fit of tes_" +r + " in pt bins and tes_"+r + "in DM")
                    POI_OPTS = "-P tid_SF_%s -P tes_%s --setParameterRanges rgx{.*tid.*}=%s:rgx{.*tes.*}=%s -m 90 --setParameters r=1 --freezeParameters r" %(r,dm, tid_SF_range, tes_range)
                    MultiDimFit_opts = "-m 90 %s %s %s -n .%s %s %s %s %s  " %(workspace, algo, POI_OPTS, BINLABELoutput, fit_opts, xrtd_opts, cmin_opts, save_opts)
                    os.system("combine -M MultiDimFit %s" %(MultiDimFit_opts))

        else:
            continue

    os.system("mv higgsCombine*root output_%s"%era)

# Plot the scan using output file of combined 
def plotScan(setup, setup_mumu, option, **kwargs):
    tid_SF_range = kwargs.get('tid_SF_range', "0.4,1.6")
    extratag     = kwargs.get('extratag',     "_DeepTau")
    era          = kwargs.get('era',          ""        )
    config       = kwargs.get('config',       ""        )
    # Plot 

    if option == '2' or option == '4'  :
        print(">>> Plot parabola")
        os.system("./TauES_ID/plotParabola_POI_region.py -p tid_SF -y %s -e %s  -s -a -c %s"% (era, extratag, config))
        #os.system("./TauES_ID/plotPostFitScan_POI.py --poi tid_SF -y %s -e %s -r %s,%s -c %s" %(era,extratag,min(tid_SF_range),max(tid_SF_range), config))

    elif option == '1' or option == '5' :
        print(">>> Plot parabola")
        os.system("./TauES_ID/plotParabola_POI_region.py -p tes -y %s -e %s -r %s,%s -s -a -c %s" % (era, extratag, min(setup["TESvariations"]["values"]), max(setup["TESvariations"]["values"]), config))
        os.system("./TauES_ID/plotPostFitScan_POI.py --poi tes -y %s -e %s -r %s,%s -c %s" %(era,extratag,min(setup["TESvariations"]["values"]),max(setup["TESvariations"]["values"]), config))

    else:
        print(" No output plot...")


### main function
def main(args):

    era    = args.era
    config = args.config
    config_mumu = args.config_mumu 
    option = args.option
    extratag     = "_DeepTau"


    print("Using configuration file: %s"%(args.config))
    with open(args.config, 'r') as file:
        setup = yaml.safe_load(file)

    if config_mumu != 'None':
        print("Using configuration file for mumu: %s"%(args.config_mumu))
        with open(args.config_mumu, 'r') as file_mumu:
            setup_mumu = yaml.safe_load(file_mumu)
    else: 
        setup_mumu = 0

    # Generating the datacards for mutau channel
    generate_datacards_mutau(era=era, config=config,extratag=extratag)

    # Generating the datacards for mumu channel
    if str(config_mumu) != 'None':
        generate_datacards_mumu(era=era, config_mumu=config_mumu,extratag=extratag)

    # Run the fit using combine with the different options 
    run_combined_fit(setup,setup_mumu, era=era, config=config, config_mumu=config_mumu, option=option)

    # Plots 
    plotScan(setup,setup_mumu, era=era, config=config, config_mumu=config_mumu, option=option)


###
if __name__ == '__main__':

    argv = sys.argv
    parser = ArgumentParser(prog="makeTESfit", description="execute all steps to run TES fit")
    parser.add_argument('-y', '--era', dest='era', choices=['2016', '2017', '2018', 'UL2016_preVFP','UL2016_postVFP', 'UL2017', 'UL2018','UL2018_v10'], default=['UL2018'], action='store', help="set era")
    parser.add_argument('-c', '--config', dest='config', type=str, default='TauES_ID/config/defaultFitSetupTES_mutau.yml', action='store', help="set config file containing sample & fit setup")
    parser.add_argument('-o', '--option', dest='option', choices=['1', '2', '3', '4', '5','6'], default='1', action='store',
                        help="set option : Scan of tes and tid SF is profiled (-o 1) ;  Scan of tid SF and tes is profiled (-o 2) ; 2D scan of tes and tid SF (-o 3) \
                        ; Scan of tid SF, tid SF and tes of other regions are profiled POIs (-o 4); Scan of tes, tid SF and tes of other regions are profiled POIs(-o 5)\
                        ; 2D scan of tes and tid SF and tes of other regions are profiled POIs (-o 6) ")
    parser.add_argument('-cmm', '--config_mumu', dest='config_mumu', type=str, default='None', action='store', help="set config file containing sample & fit setup")

    args = parser.parse_args()

    main(args)
    print(">>>\n>>> done\n")
