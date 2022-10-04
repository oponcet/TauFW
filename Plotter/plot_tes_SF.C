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

void plot_tes_SF(){


    TFile *f = new TFile("./plots/UL2018/mvis_mt-baseline-UL2018_mtlt65.root");
    // fcombine->ls();
    TCanvas *c = (TCanvas *)f->Get("canvas");
    //c->GetListOfPrimitives()->Print();
    // c->Draw(); //Need to be draw to use cd pad 1 !!!
    // c->cd(1);
    //c->ls();
    // THStack *hstack = (THStack *)c->GetPrimitive("stack_mvis");
    // hstack->Print();

    TPad *p = (TPad*)c->GetListOfPrimitives()->At(0);


    c->Close();

    TCanvas *c1 = new TCanvas("c1", "c1", 25, 25, 800, 800);

    //p->Draw();
    THStack *s = (THStack*)p->GetListOfPrimitives()->At(2);
    
    TH1D *data = (TH1D *)p->GetListOfPrimitives()->At(3);
    TH1D *error = (TH1D *)p->GetListOfPrimitives()->At(6);

    //p->GetListOfPrimitives()->Print();
    TLegend *l = (TLegend*)p->GetListOfPrimitives()->At(8);

    //p->GetListOfPrimitives()->Print();

    //p->GetListOfPrimitives()->At(2)->Print();

    cout << "<<<<<<< "  << endl;

    //s->GetHists()->Print();

    s->Draw("HIST");

    // THStack *s2 = (THStack*)s->Clone();
    // TH1D *ztt = (TH1D *)s2->GetHists()->At(6);


    THStack *s2 = (THStack*)s->Clone();
    TH1D *ztt = (TH1D *)s2->GetHists()->At(6);
    TH1D *ztt2 = (TH1D*)ztt->Clone(); //clone ztt 


    ztt->Scale(0.9); //tid
    //ztt->Reset();

    //ztt2->Scale(0.9);  sum
    int nbins = ztt2->GetNbinsX();

    // //shift in x 
    // for (int i=1;i<=nbins;i++) {
    //     double y = ztt2->GetBinContent(i); 
    //     double x = ztt2->GetXaxis()->GetBinCenter(i); 
    //     double xnew = x + 4; //your transformation 
    //     ztt->Fill(xnew,y); 
    //     } 


    
    s2->Draw("same HIST");
    data->Draw("same P");
    error->Draw("same P E2");
    error->SetLineColor(kBlack);

    ztt->SetFillColorAlpha(92, 0.99);
    ztt->SetLineStyle(9);
    ztt->SetLineColor(222); //222 tid /tes : kAzure+1 / sum : kViolet+9
    ztt->SetLineWidth(4);

    ztt->GetYaxis()->SetRangeUser(0,120000);

    l->SetTextSize(0.09);
    l->Draw();

    //s->Print();
    //s->Draw("HIST");
    //data->Draw("same P");

    c1->Update();
    c1->SaveAs("./plot_2/mvis_tid.root");
    c1->SaveAs("./plot_2/mvis_tid.pdf");


}