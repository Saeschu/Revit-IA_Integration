#! python3

import ifcopenshell
import ifctester
from ifctester import ids, reporter

# open  IDS file:
ids = ifctester.open("C:\\Users\\Sascha Hostettler\\OneDrive - FHNW\\FHNW_Msc_VDC\\_MSc_Thesis_IDS\\04_Data\\SampleData\\PoC-Sampels\\IDS_SampleFM_Space_01.xml", validate=True)

Inputparameter = ids.specifications[0].name


def print_test(Inputparameter):
    output = str(Inputparameter)
    print(output)
    return(output)

print_test(Inputparameter)