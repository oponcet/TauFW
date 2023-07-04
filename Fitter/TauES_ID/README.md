# TauFW Fitter

## Installation

See [the README.md in the parent directory](../../../#taufw).

## Creating inputs:

See [the README.md in the TauES directory ](../TauES)

## Config file : 

* important information about samples, processes, systematics, variations etc. given in config file in yaml format
* examples of yaml files are given in `TauES_ID/config/defaultFitSetupTES_mutau.yml`
  -- explanations are given as comments within the file
* this file is currently being used in TauES/createInputsTES.py, TauES_ID/harvestDatacards_TES_idSF_MCStat.py, makecombinedfitTES_SF.py, plotParabola_POI.py and ../Plotter/plot.py
  -- it can (and will) be used in further scipts / routines in the future
* each config file defines the setup for one specific channel
  -- combinations of channels can be done at datacard level, e.g. to include a mumu-CR
* you can easily make changes on cuts, observables, regions, etc. through the config file
* important information to define in the config file to use makecombinedfitTES_SF.py :
  - 'regions': one datacard file is created for each region. A region contains a definition and a title.
  - 'plottingOrder': used by plotParabola_POI.py to make the summary plot of the POI measurements.
  - 'tesRegions': tes are scanned in this regions. Title are defined. 
  - 'tid_SFRegions': tid SF are scanned in this regions.  Title are defined.
  - 'observables ': observable to fit : usally m_vis.
    - 'fitRegions': for each observable, fit regions are defined.
    - 'scanRegions': for each observable, the region to scan the poi. 


## Running the fit :

### Description of the main script `makecombinedfitTES_SF.py`: 

The script `makecombinedfitTES_SF.py` code provides functionality for generating datacards and performing fits in the mutau and mumu channels. It supports various fit options and allows for scanning and profiling of different parameters.

python makecombinedFitTES_SF.py -y UL2018 -o 1 -c TauES_ID/config/FitSetupTES_mutau_noSF.yml
-> for more information on the different parts, please look into the python script

The fit is done using [Combine tool](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/). See the documentation to change the parameter of the fit. 

### Preparing the datacards :

Datacards are generated in `makecombinedfitTES_SF.py`:
1. `generate_datacards_mutau(era, config, extratag)`: function that generates datacards for the mutau channel. This function call `harvestDatacards_TES_idSF_MCStat.py`.
2. `generate_datacards_mumu(era, config_mumu, extratag)`: function that generates datacards for the mumu channel (Control Region). This function call `harvestDatacards_zmm.py`.

The input to Combine tool is a datacards file (ztt root and txt files). The datacards are generated for each `"region"` defined in the config file.
It define the following informations:
- tes is defined as a POI `"tesRegions"`defined in the config file. Horizontale morphing is used to interpolate between the template genrated in `"TESvariations"` in config file. 
- tid SF is defined as rateParameter for each `"tid_SFRegions"`defined in the config file.
- If `-cmm Zmmconfigfile.yml` command is used, so if CR is used, dy_xsec is also implemented as rateParameter.
- If "norm_wj" is not specified in config file, a rateParameter "sf_W" is defined for the W+Jet normalisation. 
- The `autoMCstat` function is used to have bin-by-bin uncertainties for the sum of all backgrounds.

Merging of datacards is required for two case:
1. When using Zmm CR to merge the datacards between each mutau region and Zmm CR. In this casen, `merge_datacards_ZmmCR(setup, setup_mumu, era, extratag, region)` is called and it returns the the name of the CR + region datacard file (without .txt).
2. When using option for a combined fit of all the region (option 4, 5 and 6) wich require to merge the datacard of all the region (and optionnaly the Zmm CR) in one datacard file. The systematic with the same name (ex tid_pt1 of DM0 and tid_pt1 of DM10) will be assumed 100% correlated. In this case, `merge_datacards_regions(setup, setup_mumu, config_mumu, era, extratag)` is called and return the name of the datacard file (without .txt).


### Fit options :
The option 4,5,6 use combined datacards and are useful to fit on several regions. (ex: tes_DM and tid_SF_pt ...)

1.  Option 1 : This is the default option. For each `"scanRegions"` defined in the config file, a scan of tes is performed. The scan is done in the range specify in the config file (`"TESvariations"`). The tid SF is implemented as a rateParamer wich is profiled. Ex usage : Scan by DM.
2.  Option 2 :  For each `"scanRegions"` defined in the config file, a scan of tid SF is performed. The tes needs to be set as POI with `redefineSignalPOIs` to include it in the fit.
3.  Option 3 : For each 'scanRegions' of each 'observable' a 2D scan of the tes and tid SF is performed. Note that they need to be in the same region (ex: tes_DM0 and tid_SF_DM0).
4.  Option 4 : For each `"scanRegions"` defined in the config file, a scan of the parameter of interest (POI) tif_SF is done. The tes and the tid_SF of other regions are profiled POIs. Ex usage : Fit tes by DM and tid SF by pt.
5.  Option 5 : For each `"scanRegions"` defined in the config file, a scan of the parameter of interest (POI) tes is done. The tid_SF and the tes of other regions are profiled POIs. Ex usage : Fit tes by DM and tid SF by pt.
6.  Option 5 : For each "`tesRegions`" and `"tidRegions"` defined in the config file, a 2D scan of the parameters of interest (POI) tes and tid_SF is done. The tid_SF and the tes of other regions are profiled POIs. Ex usage : Fit tes by DM and tid SF by pt.

### Plotting results : 

The results of the fit are saved in a root file (ex: `higgsCombine*root` in output folder) that can be used to produced several plots.

- NLL pararabolae and summary plots can be produced via `plotScan(setup,setup_mumu, era=era, config=config, config_mumu=config_mumu, option=option)` that called `plotParabola_POI_region.py`.
- Postfit plots showing the correlation between parameters can be produced via `plotScan(setup,setup_mumu, era=era, config=config, config_mumu=config_mumu, option=option)` that called `plotPostFitScan_POI.py`. The parameter to be plot need to be change in `plotPostFitScan_POI.py` code.
- Summary plot of the results of the POI (tes or tid_SF) in function of pt (DM inclusif or not with `--dm-bins` option) via `plotpt_poi.py`. This script use the txt output file of `plotParabola_POI_region.py`to produce the plots. The values of the mean of the pt bin and its std dev need to be change in the fit. This values can be obtained using `./Plotter/get_ptmean.py` (need pt plots of the distribution).
- 2D contours of the 2D scan (usefull for option 3 and 6) via `plot2D_tid_SF.C`. Need to change input file.
