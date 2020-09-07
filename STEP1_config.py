# Import system modules

from create_project import make_project


##############################
# STEP 1 - CREATE PROJECT

# Inputs

# path to a shapefile with the desired output coordinate system
srs_template = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Snake_headwaters\BRAT\BatchRun_03\Outputs\Output_01\02_Analyses\Combined_Capacity_Model.shp"
# path to project folder
project_path = r"C:\Users\A02295870\Box\Thesis_sites\17040101\pacific_creek_b"
# file locations for RS context inputs and imagery
image_path = r"C:\Users\A02295870\Box\Thesis_sites\17040101\pacific_creek_b\imagery\google_earth_08272009.jpg"
BRAT_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Snake_headwaters\BRAT\BatchRun_03\Outputs\Output_01\02_Analyses\Combined_Capacity_Model.shp"
VBET_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Snake_headwaters\BRAT\BatchRun_03\Inputs\04_Anthropogenic\01_ValleyBottom\Valley_01\Provisional_ValleyBottom_Unedited.shp"
DEM_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Snake_headwaters\BRAT\BatchRun_03\Inputs\03_Topography\DEM_01\NED_DEM_10m.tif"
hs_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Snake_headwaters\BRAT\BatchRun_03\Inputs\03_Topography\DEM_01\Hillshade\Hillshade.tif"

# Parameters

# site parameters
site_name = "pacific_creek_b"
huc = '17040101'

# image and DCE 01 metadata
image_date = "20090827"  # use format YYYYMMDD
date_name = "August 2009"  # what you want the display name for the image to be
image_source = "google earth"  # e.g. drone, google_earth, NAIP
flow_stage = "low"  # flow stage at the time of the imagery (e.g. baseflow, low, medium, high)
image_res = '.28'  # resolution of the imagery in meters
mapper = 'Karen Bartelt'

##############################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template, image_path, site_name, huc, BRAT_path, VBET_path, DEM_path, hs_path, image_date, date_name, image_source, flow_stage, image_res, mapper)


##########################
