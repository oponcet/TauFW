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

using namespace RooFit;

void plotCMSHist(Char_t *region, Char_t *tag)
{

    // Save the canvas
    TCanvas *c = new TCanvas();

    // Open the file of the workspace
    // const char* wFileName= "../../output_UL2018/combine.root";
    // TString wFileName= "./output_UL2018_lastworkingversion/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    TString wFileName = "./output_UL2018/ztt_mt_m_vis-" + TString(region) + TString(tag) + "_DeepTau.input-UL2018-13TeV.root";

    // TString wFileName= "./output_UL2018/tid_new_output/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    std::cout << ">>> Input file : " << wFileName << std::endl;
    TFile *f = new TFile(wFileName);
    // f->ls();

    // Retrieve the worksapce, RooDataHist, and variable
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");
    w->Print();

    // // Read dataset
    // const char* pdfName = "DM0_pt1_data_obs";
    // const char* variable = "CMS_x_DM0_pt1";
    // RooDataHist *dataset = (RooDataHist *)w->data(pdfName);
    // dataset->Print("V");

    // Read CMSHistFunc::DM0_pt1_ZTT_morph[ x=CMS_x_DM0_pt1 vmorphs=(shape_dy) hmorphs=(tes_DM0) ] = 124.646

    char *dm = strtok(region, "_");
    printf("'%s'\n", dm);
    char *pt = strtok(NULL, "_");
    printf("'%s'\n", pt);
    TString sregion = TString(dm) + "_" + TString(pt);
    // TString sregion = TString(dm);

    TString stes = "tes_" + TString(dm);
    TString smvis = "CMS_x_" + TString(sregion);
    TString histfName = TString(dm) + "_" + TString(pt) + "_ZTT_morph";
    // TString histfName = TString(dm)+"_ZTT_morph";

    CMSHistFunc *histf = (CMSHistFunc *)w->obj(histfName); // use w->data() for dataset and w->pdf() for pdf

    // Variable
    RooRealVar *tes = w->var(stes);
    tes->Print();
    RooRealVar *mvis = w->var(smvis);
    mvis->Print();

    // Create a plot
    RooPlot *tesframe = tes->frame();
    RooPlot *mvisframe = mvis->frame();

    //// Mvis distrbution for TES variations
    double TESvariations[34] = {0.970, 0.971, 0.972, 0.973, 0.974, 0.975, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                                0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                                1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};

    for (int i = 0; i < 6; i++)
    {
        std::cout << "tes = " << TESvariations[i] << std::endl;
        tes->setVal(TESvariations[i]);
        tes->setConstant(true);
        histf->plotOn(mvisframe, LineColor(i));
        mvisframe->Draw();

        c->Update();
    }

    histf->Print();

    //// 2d plots tes mvis

    // TH1* hh = histf->createHistogram("hh",*mvis,Binning(100), YVar(*tes, Binning(100)));

    // c->Update();
    // hh->Draw("colz");

    // //// mvis max in function of tes
    // TH1* hmvis = histf->createHistogram("hh",*mvis,Binning(160));

    // mvis->setVal(hmvis->GetMean());

    // mvis->setConstant(true);

    // std::cout << mvis->getValV() << std::endl;

    // histf->plotOn(tesframe);
    // tesframe->Draw();

    // TH1* hh = histf->createHistogram("hh",*tes,Binning(160));
    // hh->Draw("");

    c->Update();

    TString outputFile = "./oceane/macro/plot_pdf/pdf_dat_obs_" + TString(sregion) + TString(tag) + ".root";
    c->SaveAs(outputFile);

    return;
}

