# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from lib.loghelper import Logger
from create_DCE import new_DCE


#########################

# Inputs

# path to a shapefile with the desired output coordinate system
srs_template = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\TempleFork\temple_b\10262019\GIS\inundation.shp"
# path to project folder
project_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid"
# name for new image folder (if you are not adding an image, put "None")
AP_fold = 'AP_02'
image_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid\Imagery\googleEarth_Aug2011_2.jpg"
# name for new DCE folder (this should be DCE_XX, where XX = the number of the DCE  you are on)
DCE_fold = 'DCE_02'

# image and DCE 01 metadata
image_date = "201108"  # use format YYYYMMDD
date_name = "August 2011"  # what you want the display name for the image to be
image_source = "google_earth"  # e.g. drone, google_earth, NAIP
flow_stage = "low"  # flow stage at the time of the imagery (e.g. baseflow, low, medium, high)
image_res = '.2'  # resolution of the imagery in meters
mapper = 'Karen Bartelt'

#########################
# create new DCE

new_DCE(srs_template, project_path, AP_fold, DCE_fold, image_path, image_date, date_name, image_source, flow_stage, image_res, mapper)
