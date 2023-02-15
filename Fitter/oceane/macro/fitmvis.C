#include "TROOT.h"
#include "TString.h"
#include "TObject.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TFile.h"
#include "TH1D.h"
#include "TDirectory.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooGaussian.h"
#include "RooAddPdf.h"

// This function return the ZTT histo in the input and region wanted
TH1D *getztt(TString region, TString tag, double tes)
{
    TString inputfile = "input/ztt_mt_tes_m_vis.inputs-UL2018-13TeV" + TString(tag) + ".root";
    TFile *file = TFile::Open(inputfile);
    TDirectory *dir = (TDirectory *)file->Get(region);
    TString histname;
    if (tes == 0)
    {
        histname = "ZTT";
    }
    else
    {
        histname = TString::Format("ZTT_TES%.3f", tes);
        std::cout << "histname : " << histname << std::endl;
    }
    TH1D *histZTT = (TH1D *)dir->Get(histname);
    return histZTT;
    file->Close();
}

RooWorkspace *createWorkspace(TH1 *histZTT)
{
    // Create RooRealVar for the histogram's x-axis
    RooRealVar x("x", "x", histZTT->GetXaxis()->GetXmin(), histZTT->GetXaxis()->GetXmax(), "GeV");
    // Create RooDataHist for the histogram
    RooDataHist data("data", "data", x, RooFit::Import(*histZTT));
    int binmax = histZTT->GetMaximumBin();
    double xmax = histZTT->GetXaxis()->GetBinCenter(binmax);
    double rms = histZTT->GetRMS();
    // std::cout << " rms = " << rms << std::endl;  // constant width
    // std::cout << " max = " << xmax << std::endl; // constant width
    // //   Create Gaussian PDFs
    RooRealVar mean1("mean1", "mean1", xmax, xmax - 0.5 * rms, xmax + 0.5 * rms, "GeV"); // xmax+RMS
    RooRealVar sigma1("sigma1", "sigma1", rms, 0.5 * rms, 2 * rms, "GeV");
    RooGaussian gauss1("gauss1", "gauss1", x, mean1, sigma1);
    RooRealVar mean2("mean2", "mean2", xmax, 40, 120, "GeV"); // xmax + 1-2 RMS
    RooRealVar sigma2("sigma2", "sigma2", 1, 5, 500, "GeV");
    RooGaussian gauss2("gauss2", "gauss2", x, mean2, sigma2);
    RooRealVar mean3("mean3", "mean3", xmax, 50, 100, "GeV");
    RooRealVar sigma3("sigma3", "sigma3", 1, 5, 500, "GeV");
    RooGaussian gauss3("gauss3", "gauss3", x, mean3, sigma3);
    // RooRealVar mean4("mean4", "mean4", xmax, xmax - 0.5 *rms, xmax + 0.5 *rms, "GeV"); // xmax+RMS
    // RooRealVar sigma4("sigma4", "sigma4", rms, 0, 1000, "GeV");
    // RooGaussian gauss4("gauss4", "gauss4", x, mean4, sigma4);
    RooRealVar norm("norm", "norm", histZTT->Integral(), 0, 1000000000);
    mean1.setConstant(kFALSE);
    // // Create a sum of Gaussian PDFs
    RooRealVar frac1("frac1", "frac1", 0.6, 0.4, 0.9);
    RooRealVar frac2("frac2", "frac2", 0.1, 0.0, 0.6);
    // RooRealVar frac3("frac3", "frac3", 0.1, 0.0, 0.5);

    RooAddPdf pdf("pdf", "pdf", RooArgList(gauss1, gauss2, gauss3), RooArgList(frac1, frac2));
    // RooAddPdf pdf("pdf", "pdf", RooArgList(gauss1, gauss2, gauss3, gauss4), RooArgList(frac1, frac2, frac3));
    RooExtendPdf extended_pdf("extended_pdf", "extended_pdf", pdf, norm);
    pdf.Print();
    // Create the RooWorkspace
    RooWorkspace *ws = new RooWorkspace("ws");
    // // Import the PDF, the variable, and the data into the workspace
    ws->import(extended_pdf);
    ws->import(data);
    // Return the pointer to the RooWorkspace
    return ws;
}

