# Import system modules

from create_project import make_project


##############################
# STEP 1 - CREATE PROJECT

# Inputs

# path to project folder
project_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\spawn_trib_final"
# path to a shapefile with the desired output coordinate system
srs_template = r"C:\Users\A02295870\Box\Thesis_sites\16010203\spawn_trib\01_Inputs\03_Context\BRAT_01\BRAT.shp"
image_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\temple_trib_a\01_Inputs\01_Imagery\AP_01\orthomosaic.png"
DEM_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\spawn_trib\01_Inputs\02_Topo\DEM_01\DEM.tif"
hs_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\spawn_trib\01_Inputs\02_Topo\DEM_01\hlsd.tif"
BRAT_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\spawn_trib\01_Inputs\03_Context\BRAT_01\BRAT.shp"
VBET_path = r"C:\Users\A02295870\Box\Thesis_sites\16010203\spawn_trib\01_Inputs\03_Context\VBET_01\VBET.shp"


# Parameters

# site parameters
site_name = "spawn_trib_final"
huc = '16010203'

##############################

# create project folders and empty mapping shapefiles for first DCE
make_project(project_path, srs_template, image_path, site_name, huc, BRAT_path, VBET_path, DEM_path, hs_path)


##########################
