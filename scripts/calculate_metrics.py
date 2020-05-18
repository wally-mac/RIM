
# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from loghelper import Logger
from create_project import make_folder

# Set project path
project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\rock_creek_b\rock_creek_b"

# Input the name of the folder of the desired RS Context shapefiles (the folder with the Valley Bottom polygon)
RS_folder_name = "RS_01"

# Input the name of the folder of the desired DCEs for the analysis
DCE1_name = "DCE_01"
DCE2_name = "DCE_02"

########

log = Logger('set paths')

# Set internal paths
map_folder = os.path.join(project_path, '02_Mapping')
RS_folder = os.path.join(map_folder, RS_folder_name)
DCE1 = os.path.join(map_folder, DCE1_name)
DCE1 = os.path.join(map_folder, DCE1_name)

log.info('paths set for DCEs of interest')









