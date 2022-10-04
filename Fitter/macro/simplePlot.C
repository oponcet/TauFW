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

void moresimplePlot()
{
    TFile *f = new TFile("input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV_mtlt65.root");
    // fcombine->ls();
    TDirectory *dir = f->GetDirectory("DM0");

    auto c = new TCanvas("c", "c", 1500, 1500);
    c->SetWindowSize(1000, 1000);
    TH1D *ztt = (TH1D *)dir->Get("ZTT");

    TH1D *zttnew = new TH1D("zttnew", "zttnew", 8, 50, 100);
    TH1D *zttSF = new TH1D("zttsf", "zttsf", 8, 50, 100);

    double temp = 0;
    double temp2 = 0;

    cout << ztt->GetXaxis()->GetNbins() << endl;
    for (int i = 1; i < ztt->GetXaxis()->GetNbins(); i++)
    {
        temp = 1000 + ztt->GetBinContent(i);
        temp2 = ztt->GetBinContent(i);

        zttnew->AddBinContent(i, temp2);
        zttSF->AddBinContent(i, temp);
    }
    gStyle->SetOptStat(0);

    zttnew->Draw("");
    zttSF->Draw("same");

    zttnew->SetTitle("Signal vs signal with Scale factor ");
    zttnew->GetYaxis()->SetRangeUser(0, 25000);
    zttnew->GetXaxis()->SetTitle("m_vis in GeV");
    zttnew->GetYaxis()->SetTitle("Events/5 GeV");
    zttSF->SetLineColor(kGreen + 2);

    auto leg1 = new TLegend(0.7, 0.7, 0.9, 0.85);
    leg1->AddEntry(zttnew, "Signal", "l");
    leg1->AddEntry(zttSF, "Signal with scale factor", "l");
    leg1->Draw();

    // w2->Draw("sames");

    c->Update();

    c->SaveAs("./simplePlots/simpleplot.root");
}

void simplePlot()
{

    TFile f("../Plotter/plots/UL2018/mvis_mt-baseline-UL2018_mtlt65.root", "read");
    TH1D *hmvis;
    TCanvas *c1 = (TCanvas *)f.Get("canvas");
    // c1->cd(1);
    TVirtualPad *pad = c1->GetPad(1);

    hmvis = (TH1D *)pad->GetPrimitive("mvis_SingleMuon_Run2018:");

    // hmvis->Print();

    // hmvis->Draw("same");

    // c1->SaveAs("./simplePlots/simpleplot.root");
}