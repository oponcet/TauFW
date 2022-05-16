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

double ymin_x(TGraph *g) //find the minimun of the likelihood scan 
{
  int n = g->GetN(); // number of points
  double *y = g->GetY();
  double *x = g->GetX();
  int locmin = TMath::LocMin(n, y);
  double x_ymin = x[locmin];
  double ymin = y[locmin];
  return x_ymin;
}

double sigma1(TGraph *g, int right) // find 1sigma left (=0) and rigth (=1)
{
  int n = g->GetN();
  double *y = g->GetY();
  double *x = g->GetX();

  double sigma1_left = 0;
  double ysigma1_left = y[1]; //closer value to y=1 on the left side
  double sigma1_right = 0;
  double ysigma1_right = y[1]; //closer value to y=1 on the right side 
  switch (right)
  {
  case 0: // left side
    cout << ">>>>>>>sigma 1 left" << endl;
    for (int i = 2; i < n + 1; i++)
    {
      if (x[i] > ymin_x(g))
      {
        break;
      }
      // cout << "y = " << y[i] << endl;
      // cout << "x = " << x[i] << endl;
      if (abs(1 - ysigma1_left) > abs(1 - y[i]))
      {
        ysigma1_left = y[i];
        sigma1_left = x[i] - ymin_x(g);
      }
      else
      {
        break;
      }
    }
    return sigma1_left;
    break;
  case 1: // right side
    cout << ">>>>>>>sigma 1 right" << endl;
    for (int i = 2; i < n + 1; i++)
    {
      if (x[i] < ymin_x(g))
      {
        continue;
      }
      // cout << "y = " << y[i] << endl;
      // cout << "x = " << x[i] << endl;
      if (abs(1 - ysigma1_right) > abs(1 - y[i]))
      {
        ysigma1_right = y[i];
        sigma1_right = x[i] - ymin_x(g);
      }
      else
      {
        break;
      }
    }
    return sigma1_right;
    break;
  default:
    return 0;
    break;
  }
}

void plot1D_Scan(Char_t *tag, Char_t *channel, Char_t *observable)
{
  cout << "filename = ./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root" << endl;
  TFile *f = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  TTree *tree = (TTree *)f->Get("limit");

  TCanvas *c = new TCanvas("c", "tid_SF", 25, 25, 800, 800);

  // Graph
  int n = tree->Draw("tid_SF_" + TString(channel) + ":2*deltaNLL", "", "gOff");
  TGraph *g = new TGraph(n, tree->GetV1(), tree->GetV2());
  g->GetXaxis()->SetTitle("tid_SF_" + TString(channel));
  g->GetYaxis()->SetTitle("-2log(L)");
  g->Draw("ap");
  g->SetMarkerStyle(2);

  // 1 Sigma
  // left
  double sigma1_left = sigma1(g, 0);
  TString str_sigma1_left = "";
  str_sigma1_left += sigma1_left;
  str_sigma1_left.Resize(6);
  TLatex *l_sigma1_left = new TLatex(0.2, 0.45, "sigma1_left");
  l_sigma1_left->SetTextSize(0.020);
  l_sigma1_left->DrawTextNDC(0.5, 0.75, "#sigma1_{left} = " + str_sigma1_left);
  cout << "sigmaleft = " << sigma1_left << endl;
  //right
  double sigma1_right = sigma1(g, 1);
  cout << sigma1_right << endl;
  TString str_sigma1_right = "";
  str_sigma1_right += sigma1_right;
  str_sigma1_right.Resize(6);
  TLatex *l_sigma1_right = new TLatex(0.2, 0.15, "sigma1_right");
  l_sigma1_right->SetTextSize(0.020);
  l_sigma1_right->DrawTextNDC(0.5, 0.85, "#sigma1_{right} = " + str_sigma1_left);
  cout << "sigmaright = " << sigma1_right << endl;

  // Canvas saved
  c->Update();
  c->SaveAs("./plotUL_2018" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".root");
}

void plot1D_tid_SF()
{
  Char_t tag[2][12] = {"_mtlt65", "_mtlt65_pT"};
  Char_t channel[13][15] = {"baseline", "DM0", "DM1", "DM10", "DM11", "DM0_pTlow",
                            "DM1_pTlow", "DM10_pTlow", "DM11_pTlow", "DM0_pThigh", "DM1_pThigh",
                            "DM10_pThigh", "DM11_pThigh"};
  Char_t observable[2][10] = {"m_vis", "m_2"};

  plot1D_Scan(tag[0], channel[4], observable[0]);
}