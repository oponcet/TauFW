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

double z_min(TGraph2D *g) //find the minimun of the likelihood scan 
{
  int n = g->GetN(); // number of points
  double *z = g->GetZ();
  int locmin = TMath::LocMin(n, z);
  double z_min = z[locmin];
  return z_min;
}

void plot2D_Scan(Char_t *tag, Char_t *channel, Char_t *observable)
{
  cout << "filename = ./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root" << endl;
  TFile *f = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  TTree *tree = (TTree *)f->Get("limit");

  TCanvas *c = new TCanvas("c", "tid_SF", 25, 25, 800, 800);

  // Graph
  
  //tree->Draw("2*deltaNLL:tid_SF_" + TString(channel) +":tes_" + TString(channel) +">>h(25 ,0.97,1.03,35,0.7,1.2)","2*deltaNLL<10","prof colz"); //(tid_SF = y , tes_ = x)
  tree->Draw("2*deltaNLL:tid_SF_" + TString(channel) +":tes_DM11>>h(10 ,0.97,1.03,15,0.7,1.2)","2*deltaNLL<10","prof colz"); //(tid_SF = y , tes_ = x)

 // int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel) ,"quantileExpected == -1","P same");
  int n = tree->Draw("tid_SF_" + TString(channel) +":tes_DM11","","P same");


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

void plot3D_Scan(Char_t *tag, Char_t *channel, Char_t *observable)
{
  cout << "filename = ./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root" << endl;
  TFile *f = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  TTree *tree = (TTree *)f->Get("limit");

  TCanvas *c = new TCanvas("c", "tid_SF", 25, 25, 800, 800);

  // Graph
  
  int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel)+":2*deltaNLL","2*deltaNLL<20 &&  (tid_SF_" + TString(channel)+">0.7 && tid_SF_" + TString(channel)+"<1.2 && tes_" + TString(channel)+">0.95 && tes_" + TString(channel)+"<1.05)","gOff");
  
  // int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel) + ":2*deltaNLL", "", "gOff");
  // int n = tree->Draw("tid_SF_" + TString(channel) +":tes_" + TString(channel) + ":2*deltaNLL", "", "gOff");

  TGraph2D *g = new TGraph2D(n, tree->GetV1(), tree->GetV2(), tree->GetV3());
  g->SetTitle("Combinedfit ;tid_SF_" + TString(channel)+";tes_" + TString(channel));

  //min
  double nllmin = z_min(g);
  cout << "zmin = "<< nllmin << endl;


  double *x = g->GetX();
  double *y = g->GetY();
  double *z = g->GetZ();
  for(int i = 0; i< g->GetN(); i++){
    g->SetPoint(i,x[i],y[i],z[i]-nllmin+0.0001);
  }

  // auto cutg = new TCutG("cutg",4);
  // cutg->SetPoint(0,0.97,0.7);
  // cutg->SetPoint(1,0.97,1.2);
  // cutg->SetPoint(2,1.028,1.2);
  // cutg->SetPoint(3,1.028,0.7);

  // g->GetXaxis()->SetLimits(0.8,1.05);
  // g->GetYaxis()->SetLimits(0.8,1.05);
  // g->GetZaxis()->SetLimits(0,10);

  g->Draw("surf2");
  g->SetMarkerSize(1.2);
  // Canvas saved
  c->Update();
  c->Modified();
  c->SaveAs("./plots_UL2018/plot3D_" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".root");
  c->SaveAs("./plots_UL2018/plot3D_" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".pdf");

}


void plot2D_tid_SF()
{
  Char_t tag[3][25] = {"_mtlt65_noSF", "_mtlt65_pT","_mtlt65_SF_regionpt_"};
  Char_t channel[14][15] = {"baseline", "DM0", "DM1", "DM10", "DM11", "DM0_pTlow",
                            "DM1_pTlow", "DM10_pTlow", "DM11_pTlow", "DM0_pThigh", "DM1_pThigh",
                            "DM10_pThigh", "DM11_pThigh","pt1"};
  Char_t observable[2][10] = {"m_vis", "m_2"};


  // for (int i = 1; i < 5; i++)
  // {
  //   plot2D_Scan(tag[0], channel[i], observable[0]);
  // }
  // for (int i = 1; i < 5; i++)
  // {
  //   plot3D_Scan(tag[0], channel[i], observable[0]);
  // }
 
  plot2D_Scan(tag[2], channel[13], observable[0]);
}