void checkMorphing(Char_t *region, Char_t *tag)
{
    // Canvas to save
    TCanvas *c1 = new TCanvas();

    // Workspace containing the workspace
    // TString wFileName= "./output_UL2018/combinecards.root"; // For combined datacards (option 5)
    // TString wFileName= "./output_UL2018_lastworkingversion/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    TString wFileName = "./output_UL2018/ztt_mt_m_vis-" + TString(region) + TString(tag) + "_DeepTau.input-UL2018-13TeV.root";

    // TString wFileName= "./output_UL2018/tid_new_output/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    std::cout << ">>> Input file : " << wFileName << std::endl;
    TFile *f = new TFile(wFileName);
    // f->ls();

    // Retrieve the worksapce, RooDataHist, and variable
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");
    // RooWorkspace *w = (RooWorkspace *)f->Get("w"); // Workspace in combinecards

    w->Print();

    // Read the morph function, example : CMSHistFunc::DM0_pt1_ZTT_morph[ x=CMS_x_DM0_pt1 vmorphs=(shape_dy) hmorphs=(tes_DM0) ] = 124.646

    char *dm = strtok(region, "_");
    printf("'%s'\n", dm);
    char *pt = strtok(NULL, "_");
    printf("'%s'\n", pt);
    TString sregion = TString(dm) + "_" + TString(pt);
    // TString sregion = TString(dm); // dm only

    // Variable
    TString stes = "tes_" + TString(dm);
    TString smvis = "CMS_x_" + TString(sregion);
    TString histfName = TString(dm) + "_" + TString(pt) + "_ZTT_morph";
    // TString histfName = TString(dm)+"_ZTT_morph"; // dm only

    CMSHistFunc *histf = (CMSHistFunc *)w->obj(histfName); // use w->data() for dataset and w->pdf() for pdf

    std::cout << "histf " << histf << std::endl;
    std::cout << "histfName " << histfName << std::endl;

    // Variable
    RooRealVar *tes = w->var(stes);
    tes->Print();
    RooRealVar *mvis = w->var(smvis);
    mvis->Print();

    //// Mvis distrbution for TES variations
    int nbins = 62;
    double TESvariations[nbins];
    double mvisvariations[nbins];
    double mvisIntegrale[nbins];
    double mviserror[nbins];

    double tmptes = 0.970; // tempory tes value

    TH1F *hMeanmvis = new TH1F("hMeanmvis", "", nbins, 0.970, 1.03);
    TH1F *hIntegralmvis = new TH1F("hIntegralmvis", "", nbins, 0.970, 1.03);

    for (int i = 1; i < nbins; i++)
    {
        TESvariations[i] = tmptes;
        tes->setVal(TESvariations[i]);
        tes->setConstant(true);

        TH1 *hmvis = histf->createHistogram("hh", *mvis, Binning(8));
        //  mvis fit
        hmvis->Fit("gaus", "", "", 55.0, 75.0);
        TF1 *fitresult = hmvis->GetFunction("gaus");

        mviserror[i] = fitresult->GetParError(1);
        mvisvariations[i] = hmvis->GetFunction("gaus")->GetParameter(1); // getMean of the gaussiane fit
        mvisIntegrale[i] = hmvis->Integral();

        // Print out
        std::cout << "Mean = " << mvisvariations[i] << std::endl;
        std::cout << "Error = " << mviserror[i] << std::endl;
        std::cout << "Tes = " << TESvariations[i] << std::endl;
        std::cout << "Integral = " << mvisIntegrale[i] << std::endl;

        // hmvis->Draw("");
        hMeanmvis->Fill(TESvariations[i], mvisvariations[i]);
        hIntegralmvis->Fill(TESvariations[i], mvisIntegrale[i]);
        tmptes += 0.001;
        // c1->Update();
        // TString outputFile1 = "./oceane/macro/plot_pdf/fit_mvis/pdf_ztt_morph_mvis"+TString(sregion)+TString(tag)+".root";
        // c1->SaveAs(outputFile1);
    }
    hMeanmvis->SetError(mviserror);

    // // Save 1st canvas

    if (c1)
        c1->Close();

    // // 2nd canvas

    TCanvas *c2 = new TCanvas();
    c2->SetGrid();
    gStyle->SetOptStat(0);

    // hMeanmvis->GetXaxis()->SetNdivisions(30);
    // hMeanmvis->GetXaxis()->SetLabelSize(.015);
    // hMeanmvis->GetYaxis()->SetRangeUser(59,65);
    // hMeanmvis->GetXaxis()->SetTitle("TES");
    // hMeanmvis->GetYaxis()->SetTitle("mvis peak in GeV");
    // c2->Modified();
    // hMeanmvis->Draw("E");

    // Draw integrale value for each TES
    hIntegralmvis->GetXaxis()->SetNdivisions(30);
    hIntegralmvis->GetXaxis()->SetLabelSize(.015);
    hIntegralmvis->GetYaxis()->SetRangeUser(3100, 3500);
    hIntegralmvis->SetMarkerStyle(2); // small crosses
    hIntegralmvis->SetMarkerSize(1);
    hIntegralmvis->GetXaxis()->SetTitle("TES");
    hIntegralmvis->GetYaxis()->SetTitle("mvis Integrale");
    c2->Modified();
    hIntegralmvis->Draw("hist p"); // histogram no erro bar 

    // // mvis->setVal(hmvis->GetMean());

    // // mvis->setConstant(true);

    // // std::cout << mvis->getValV() << std::endl;

    // // // histf->plotOn(tesframe);
    // // // tesframe->Draw();

    // // TH1* hh = histf->createHistogram("hh",*tes,Binning(100));

    // c2->Update();

    TString outputFile2 = "./oceane/macro/plot_pdf/pdf_ztt_morph" + TString(sregion) + TString(tag) + ".root";
    TString outputFile2_pdf = "./oceane/macro/plot_pdf/pdf_ztt_morph" + TString(sregion) + TString(tag) + ".pdf";
    c2->SaveAs(outputFile2);
    c2->SaveAs(outputFile2_pdf);

    return;
}

