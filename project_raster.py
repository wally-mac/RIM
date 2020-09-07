import os
import arcpy
import sys
from create_project import make_folder

arcpy.env.overwriteOutput = True

# path to folder with unprojected rasters
in_folder = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Idaho\Trail_Creek\Dronedeploy"

# create folder for projected outputs
out_folder = make_folder(in_folder, 'Projected')

srs_template = r"C:\Users\A02295870\Box\Thesis_sites\17040219\big_wood_a\02_Mapping\DCE_01\thalwegs.shp"

# Project drone deploy output rasters


def project_rasters(in_folder, out_folder, srs_template):

    spatial_reference = arcpy.Describe(srs_template).spatialReference

    # Orthomosaic
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'orthomosaic.tif'), os.path.join(out_folder, 'orthomosaic.tif'), spatial_reference, 'NEAREST', '.02')

    # DEM
    #arcpy.ProjectRaster_management(os.path.join(in_folder, 'DEM.tif'), os.path.join(out_folder, 'DEM.tif'), spatial_reference, 'NEAREST', '.02')

    # Orthomosaic
    #arcpy.ProjectRaster_management(os.path.join(in_folder, 'NDVI.tif'), os.path.join(out_folder, 'NDVI.tif'), spatial_reference, 'NEAREST', '.02')


project_rasters(in_folder, out_folder, srs_template)
