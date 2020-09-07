# Import system modules

from calculate_metrics import calculate_metrics
import arcpy
from arcpy import env
import os
import argparse
from create_project import make_folder
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')

################################
# Step 3 - CALCULATE METRICS

# Inputs

# project path
project_path = r"C:\Users\A02295870\Box\Thesis_sites\17040101\pacific_creek_b"
# name of the folder of the desired RS Context shapefiles (the folder with the Valley Bottom polygon)
RS_folder_name = "RS_01"
# path to DEM to be used to calculate slopes
DEM = os.path.join(project_path, '01_Inputs', '02_Topo', 'DEM_01', 'DEM.tif')

# DCE Parameters
# site parameters
site_name = "pacific_creek_b"
huc8 = ""
# name of the folder of the desired DCEs for the analysis
DCE1_name = "DCE_01"
DCE2_name = 'DCE_02'
# DCE 1 Parameters
DCE1_date = "20140701"
DCE1_flow_stage = 'low'
DCE1_active = 'NA'
DCE1_maintained = 'NA'
DCE1_res = '.28'
# DCE 2 Parameters
DCE2_date = 'estimated_pre'
DCE2_flow_stage = 'high'
DCE2_active = 'NA'
DCE2_maintained = 'NA'
DCE2_res = '.27'

setting = ""  # classic, steep, or floodplain

calculate_metrics(project_path, RS_folder_name, DEM, site_name, DCE1_name, DCE1_date, DCE1_flow_stage, DCE1_active, DCE1_maintained, DCE2_name, DCE2_date, DCE2_flow_stage, DCE2_active, DCE2_maintained, DCE1_res, DCE2_res, setting, huc8)
################################
