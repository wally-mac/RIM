---
title: Step 2 - Project Builder
weight: 1
---

## Riverscape Inundation Mapper inputs

The next step is to run the Project Builder script. This script is designed to take the inputs and organize them and create a folder structure as well as an XML file for the project. This script will create empty shapefiles to map the riverscape context features and for your first Data Capture Event (DCE)

## Inputs
### Files
- **project_path** - The path to a folder where you want the project folder structure to be created
- **srs_template** - The path to a shapefile that contains the desired coordinate system and projection for your project shapefiles
- **image_path** - The path to an image raster of the site 
- **DEM_path** - The path to the input DEM
- **hs_path** - The path to a hillshade
- **site_name** The name of the project
- **huc8** - the 8 digit Hydrologic Unit Code

### Parameters
- **site_name** The name of the project
- **huc8** - the 8 digit Hydrologic Unit Code
#### Metadata for the imagery provided for the imagery input image_path
- **site_name** The name of the project
- **image_date** - The date the imagery was collected. Use format YYYYMMDD
- **image_source** - The source of the imagery
- **image_res** - The resolution of the imagery in meters
- **flow_stage** - The flow stage at the time of the imagery (e.g. baseflow, low, medium, high)

