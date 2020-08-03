# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from loghelper import Logger
from create_DCE import new_DCE
from create_project import make_project
from create_project import make_folder
from organize_inputs import gather_RSinputs

##############################
# STEP 1 - CREATE PROJECT

## Inputs

### path to a shapefile with the desired output coordinate system
srs_template = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\TempleFork\temple_b\10262019\GIS\inundation.shp"
### path to project folder
project_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\temple_upper"
### file locations for RS context inputs and imagery 
image_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\temple_upper\DroneDeploy\06202020\projected\orthomosaic.tif"
BRAT_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\BRAT\BRAT\BatchRun_03\Outputs\Output_01\02_Analyses\Combined_Capacity_Model.shp"
VBET_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\VBET\BatchRun_01\02_Analyses\Output_1\Provisional_ValleyBottom_Unedited.shp"
DEM_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\topography\dem.tif"
hs_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\topography\dem_hillshade.tif"

## Parameters

### site parameters
site_name = "lower_owens"
huc = '16010203'

### image AP01 metadata
image_date = "20200620"  # use format YYYYMMDD
image_source = "drone" # e.g. drone, google_earth, NAIP
flow_stage = "moderate" # flow stage at the time of the imagery (e.g. baseflow, low, medium, high)
image_res = '.02' # resolution of the imagery in meters

##############################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template, image_path, site_name, huc, BRAT_path, VBET_path, DEM_path, hs_path)

# gather RS context inputs
#gather_RSinputs(context_folder, huc8, project_path, srs_template)

# gather image for DCE1


