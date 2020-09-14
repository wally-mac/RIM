---
title: Step 2 - Project Builder
weight: 1
---

## Project Builder

The next step is to run the Project Builder script (Step2_ProjectBuilder.py). This script is designed to take the inputs and organize them and create a folder structure as well as an XML file for the project. This script will create empty shapefiles to map context features and your first Data Capture Event (DCE)

## Inputs
### Files
- **project_path** - The path to a folder where you want the project folder structure to be created
- **srs_template** - The path to a shapefile that contains the desired coordinate system and projection for your project shapefiles
- **image_path** - The path to an image raster of the site 
- **DEM_path** - The path to the input DEM
- **hs_path** - The path to a hillshade
- **BRAT_path** - The path to a BRAT output shapefile
- **VBET_path** - The path to a VBET output shapefile

### Parameters
#### Site or project parameters
- **site_name** The name of the project
- **huc** - the 8 digit Hydrologic Unit Code

#### Metadata and parameters describing the input imagery
- **image_date** - The date the imagery was collected. Use format YYYYMMDD
- **date_name** - The dispay name for the image (e.g. "June 2019")
- **image_source** - The source of the imagery (e.g. drone, google_earth, NAIP)
- **flow_stage** - The flow stage at the time of the imagery (e.g. baseflow, low, moderate, high)
- **image_res** - The resolution of the imagery in meters
- **mapper** - The name of the person digitizing the features

