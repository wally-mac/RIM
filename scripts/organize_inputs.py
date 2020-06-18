import os
import arcpy
import sys
from create_project import make_folder

# path to folder with unprojected rasters
#in_folder = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid\DroneDeploy\05292019"

# create folder for projected outputs
#out_folder = make_folder(in_folder, 'Projected')

# Project drone deploy output rasters
def project_rasters(in_folder, out_folder, srs_template):

    # Orthomosaic
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'orthomosaic.tif'), os.path.join(out_folder, 'orthomosaic.tif'), srs_template, 'NEAREST', '.02')

    # DEM
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'DEM.tif'), os.path.join(out_folder, 'DEM.tif'), srs_template, 'NEAREST', '.02')

    # Orthomosaic
    arcpy.ProjectRaster_management(os.path.join(in_folder, 'NDVI.tif'), os.path.join(out_folder, 'NDVI.tif'), srs_template, 'NEAREST', '.02')


# pull files from RS_context folder
def gather_RSinputs(context_folder, huc8, project_path):
    arcpy.CopyRaster_management(os.path.join(context_folder, huc8, 'topography/dem.tif'), os.path.join(project_path, '01_Inputs/02_Topo/DEM_01', 'DEM.tif'))
    arcpy.CopyRaster_management(os.path.join(context_folder, huc8, 'topography/dem_hillshade.tif'), os.path.join(project_path, '01_Inputs/02_Topo/DEM_01', 'hlsd.tif'))
    # arcpy.CopyRaster_management(os.path.join(context_folder, huc8, 'topography/hand.tif'), os.path.join(project_path, '01_Inputs/02_Topo/DEM_01', 'hand.tif'))
    # arcpy.CopyRaster_management(os.path.join(context_folder, huc8, 'topography/slope.tif'), os.path.join(project_path, '01_Inputs/02_Topo/DEM_01', 'slope.tif'))

    arcpy.CopyFeatures_management(os.path.join(context_folder, huc8, 'BRAT/BRAT.shp'), os.path.join(project_path, '01_Inputs/03_Context/BRAT_01', 'BRAT.shp'))
    arcpy.CopyFeatures_management(os.path.join(context_folder, huc8, 'hydrology/WBDHU8.shp'), os.path.join(project_path, '01_Inputs/03_Context/WBD', 'HUC8.shp'))
    arcpy.CopyFeatures_management(os.path.join(context_folder, huc8, 'hydrology/WBDHU10.shp'), os.path.join(project_path, '01_Inputs/03_Context/WBD', 'HUC10.shp'))
    arcpy.CopyFeatures_management(os.path.join(context_folder, huc8, 'hydrology/WBDHU12.shp'), os.path.join(project_path, '01_Inputs/03_Context/WBD', 'HUC12.shp'))
