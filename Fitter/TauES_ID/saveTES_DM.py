import ROOT

def create_root_file(input_file, output_file):
    # Create a TH1F histogram to store the TES values
    hist = ROOT.TH1F("tes_values", "TES Values", 12, -0.5, 11.5)
    hist.GetXaxis().SetBinLabel(1, "DM0")
    hist.GetXaxis().SetBinLabel(2, "DM1")
    hist.GetXaxis().SetBinLabel(11, "DM10")
    hist.GetXaxis().SetBinLabel(12, "DM11")

    # Read data from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line
        for line in lines:
            # Split the line into columns
            columns = line.split()

            # Extract values
            dm_value = columns[0]
            tes_value = float(columns[1])
            error_low_value = float(columns[2])
            error_high_value = float(columns[3])

            # Fill the histogram with the TES value
            if dm_value == "DM0":
                hist.SetBinContent(1, tes_value)
                hist.SetBinError(1, error_high_value)
            elif dm_value == "DM1":
                hist.SetBinContent(2, tes_value)
                hist.SetBinError(2, error_high_value)
            elif dm_value == "DM10":
                hist.SetBinContent(11, tes_value)
                hist.SetBinError(11, error_high_value)
            elif dm_value == "DM11":
                hist.SetBinContent(12, tes_value)
                hist.SetBinError(12, error_high_value)

    # Save the histogram to the output ROOT file
    output_root = ROOT.TFile(output_file, "RECREATE")
    hist.Write()
    output_root.Close()


# Usage example
input_file_path = "plots_UL2018_v10/_mutau_mt65_DM_Dt2p5_binningv2/measurement_poi_mt_mutau_mt65_DM_Dt2p5_binningv2_DeepTau_fit_asymm.txt"
output_file_path = "plots_UL2018_v10/_mutau_mt65_DM_Dt2p5_binningv2/TES_mutau_mt65_DM_Dt2p5_binningv2.root"
create_root_file(input_file_path, output_file_path)