// Function for fitting the data to the PDF
void fitZTT(RooWorkspace *ws)
{
    // Get the PDF, the variable, and the data from the workspace
    RooAbsPdf *pdf = (RooAbsPdf *)ws->pdf("extended_pdf");
    RooRealVar *x = (RooRealVar *)ws->var("x");
    RooDataHist *data = (RooDataHist *)ws->data("data");
    // Perform the fit
    RooFitResult *result = pdf->fitTo(*data, RooFit::SumW2Error(kTRUE), RooFit::Minimizer("Minuit2"), RooFit::Extended(true), RooFit::Save());
    result->Print();
    ws->import(*result); // import the result object into the workspace
    return result;
}

// Function for plotting the results
void plotResults(RooWorkspace *ws, TString region, TString tag)
{
    // Output file
    TString outputFile1 = "./oceane/macro/output/zttfit/zttfit" + TString(tag) + "_" + TString(region) + ".root";
    TString outputFilepdf = "./oceane/macro/output/zttfit/zttfit" + TString(tag) + "_" + TString(region) + ".pdf";
    TFile *outf = new TFile(outputFile1, "RECREATE");

    std::cout << " >>> Region = " << region << std::endl;
    // Get the PDF, the variable, and the data from the workspace
    RooAddPdf *pdf = (RooAddPdf *)ws->pdf("pdf");
    RooRealVar *x = (RooRealVar *)ws->var("x");
    RooRealVar *norm = (RooRealVar *)ws->var("norm"); // get the normalisation of the pdf
    RooDataHist *data = (RooDataHist *)ws->data("data");
    // ws->Print();
    RooFitResult *result = (RooFitResult *)ws->obj("fitresult_extended_pdf_data");
    RooPlot *frame = x->frame();
    std::cout << "nbins = " << data->numEntries() << std::endl;
    // Draw the frame on a canvas
    TCanvas *c = new TCanvas("c", "Fit Result", 800, 600);
    // Upper plot will be in pad1
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1->SetBottomMargin(0); // Upper and lower plot are joined
    pad1->SetGridx();         // Vertical grid
    pad1->Draw();             // Draw the upper pad: pad1
    pad1->cd();               // pad1 becomes the current pad
    // Draw the histogram with error bars
    data->plotOn(frame, RooFit::Name("histZTT"), RooFit::DataError(RooAbsData::SumW2));
    // Draw the fit function on top of the histogram
    pdf->plotOn(frame, RooFit::LineColor(kRed), RooFit::Name("pdf"), RooFit::DrawOption("same"));
    // Get the gauss functions
    RooArgSet *compSet = pdf->getComponents();
    RooGaussian *gauss1 = (RooGaussian *)compSet->find("gauss1");
    RooGaussian *gauss2 = (RooGaussian *)compSet->find("gauss2");
    RooGaussian *gauss3 = (RooGaussian *)compSet->find("gauss3");
    // RooGaussian *gauss4 = (RooGaussian *)compSet->find("gauss3");

    // Get the frac
    RooRealVar *frac1 = (RooRealVar *)ws->var("frac1");

    // Draw the fit function on top of the histogram
    gauss1->plotOn(frame, RooFit::LineColor(kBlue), RooFit::Name("gauss1"), RooFit::DrawOption("same"), RooFit::LineStyle(9));
    gauss2->plotOn(frame, RooFit::LineColor(kCyan + 2), RooFit::Name("gauss2"), RooFit::DrawOption("same"), RooFit::LineStyle(9));
    gauss3->plotOn(frame, RooFit::LineColor(kViolet + 2), RooFit::Name("gauss3"), RooFit::DrawOption("same"), RooFit::LineStyle(9));
    // gauss4->plotOn(frame, RooFit::LineColor(kViolet + 4), RooFit::Name("gauss4"), RooFit::DrawOption("same"), RooFit::LineStyle(9));
    frame->Draw();
    // Add a legend
    TLegend *legend = new TLegend(0.7, 0.7, 0.9, 0.9);
    legend->AddEntry(frame->findObject("histZTT"), "histZTT", "l");
    legend->AddEntry(frame->findObject("pdf"), "pdf", "l");
    legend->AddEntry(frame->findObject("gauss1"), "gauss1", "l");
    legend->AddEntry(frame->findObject("gauss2"), "gauss2", "l");
    legend->AddEntry(frame->findObject("gauss3"), "gauss3", "l");
    // legend->AddEntry(frame->findObject("gauss4"), "gauss4", "l");
    legend->Draw();
    // result->Print();


     //Create a RooChi2Var object
    //RooChi2Var chi2("chi2", "chi2", *pdf, *data);
    //std::cout << "chi2 = " << chi2.getVal() << std::endl;
     //  // // Get the number of degrees of freedom
    int nfparam = result->floatParsFinal().getSize();               // number degrees of freedom
    double chi2_ndof = frame->chiSquare("pdf", "histZTT", nfparam); // chi2_dof
    int nbins = data->numEntries();
    std::cout << "nbins = " << nbins << std::endl;
    int ndof = nbins - nfparam;
    std::cout << "ndof = " << ndof << std::endl;
    // Calculate chi2/dof
    //double chi2_ndof = chi2.getVal() / ndof*1.0;
    std::cout << "chi2/ndof = " << chi2_ndof << std::endl;
    // Add the chi2/dof value to the plot
    TPaveText *pt = new TPaveText(0.7, 0.6, 0.9, 0.7, "NDC");
    TString text = TString::Format("#chi^{2}/dof = %.2f", chi2_ndof );
    pt->AddText(text);
    pt->SetFillColor(0);
    pt->SetBorderSize(0);
    pt->Draw("same");

    // Get Parameters 
    RooRealVar *mean1 = (RooRealVar *)ws->var("mean1");
    RooRealVar *mean2 = (RooRealVar *)ws->var("mean2");
    RooRealVar *mean3 = (RooRealVar *)ws->var("mean3");
    RooRealVar *sigma1 = (RooRealVar *)ws->var("sigma1");
    RooRealVar *sigma2 = (RooRealVar *)ws->var("sigma2");
    RooRealVar *sigma3 = (RooRealVar *)ws->var("sigma3");

    // Display parameter value 
    // Draw the mean and sigma values on the plot
    TString mean_str1 = Form("mean1 = %.2f #pm %.2f", mean1->getVal(), mean1->getError());
    TString sigma_str1 = Form("#sigma1 = %.2f #pm %.2f", sigma1->getVal(), sigma1->getError());
    TString mean_str2 = Form("mean2 = %.2f #pm %.2f", mean2->getVal(), mean2->getError());
    TString sigma_str2 = Form("#sigma2 = %.2f #pm %.2f", sigma2->getVal(), sigma2->getError());
    TString mean_str3 = Form("mean3 = %.2f #pm %.2f", mean3->getVal(), mean3->getError());
    TString sigma_str3 = Form("#sigma3 = %.2f #pm %.2f", sigma3->getVal(), sigma3->getError());
    //gauss1
    TPaveText *pt1 = new TPaveText(0.7, 0.5, 0.9, 0.6, "NDC");
    pt1->AddText(mean_str1+";"+sigma_str1);
    pt1->SetFillColor(0);
    pt1->SetBorderSize(0);
    pt1->Draw("same");
    //gauss2
    TPaveText *pt2= new TPaveText(0.7, 0.4, 0.9, 0.5, "NDC");
    pt2->AddText(mean_str2+";"+sigma_str3);
    pt2->SetFillColor(0);
    pt2->SetBorderSize(0);
    pt2->Draw("same");
      //gauss2
    TPaveText *pt3 = new TPaveText(0.7, 0.3, 0.9, 0.4, "NDC");
    pt3->AddText(mean_str3+";"+sigma_str3);
    pt3->SetFillColor(0);
    pt3->SetBorderSize(0);
    pt3->Draw("same");

    // pdf->paramOn(frame, RooFit::Layout(0.6, 0.9, 0.9));
    data->Write();
    pdf->Write();
    c->Update();
    //
    //  Ratio plot
    TH1D *ztt_hist = getztt(region, tag, 0);
    outf->cd();
    TH1 *pdf_hist = pdf->createHistogram("pdf_hist", *x, RooFit::Binning(data->numEntries()));
    //TH1 *ztt_hist = data->createHistogram("ztt_hist", *x, RooFit::Binning(data->numEntries()));
    pdf_hist->Scale(norm->getVal());
    double pdf_error[50] = {1.0};
    pdf_hist->SetError(pdf_error);
    std::cout << "bins pdf_hist = " << pdf_hist->GetNbinsX() << std::endl;
    std::cout << "bins ztt_hist = " << ztt_hist->GetNbinsX() << std::endl;
    std::cout << "bins ztt_hist = " << ztt_hist->GetBinError(20) << std::endl;
    std::cout << ">>>>>>error pdf_hist = " << pdf_hist->GetBinError(20) << std::endl;
    // lower plot will be in pad
    c->cd(); // Go back to the main canvas before defining pad2
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0.05, 1, 0.3);
    pad2->SetTopMargin(0);
    pad2->SetBottomMargin(0.2);
    pad2->SetGridx(); // vertical grid
    pad2->Draw();
    pad2->cd();
    // Define the ratio plot
    TH1 *h3 = (TH1 *)ztt_hist->Clone("h3");
    h3->SetLineColor(kBlack);
    h3->Sumw2();
    h3->SetStats(0); // No statistics on lower plot
    h3->Divide(pdf_hist);
    h3->SetMarkerStyle(20);
    h3->SetMarkerColor(kBlack);
    h3->SetMinimum(0); // Define Y ..
    h3->SetMaximum(2); // .. range
    // ztt_hist->Draw();
    // pdf_hist->Draw();
    h3->Draw("ep"); // Draw the ratio plot
    //Draw a line at y = 1 
    TLine *line = new TLine(h3->GetBinLowEdge(1), 1, h3->GetBinLowEdge(h3->GetNbinsX() + 1), 1);
    line->SetLineColor(kBlack);
    line->SetLineStyle(2);
    line->Draw("same");
    c->Update();
    c->Write();
    c->Modified();
    outf->Close();
    //c->SaveAs(outputFilepdf);
    delete outf;

}

