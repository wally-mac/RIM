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
srs_template = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Oregon\Bridge Creek\Lower_Owens\07102019\Agisoft\without_obliques\GIS\inundation.shp"
### path to project folder
project_path = r"C:\Users\karen\Box\Thesis_sites\17070204\lower_owens"
### file locations for RS context inputs and imagery 
context_folder = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context"
image_path = 

## Parameters

### site parameters
site_name = "lower_owens"
huc = '17070204'

### image AP01 metadata
image_date = ""  # use format YYYYMMDD
image_source = "" # e.g. drone, google_earth, NAIP
flow_stage = "" # flow stage at the time of the imagery (e.g. baseflow, low, medium, high)


##############################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template, site_name, huc8)

# gather RS context inputs
gather_RSinputs(context_folder, huc8, project_path, srs_template)

# gather image for DCE1


