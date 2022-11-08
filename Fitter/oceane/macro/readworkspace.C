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

void plotCMSHist(Char_t *region, Char_t *tag){
    // Save the canvas
    TCanvas *c = new TCanvas();

    // Open the file of the workspace
    //const char* wFileName= "../../output_UL2018/combine.root";
    // TString wFileName= "./output_UL2018_lastworkingversion/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    TString wFileName= "./output_UL2018/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";

    //TString wFileName= "./output_UL2018/tid_new_output/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    std::cout <<">>> Input file : " <<  wFileName << std::endl;
    TFile *f = new TFile(wFileName);
    //f->ls();

    // Retrieve the worksapce, RooDataHist, and variable 
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");    
    //w->Print();

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
    //TString sregion = TString(dm)+"_"+TString(pt);
    TString sregion = TString(dm);


    TString stes = "tes_"+TString(dm);
    TString smvis = "CMS_x_"+TString(sregion);
    //TString histfName = TString(dm)+"_"+TString(pt)+"_ZTT_morph";
    TString histfName = TString(dm)+"_ZTT_morph";

    CMSHistFunc *histf = (CMSHistFunc *)w->obj(histfName); //use w->data() for dataset and w->pdf() for pdf

    // Variable 
    RooRealVar *tes = w->var(stes);
    tes->Print();
    RooRealVar *mvis = w->var(smvis);
    mvis->Print();

    // Create a plot 
    RooPlot *tesframe = tes->frame();
    RooPlot *mvisframe = mvis->frame();


    //// Mvis distrbution for TES variations 
    double TESvariations[32] = {0.970,0.971, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                              0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                              1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};

    // for (int i = 0; i <1; i++)
    // {
    //     std::cout << "tes = " << TESvariations[i] << std::endl;
    //     tes->setVal(TESvariations[i]);
    //     tes->setConstant(true);
    //     histf->plotOn(mvisframe);
    //     mvisframe->Draw();

    //     c->Update();
    // }

    // histf->Print();



    //// 2d plots tes mvis 

    //TH1* hh = histf->createHistogram("hh",*mvis,Binning(100), YVar(*tes, Binning(100)));

 
    // c->Update();
    // hh->Draw("colz");


    //// mvis max in function of tes 
    TH1* hmvis = histf->createHistogram("hh",*mvis,Binning(100));

    mvis->setVal(hmvis->GetMean());

    mvis->setConstant(true);

    std::cout << mvis->getValV() << std::endl;

    // histf->plotOn(tesframe);
    // tesframe->Draw();

    TH1* hh = histf->createHistogram("hh",*tes,Binning(100));
    hh->Draw("");

    c->Update();

    TString outputFile = "./oceane/macro/plot_pdf/pdf_dat_obs_"+TString(sregion)+TString(tag)+".root";
    c->SaveAs(outputFile);

    return;
}