// Compare the template generated in the inputs and the ones generated by the morphing
void compareMorph(Char_t *region, Char_t *tag)
{

    // Workspace containing the workspace
    // TString wFileName= "./output_UL2018/combinecards.root"; // For combined datacards (option 5)
    // TString wFileName= "./output_UL2018_lastworkingversion/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    TString wFileName = "./output_UL2018/ztt_mt_m_vis-" + TString(region) + TString(tag) + "_DeepTau.input-UL2018-13TeV.root";
    std::cout << ">>> Input file : " << wFileName << std::endl;
    TFile *f = new TFile(wFileName);
    // f->ls();

    // Retrieve the worksapce, RooDataHist, and variable
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");
    // RooWorkspace *w = (RooWorkspace *)f->Get("w"); // Workspace in combinecards

    // w->Print();

    // Read the morph function, example : CMSHistFunc::DM0_pt1_ZTT_morph[ x=CMS_x_DM0_pt1 vmorphs=(shape_dy) hmorphs=(tes_DM0) ] = 124.646

    char *dm = strtok(region, "_");
    printf("'%s'\n", dm);
    char *pt = strtok(NULL, "_");
    printf("'%s'\n", pt);
    // TString sregion = TString(dm)+"_"+TString(pt);
    TString sregion = TString(dm); // dm only

    // Variable
    TString stes = "tes_" + TString(dm);
    TString smvis = "CMS_x_" + TString(sregion);
    // TString histfName = TString(dm)+"_"+TString(pt)+"_ZTT_morph";
    TString histfName = TString(dm) + "_ZTT_morph"; // dm only

    CMSHistFunc *histf = (CMSHistFunc *)w->obj(histfName); // use w->data() for dataset and w->pdf() for pdf

    std::cout << "histf " << histf << std::endl;
    std::cout << "histfName " << histfName << std::endl;

    // Variable
    RooRealVar *tes = w->var(stes);
    tes->Print();
    RooRealVar *morphmvis = w->var(smvis);
    morphmvis->Print();

    //// Mvis distrbution for TES variations
    double TESvariations[31] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                                0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                                1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};
    TString sTESvariations[31] = {"0.970", "0.972", "0.974", "0.976", "0.978", "0.980", "0.982", "0.984", "0.986", "0.988", "0.990",
                                  "0.992", "0.994", "0.996", "0.998", "1.000", "1.002", "1.004", "1.006", "1.008", "1.010", "1.012",
                                  "1.014", "1.016", "1.018", "1.020", "1.022", "1.024", "1.026", "1.028", "1.030"};

    for (int i = 15; i < 31; i++)
    {
        // Canvas to save
        TCanvas *c1 = new TCanvas();

        //// Mvis distribution for one TES variations
        tes->setVal(TESvariations[i]);
        std::cout << "TESvariations[1]=" << sTESvariations[i] << std::endl;
        tes->setConstant(true);
        TH1 *hmvismorph = histf->createHistogram("hh", *morphmvis, Binning(8));
        hmvismorph->Draw();
        c1->Update();

        // Generated template from nTuples
        TString wFileNameInput = "./input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV" + TString(tag) + ".root";
        std::cout << ">>> Input file with input template : " << wFileNameInput << std::endl;
        TFile *finputs = new TFile(wFileNameInput);

        // finputs->ls();

        // Directory corresponding to the region of interest:
        TDirectory *dirregion = finputs->GetDirectory(region);

        // dirregion->ls();

        TString sinput_tes = "ZTT_TES";
        // TString stesval = Form("%g", TESvariations[i]);
        sinput_tes += sTESvariations[i];

        TH1D *hmvisinput = (TH1D *)dirregion->Get(sinput_tes);
        std::cout << "get TH1D = " << sinput_tes << std::endl;

        hmvisinput->Draw("same");
        c1->Update();

        // Ratio plot
        auto rp = new TRatioPlot(hmvismorph, hmvisinput);
        c1->SetTicks(0, 1);
        rp->Draw();
        c1->Update();

        // Save outfile
        TString outputFile1 = "./oceane/macro/plot_pdf/morphvsinput/" + TString(sinput_tes) + "_morph_input" + TString(sregion) + TString(tag) + ".root";
        c1->SaveAs(outputFile1);
        if (c1)
            c1->Close();
    }

    return;
}

