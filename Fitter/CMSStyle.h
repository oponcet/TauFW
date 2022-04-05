#ifndef CMSStyle_H
#define CMSStyle_H

void SetCmsStyle(){
  TStyle *cmsStyle = new TStyle("CMS","Cms style");

  // use plain black on white colors
  Int_t icol=0; // WHITE
  cmsStyle->SetFrameBorderMode(icol);
  cmsStyle->SetFrameFillColor(icol);
  cmsStyle->SetCanvasBorderMode(icol);
  cmsStyle->SetCanvasColor(icol);
  cmsStyle->SetPadBorderMode(icol);
  cmsStyle->SetPadColor(icol);
  cmsStyle->SetStatColor(icol);

  // set the paper & margin sizes
  cmsStyle->SetPaperSize(20,26);

  // set margin sizes
  cmsStyle->SetPadTopMargin(0.05);
  cmsStyle->SetPadRightMargin(0.05);
  cmsStyle->SetPadBottomMargin(0.16);
  cmsStyle->SetPadLeftMargin(0.16);

  // set title offsets (for axis label)
  cmsStyle->SetTitleXOffset(1.1);
  cmsStyle->SetTitleYOffset(1.3);

  // use large fonts
  Int_t font=42; // Helvetica
  Double_t tsize=0.06;
  cmsStyle->SetTextFont(font);

  cmsStyle->SetTextSize(tsize);
  cmsStyle->SetLabelFont(font,"x");
  cmsStyle->SetTitleFont(font,"x");
  cmsStyle->SetLabelFont(font,"y");
  cmsStyle->SetTitleFont(font,"y");
  cmsStyle->SetLabelFont(font,"z");
  cmsStyle->SetTitleFont(font,"z");

  cmsStyle->SetLabelSize(tsize,"x");
  cmsStyle->SetTitleSize(tsize,"x");
  cmsStyle->SetLabelSize(tsize,"y");
  cmsStyle->SetTitleSize(tsize,"y");
  cmsStyle->SetLabelSize(tsize,"z");
  cmsStyle->SetTitleSize(tsize,"z");

  // use bold lines and markers
  cmsStyle->SetMarkerStyle(20);
  cmsStyle->SetMarkerSize(1.2);
  cmsStyle->SetHistLineWidth((Width_t)3.0);
  cmsStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes

  // get rid of error bar caps
  cmsStyle->SetEndErrorSize(0.);

  // do not display any of the standard histogram decorations
  cmsStyle->SetOptTitle(0);
  cmsStyle->SetOptStat(0);
  cmsStyle->SetOptFit(0);

  // put tick marks on top and RHS of plots
  cmsStyle->SetPadTickX(1);
  cmsStyle->SetPadTickY(1);

  std::cout << "\nApplying CMS style settings...\n" << std::endl ;
  gROOT->SetStyle("CMS");
  gROOT->ForceStyle();

  return;
}

void CMSLabel(Double_t x,Double_t y,const char* text,Color_t color, Double_t tsize){

  TLatex l;
  l.SetTextSize(tsize);
  l.SetNDC();
  l.SetTextFont(72);
  l.SetTextColor(color);
  double delx = 0.14*696*gPad->GetWh()/(472*gPad->GetWw());
  l.DrawLatex(x,y,"");
  if (text) {
    TLatex p;
    p.SetNDC();
    p.SetTextFont(42);
    p.SetTextColor(color);
    p.SetTextSize(tsize);
    p.DrawLatex(x+delx,y,text);
  }
}

#endif
