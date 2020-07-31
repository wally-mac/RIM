# Description: Create project folders and empty shapefiles for the first Data capture event

import os
import arcpy
import sys
from settings import ModelConfig

cfg = ModelConfig('http://xml.riverscapes.xyz/Projects/XSD/V1/RSContext.xsd')
# Functions from BRAAT
# Make folder function from supportingFunctions.py
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

# RIM projecy creation functions
def make_project(project_path, srs_template, image_path, site_name, huc8):
    """
    Creates project folders
    :param project_path: where we want project to be located
    """

    # set workspace to desired project location
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = project_path

    if not os.path.exists(project_path):
        os.mkdir(project_path)

    # build project folder structure in project path
    # inputs folders
    inputs_folder = make_folder(project_path, "01_Inputs")

    image_folder = make_folder(inputs_folder, "01_Imagery")
    AP01_folder = make_folder(image_folder, "AP_01")
    make_folder(image_folder, "AP_02")
    make_folder(image_folder, "AP_03")

    topo_folder = make_folder(inputs_folder, "02_Topo")
    make_folder(topo_folder, "DEM_01")

    context_folder = make_folder(inputs_folder, "03_Context")
    make_folder(context_folder, "BRAT_01")
    make_folder(context_folder, "VBET_01")
    make_folder(context_folder, 'WBD')

    def add_image(image_path, AP_folder):
        # put input imagery in folder
        arcpy.CopyRaster_management(image_path, os.path.join(AP_folder, 'orthomosaic.tif'))
    add_image(image_path, AP01_folder)


    # mapping folder
    # subsequent DCE and RS folders are created when a new DCE is made using new dce script
    mapping_folder = make_folder(project_path, "02_Mapping")
    DCE01_folder =  make_folder(mapping_folder, "DCE_01")
    # make empty shapefiles for first DCE
    # Use Describe to get a SpatialReference object
    spatial_reference = arcpy.Describe(srs_template).spatialReference
    # inundation
    arcpy.CreateFeatureclass_management(DCE01_folder, "inundation.shp", "POLYGON", "", "DISABLED", "DISABLED", spatial_reference)
    #add field for inundation type
    arcpy.AddField_management(os.path.join(DCE01_folder, 'inundation.shp'), 'type', "TEXT")
    # dam crests
    arcpy.CreateFeatureclass_management(DCE01_folder, "dam_crests.shp", "POLYLINE", "", "DISABLED", "DISABLED", spatial_reference)
    #add fields for dam state and crest type
    arcpy.AddField_management(os.path.join(DCE01_folder, 'dam_crests.shp'), 'dam_state', "TEXT")
    arcpy.AddField_management(os.path.join(DCE01_folder, 'dam_crests.shp'), 'crest_type', "TEXT")
    arcpy.AddField_management(os.path.join(DCE01_folder, 'dam_crests.shp'), 'dam_id', "DOUBLE")
    # thalwegs
    arcpy.CreateFeatureclass_management(DCE01_folder, "thalwegs.shp", "POLYLINE", "", "DISABLED", "DISABLED", spatial_reference)
    #add fields for thalweg type
    arcpy.AddField_management(os.path.join(DCE01_folder, 'thalwegs.shp'), 'type', "TEXT")
    # make first RS folder
    RS01_folder = make_folder(mapping_folder, "RS_01")
    # create empty shapefiles for valley bottom and valley bottom centerline
    # valley bottom
    arcpy.CreateFeatureclass_management(RS01_folder, "valley_bottom.shp", "POLYGON", "", "DISABLED", "DISABLED", spatial_reference)
    arcpy.AddField_management(os.path.join(RS01_folder, 'valley_bottom.shp'), 'site_name', "TEXT")
    arcpy.AddField_management(os.path.join(RS01_folder, 'valley_bottom.shp'), 'huc8', "DOUBLE")
    # valley bottom centerline
    arcpy.CreateFeatureclass_management(RS01_folder, "vb_centerline.shp", "POLYLINE", "", "DISABLED", "DISABLED", spatial_reference)
    
    # analysis folder
    analysis_folder = make_folder(project_path, "03_Analysis")
    DCE01_fold = make_folder(analysis_folder, "DCE_01")
    make_folder(analysis_folder, "CDs")
    make_folder(analysis_folder, "Summary")

    with arcpy.da.UpdateCursor(os.path.join(RS01_folder, 'valley_bottom.shp'), ['site_name', 'huc8']) as cursor:
        for row in cursor:
            row[0] = site_name
            row[1] = huc8
            cursor.updateRow(row)

# xml creation


def create_project(huc, output_dir, site_name, image_date):

    project_name = site_name
    project = RSProject(cfg, output_dir)
    project.create(project_name, 'RIM')

    project.add_project_meta({
        'HUC{}'.format(len(huc)): str(huc),
        'site_name': site_name,
        'date_created': datetime.datetime.now().isoformat()
    })

    inputs = project.XMLBuilder.add_sub_element(project.XMLBuilder.root, 'Inputs')
    realizations = project.XMLBuilder.add_sub_element(project.XMLBuilder.root, 'Realizations')
    rs_context = project.XMLBuilder.add_sub_element(realizations, 'RS_Context', None, {
        'id': 'RS_01',
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version
    })
    dce = project.XMLBuilder.add_sub_element(realizations, 'DCE', None, {
        'id': 'DCE_01',
        'image_date': image_date
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version
    })
    project.XMLBuilder.add_sub_element(dce, 'Name', image_date)

    project.XMLBuilder.write()
    return project, inputs, rs_context, dce

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('srs_template', help='path to a shapefile with desired output coordinate system', type=str)
    parser.add_argument('project_path', help='path to output folder', type=str)
    args = parser.parse_args()

    make_project(project_path)




