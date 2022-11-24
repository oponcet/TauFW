#include <TROOT.h>
#include <TObject.h>
#include <TMath.h>
#include <TString.h>
#include <TFile.h>
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include "RooConstVar.h"
#include "RooProdPdf.h"
#include "TH1.h"




void rebin(){

    // // File
    // //TString inFileName = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV_mutau_mt65_noSF_DM_binmvis1000_rebin.root";
    // TString inFileName = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV_mtlt65_noSF_DMpt_mvisbin_200_rebin.root";
    // TFile* file = new TFile(inFileName, "UPDATE");

    // Directory 
    Char_t dirName[99][99] = {"baseline","DM0_pt1","DM0_pt2","DM0_pt3","DM0_pt4",
                            "DM0_pt5","DM0_pt6","DM0_pt7","DM1_pt1",
                            "DM1_pt2","DM1_pt3","DM1_pt4","DM1_pt5",
                            "DM1_pt6","DM1_pt7","DM10_pt1","DM10_pt2",
                            "DM10_pt3","DM10_pt4","DM10_pt5","DM10_pt6", 
                            "DM10_pt7","DM11_pt1","DM11_pt2","DM11_pt3",
                            "DM11_pt4","DM11_pt5","DM11_pt6","DM11_pt7",
                            "DM0","DM1","DM10","DM11"};
    //TString dirName = "baseline";
    //TString dirName = "DM11";

    for(int i = 0; i<29; i++){

        // File
        //TString inFileName = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV_mutau_mt65_noSF_DM_binmvis1000_rebin.root";
        TString inFileName = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV_mtlt65_noSF_DMpt_mvisbin_200_rebin.root";
        TFile* file = new TFile(inFileName, "UPDATE");

        std::cout << dirName[i] << std::endl;
        TDirectory *dir = (TDirectory*)file->GetDirectory(dirName[i]);

        // Dataset
        TH1D *dataset = (TH1D*)dir->Get("data_obs");
        dataset->Rebin(20);
        int nbins = dataset->GetNbinsX();

        std::cout << "nbins = " << nbins << std::endl;

        file->Write();

        dir->Delete("data_obs;1");

        file->Close();
    }

    


    return;
}
