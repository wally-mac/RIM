# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from loghelper import Logger
from create_files import create_files


## Inputs
### path to a shapefile with the desired output coordinate system

srs_template = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\08042019\GIS\dam_crests.shp"

### path to project folder

project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\test"

#########################

# create project folders and empty mapping shapefiles
create_files(srs_template=srs_template, project_path=project_path)

