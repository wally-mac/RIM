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
project_path = r"C:\Users\A02295870\Documents\RH_Fork_mid_T1"
srs_template = r"C:\Users\A02295870\Downloads\RH_fork_mid_full\02_Mapping\DCE_01\inundation.shp"
# name for new image folder (if you are not adding an image, put "None")
AP_fold = 'AP_02'
image_path = r"C:\Users\A02295870\Downloads\RH_fork_mid_full\01_Inputs\01_Imagery\AP_02\imagery.tif"
# name for new DCE folder (this should be DCE_XX, where XX = the number of the DCE  you are on)
DCE_fold = 'DCE_02'

#########################
# create new DCE

new_DCE(srs_template, project_path, AP_fold, DCE_fold, image_path)
