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
#include "CMSStyle.h"


using namespace RooFit;

void readworkspace(){

    // Open the file of the workspace
    //const char* wFileName= "../../output_UL2018/combine.root";
    const char* wFileName= "./output_UL2018/ztt_mt_m_vis-DM0_pt1_mtlt65_noSF_DMpt_DeepTau.input-UL2018-13TeV.root";

    TFile *f = new TFile(wFileName);
    f->ls();

    // Retrieve the worksapce, RooDataHist, and variable 
    RooWorkspace *w = (RooWorkspace *)f->Get("ztt");    
    w->Print();
    const char* pdfName = "DM0_pt1_data_obs";
    const char* variable = "CMS_x_DM0_pt1";
    RooDataHist *dataset = (RooDataHist *)w->data(pdfName);
    dataset->Print("V");
    RooRealVar *x = w->var(variable);


    // Create a plot 
    RooPlot *xframe = x->frame();

    // Save the canvas
    TCanvas *c = new TCanvas();

    dataset->plotOn(xframe);
    xframe->Draw();

    c->Update();
    const char* outputFile = "./pdf_dat_obs.root";
    c->SaveAs(outputFile);

}