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

#########################

## Inputs

### path to a shapefile with the desired output coordinate system
srs_template = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Oregon\Bridge Creek\Lower_Owens\07102019\Agisoft\without_obliques\GIS\inundation.shp"
### path to project folder
project_path = r"C:\Users\karen\Box\Thesis_sites\17070204\lower_owens"
### name for new DCE folder
DCE_fold = 'DCE_02'

#########################
# create new DCE

new_DCE(srs_template, project_path, DCE_fold)

