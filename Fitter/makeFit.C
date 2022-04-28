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
#include "RooStats/ModelConfig.h"
#include <fstream>
#include "CMSStyle.h"

void fit(Char_t *tag, Char_t *channel, Char_t *observable)
{

  double TESvariations[31] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                              0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                              1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};

  gROOT->SetBatch(kTRUE);

  double precision = 0.001;
  // ----------------------------------
  // // ASIMOV DATASET
  // TFile *fcombine = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  // // fcombine->ls();
  // TDirectory *dir = fcombine->GetDirectory("toys");
  // // dir->ls();
  // RooDataSet *dataset = (RooDataSet *)dir->Get("toy_asimov");

  // ----------------------------------
  // ZTT WORKSAPCE
  //TFile *fztt = new TFile("./output_UL2018/ztt_mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.root"); // workspace
                                                                                                                                                   // Retrieve workspace from file
   TFile *fztt = new TFile("./output_UL2018/combinecards.root"); //Combine DM 
  RooWorkspace *w = (RooWorkspace *)fztt->Get("w");
  RooStats::ModelConfig *mc = (RooStats::ModelConfig *)w->obj("ModelConfig");
  RooAbsPdf *pdf = mc->GetPdf();
  RooAbsData *dataset = w->data("data_obs");//dataset of the real data 

  //mc->Print();
  //w->Print();
  // RooAbsRealLValue *tes_var = w->var("tes");
  // tes_var->setConstant(false);
  // RooArgSet tes(*tes_var);
  RooAbsRealLValue *r = w->var("r");
  r->setConstant(true);

  // //Case with combined DM 
  RooRealVar *tes_DM0 = w->var("tes_DM0");
  RooRealVar *tes_DM1 = w->var("tes_DM1");
  RooRealVar *tes_DM10 = w->var("tes_DM10");
  RooRealVar *tes_DM11 = w->var("tes_DM11");
 
  tes_DM0->setConstant(false);
  tes_DM1->setConstant(false);
  tes_DM10->setConstant(false);
  tes_DM11->setConstant(false);
  RooArgSet tes(*tes_DM0,*tes_DM1,*tes_DM10,*tes_DM11); //

  tes_DM0->setVal(1);
  tes_DM1->setVal(1);
  tes_DM10->setVal(1);
  tes_DM11->setVal(1);

  //Initialize the error of the systematcis to one 
  //cout << "nuisance : " << *mc->GetNuisanceParameters() << endl;

  //NLL 
  RooAbsReal *nll = pdf->createNLL(*dataset, RooFit::Constrain(*mc->GetNuisanceParameters()), RooFit::GlobalObservables(*mc->GetGlobalObservables()));
  nll->enableOffsetting(kTRUE);

  // // ----------------------------------
  // Minimise: take errors from MINUIT
  RooMinimizer minim_tot(*nll);
  minim_tot.setPrintLevel(-1);
  minim_tot.setEps(precision);
  minim_tot.setVerbose(0);
  minim_tot.setStrategy(2);
  minim_tot.setOffsetting(true);
  minim_tot.setProfile();
  minim_tot.minimize("Minuit2");
  minim_tot.hesse();
  minim_tot.minos(tes);

  RooFitResult *result_tot = minim_tot.save();
  result_tot->Print("v");

  // // ----------------------------------
  // SAVE FIT RESULT IN .txt FILE
  //std::ofstream text_file("./fit/fit" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".txt", std::ofstream::out);
  std::ofstream text_file("./fit/fitcombineDM.txt", std::ofstream::out);
  result_tot->printMultiline(text_file, 1111, true);

  text_file.close();

  return;
}

