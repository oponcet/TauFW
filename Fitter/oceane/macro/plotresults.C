//macro to plot de 1D scan of tid_SF and find the 1 sigma value
#include <TROOT.h>
#include <TObject.h>
#include <TMath.h>
#include "TGraph.h"
#include <TString.h>
#include <TFile.h>
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"
#include "RooStats/ModelConfig.h"
#include <fstream>
#include "CMSStyle.h"
#include <iostream>
#include <fstream>
using namespace std;


void plotresults(){

  TCanvas *c = new TCanvas("c", "tid_SF", 25, 25, 800, 800);
  //c->DrawFrame(0,0,1000,1.5);

  //TID
  // c->Print("./plots_UL2018/results_tid.pdf[");
  // TGraphAsymmErrors *g = new TGraphAsymmErrors("./plots_UL2018/tid.txt","%lg %lg %lg %lg %lg %lg");

  // g->SetTitle( "Measurement of tid SF;""Tau pt (GeV);""tid sf");
  // g->SetMarkerStyle(8);

  // c->cd();
  // g->Draw("APE");
  // g->Print();

  // g->GetYaxis()->SetRangeUser(0,1.5);
  // g->GetXaxis()->SetRangeUser(20,1000);
 
  // gPad->SetLogx();


  // // Canvas saved
  // c->Update();
  // c->Modified();
  
  // c->Print("./plots_UL2018/results_tid.pdf");
  // c->Print("./plots_UL2018/results_tid.pdf]");
  // c->SaveAs("./plots_UL2018/results_tid.root");

  c->Print("./plots_UL2018/results_tid.pdf[");
  TGraphAsymmErrors *g = new TGraphAsymmErrors("./plots_UL2018/tes.txt","%lg %lg %lg %lg %lg %lg");

  g->SetTitle( "Measurement of tes;""tes;""DM");
  g->SetMarkerStyle(8);

  c->cd();
  g->Draw("APE");
  g->Print();

  g->GetXaxis()->SetRangeUser(0.95,1.05);
  g->GetYaxis()->SetRangeUser(0,10);
 


  // Canvas saved
  c->Update();
  c->Modified();
  
  c->Print("./plots_UL2018/results_tes.pdf");
  c->Print("./plots_UL2018/results_tes.pdf]");
  c->SaveAs("./plots_UL2018/results_tes.root");

  
  



}

