import os
import arcpy
import sys
from create_project import make_folder

# path to folder with unprojected rasters
in_folder = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid\DroneDeploy\05292019"

# create folder for projected outputs
out_folder = make_folder(in_folder, 'Projected')

# Project drone deploy output rasters
def project_rasters(in_folder, out_folder, srs_template):

    # Orthomosaic
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'orthomosaic.tif'), os.path.join(out_folder, 'orthomosaic.tif'), srs_template, 'NEAREST', '.02')

    # DEM
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'DEM.tif'), os.path.join(out_folder, 'DEM.tif'), srs_template, 'NEAREST', '.02')

    # Orthomosaic
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'NDVI.tif'), os.path.join(out_folder, 'NDVI.tif'), srs_template, 'NEAREST', '.02')


