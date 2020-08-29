# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:04:43 2020

@author: karen
"""

# Name: new_DCE.py
# Description: Create shapefiles for inundation work

# Import system modules
import os
import arcpy
import sys
from settings import ModelConfig
import uuid
from lib.project import RSProject, RSLayer
from lib.util import safe_makedirs
from lib.loghelper import Logger
import time
import datetime

cfg = ModelConfig('http://xml.riverscapes.xyz/Projects/XSD/V1/Inundation.xsd')

# function for create files


def new_DCE(srs_template, project_path, AP_fold, DCE_fold, image_path, image_date, date_name, image_source, flow_stage, image_res, mapper):

    LayerTypes = {
        # RSLayer(name, id, tag, rel_path)
        'AP_new': RSLayer(date_name, AP_fold, 'Raster', os.path.join('01_Inputs/01_Imagery', AP_fold, 'imagery.tif')),
        'INUN_new': RSLayer('Inundation', 'DCE_01_inun', 'Vector', os.path.join('03_Analysis', DCE_fold, 'Shapefiles/inundation.shp')),
        'DAM_CREST_new': RSLayer('Dam Crests', 'DCE_01_damcrests', 'Vector', os.path.join('03_Analysis', DCE_fold, 'Shapefiles/dam_crests.shp')),
        'TWG_new': RSLayer('Thalwegs', 'DCE_01_thalwegs', 'Vector', os.path.join('03_Analysis', DCE_fold, 'Shapefiles/thalwegs.shp'))
    }

    log = Logger('edit_xml')
    log.info('Loading the XML to make edits...')
    # Load up a new RSProject class
    project = RSProject(cfg, project_path)

    log = Logger('new_DCE')

    # Set local variables
    has_m = "DISABLED"
    has_z = "DISABLED"

    log.info('before getting spatial reference')
    # Use Describe to get a SpatialReference object
    spatial_reference = arcpy.Describe(srs_template).spatialReference

    log.info('checking if project folders exist')
    # check if Inputs, Mapping, and Analysis folders exist, if not create them
    folder_list = ['01_Inputs', '02_Mapping', '03_Analysis']
    for folder in folder_list:
        if not os.path.exists(os.path.join(project_path, folder)):
            os.makedirs(os.path.join(project_path, folder))

    log.info('Inputs, Mapping, Analysis folders exist')

    # set pathway to imagery folder
    image_folder = os.path.join(project_path, '01_Inputs/01_Imagery')

    # create new AP folder
    if not os.path.exists(os.path.join(image_folder, AP_fold)):
        os.makedirs(os.path.join(image_folder, AP_fold))
        AP_path = os.path.join(image_folder, AP_fold)
    else:
        AP_path = os.path.join(image_folder, AP_fold)

    log.info('copying image to project folder...')

    def add_image(image_path, AP_folder):
        # put input imagery in folder
        if not os.path.exists(os.path.join(AP_folder, 'imagery.tif')):
            arcpy.CopyRaster_management(image_path, os.path.join(AP_folder, 'imagery.tif'))
        else:
            print("existing image already exists in this AP folder")
    add_image(image_path, AP_path)

    # Add new AP to xml
    inputs = project.XMLBuilder.find_by_id('inputs')
    project.add_project_raster(inputs, LayerTypes['AP_new'])
    # add new AP metadata
    APnew_node = project.XMLBuilder.find_by_id(AP_fold)
    project.add_metadata({
        'image_date': image_date,
        'source': image_source,
        'flow_stage': flow_stage,
        'image_res': image_res,
    }, APnew_node)

    # set pathway to mapping folder
    map_path = os.path.join(project_path, '02_Mapping')

    #  check if RS folder exists, if not make one
    if not os.path.exists(os.path.join(map_path, 'RS_01')):
        os.makedirs(os.path.join(map_path, 'RS_01'))

    # create new DCE folder
    if not os.path.exists(os.path.join(map_path, DCE_fold)):
        log.info('creating new DCE shapefiles...')
        os.makedirs(os.path.join(map_path, DCE_fold))

        # inundation
        arcpy.CreateFeatureclass_management(os.path.join(map_path, DCE_fold), "inundation.shp", "POLYGON", "", has_m, has_z, spatial_reference)
        # add field for inundation type
        arcpy.AddField_management(os.path.join(map_path, DCE_fold, 'inundation.shp'), 'type', "TEXT")

        # dam crests
        arcpy.CreateFeatureclass_management(os.path.join(map_path, DCE_fold), "dam_crests.shp", "POLYLINE", "", has_m, has_z, spatial_reference)
        # add fields for dam state and crest type
        arcpy.AddField_management(os.path.join(map_path, DCE_fold, 'dam_crests.shp'), 'dam_state', "TEXT")
        arcpy.AddField_management(os.path.join(map_path, DCE_fold, 'dam_crests.shp'), 'crest_type', "TEXT")
        arcpy.AddField_management(os.path.join(map_path, DCE_fold, 'dam_crests.shp'), 'dam_id', "DOUBLE")

        # thalwegs
        arcpy.CreateFeatureclass_management(os.path.join(map_path, DCE_fold), "thalwegs.shp", "POLYLINE", "", has_m, has_z, spatial_reference)

    else:
        print("this DCE already exists")
    log.info('updating xml with new DCE...')

    # Add new AP to xml
    realizations = project.XMLBuilder.find_by_id('realizations')
    # Create the InundationDCE container node and metadata
    DCEnew_node = project.XMLBuilder.add_sub_element(realizations, 'InundationDCE', None, {
        'id': DCE_fold,
        'Name': date_name,
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version
    })
    project.add_metadata({
        'image_date': image_date,
        'source': image_source,
        'flow_stage': flow_stage,
        'image_res': image_res,
        'mapper': mapper,
        'rs_used': "RS_01"
    }, DCEnew_node)

    # Add DCE01 files to xml
    project.add_project_vector(DCEnew_node, LayerTypes['INUN_new'])
    project.add_project_vector(DCEnew_node, LayerTypes['DAM_CREST_new'])
    project.add_project_vector(DCEnew_node, LayerTypes['TWG_new'])

    # create a folder in Analysis for this DCE
    analysis_path = os.path.join(project_path, '03_Analysis')
    if not os.path.exists(os.path.join(analysis_path, DCE_fold)):
        os.makedirs(os.path.join(analysis_path, DCE_fold))
        DCEout = os.path.join(analysis_path, DCE_fold)
        if not os.path.exists(os.path.join(DCEout, 'shapefiles')):
            os.makedirs(os.path.join(DCEout, 'Shapefiles'))

    log.info('Writing file')
    project.XMLBuilder.write()
    log.info('Done')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('srs_template', help='path to a shapefile with desired output coordinate system', type=str)
    parser.add_argument('project_path', help='path to output folder', type=str)
    args = parser.parse_args()
