# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:04:43 2020

@author: karen
"""

# Name: create_files.py
# Description: Create shapefiles for inundation work

# Import system modules
import arcpy
from arcpy import env
import os
import argparse


# define folder with a template file in the desired coordinate system and output folder
srs_template = 
out_path = 

# Set local variables
has_m = "DISABLED"
has_z = "DISABLED"



# Use Describe to get a SpatialReference object
spatial_reference = arcpy.Describe(srs_template).spatialReference

# Execute CreateFeatureclass

# inundation
arcpy.CreateFeatureclass_management(out_path, "inundation.shp", "POLYGON", "",has_m, has_z, spatial_reference)
#add field for inundation type
arcpy.management.AddFields(os.path.join(out_path, 'inundation.shp'), ['type', 'TEXT'])

# dam crests
arcpy.CreateFeatureclass_management(out_path, "dam_crests.shp", "POLYLINE", "", has_m, has_z, spatial_reference)
#add fields for dam state and crest type
arcpy.management.AddFields(os.path.join(out_path, 'inundation.shp'), [['dam_state', 'TEXT'], ['crest_type', 'TEXT"]])

# valley bottom
arcpy.CreateFeatureclass_management(out_path, "valley_bottom.shp", "POLYGON", "", has_m, has_z, spatial_reference)

# valley bottom centerline
arcpy.CreateFeatureclass_management(out_path, "vb_centerline.shp", "POLYLINE", "", has_m, has_z, spatial_reference)

# thalwegs
arcpy.CreateFeatureclass_management(out_path, "thalwegs.shp", "POLYLINE", "", has_m, has_z, spatial_reference)