// Compare the yield of each bin in function of TES
void yieldmvis(Char_t *region, Char_t *tag, const int ibin)
{

    // Workspace containing the workspace
    // TString wFileName= "./output_UL2018/combinecards.root"; // For combined datacards (option 5)
    // TString wFileName= "./output_UL2018_lastworkingversion/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    TString wFileName = "./output_UL2018/ztt_mt_m_vis-" + TString(region) + TString(tag) + "_DeepTau.input-UL2018-13TeV.root";
    std::cout << ">>> Input file : " << wFileName << std::endl;
    TFile *f = new TFile(wFileName);
    // f->ls();

    // Retrieve the worksapce, RooDataHist, and variable
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");
    // RooWorkspace *w = (RooWorkspace *)f->Get("w"); // Workspace in combinecards

    // w->Print();

    // Read the morph function, example : CMSHistFunc::DM0_pt1_ZTT_morph[ x=CMS_x_DM0_pt1 vmorphs=(shape_dy) hmorphs=(tes_DM0) ] = 124.646

    char *dm = strtok(region, "_");
    printf("'%s'\n", dm);
    char *pt = strtok(NULL, "_");
    printf("'%s'\n", pt);
    //TString sregion = TString(dm)+"_"+TString(pt);
    TString sregion = TString(dm); // dm only

    // Variable
    TString stes = "tes_" + TString(dm);
    TString smvis = "CMS_x_" + TString(sregion);
    //TString histfName = TString(dm)+"_"+TString(pt)+"_ZTT_morph";
    TString histfName = TString(dm) + "_ZTT_morph"; // dm only

    CMSHistFunc *histf = (CMSHistFunc *)w->obj(histfName); // use w->data() for dataset and w->pdf() for pdf

    std::cout << "histf " << histf << std::endl;
    std::cout << "histfName " << histfName << std::endl;

    // Variable
    RooRealVar *tes = w->var(stes);
    tes->Print();
    RooRealVar *morphmvis = w->var(smvis);
    //morphmvis->Print();

    //// Mvis distribution for TES variation
    const int nbinstes = 31;
    double TESvariations[nbinstes] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                                      0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                                      1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};

    double binyiedl[nbinstes]; // contains the values of the yeild for each TEvariation
    double binyiedlerror[nbinstes];
    // Canvas to save
    TCanvas *c1 = new TCanvas();

    // Find the yield of the j bin for each value of TES in TESvariation
    for (int i = 0; i < 31; i++)
    {
        //// Mvis distribution for one TES variations
        tes->setVal(TESvariations[i]);
        std::cout << "TESvariations=" << TESvariations[i] << std::endl;
        //tes->setConstant(true);
        TH1 *hmvismorph = histf->createHistogram("hh", *morphmvis, Binning(8));
        // hmvismorph->Draw();
        binyiedl[i] = hmvismorph->GetBinContent(ibin);
        binyiedlerror[i] = hmvismorph->GetBinError(ibin);
        //std::cout << "binyield 1 = " << binyiedl[i] << std::endl;
        hmvismorph->Delete();
    }
    TH1F *hyieldbin = new TH1F("hyiedlbin", "", nbinstes, 0.970, 1.03); // nbins-1
    hyieldbin->FillN(nbinstes, TESvariations, binyiedl);
    for (int i = 1; i < nbinstes; i++)
    {
        hyieldbin->SetBinError(i,binyiedlerror[i]);
    }
    
    hyieldbin->Draw("");
    //hyieldbin->GetYaxis()->SetRangeUser(14000, 16000);
    hyieldbin->SetMarkerStyle(2); // small crosses  
    hyieldbin->SetMarkerSize(1);
    hyieldbin->GetXaxis()->SetTitle("TES");
    hyieldbin->GetYaxis()->SetTitle("Yield");
    

    c1->Update();
    TString sbin = std::to_string(ibin);

    // Save outfile
    TString outputFile1 = "./oceane/macro/plot_pdf/binyield/mvis_binyeild" + sbin + TString(tag)+"_"+TString(region) + ".root";
    c1->SaveAs(outputFile1);
    if (c1)
        c1->Close();
    hyieldbin->Delete();

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Main function

