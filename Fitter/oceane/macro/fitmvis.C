#include "TROOT.h"
#include "TString.h"
#include "TObject.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TFile.h"
#include "TH1D.h"
#include "TDirectory.h"

// This function return the ZTT histo in the input and region wanted 
TH1D* getztt(TString region, TString tag) {
    TString inputfile = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV_"+TString(tag)+".root";
    TFile *file = TFile::Open(inputfile);
    TDirectory *dir = (TDirectory*)file->Get(region);
    TString histname = "ZTT";
    TH1D *histZTT = (TH1D*)dir->Get(histname);
    TFile *outf = new TFile("file.root", "RECREATE");
    return histZTT;
}

// Fit ZTT with a sum of three gaussian 
RooAddPdf* fitztt(TH1D* histZTT) {
    // Create RooRealVar for the observable
    RooRealVar x("x", "x", histZTT->GetXaxis()->GetXmin(), histZTT->GetXaxis()->GetXmax());
    // Create RooDataHist for the histogram
    RooDataHist data("data", "data", x,  RooFit::Import(*histZTT));
    // Create Gaussian PDFs
    RooRealVar mean1("mean1", "mean1", histZTT->GetMaximum());
    RooRealVar sigma1("sigma1", "sigma1", 1);
    RooGaussian gauss1("gauss1", "gauss1", x, mean1, sigma1);
    RooRealVar mean2("mean2", "mean2", histZTT->GetMaximum());
    RooRealVar sigma2("sigma2", "sigma2", 1);
    RooGaussian gauss2("gauss2", "gauss2", x, mean2, sigma2);
    RooRealVar mean3("mean3", "mean3", histZTT->GetMaximum());
    RooRealVar sigma3("sigma3", "sigma3", 1);
    RooGaussian gauss3("gauss3", "gauss3", x, mean3, sigma3);
    // Create a sum of Gaussian PDFs
    RooRealVar frac1("frac1", "frac1", 0.4);
    RooRealVar frac2("frac2", "frac2", 0.3);
    RooRealVar frac3("frac3", "frac3", 0.3);

    RooAddPdf* pdf = new RooAddPdf("pdf", "pdf", RooArgList(gauss1, gauss2, gauss3), RooArgList(frac1, frac2, frac3));
    // Perform the fit
    pdf->fitTo(data,RooFit::SumW2Error(kTRUE));
    pdf->Print();
    return pdf;
}


void drawHistFunc(TH1D* histZTT, TString region, TString tag ) {
    // Create RooRealVar for the observable
    RooRealVar x("x", "x", histZTT->GetXaxis()->GetXmin(), histZTT->GetXaxis()->GetXmax());
    // Create RooDataHist for the histogram
    RooDataHist data("data", "data", x,  RooFit::Import(*histZTT));
    // Create Gaussian PDFs
    RooRealVar mean1("mean1", "mean1", 62);
    RooRealVar sigma1("sigma1", "sigma1", 1);
    RooGaussian gauss1("gauss1", "gauss1", x, mean1, sigma1);
    RooRealVar mean2("mean2", "mean2",62);
    RooRealVar sigma2("sigma2", "sigma2", 1);
    RooGaussian gauss2("gauss2", "gauss2", x, mean2, sigma2);
    RooRealVar mean3("mean3", "mean3", 62);
    RooRealVar sigma3("sigma3", "sigma3", 1);
    RooGaussian gauss3("gauss3", "gauss3", x, mean3, sigma3);
    // Create a sum of Gaussian PDFs
    RooRealVar frac1("frac1", "frac1", 0.6); //sum should be 1 
    RooRealVar frac2("frac2", "frac2", 0.3);
    RooRealVar frac3("frac3", "frac3", 0.1);

    RooAddPdf* pdf = new RooAddPdf("pdf", "pdf", RooArgList(gauss1, gauss2, gauss3), RooArgList(frac1, frac2, frac3));
    
    // Set fit parameter 
    mean1.setVal(62);
    sigma1.setVal(1);
    frac1.setVal(0.6);
    mean2.setVal(62);
    sigma2.setVal(1);
    frac2.setVal(0.3);
    mean3.setVal(62);
    sigma3.setVal(1);
    frac3.setVal(0.1);  

    // Perform the fit
    pdf->fitTo(data,RooFit::SumW2Error(kTRUE), RooFit::Minimizer("Minuit2"));

    // Output file 
    TString outputFile1 = "./oceane/macro/output/zttfit/zttfit" + TString(tag)+"_"+TString(region) + ".root";
    TFile *outf = new TFile(outputFile1, "RECREATE"); 

    // Create a new RooPlot
    RooPlot* frame = x.frame();
    // Draw the histogram with error bars
    data.plotOn(frame, RooFit::Name("histZTT"));
    // Draw the fit function on top of the histogram
    pdf->plotOn(frame, RooFit::LineColor(kRed), RooFit::Name("pdf"),RooFit::DrawOption("same"));
    // Draw the fit function on top of the histogram
    gauss1.plotOn(frame, RooFit::LineColor(kBlue), RooFit::Name("gauss1"),RooFit::DrawOption("same"),RooFit::LineStyle(9));
    gauss2.plotOn(frame, RooFit::LineColor(kGreen), RooFit::Name("gauss2"),RooFit::DrawOption("same"),RooFit::LineStyle(9));
    gauss3.plotOn(frame, RooFit::LineColor(kRed), RooFit::Name("gauss3"),RooFit::DrawOption("same"),RooFit::LineStyle(9));
    // Draw the frame on a canvas
    TCanvas* c = new TCanvas("c", "Fit Result", 800, 600);
    frame->Draw();
    // Add a legend
    TLegend *legend = new TLegend(0.7,0.7,0.9,0.9);
    legend->AddEntry(frame->findObject("histZTT"),"histZTT","l");
    legend->AddEntry(frame->findObject("pdf"),"pdf","l");
    legend->AddEntry(frame->findObject("gauss1"),"gauss1","l");
    legend->AddEntry(frame->findObject("gauss2"),"gauss2","l");
    legend->AddEntry(frame->findObject("gauss3"),"gauss3","l");
    legend->Draw();
    // Display the fit result on the canvas
    pdf->paramOn(frame);
    //pdf->paramOn(frame, RooFit::Layout(0.6, 0.9, 0.9));
    histZTT->Write();
    pdf->Write();
    c->Update();
    c->Write();
    outf->Close();
    delete outf;
}
   



void fitmvis(){
    

    TH1D *histZTT = getztt("DM0","mutau_mt65_noSF_DM_binmvis1000"); // get ZTT 
    // RooAddPdf *pdf = fitztt(histZTT);
    // pdf->Print();

    drawHistFunc(histZTT,"DM0","mutau_mt65_noSF_DM");


}