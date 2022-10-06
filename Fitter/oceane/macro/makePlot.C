

void makePlot(){


  TFile f("./output_UL2018/higgsCombine.mt_m_vis-DM0_mtlt65_noSF_DeepTau-UL2018-13TeV.MultiDimFit.mH90.root");

  TTree *t = (TTree*)f.Get("limit");
  t->SetBranchStatus("*",false);

  Float_t deltaNLL;
  t->SetBranchStatus("deltaNLL",true);
  t->SetBranchAddress("deltaNLL",&deltaNLL);
  Float_t tes;
  t->SetBranchStatus("tes_DM0",true);
  t->SetBranchAddress("tes_DM0",&tes);
  Float_t tidSF;
  t->SetBranchStatus("tid_SF_DM0",true);
  t->SetBranchAddress("tid_SF_DM0",&tidSF);

  TH2D h("h","",20,0.97,1.01,20,0.7,1.05);
  
  int nPts = t->GetEntries();
  for(int i=0; i<nPts; i++){
    t->GetEntry(i);
    h.SetBinContent(h.FindBin(tes,tidSF),2*(deltaNLL));
  }

  for(int i=0; i<20; i++){
    for(int j=0; j<30; j++){
      if(h.GetBinContent(i+1,j+1)==0) h.SetBinContent(i+1,j+1,h.GetBinContent(i+1,j+2));
    }
  }
  for(int i=0; i<20; i++){
    for(int j=0; j<30; j++){
      if(h.GetBinContent(i+1,j+1)==0) h.SetBinContent(i+1,j+1,h.GetBinContent(i+1,j+2));
    }
  }

  double min = h.GetMinimum();
  for(int i=0; i<20; i++){
    for(int j=0; j<20; j++){
      h.SetBinContent(i+1,j+1,h.GetBinContent(i+1,j+1)-min);
    }
  }

  auto cutg = new TCutG("cutg",8);
  cutg->SetPoint(0, 0.970, 0.82);
  cutg->SetPoint(1, 0.970, 0.90);
  cutg->SetPoint(2, 0.985, 0.99);
  cutg->SetPoint(3, 0.997, 0.99);
  cutg->SetPoint(4, 1.004, 0.93);
  cutg->SetPoint(5, 1.004, 0.84);
  cutg->SetPoint(6, 0.993, 0.77);
  cutg->SetPoint(7, 0.980, 0.77);

  
  TCanvas canv;
  canv.SetRightMargin(1.6);
  h.GetXaxis()->SetNdivisions(505);
  h.GetYaxis()->SetNdivisions(505);
  h.SetMaximum(6);
  h.SetXTitle("energy scale factor");
  h.SetYTitle("ID scale factor");
  h.Draw("surf2 [cutg]");
  canv.SaveAs("./plots_UL2018/2Dscan.pdf");
  
  delete t;
  f.Close();
  
  gApplication->Terminate();
}
