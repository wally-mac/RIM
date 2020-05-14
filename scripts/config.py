# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from loghelper import Logger
from create_DCE import new_DCE
from create_project import make_project
from create_project import make_folder


## Inputs
### path to a shapefile with the desired output coordinate system

srs_template = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\08042019\GIS\dam_crests.shp"

### path to project folder

project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\rock_creek_b\rock_creek_b"

#########################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template)

# create new DCE
new_DCE(srs_template=srs_template, project_path=project_path)

