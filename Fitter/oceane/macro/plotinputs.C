#include "TROOT.h"
#include "TString.h"
#include "TObject.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TFile.h"
#include "TH1D.h"
#include "TDirectory.h"

// This functin retrun a list of histogram. Each histogram contains the bin content of
// the ZTT histo in function of TES. There is one histo for each bin (default 8) 
void fill_new_hists(TString region, int nbins, TString tag) {
    TString inputfile = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV"+TString(tag)+".root";
    TFile *file = TFile::Open(inputfile);
    TDirectory *dir = (TDirectory*)file->Get(region);
    TH1D *hist[31];

    TString outputFile1 = "./oceane/macro/output/bincontent/bincontent" + TString(tag)+"_"+TString(region) + ".root";
    TFile *outf = new TFile(outputFile1, "RECREATE"); // output file for each DM 


    double tes_values[31] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                            0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                            1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};
    for (int ibin = 0; ibin < nbins; ibin++) {
        TH1D *newHist = new TH1D("binContent"+ TString::Format("%d", ibin), "Bin Content", 31, 0.970, 1.030);
        for (int i = 0; i < 31; i++)
        {
            TString histname = "ZTT_TES"+ TString::Format("%.3f", tes_values[i]);
            //std::cout << "histname= " << histname << std::endl; 
            hist[i] = (TH1D*)dir->Get(histname);
            newHist->Fill(tes_values[i], hist[i]->GetBinContent(ibin+1));
            newHist->SetBinError(i, hist[i]->GetBinError(ibin+1));
        } 
        //newHist->Draw();
        newHist->Write();
        delete newHist;

    }
    outf->Close();
    delete outf;

}

void plotinputs(){

    std::vector<TString> decaymodes = {"DM0","DM1","DM10","DM11"};
    std::vector<TString> decaymodespt = {"DM0_pt1","DM0_pt2","DM0_pt3","DM0_pt4","DM0_pt5","DM0_pt6","DM0_pt7", "DM1_pt1","DM1_pt2","DM1_pt3","DM1_pt4","DM1_pt5","DM1_pt6","DM1_pt7","DM10_pt1","DM10_pt2","DM10_pt3","DM10_pt4","DM10_pt5","DM10_pt6","DM10_pt7","DM11_pt1","DM11_pt2","DM11_pt3","DM11_pt4","DM11_pt5","DM11_pt6","DM11_pt7"};//28
    std::vector<TString> tags = {"_mutau_mt65_noSF_DM","_mutau_mt65_noSF_DM_stitching_baseline","_mtlt65_noSF_DMpt_stitching","_mtlt65_noSF_DMpt"};

    //fill_new_hists(decaymodes[0], 8, tags[2]);

    for (int i = 0; i < 28; i++)
    {
        fill_new_hists(decaymodespt[i], 8, tags[2]);
    }
    
}