void plotShiftedPdf(RooWorkspace *ws_original, TString region, TString tag, double tes)
{
    // Output file
    TString outputFile1 = "./oceane/macro/output/zttfit/zttfit_shift" + TString(tag) + "_" + TString(region) + ".root";
    TString outputFilepdf = "./oceane/macro/output/zttfit/zttfit_shift" + TString(tag) + "_" + TString(region) + TString::Format("tes_%.3f", tes)+".pdf";
    TFile *outf1 = new TFile(outputFile1, "UPDATE");
    //TFile *outf2 = new TFile(outputFilepdf, "UPDATE");


    // Create a new workspace
    RooWorkspace *ws = new RooWorkspace(*ws_original);

    // Get the PDF, the variable, and the data from the workspace
    RooAddPdf *pdf = (RooAddPdf *)ws->pdf("pdf");
    RooRealVar *x = (RooRealVar *)ws->var("x");
    RooDataHist *data = (RooDataHist *)ws->data("data");
    RooRealVar *norm = (RooRealVar *)ws->var("norm"); // get the normalisation of the pdf

    // Get the gauss functions
    RooArgSet *compSet = pdf->getComponents();
    RooGaussian *gauss1 = (RooGaussian *)compSet->find("gauss1");
    RooGaussian *gauss2 = (RooGaussian *)compSet->find("gauss2");
    RooGaussian *gauss3 = (RooGaussian *)compSet->find("gauss3");

    // gauss1->Print();

    // Get the mean variables for the Gaussian PDFs
    RooRealVar *mean1 = (RooRealVar *)ws->var("mean1");
    RooRealVar *mean2 = (RooRealVar *)ws->var("mean2");
    RooRealVar *mean3 = (RooRealVar *)ws->var("mean3");
    // Get the sigma variables for the Gaussian PDFs
    RooRealVar *sigma1 = (RooRealVar *)ws->var("sigma1");
    RooRealVar *sigma2 = (RooRealVar *)ws->var("sigma2");
    RooRealVar *sigma3 = (RooRealVar *)ws->var("sigma3");
    std::cout << "mean1_shifted = " << mean1->getVal() << std::endl;

    if (tes != 0)
    {
        // // Shift the means and the sigma by applying the TES factor
        mean1->setVal(mean1->getVal() * tes);
        mean2->setVal(mean2->getVal() * tes);
        mean3->setVal(mean3->getVal() * tes);
        sigma1->setVal(sigma1->getVal() * tes);
        sigma2->setVal(sigma2->getVal() * tes);
        sigma3->setVal(sigma3->getVal() * tes);
    }
    else
    {
        std::cout << "nominal tes : no shift" << std::endl;
    }

    // // Get the ZTT_tes0.97 histogram
    TH1D *histZTT_tes = getztt(region, tag, tes);

    // // Create a new RooPlot object
    RooPlot *xframe = ws->var("x")->frame();

    // Create RooDataHist for the histogram
    RooDataHist data_shifted("data_shifted", "data_shifted", *x, RooFit::Import(*histZTT_tes));

    // Create the canvas
    outf1->cd();
    TCanvas *c1 = new TCanvas(TString::Format("tes_%.3f", tes), TString::Format("tes_%.3f", tes), 800, 600);
    c1->cd();
    // Upper plot will be in pad1
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
    pad1->SetBottomMargin(0); // Upper and lower plot are joined
    pad1->SetGridx();         // Vertical grid
    pad1->Draw();             // Draw the upper pad: pad1
    pad1->cd();               // pad1 becomes the current pad
    // Plot the ZTT_tes0.97 histogram on the RooPlot
    data_shifted.plotOn(xframe, RooFit::MarkerColor(kBlack));

    // Plot the shifted PDF on the RooPlot
    pdf->plotOn(xframe, RooFit::LineColor(kRed), RooFit::DrawOption("same"));

    // Draw the RooPlot

    xframe->Draw();

    // Display parameter value 
    // Draw the mean and sigma values on the plot
    TString mean_str1 = Form("mean1 = %.2f #pm %.2f", mean1->getVal(), mean1->getError());
    TString sigma_str1 = Form("#sigma1 = %.2f #pm %.2f", sigma1->getVal(), sigma1->getError());
    TString mean_str2 = Form("mean2 = %.2f #pm %.2f", mean2->getVal(), mean2->getError());
    TString sigma_str2 = Form("#sigma2 = %.2f #pm %.2f", sigma2->getVal(), sigma2->getError());
    TString mean_str3 = Form("mean3 = %.2f #pm %.2f", mean3->getVal(), mean3->getError());
    TString sigma_str3 = Form("#sigma3 = %.2f #pm %.2f", sigma3->getVal(), sigma3->getError());
    //gauss1
    TPaveText *pt1 = new TPaveText(0.7, 0.5, 0.9, 0.6, "NDC");
    pt1->AddText(mean_str1+";"+sigma_str1);
    pt1->SetFillColor(0);
    pt1->SetBorderSize(0);
    pt1->Draw("same");
    //gauss2
    TPaveText *pt2= new TPaveText(0.7, 0.4, 0.9, 0.5, "NDC");
    pt2->AddText(mean_str2+";"+sigma_str3);
    pt2->SetFillColor(0);
    pt2->SetBorderSize(0);
    pt2->Draw("same");
      //gauss2
    TPaveText *pt3 = new TPaveText(0.7, 0.3, 0.9, 0.4, "NDC");
    pt3->AddText(mean_str3+";"+sigma_str3);
    pt3->SetFillColor(0);
    pt3->SetBorderSize(0);
    pt3->Draw("same");

    // lower plot will be in pad
    c1->cd(); // Go back to the main canvas before defining pad2
    TPad *pad2 = new TPad("pad2", "pad2", 0, 0.05, 1, 0.3);
    pad2->SetTopMargin(0);
    pad2->SetBottomMargin(0.2);
    pad2->SetGridx(); // vertical grid
    pad2->Draw();
    pad2->cd();
    //  Ratio plot
    outf1->cd();
    TH1 *pdf_hist = pdf->createHistogram("pdf_hist", *x, RooFit::Binning(histZTT_tes->GetNbinsX()));
    pdf_hist->Scale(norm->getVal());
    double pdf_error[50] = {1.0};
    pdf_hist->SetError(pdf_error);
    // Define the ratio plot
    TH1 *h3 = (TH1 *)histZTT_tes->Clone("h3");
    h3->SetLineColor(kBlack);
    h3->Sumw2();
    h3->SetStats(0); // No statistics on lower plot
    h3->Divide(pdf_hist);
    h3->SetMarkerStyle(20);
    h3->SetMarkerColor(kBlack);
    h3->SetMinimum(0); // Define Y ..
    h3->SetMaximum(3); // .. range
    // ztt_hist->Draw();
    // pdf_hist->Draw();
    h3->Draw("ep"); // Draw the ratio plot
    //Draw a line at y = 1 
    TLine *line = new TLine(h3->GetBinLowEdge(1), 1, h3->GetBinLowEdge(h3->GetNbinsX() + 1), 1);
    line->SetLineColor(kBlack);
    line->SetLineStyle(2);
    line->Draw("same");
    c1->Update();
    c1->Modified();
    // c1->ls();
    // outf1->ls();
    c1->Write();
    //c1->SaveAs(outputFilepdf);
    outf1->Close();
    
}