void checkMorphing(Char_t *region, Char_t *tag){
    //// Save the canvas
    TCanvas *c = new TCanvas();

    // Open the file of the workspace
    //const char* wFileName= "../../output_UL2018/combine.root";
    // TString wFileName= "./output_UL2018_lastworkingversion/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    TString wFileName= "./output_UL2018/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";

    //TString wFileName= "./output_UL2018/tid_new_output/ztt_mt_m_vis-"+TString(region)+ TString(tag)+"_DeepTau.input-UL2018-13TeV.root";
    std::cout <<">>> Input file : " <<  wFileName << std::endl;
    TFile *f = new TFile(wFileName);
    //f->ls();

    // Retrieve the worksapce, RooDataHist, and variable 
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");    
    //w->Print();

// Read CMSHistFunc::DM0_pt1_ZTT_morph[ x=CMS_x_DM0_pt1 vmorphs=(shape_dy) hmorphs=(tes_DM0) ] = 124.646
    
    char *dm = strtok(region, "_");
    printf("'%s'\n", dm);
    char *pt = strtok(NULL, "_");
    printf("'%s'\n", pt);
    //TString sregion = TString(dm)+"_"+TString(pt);
    TString sregion = TString(dm);


    TString stes = "tes_"+TString(dm);
    TString smvis = "CMS_x_"+TString(sregion);
    //TString histfName = TString(dm)+"_"+TString(pt)+"_ZTT_morph";
    TString histfName = TString(dm)+"_ZTT_morph";

    CMSHistFunc *histf = (CMSHistFunc *)w->obj(histfName); //use w->data() for dataset and w->pdf() for pdf

    // Variable 
    RooRealVar *tes = w->var(stes);
    tes->Print();
    RooRealVar *mvis = w->var(smvis);
    mvis->Print();

    
    //// Mvis distrbution for TES variations 
    double TESvariations[61] ;

    double mvisvariations[61];
    double mviserror[61];

    double tmptes = 0.970;

    TH1F* hMeanmvis = new TH1F("hMeanmvis", "",100, 0.970,1.030);
    
    for (int i = 0; i <61; i++)
    {
        TESvariations[i] = tmptes;
        std::cout << "tes = " << TESvariations[i] << std::endl;
        tes->setVal(TESvariations[i]);
        tes->setConstant(true);

        TH1* hmvis = histf->createHistogram("hh",*mvis,Binning(40));
        hmvis->Fit("gaus","","", 52.0, 75.0);
        TF1 *fitresult = hmvis->GetFunction("gaus");
        mviserror[i] =  fitresult->GetParError(1);
        mvisvariations[i] = hmvis->GetFunction("gaus")->GetParameter(1); //getMean of the gaussiane fit 
        
        // Print out 
        std::cout << "Mean = " <<  mvisvariations[i] <<  std::endl;
        std::cout << "Error = " <<  mviserror[i] <<  std::endl;
        std::cout << "Tes = " <<  TESvariations[i] <<  std::endl;
       
        //hmvis->Draw("");
        hMeanmvis->Fill(TESvariations[i], mvisvariations[i]);
        c->Update();
        tmptes += 0.001;
    }
    //hMeanmvis->SetError(mviserror);
    hMeanmvis->Draw("");


  
    // mvis->setVal(hmvis->GetMean());

    // mvis->setConstant(true);

    // std::cout << mvis->getValV() << std::endl;

    // // histf->plotOn(tesframe);
    // // tesframe->Draw();

    // TH1* hh = histf->createHistogram("hh",*tes,Binning(100));
    

    c->Update();

    TString outputFile = "./oceane/macro/plot_pdf/pdf_dat_obs_"+TString(sregion)+TString(tag)+".root";
    c->SaveAs(outputFile);

    return;
}



void readworkspace(){

   Char_t region[99][99] = {"DM0_pt1","DM0_pt2","DM0_pt3","DM0_pt4",
                            "DM0_pt5","DM0_pt6","DM0_pt7","DM1_pt1",
                            "DM1_pt2","DM1_pt3","DM1_pt4","DM1_pt5",
                            "DM1_pt6","DM1_pt7","DM10_pt1","DM10_pt2",
                            "DM10_pt3","DM10_pt4","DM10_pt5","DM10_pt6", 
                            "DM10_pt7","DM11_pt1","DM11_pt2","DM11_pt3",
                            "DM11_pt4","DM11_pt5","DM11_pt6","DM11_pt7",
                            "DM0","DM1","DM10","DM11"};
    Char_t tag[99][99] = {"_mtlt65_noSF_DMpt","_mtlt65_SF_regionpt_","_mtlt65_noSF_DMpt_mvisbin","_mutau_mt65_noSF_DM_binmvis"};



//    for (int i = 28; i < 32; i++)
//    {
//     plotCMSHist(region[i],tag[3]);
//    }
    

for (int i = 29; i < 30; i++)
   {
    checkMorphing(region[i],tag[3]);
   }
    
 


    return;
}