void readworkspace()
{

    Char_t region[99][99] = {"DM0_pt1", "DM0_pt2", "DM0_pt3", "DM0_pt4",
                             "DM0_pt5", "DM0_pt6", "DM0_pt7", "DM1_pt1",
                             "DM1_pt2", "DM1_pt3", "DM1_pt4", "DM1_pt5",
                             "DM1_pt6", "DM1_pt7", "DM10_pt1", "DM10_pt2",
                             "DM10_pt3", "DM10_pt4", "DM10_pt5", "DM10_pt6",
                             "DM10_pt7", "DM11_pt1", "DM11_pt2", "DM11_pt3",
                             "DM11_pt4", "DM11_pt5", "DM11_pt6", "DM11_pt7",
                             "DM0", "DM1", "DM10", "DM11"}; // lasy [31]
    Char_t tag[99][99] = {"_mtlt65_noSF_DMpt", "_mtlt65_SF_regionpt", "_mtlt65_noSF_DMpt_mvisbin",
                          "_mutau_mt65_noSF_DM_binmvis", "_mutau_mt65_noSF_DM","_mtlt65_noSF_DMpt_var_stich"};

    //    for (int i = 0; i < 1; i++)
    //    {
    //     plotCMSHist(region[i],tag[0]);
    //    }

    // for (int i = 21; i < 28; i++)
    //    {
    //     checkMorphing(region[i],tag[3]);
    //    }

    //    checkMorphing(region[23],tag[0]);

    // plotCMSHist(region[21],tag[0]);

    // compareMorph(region[28], tag[4]);

    // for (int ibin = 1; ibin < 9; ibin++)
    // {
    //      yieldmvis(region[31], tag[4], ibin);
    // }
    //yieldmvis(region[0], tag[0], 3);
   
    plotCMSHist(region[0],tag[5]);

    return;
}