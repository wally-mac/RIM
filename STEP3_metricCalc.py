# Import system modules
from arcpy.sa import *
import arcpy
from arcpy import env
import os
import argparse
import numpy
import csv
import pandas as pd
from loghelper import Logger
from create_project import make_folder
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')

################################
# Step 3 - CALCULATE METRICS

# Inputs

# project path
project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\codetest_0622"
# name of the folder of the desired RS Context shapefiles (the folder with the Valley Bottom polygon)
RS_folder_name = "RS_01"
# path to DEM to be used to calculate slopes
DEM = os.path.join(project_path, '01_Inputs', '02_Topo', 'DEM_01', 'DEM.tif')

# DCE Parameters
# site parameters
site_name = "mill_creek"

# name of the folder of the desired DCEs for the analysis
DCE1_name = "DCE_01"
DCE2_name = "DCE_02"
# DCE 1 Parameters
DCE1_date = '20190804'
DCE1_flow_stage = 'low'
DCE1_active = 'yes'
DCE1_maintained = 'yes'
# DCE 2 Parameters
DCE2_date = 'pre beaver'
DCE2_flow_stage = 'low'
DCE2_active = 'NA'
DCE2_maintained = 'NA'

################################
