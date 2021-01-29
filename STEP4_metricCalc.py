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
project_path = r"C:\Users\A02295870\Documents\RH_Fork_mid_T1"
# name of the folder of the desired RS Context shapefiles (the folder with the Valley Bottom polygon)
RS_folder_name = "RS_01"
# path to DEM to be used to calculate slopes
DEM = os.path.join(project_path, '01_Inputs', '02_Topo', 'DEM_01', 'DEM.tif')

# metadata
mapper = 'Karen Bartelt'

# DCE Parameters
# site parameters
project_name = "RH Fork Mid Test 1"  # readable version of site name
site_name = "RH_fork_mid_T1"  # shorthand version
huc8 = '16010203'
setting = "classic"  # classic, steep, or floodplain

# name of the folder of the desired DCEs for the analysis
DCE1_name = "DCE_01"
DCE2_name = 'DCE_02'

# DCE 1 Parameters
DCE1_date = "201108"
DCE1_image_source = 'drone'
DCE1_date_name = "August 2019"
DCE1_flow_stage = 'moderate'
DCE1_active = 'Yes'
DCE1_maintained = 'No'
DCE1_res = '.02'
# DCE 2 Parameters
DCE2_date = '201108'
DCE2_image_source = 'google earth'
DCE2_date_name = "Undammed"
DCE2_flow_stage = 'moderate'
DCE2_active = 'Yes'
DCE2_maintained = 'Yes'
DCE2_res = '.46'


calculate_metrics(project_path, RS_folder_name, DEM, mapper, project_name, site_name, DCE1_name, DCE1_date, DCE1_image_source, DCE2_image_source, DCE1_date_name, DCE2_date_name, DCE1_flow_stage, DCE1_active, DCE1_maintained, DCE2_name, DCE2_date, DCE2_flow_stage, DCE2_active, DCE2_maintained, DCE1_res, DCE2_res, setting, huc8)
################################
