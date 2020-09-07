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
srs_template = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Snake_headwaters\BRAT\BatchRun_03\Outputs\Output_01\02_Analyses\Combined_Capacity_Model.shp"
project_path = r"C:\Users\A02295870\Box\Thesis_sites\17040101\pacific_creek_b"
# name for new image folder (if you are not adding an image, put "None")
AP_fold = 'AP_02'
image_path = r"C:\Users\A02295870\Box\Thesis_sites\17040101\pacific_creek_b\imagery\google_earth_06292014.jpg"
# name for new DCE folder (this should be DCE_XX, where XX = the number of the DCE  you are on)
DCE_fold = 'DCE_02'

# image and DCE 01 metadata
image_date = "20140629"  # use format YYYYMMDD
date_name = "Estimated Pre Beaver"  # what you want the display name for the image to be
image_source = "google_earth"  # e.g. drone, google_earth, NAIP
flow_stage = "high"  # flow stage at the time of the imagery (e.g. baseflow, low, medium, high)
image_res = '.27'  # resolution of the imagery in meters
mapper = 'Karen Bartelt'

#########################
# create new DCE

new_DCE(srs_template, project_path, AP_fold, DCE_fold, image_path, image_date, date_name, image_source, flow_stage, image_res, mapper)
