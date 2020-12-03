# Description: Create project folders and empty shapefiles for the first Data capture event

import os
import arcpy
import sys
from settings import ModelConfig
import uuid
from lib.project import RSProject, RSLayer
from lib.util import safe_makedirs
from lib.loghelper import Logger
import numpy
import csv
import pandas as pd
import time
import datetime
arcpy.CheckOutExtension('Spatial')

cfg = ModelConfig('http://xml.riverscapes.xyz/Projects/XSD/V1/Inundation.xsd')

# Functions from BAAT


def make_folder(path_to_location, new_folder_name):
    """
    Makes a folder and returns the path to it
    :param path_to_location: Where we want to put the folder
    :param new_folder_name: What the folder will be called
    :return: String
    """
    newFolder = os.path.join(path_to_location, new_folder_name)
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
    return newFolder

# RIM project creation functions


def make_project(project_path, srs_template, image_path, site_name, huc8, BRAT_path, VBET_path, DEM_path, hs_path, image_date, date_name, image_source, flow_stage, image_res, mapper):
    """
    Creates project folders
    :param project_path: where we want project to be located
    """

    LayerTypes = {
        # RSLayer(name, id, tag, rel_path)
        'AP_01': RSLayer(date_name, 'AP_01', 'Raster', '01_Inputs/01_Imagery/AP_01/orthomosaic.png'),
        'DEM': RSLayer('NED 10m DEM', 'DEM', 'DEM', '01_Inputs/02_Topo/DEM_01/DEM.tif'),
        'HILLSHADE': RSLayer('DEM Hillshade', 'HILLSHADE', 'Raster', '01_Inputs/02_Topo/DEM_01/hlsd.tif'),
        'BRAT': RSLayer('BRAT', 'BRAT', 'Vector', '01_Inputs/03_Context/BRAT_01/BRAT.shp'),
        'VBET': RSLayer('VBET', 'VBET', 'Vector', '01_Inputs/03_Context/VBET_01/VBET.shp'),
        'VB': RSLayer('Valley Bottom', 'VB_01', 'Vector', '02_Mapping/RS_01/valley_bottom.shp'),
        'VB_CL': RSLayer('VB Centerline', 'vbCL_01', 'Vector', '02_Mapping/RS_01/vb_centerline.shp'),
        'INUN': RSLayer('Inundation', 'DCE_01_inun', 'Vector', '03_Analysis/DCE_01/Shapefiles/inundation.shp'),
        'DAM_CREST': RSLayer('Dam Crests', 'DCE_01_damcrests', 'Vector', '03_Analysis/DCE_01/Shapefiles/dam_crests.shp'),
        'TWG': RSLayer('Thalwegs', 'DCE_01_thalwegs', 'Vector', '03_Analysis/DCE_01/Shapefiles/thalwegs.shp')
    }

    log = Logger('build_xml')
    log.info('Starting the build of the XML')

    project_name = site_name
    project = RSProject(cfg, project_path.replace('\\', '/'))
    project.create(project_name, 'Inundation')

    # Add the root metadata
    project.add_metadata({
        'ModelVersion': cfg.version,
        'HUC8': huc8,
        'InundationVersion': cfg.version,
        'site_name': site_name
    })

    # Create the inputs container node
    inputs = project.XMLBuilder.add_sub_element(project.XMLBuilder.root, 'Inputs', None, {
        'id': 'inputs'
    })

    # Create the realizations container node
    realizations = project.XMLBuilder.add_sub_element(project.XMLBuilder.root, 'Realizations', None, {
        'id': 'realizations'
    })

    # Create the InundationContext (vb and vb centerline) container node
    RS01_node = project.XMLBuilder.add_sub_element(realizations, 'InundationContext', None, {
        'id': 'RS_01',
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version,
    })

    project.add_metadata({
        'mapper': mapper
    }, RS01_node)
    # Create the InundationDCE container node and metadata
    DCE01_node = project.XMLBuilder.add_sub_element(realizations, 'InundationDCE', None, {
        'Name': date_name,
        'id': 'DCE_01',
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version
    })
    project.add_metadata({
        'image_date': image_date,
        'source': image_source,
        'flow_stage': flow_stage,
        'image_res': image_res,
        'mapper': mapper
    }, DCE01_node)

    # set workspace to desired project location
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = project_path

    if not os.path.exists(project_path):
        os.mkdir(project_path)

    # build project folder structure in project path
    # inputs folders

    log = Logger('create_project')
    log.info('creating project folders...')

    inputs_folder = make_folder(project_path, "01_Inputs")

    image_folder = make_folder(inputs_folder, "01_Imagery")
    AP01_folder = make_folder(image_folder, "AP_01")

    topo_folder = make_folder(inputs_folder, "02_Topo")
    DEM01_folder = make_folder(topo_folder, "DEM_01")

    context_folder = make_folder(inputs_folder, "03_Context")
    BRAT01_folder = make_folder(context_folder, "BRAT_01")
    VBET01_folder = make_folder(context_folder, "VBET_01")
    make_folder(context_folder, 'WBD')

    log.info('copying input files into new project folder...')

    def add_image(image_path, AP_folder):
        # put input imagery in folder
        arcpy.CopyRaster_management(image_path, os.path.join(AP_folder, 'orthomosaic.png'))
    add_image(image_path, AP01_folder)

    # copy DEM, hillshade to project folder
    arcpy.CopyRaster_management(DEM_path, os.path.join(DEM01_folder, 'DEM.tif'))
    arcpy.CopyRaster_management(hs_path, os.path.join(DEM01_folder, 'hlsd.tif'))

    # copy BRAT, VBET to project folder
    arcpy.CopyFeatures_management(BRAT_path, os.path.join(BRAT01_folder, 'BRAT.shp'))
    arcpy.CopyFeatures_management(VBET_path, os.path.join(VBET01_folder, 'VBET.shp'))

    log = Logger('build_xml')
    log.info('adding inputs to xml...')

    # add the input rasters to xml
    project.add_project_raster(inputs, LayerTypes['DEM'])
    project.add_project_raster(inputs, LayerTypes['AP_01'])
    AP01_node = project.XMLBuilder.find_by_id('AP_01')
    project.add_metadata({
        'image_date': image_date,
        'source': image_source,
        'flow_stage': flow_stage,
        'image_res': image_res,
    }, AP01_node)
    project.add_project_raster(inputs, LayerTypes['HILLSHADE'])

    # add the input vectors to xml
    project.add_project_vector(inputs, LayerTypes['BRAT'])
    project.add_project_vector(inputs, LayerTypes['VBET'])

    # mapping folder
    # subsequent DCE and RS folders are created when a new DCE is made using new dce script
    mapping_folder = make_folder(project_path, "02_Mapping")
    DCE01_folder = make_folder(mapping_folder, "DCE_01")

    log = Logger('create_project')
    log.info('creating blank RS and DCE shapefiles...')

    # make empty shapefiles for first DCE
    # Use Describe to get a SpatialReference object
    spatial_reference = arcpy.Describe(srs_template).spatialReference
    # inundation
    if not os.path.exists(os.path.join(DCE01_folder, "inundation.shp")):
        arcpy.CreateFeatureclass_management(DCE01_folder, "inundation.shp", "POLYGON", "", "DISABLED", "DISABLED", spatial_reference)
    # add field for inundation type
        arcpy.AddField_management(os.path.join(DCE01_folder, 'inundation.shp'), 'type', "TEXT")
    # dam crests
    if not os.path.exists(os.path.join(DCE01_folder, "dam_crests.shp")):
        arcpy.CreateFeatureclass_management(DCE01_folder, "dam_crests.shp", "POLYLINE", "", "DISABLED", "DISABLED", spatial_reference)
    # add fields for dam state and crest type
        arcpy.AddField_management(os.path.join(DCE01_folder, 'dam_crests.shp'), 'dam_state', "TEXT")
        arcpy.AddField_management(os.path.join(DCE01_folder, 'dam_crests.shp'), 'crest_type', "TEXT")
        arcpy.AddField_management(os.path.join(DCE01_folder, 'dam_crests.shp'), 'dam_id', "DOUBLE")
    # thalwegs
    if not os.path.exists(os.path.join(DCE01_folder, "thalwegs.shp")):
        arcpy.CreateFeatureclass_management(DCE01_folder, "thalwegs.shp", "POLYLINE", "", "DISABLED", "DISABLED", spatial_reference)
    # add fields for thalweg type
        arcpy.AddField_management(os.path.join(DCE01_folder, 'thalwegs.shp'), 'type', "TEXT")
    # make first RS folder
    RS01_folder = make_folder(mapping_folder, "RS_01")
    # create empty shapefiles for valley bottom and valley bottom centerline
    # valley bottom
    if not os.path.exists(os.path.join(RS01_folder, "valley_bottom.shp")):
        arcpy.CreateFeatureclass_management(RS01_folder, "valley_bottom.shp", "POLYGON", "", "DISABLED", "DISABLED", spatial_reference)
        arcpy.AddField_management(os.path.join(RS01_folder, 'valley_bottom.shp'), 'site_name', "TEXT")
        arcpy.AddField_management(os.path.join(RS01_folder, 'valley_bottom.shp'), 'huc8', "DOUBLE")
        with arcpy.da.UpdateCursor(os.path.join(RS01_folder, 'valley_bottom.shp'), ['site_name', 'huc8']) as cursor:
            for row in cursor:
                row[0] = site_name
                row[1] = huc8
                cursor.updateRow(row)
    # valley bottom centerline
    if not os.path.exists(os.path.join(RS01_folder, "vb_centerline.shp")):
        arcpy.CreateFeatureclass_management(RS01_folder, "vb_centerline.shp", "POLYLINE", "", "DISABLED", "DISABLED", spatial_reference)

    # Add RS01 files to xml
    project.add_project_vector(RS01_node, LayerTypes['VB'])
    project.add_project_vector(RS01_node, LayerTypes['VB_CL'])

    # Add DCE01 files to xml
    project.add_project_vector(DCE01_node, LayerTypes['INUN'])
    project.add_project_vector(DCE01_node, LayerTypes['DAM_CREST'])
    project.add_project_vector(DCE01_node, LayerTypes['TWG'])

    # analysis folder
    analysis_folder = make_folder(project_path, "03_Analysis")
    DCEout = make_folder(analysis_folder, "DCE_01")
    make_folder(DCEout, "Shapefiles")
    make_folder(analysis_folder, "CDs")
    make_folder(analysis_folder, "Summary")

    # Finally write the file
    log.info('Writing file')
    project.XMLBuilder.write()
    log.info('Done')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('srs_template', help='path to a shapefile with desired output coordinate system', type=str)
    parser.add_argument('project_path', help='path to output folder', type=str)
    args = parser.parse_args()
