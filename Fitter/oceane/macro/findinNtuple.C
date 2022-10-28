#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TLeaf.h>
#include <TMath.h>
#include <iostream>


int findinNtuple(){


    //const char* inputFile = "/eos/user/o/oponcet/TauPOG/analysis/UL2018v10/TT/TTTo2L2Nu_mutau.root";
    //const char* inputFile = "/eos/user/o/oponcet/TauPOG/analysis/UL2018v10/TT/TTToHadronic_mutau.root";
    const char* inputFile = "/eos/user/o/oponcet/TauPOG/analysis/UL2018v10/TT/TTToSemiLeptonic_mutau.root";

    // 
    TFile *f = new TFile(inputFile, "r");
    //f->ls();
    TTree *t=(TTree *)f->Get("tree");
    //t->Print();

    t->SetBranchStatus("*",0);

    for(int i = 1; i<118; i++){
        const char* branchName = t->GetListOfBranches()->At(i)->GetName();

        Float_t variable; 

        TString type = t->GetLeaf(branchName)->GetTypeName();
        std::cout << type << std::endl;

        if (type=="Flaot_t")
        {
            t->SetBranchStatus(branchName,1);
            t->SetBranchAddress(branchName,&variable);
            Int_t nEvts = t->GetEntries();
            for(int i=0; i<nEvts; i++){
                t->GetEntry(i);
                if(TMath::IsNaN(variable)){
                    std::cout << variable << " " << i <<  std::endl;
                }
            }
        
    }
    }




    

    // const char* branchName = t->GetListOfBranches()->At(1)->GetName();
    // // TBranch* b = t->GetBranch(branchName);

    // int nbval = b->GetEntries();
    // cout << "nval = " << nbval << endl;
    //cout << branchName << endl;

    //t->FindLeaf(branchName)->Print();

    // double val = t->FindLeaf(branchName)->GetValue(2);
    // std::cout << val << " " << 2 << std::endl;

    // for (int i = 1034000; i < 1035000; i++)
    // {
    //     double val = t->FindLeaf(branchName)->GetValue(i);
    //     cout << val<< " " << i << endl;
    //     if(TMath::IsNaN(val)){
    //         cout << val<< " " << i << endl;
    //     }
        
    // }
    

    return 0;
}