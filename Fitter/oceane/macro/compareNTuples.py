import ROOT

# Set batch mode to True
ROOT.gROOT.SetBatch(True)

# Open the ROOT files
file_tc = ROOT.TFile("/afs/cern.ch/work/d/dwinterb/public/TauFW_sync/UL_sync_2018/SYNCFILE_DYJetsToLL-LO_mt_2018.root")
file_tree = ROOT.TFile("/eos/user/s/smonig/TauPOG/DeepTauv2p5_SFchecks/analysis/UL2018_v10/DY/DYJetsToLL_M-50_mutau.root")

# Get the trees
tree_tc = file_tc.Get("TauCheck")
tree_tree = file_tree.Get("tree")

# Create histograms for each branch in each tree
for tree in [tree_tc, tree_tree]:
    branch_list = tree.GetListOfBranches()
    for branch in branch_list:
        branch_name = branch.GetName()
        if branch_name in tree_tc.GetListOfBranches() and branch_name in tree_tree.GetListOfBranches():
            canvas = ROOT.TCanvas("canvas_" + branch_name, "canvas_" + branch_name, 800, 600)
            hist_tc = ROOT.TH1F("hist_tc_" + branch_name, "TauCheck", 100, 0, 100)
            hist_tree = ROOT.TH1F("hist_tree_" + branch_name, "1tree", 100, 0, 100)
            tree_tc.Draw(branch_name + ">>hist_tc_" + branch_name, "", "goff")
            tree_tree.Draw(branch_name + ">>hist_tree_" + branch_name, "", "goff")
            # Compare the integrals of the two histograms
            if abs(hist_tc.Integral() - hist_tree.Integral()) > 1e-5:
                print("Integral values differ for branch:", branch_name)
                print(abs(hist_tc.Integral() - hist_tree.Integral()))
            xmax = hist_tc.GetMaximumBin()
            # print("xmax = %d" %xmax)
            nbin = xmax
            if xmax<10:
                xmax
                nbin = xmax*10
            hist_tc.SetBins(nbin, 0, xmax)
            hist_tree.SetBins(nbin, 0, xmax)
            hist_tc.SetLineColor(ROOT.kRed)
            hist_tree.SetLineColor(ROOT.kBlue)
            hist_tc.Draw()
            hist_tree.Draw("same")
            # Create a TFile to save the histograms and canvases
            output_file = ROOT.TFile("output/compareNTuples/compareNTuples_"+ branch_name +".root", "RECREATE")
            canvas.Write()
            hist_tc.Write()
            hist_tree.Write()
            canvas.Clear()
            del hist_tc
            del hist_tree
            # Close the output file
            output_file.Close()
        else:
            print("%s branch is not in both TTree" %branch_name)