void fitmvis()
{
    gROOT->SetBatch(kTRUE);
    std::vector<TString> decaymodes = {"DM0", "DM1", "DM10", "DM11"};
    std::vector<TString> decaymodespt = {"DM0_pt1", "DM0_pt2", "DM0_pt3", "DM0_pt4", "DM0_pt5", "DM0_pt6", "DM0_pt7", "DM1_pt1", "DM1_pt2", "DM1_pt3", "DM1_pt4", "DM1_pt5", "DM1_pt6", "DM1_pt7", "DM10_pt1", "DM10_pt2", "DM10_pt3", "DM10_pt4", "DM10_pt5", "DM10_pt6", "DM10_pt7", "DM11_pt1", "DM11_pt2", "DM11_pt3", "DM11_pt4", "DM11_pt5", "DM11_pt6", "DM11_pt7"}; // 28
    std::vector<TString> tags = {"_mutau_mt65_noSF_DM", "_mutau_mt65_noSF_DM_stitching_baseline", "_mtlt65_noSF_DMpt_stitching",
                                 "_mtlt65_noSF_DMpt", "_mtlt65_noSF_DMpt_mvisbin_50", "_mutau_mt65_noSF_DM_2pt_stitching_8bins",
                                 "_mutau_mt65_noSF_DM_binmvis1000", "_mtlt65_noSF_DMpt_mvisbin_50", "_mutau_mt65_noSF_DM_varbins",
                                 "_mtlt65_noSF_DMpt_100bins"};
    int idm = 4;

    for (int idm = 0; idm < 2; idm++) // decaymodespt.size()
    { 
        // // Get ZTT from inputs
        std::cout << ">>>>> get ztt region : " << decaymodespt[idm] << std::endl;
        TH1D *histZTT = getztt(decaymodespt[idm], tags[7], 0);
        // // Create the workspace
        // std::cout << ">>>>> create workspace  " << std::endl;
        RooWorkspace *ws = createWorkspace(histZTT);
        // Fit ZTT with pdf
        // std::cout << ">>>>> fit ztt  " << std::endl;
        fitZTT(ws);
        // std::cout << ">>>>> plot   " << std::endl;
        plotResults(ws, decaymodespt[idm], tags[7]);

        const int ntes = 31;

        double tes_values[ntes] = {0.970, 0.972, 0.974, 0.976, 0.978, 0.980, 0.982, 0.984, 0.986, 0.988, 0.990,
                                   0.992, 0.994, 0.996, 0.998, 1.000, 1.002, 1.004, 1.006, 1.008, 1.010, 1.012,
                                   1.014, 1.016, 1.018, 1.020, 1.022, 1.024, 1.026, 1.028, 1.030};

        for (int ites = 0; ites < 1; ites++) //ntes
        {
            plotShiftedPdf(ws, decaymodespt[idm], tags[7], tes_values[ites]);
        }
    }
    // plotShiftedPdf(ws, decaymodespt[0], tags[9], 0.970);
}