void parabola(Char_t *tag, Char_t *channel, Char_t *observable)
{
  SetCmsStyle();
  // ----------------------------------
  double TESvariations[31] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                              0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                              1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};
  gROOT->SetBatch(kTRUE);
  double precision = 0.1;
  TCanvas *c1 = new TCanvas("Parabole" + TString(channel), "Parabole" + TString(channel), 900, 900);

  TGraph *g = new TGraph(31);
  // ----------------------------------
  // ASIMOV DATASET
  TFile *fcombine = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  // fcombine->ls();
  TDirectory *dir = fcombine->GetDirectory("toys");
  // dir->ls();
  RooDataSet *dataset = (RooDataSet *)dir->Get("toy_asimov");

  // ----------------------------------
  // ZTT WORKSAPCE
  TFile *fztt = new TFile("./output_UL2018/ztt_mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.root"); // workspace
                                                                                                                                                   // Retrieve workspace from file
  RooWorkspace *w = (RooWorkspace *)fztt->Get("w");
  RooStats::ModelConfig *mc = (RooStats::ModelConfig *)w->obj("ModelConfig");
  RooAbsPdf *pdf = mc->GetPdf();

  mc->Print();
  // w->Print();

  RooAbsRealLValue *tes = w->var("tes");
  RooAbsRealLValue *r = w->var("r");
  r->setConstant(true);

  // Set tes to 1 to have it as reference for the calculation of NLL
  tes->setVal(1);
  tes->setConstant(true);

  // Create representation of -log(L) given asimov dataset
  RooAbsReal *nll = pdf->createNLL(*dataset, RooFit::Constrain(*mc->GetNuisanceParameters()), RooFit::GlobalObservables(*mc->GetGlobalObservables()));
  for (int i = 0; i < 31; i++)
  {
    tes->setVal(TESvariations[i]);
    tes->setConstant(true);
    // cout << "TES  = " << TESvariations[i] << " nll = " << nll->getVal() << endl;
    g->SetPoint(i, TESvariations[i], nll->getVal());
  }

  // Graph
  g->SetMarkerStyle(2);
  g->SetTitle("Likelihood Asimov no systematics");
  g->GetXaxis()->SetTitle("TES");
  g->GetYaxis()->SetTitle("-log(L)");
  g->Draw("AP");
  CMSLabel(0, 0.001, TString(observable) + "-" + TString(channel), kBlack, 0.08);
  c1->Update();
  c1->SaveAs("./fit/parabole" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".root");

  return;
}

