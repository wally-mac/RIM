---
title: Step 3b - Create New DCE
weight: 3
---

## Create new DCE

Run the ([Step3b_newDCE.py](https://github.com/Riverscapes/inundation/blob/master/STEP3b_newDCE.py)) script to create an additional data capture event. 

Examples for which you might want to create a 2nd, 3rd, etc DCE:
- to map a different snapshot in time at the same site (e.g. using imagery with a different date)
- using imagery from the same date but from a different source (e.g. to make a comparison between UAV acquired imagery and NAIP imagery)
- to compare outputs from two different mappers

## Inputs
- **project_path** - The path to a folder where you want the project folder structure to be created
- **srs_template** - The path to a shapefile that contains the desired coordinate system and projection for your project shapefiles
- **AP_fold** - The name for the folder containing the new image. Use AP_02, AP_03, AP_04, etc.
- **image_path** - The path to an image raster  
- **DCE_fold** - The name for the folder that will contain the new DCE shapefiles. Use DCE_01, DCE_02, DCE_03, etc.

#### Metadata and parameters describing the new input imagery
- **image_date** - The date the imagery was collected. Use format YYYYMMDD
- **date_name** - The dispay name for the image (e.g. "June 2019")
- **image_source** - The source of the imagery (e.g. drone, google_earth, NAIP)
- **flow_stage** - The flow stage at the time of the imagery (e.g. baseflow, low, moderate, high)
- **image_res** - The resolution of the imagery in meters
- **mapper** - The name of the person digitizing the features

After you run this step return to step 3a to map the features in your 2nd DCE. While context features may occasionially change between DCEs, typically the only features you will re-map are the DCE features.

