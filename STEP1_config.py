# Import system modules

from create_project import make_project


##############################
# STEP 1 - CREATE PROJECT

# Inputs

# path to a shapefile with the desired output coordinate system
srs_template = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\TempleFork\temple_b\10262019\GIS\inundation.shp"
# path to project folder
project_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid"
# file locations for RS context inputs and imagery
image_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\RH_fork_mid\DroneDeploy\05292019\Projected\orthomosaic.tif"
BRAT_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\BRAT\BRAT\BatchRun_03\Outputs\Output_01\02_Analyses\Combined_Capacity_Model.shp"
VBET_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\VBET\BatchRun_01\02_Analyses\Output_1\Provisional_ValleyBottom_Unedited.shp"
DEM_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\topography\dem.tif"
hs_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Riverscapes_Context\16010203\topography\dem_hillshade.tif"

# Parameters

# site parameters
site_name = "RH_fork_mid"
huc = '16010203'

# image and DCE 01 metadata
image_date = "20200529"  # use format YYYYMMDD
date_name = "May 2019"  # what you want the display name for the image to be
image_source = "drone"  # e.g. drone, google_earth, NAIP
flow_stage = "moderate"  # flow stage at the time of the imagery (e.g. baseflow, low, medium, high)
image_res = '.02'  # resolution of the imagery in meters
mapper = 'Karen Bartelt'

##############################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template, image_path, site_name, huc, BRAT_path, VBET_path, DEM_path, hs_path, image_date, date_name, image_source, flow_stage, image_res, mapper)


##########################