void parabola_syst(Char_t *tag, Char_t *channel, Char_t *observable)
{
  SetCmsStyle();
  // ----------------------------------
  double TESvariations[31] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                              0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                              1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};
  gROOT->SetBatch(kTRUE);
  double precision = 0.001;
  TCanvas *c1 = new TCanvas("Parabole" + TString(channel), "Parabole" + TString(channel), 900, 900);

  TGraph *g = new TGraph(31);
  // ----------------------------------
  // // ASIMOV DATASET
  // TFile *fcombine = new TFile("./output_UL2018/higgsCombine.mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");
  // // fcombine->ls();
  // TDirectory *dir = fcombine->GetDirectory("toys");
  // // dir->ls();
  // RooDataSet *dataset = (RooDataSet *)dir->Get("toy_asimov"); 
  // ----------------------------------
  // ZTT WORKSAPCE
  
  // TFile *fztt = new TFile("./output_UL2018/ztt_mt_" + TString(observable) + "-" + TString(channel) + TString(tag) + "_DeepTau-UL2018-13TeV.root"); // workspace
  TFile *fztt = new TFile("./output_UL2018/combinecards.root"); 
  RooWorkspace *w = (RooWorkspace *)fztt->Get("w");
  RooStats::ModelConfig *mc = (RooStats::ModelConfig *)w->obj("ModelConfig");
  RooAbsPdf *pdf = mc->GetPdf();
  RooAbsData *dataset = w->data("data_obs");//dataset of the real data 

  // mc->Print();
  //  w->Print();
  // RooAbsRealLValue *tes = w->var("tes");
  // RooAbsRealLValue *r = w->var("r");
  // // Set tes to 1 to have it as reference for the calculation of NLL
  // tes->setVal(1);
  // tes->setConstant(true);
  RooAbsRealLValue *r = w->var("r");
  r->setConstant(true);

  //Case with combined DM 
  RooRealVar *tes_DM0 = w->var("tes_DM0");
  RooRealVar *tes_DM1 = w->var("tes_DM1");
  RooRealVar *tes_DM10 = w->var("tes_DM10");
  RooRealVar *tes_DM11 = w->var("tes_DM11");
 
  tes_DM0->setVal(1);
  tes_DM1->setVal(1);
  tes_DM10->setVal(1);
  tes_DM11->setVal(1);
  RooArgSet tes(*tes_DM0,*tes_DM1,*tes_DM10,*tes_DM11);

  RooAbsReal *nll = pdf->createNLL(*dataset, RooFit::Constrain(*mc->GetNuisanceParameters()), RooFit::GlobalObservables(*mc->GetGlobalObservables()));
  nll->enableOffsetting(kTRUE);

  for (size_t i = 0; i < 31; i++)
  {
    // tes->setVal(TESvariations[i]);
    // tes->setConstant(true);
    tes_DM0->setVal(TESvariations[i]);
    tes_DM1->setVal(TESvariations[i]);
    tes_DM10->setVal(TESvariations[i]);
    tes_DM11->setVal(TESvariations[i]);
    tes_DM0->setConstant(false);
    tes_DM1->setConstant(false);
    tes_DM10->setConstant(false);
    tes_DM11->setConstant(false);
    // // ----------------------------------
    // Minimise: take errors from MINUIT
    cout << "TES = " << TESvariations[i] << endl;
    RooMinimizer minim_tot(*nll);
    minim_tot.setPrintLevel(-1);
    minim_tot.setEps(precision);
    minim_tot.setStrategy(2);
    minim_tot.setOffsetting(true);
    minim_tot.setProfile();
    minim_tot.minimize("Minuit2");
    minim_tot.hesse();
    minim_tot.minos(tes);
    RooFitResult *result_tot = minim_tot.save();

    cout << "TES = " << TESvariations[i] << " result = " << result_tot->minNll() << endl;
    g->SetPoint(i, TESvariations[i], result_tot->minNll());
    result_tot->Print("v");
  }
  // // ----------------------------------
  // Graph
  g->SetMarkerStyle(2);
  g->SetTitle("Likelihood Asimov with systematics");
  g->GetXaxis()->SetTitle("TES");
  g->GetYaxis()->SetTitle("-log(L)");
  g->GetXaxis()->SetRangeUser(0.96, 1.04);
  g->Draw("AP");
  CMSLabel(0, 0.001, TString(observable) + "-" + TString(channel), kBlack, 0.08);
  c1->Update();
  c1->SaveAs("./fit/parabole_syst" + TString(observable) + "-" + TString(channel) + "-UL2018-13TeV" + TString(tag) + ".root");


  return;
}

void makeFit()
{
  Char_t tag[2][12] = {"_mtlt65", "_mtlt65_pT"};
  Char_t channel[13][15] = {"baseline", "DM0", "DM1", "DM10", "DM11", "DM0_pTlow",
                            "DM1_pTlow", "DM10_pTlow", "DM11_pTlow", "DM0_pThigh", "DM1_pThigh",
                            "DM10_pThigh", "DM11_pThigh"};
  Char_t observable[2][10] = {"m_vis", "m_2"};

  // fit(tag[0], channel[2], observable[1]);
  // parabola(tag[1], channel[11], observable[1]);
  // for (int i = 2; i < 5; i++)
  // {
  //   parabola_syst(tag[0], channel[i], observable[1]);
  // }
  
  fit(tag[0], channel[1], observable[0]);
  //parabola_syst(tag[0], channel[1], observable[0]);
  return;
}