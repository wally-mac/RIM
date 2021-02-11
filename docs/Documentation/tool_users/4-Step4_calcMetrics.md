---
title: Step 4 - Calculate Metrics
weight: 4
---

## Calculate metrics

Run [this script](https://github.com/Riverscapes/inundation/blob/master/STEP4_metricCalc.py) to calculate summary metrics from the features mapped in the DCEs

### Inputs:
- **project_path** - The path to a folder where you want the project folder structure to be created
- **RS_folder_name** - The name of the folder with RS Context shapefiles you want to use to calculate site metrics (the folder with the Valley Bottom polygon)
- **DEM** - The path to the input DEM

#### Site or project parameters
- **project_name** A readable name of the site
- **site_name** The shorthand name of the site
- **huc8** - the 8 digit Hydrologic Unit Code
- **setting** - the dominant beaver dam building opportunity present ("classic", "steep", or "floodplain")

#### Metadata and parameters describing both DCEs that will be compared
- **DCE1_name** - the name of the first DCE folder you want to use for the metric calculation (e.g. "DCE_01")
- **DCE2_name** - the name of the second DCE folder you want to use for the metric calculation (e.g. "DCE_02")
##### DCE 1 parameters
- **DCE1_date** - the date that the imagery was acquired
- **DCE1_flow_stage** - the flow stage at the time of the imagery (e.g. low, moderate, high)
- **DCE1_active** - was there evidence of recent beaver activity at the site during the time of the imagery acquisition?
- **DCE1_maintained** - was there evidence of recent beaver dam maintenence at the site during the time of the imagery acquisition?
- **DCE1_res** - the resolution of the input imagery in  meters
##### DCE 2 parameters
- **DCE2_date** - the date that the imagery was acquired
- **DCE2_flow_stage** - the flow stage at the time of the imagery (e.g. low, moderate, high)
- **DCE2_active** - was there evidence of recent beaver activity at the site during the time of the imagery acquisition?
- **DCE2_maintained** - was there evidence of recent beaver dam maintenence at the site during the time of the imagery acquisition?
- **DCE2_res** - the resolution of the input imagery in  meters

## Output Metrics
The following table includes all metric outputs

![outputMetrics]({{ site.baseurl }}/assets/images/s1.png)

