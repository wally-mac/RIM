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


# define inputs to the create_files function
# path to a shapefile with the desired output coordinate system
#srs_template = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\08042019\GIS\dam_crests.shp"
# path to project folder
#project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\test"

#function for create files
def create_files(srs_template, project_path):

    # Set local variables
    has_m = "DISABLED"
    has_z = "DISABLED"

    # Use Describe to get a SpatialReference object
    spatial_reference = arcpy.Describe(srs_template).spatialReference

    #check if Inputs, Mapping, and Analysis folders exist, if not create them
    folder_list = ['01_Inputs', '02_Mapping', '03_Analysis']
    for folder in folder_list:
        if not os.path.exists(os.path.join(project_path, folder)):
            os.makedirs(os.path.join(project_path, folder))
    
    # set pathway to mapping folder
    map_path = os.path.join(project_path, '02_Mapping')

    #  check if RS folder exists, if not make one
    if not os.path.exists(os.path.join(map_path, 'RS_01')):
        os.makedirs(os.path.join(map_path, 'RS_01'))

    #create new DCE folder
    if not os.path.exists(os.path.join(map_path, 'DCE_01')):
        os.makedirs(os.path.join(map_path, 'DCE_01')) 

    # inundation
    arcpy.CreateFeatureclass_management(os.path.join(map_path, 'DCE_01'), "inundation.shp", "POLYGON", "",has_m, has_z, spatial_reference)
    #add field for inundation type
    arcpy.AddField_management(os.path.join(map_path, 'DCE_01', 'inundation.shp'), type, "TEXT")

    # dam crests
    arcpy.CreateFeatureclass_management(os.path.join(map_path, 'DCE_01'), "dam_crests.shp", "POLYLINE", "", has_m, has_z, spatial_reference)
    #add fields for dam state and crest type
    arcpy.AddField_management(os.path.join(map_path, 'DCE_01', 'dam_crests.shp'), 'dam_state', "TEXT")
    arcpy.AddField_management(os.path.join(map_path, 'DCE_01', 'dam_crests.shp'), 'crest_type', "TEXT")

    # valley bottom
    arcpy.CreateFeatureclass_management(os.path.join(map_path, 'RS_01'), "valley_bottom.shp", "POLYGON", "", has_m, has_z, spatial_reference)

    # valley bottom centerline
    arcpy.CreateFeatureclass_management(os.path.join(map_path, 'RS_01'), "vb_centerline.shp", "POLYLINE", "", has_m, has_z, spatial_reference)

    # thalwegs
    arcpy.CreateFeatureclass_management(os.path.join(map_path, 'DCE_01'), "thalwegs.shp", "POLYLINE", "", has_m, has_z, spatial_reference)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('srs_template', help='path to a shapefile with desired output coordinate system', type=str)
    parser.add_argument('project_path', help='path to output folder', type=str)
    args = parser.parse_args()

    create_files(args.srs_template, args.project_path)

#create_files(srs_template, project_path)