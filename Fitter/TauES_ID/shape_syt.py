
"""
Date : December 2023
Author : @oponcet
Description: Calculate Postfit Values for Shape Systematics.

Function:
calculate_shape_syst()
- Calculates postfit values for shape systematics parameters based on a specified variation.
- Reads parameter values from a text file and calculates the postfit values.
- Prints the postfit values for each relevant parameter.

Parameters:
- None (parameters are predefined within the function).
"""
import re
import yaml

def calculate_shape_syst():

    year = "UL2018_v10"
    tag= "_mutau_mt65_DM_Dt2p5"
    
    
    for region in ["DM0", "DM1", "DM10", "DM11"]:
    #for region in ["DM0_pt1","DM0_pt2", "DM0_pt3", "DM0_pt4", "DM1_pt1","DM1_pt2" ,"DM1_pt3", "DM1_pt4", "DM10_pt1","DM10_pt2","DM10_pt3", "DM10_pt4","DM11_pt1","DM11_pt2","DM11_pt3", "DM11_pt4"]:
        param_postfit_ltf = 1
        param_postfit_jtf = 1
        param_postfit_tes = 1

        with open('./postfit_%s/FitparameterValues_%s_DeepTau_%s-13TeV_%s.txt' % (year,tag, year,region), 'r') as txt_file:
            txt_data = txt_file.readlines()
        for line in txt_data:
            match = re.match(r'(\w+)\s*:\s*([\d.-]+)', line)
            param_name_txt = match.group(1)
            if "tes" in param_name_txt:
                param_postfit_tes = float(match.group(2))

            if "shape" in param_name_txt:
                param_value = float(match.group(2))
                #print("Parameter : %s with value : %s"  %(param_name_txt,param_value))  
                # Replace regions according to mapping
                if "shape_mTauFake" in param_name_txt:
                    var = 0.03
                    param_postfit_ltf = 1 + (var * param_value)
                elif "shape_jTauFake":
                    var = 0.1
                    param_postfit_jtf = 1 + (var * param_value)
                else :
                    var = 1 
                    print("not found")


                # if "shape_mTauFake" in param_name_txt:
                #     print( " \"mutau_LTF%s\": \"Run3_DEV.puppiMET.ModuleMuTau ltf=%s\" "  %(formatted_param,param_postfit))  
                # elif "shape_jTauFake":
                #     print( " \"mutau_JTF%s\": \"Run3_DEV.puppiMET.ModuleMuTau jtf=%s\" "  %(formatted_param,param_postfit))  

        #print( " \"mutau_%s_postEE\": \"Run3_DEV.puppiMET.ModuleMuTau ltf=%s tes=%s jtf=%s\" "  %(region,param_postfit_ltf,param_postfit_tes,param_postfit_jtf))  
        #print(" \"mutau_%s_postEE\": \"Run3_DEV.puppiMET.ModuleMuTau ltf=%.3f tes=%.3f jtf=%.3f\", " % (region, param_postfit_ltf, param_postfit_tes, param_postfit_jtf))
        print(" \"mutau_%s_preEE\": \"Run3_DEV.puppiMET.ModuleMuTau ltf=%.3f tes=%.3f jtf=%.3f\", " % (region, param_postfit_ltf, param_postfit_tes, param_postfit_jtf))

                #print("Parameter : %s with posfit value : %s"  %(param_name_txt,param_postfit))  


calculate_shape_syst()