---
title: Step 3b - Create New DCE
weight: 1
---

## Create new DCE

Run this script to create an additional data capture event. 

Examples for which you might want to create a 2nd, 2rd, etc DCE:
- to map a different snapshot in time at the same site (e.g. using imagery with a different date)
- using imagery from the same date but from a different source (e.g. to make a comparison between UAV acquired imagery and NAIP imagery)
- to compare outputs from two different mappers

## Inputs
- **project_path** - The path to a folder where you want the project folder structure to be created
- **srs_template** - The path to a shapefile that contains the desired coordinate system and projection for your project shapefiles
- **DCE_fold** - The name you want the folder containing the new DCE to be called. It is recommended to use DCE_01, DCE_02, DCE_03, etc.

Following this step return to step 3a to map the features in your 2nd DCE. While context features may occasionially change between DCEs, typically the only features you will re-map are the DCE features.

