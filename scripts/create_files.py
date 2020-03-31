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


# define folder with template shapefiles and output folder
template_folder(r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS")
out_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites"

# Set local variables
has_m = "DISABLED"
has_z = "DISABLED"



# Use Describe to get a SpatialReference object
spatial_reference = arcpy.Describe(inundation_template).spatialReference

# Execute CreateFeatureclass

# inundation
arcpy.CreateFeatureclass_management(out_path, "inundation.shp", "POLYGON", inundation_template, has_m, has_z, spatial_reference)

# dam crests
arcpy.CreateFeatureclass_management(out_path, "dam_crests.shp", "POLYLINE", dam_crests_template, has_m, has_z, spatial_reference)

# valley bottom
arcpy.CreateFeatureclass_management(out_path, "valley_bottom.shp", "POLYGON", valleybottom_template, has_m, has_z, spatial_reference)

# valley bottom centerline
arcpy.CreateFeatureclass_management(out_path, "vb_centerline.shp", "POLYLINE", vbcenterline_template, has_m, has_z, spatial_reference)

# thalwegs
arcpy.CreateFeatureclass_management(out_path, "thalwegs.shp", "POLYLINE", thalwegs_template, has_m, has_z, spatial_reference)

# pre beaver inundation
arcpy.CreateFeatureclass_management(out_path, "inundation_pre.shp", "POLYGON", inundation_template, has_m, has_z, spatial_reference)

# valley bottom
arcpy.CreateFeatureclass_management(out_path, "active_channel.shp", "POLYGON", valleybottom_template, has_m, has_z, spatial_reference)
