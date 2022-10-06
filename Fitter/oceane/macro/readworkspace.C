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
    TFile *f = new TFile("workspace_py.root");
    f->ls();
    // Retrieve the worksapce, RooDataHist, and variable 
    RooWorkspace *ztt = (RooWorkspace *)f->Get("ztt");    ztt->Print();
    RooDataHist *dataset = (RooDataHist *)ztt->data("DM0_data_obs");
    dataset->Print("V");
    RooRealVar *x = ztt->var("CMS_x_DM0");
    // Create a plot 
    RooPlot *xframe = x->frame();

    // Save the canvas
    TCanvas *c = new TCanvas();

    dataset->plotOn(xframe);
    xframe->Draw();

    c->Update();
    c->SaveAs("./test.root");

}