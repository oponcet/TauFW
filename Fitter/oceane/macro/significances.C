//O.Poncet 08/03/22
//Small macro to compute the significance for different cuts on m_T(muon,MET) = mT_1 
//The best value of the cut (the one that maximize the significance) is printed and the graph of the evolution of the significance is saved in a root file for every channel ( baseline, DM0, DM1, DM10, DM11)
//The data used are genereted by createinputsTES.py and the config file defaultFitSetupTES_mutau_MET.yml


#include <TROOT.h>
#include <TObject.h>
#include <TMath.h>
#include <TString.h>
#include <TFile.h>
#include <TH1.h>
#include <TGraph.h>
#include <TF1.h>
#include <TGraphAsymmErrors.h>

using namespace std;

int significance(Char_t  *channel){

TCanvas *c1 = new TCanvas("Siginificance"+TString(channel) , "Siginificance"+TString(channel), 900, 900);
c1->SetGrid();


//Access to the data 
TFile *f = new TFile("./input/ztt_mt_tes_mt_1.inputs-UL2018-13TeVsignificance.root");
//f->ls();
TDirectory *dir = gFile->GetDirectory(channel);
//dir->ls();

TH1D *histo[10];
Char_t histoNames[10][8] ={"ZTT", "ZL", "ZJ", "W", "VV", "TTT", "TTL", "TTJ", "ST", "QCD"};

//histograms of signal and background
for (int i = 0; i < 10 ; i++)
	{
        histo[i] = (TH1D *)dir->Get(histoNames[i]);
        //cout << "histo name = " << histoNames[i] << " and integral = " << histo[i]->Integral(0,1, "width") << endl;
        //cout << "Bin width = " << histo[i]->GetBinWidth(1) << endl;
	}
//different cuts
int nbcuts = 40; 
TGraph *g = new TGraph(nbcuts);
double signal, background, significance, significancemax, bestcut;
significance = 0;
for (int i = 1; i <= nbcuts ; i++)
	{
	signal = 0;
	background = 0;
	signal = histo[0]->Integral(1,i, "width"); //Signal ZTT
	for (int j = 1; j < 10 ; j++) //calculation of the background 
		{
        	background += histo[j]->Integral(1,i, "width"); //background is the sum of all others channels 
		}
	//cout << "signal= " << signal << " and background = " << background << endl;
	if(significance < signal / sqrt(signal+background)) //find maximum
	{
	significancemax = signal / sqrt(signal+background); 
	bestcut = i*histo[1]->GetBinWidth(1); //best cut that maximize the significance
	}
	significance = signal / sqrt(signal+background); //calculation significance
	//cout << "y = " << i*histo[1]->GetBinWidth(1) <<  " significance = " << significance << endl; //with constant width
  	g->SetPoint(i, i*histo[1]->GetBinWidth(1), significance); 
	}
g->SetTitle("Significance for different cuts on mt_1"+TString(channel));
g->GetXaxis()->SetTitle("Cuts on mt_1 in GeV");
g->GetYaxis()->SetTitle("Significance");
g->SetMarkerStyle(2);
g->Draw("AP");
cout << "maximum signicance = " << significancemax << " and best cut = " << bestcut << " GeV" << endl;

c1->Update();
c1->SaveAs("./significance/significance"+TString(channel)+".root");

return 0;
}

//main function that plot the significance for every channels 
int significances(){
Char_t channel[5][10] ={"baseline", "DM0", "DM1", "DM10", "DM11"};
 
for(int i = 0; i<5; i++)
	{
	significance(channel[i]);
	}

return 0;
}
