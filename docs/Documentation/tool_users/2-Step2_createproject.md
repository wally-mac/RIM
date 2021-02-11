---
title: Step 2 - Project Builder
weight: 2
---

## Project Builder

The next step is to run the [Project Builder script](https://github.com/Riverscapes/inundation/blob/master/Step2_ProjectBuilder.py). This script is designed to take the inputs and organize them into a consistent project folder structure. This script will create empty shapefiles to map context features and your first Data Capture Event (DCE)

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


