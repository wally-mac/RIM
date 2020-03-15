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

# Set workspace
env.workspace = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites"

# Set local variables
out_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites"
#out_name = "habitatareas.shp"
#geometry_type = "POLYGON"
#template = "study_quads.shp"
has_m = "DISABLED"
has_z = "DISABLED"

# Use Describe to get a SpatialReference object
spatial_reference = arcpy.Describe(r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\inundation.shp").spatialReference

# Execute CreateFeatureclass

# inundation
arcpy.CreateFeatureclass_management(out_path, "inundation.shp", "POLYGON", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\inundation.shp", has_m, has_z, spatial_reference)

# dam crests
arcpy.CreateFeatureclass_management(out_path, "dam_crests.shp", "POLYLINE", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\dam_crests.shp", has_m, has_z, spatial_reference)

# valley bottom
arcpy.CreateFeatureclass_management(out_path, "valley_bottom.shp", "POLYGON", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\valley_bottom.shp", has_m, has_z, spatial_reference)

# valley bottom centerline
arcpy.CreateFeatureclass_management(out_path, "vb_centerline.shp", "POLYLINE", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\vb_centerline.shp", has_m, has_z, spatial_reference)

# thalwegs
arcpy.CreateFeatureclass_management(out_path, "thalwegs.shp", "POLYLINE", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\thalwegs.shp", has_m, has_z, spatial_reference)

# pre beaver inundation
arcpy.CreateFeatureclass_management(out_path, "inundation_pre.shp", "POLYGON", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\inundation_pre.shp", has_m, has_z, spatial_reference)

# valley bottom
arcpy.CreateFeatureclass_management(out_path, "active_channel.shp", "POLYGON", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Franklin_basin\06052019\GIS\valley_bottom.shp", has_m, has_z, spatial_reference)
