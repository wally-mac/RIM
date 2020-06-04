# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from loghelper import Logger
from create_DCE import new_DCE
from create_project import make_project
from create_project import make_folder
from project_rasters import project_rasters


## Inputs
### path to a shapefile with the desired output coordinate system

srs_template = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\08042019\GIS\dam_crests.shp"

### path to Drone Deploy rasters that need to be reprojected

# path to folder with unprojected rasters
in_folder = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid\DroneDeploy\05292019"

# create folder for projected outputs
out_folder = make_folder(in_folder, 'Projected')

### path to project folder

project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\rock_creek_b\rock_creek_b"

### name for new DCE folder

DCE_fold = 'DCE_02'

#########################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template)

# create new DCE

new_DCE(srs_template, project_path, DCE_fold)

