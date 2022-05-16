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

void plot2D_Scan(Char_t *tag, Char_t *channel, Char_t *observable)
{
  cout << "filename = ./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root" << endl;
  TFile *f = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  TTree *tree = (TTree *)f->Get("limit");

  TCanvas *c = new TCanvas("c", "tid_SF", 25, 25, 800, 800);

  // Graph
  
  tree->Draw("2*deltaNLL:tid_SF_" + TString(channel) +":tes_" + TString(channel) +">>h(25 ,0.97,1.03,35,0.7,1.2)","2*deltaNLL<10","prof colz"); //(tid_SF = y , tes_ = x)
  int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel) ,"quantileExpected == -1","P same");
  
  // int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel) + ":2*deltaNLL", "", "gOff");
  // int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel) + ":2*deltaNLL", "", "gOff");

  TGraph *g = new TGraph(n, tree->GetV1(), tree->GetV2());
  g->SetTitle("Combinedfit ;tes_" + TString(channel)+";tid_SF_" + TString(channel));

  g->Draw("p same");
  
  // Canvas saved
  c->Update();
  
  c->SaveAs("./plots_UL2018/plot2D_" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".root");
  c->SaveAs("./plots_UL2018/plot2D_" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".pdf");

}

void plot2D_tid_SF()
{
  Char_t tag[2][15] = {"_mtlt65_noSF", "_mtlt65_pT"};
  Char_t channel[13][15] = {"baseline", "DM0", "DM1", "DM10", "DM11", "DM0_pTlow",
                            "DM1_pTlow", "DM10_pTlow", "DM11_pTlow", "DM0_pThigh", "DM1_pThigh",
                            "DM10_pThigh", "DM11_pThigh"};
  Char_t observable[2][10] = {"m_vis", "m_2"};


  for (int i = 1; i < 5; i++)
  {
    plot2D_Scan(tag[0], channel[i], observable[0]);
  }
  
 
}