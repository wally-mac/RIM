---
title: Step 3 - Mapping
weight: 1
---

## Map Features

There are 2 types of features that you will map
- Context features
- Data Capture Events (DCEs)

### Context features
The context features you need to map are the valley bottom and a valley bottom centerline. These features are typically consistent over time. 

Empty shapefiles were created for the context features when you ran the Project Builder script in [Step 2](https://riverscapes.github.io/inundation/Documentation/Step2_createproject.html) and are located in the **02_Mapping/RS_01 folder** of your project folder.

Because the context features will typically not change over time, you will likely only need or want to map them once. However, additional versions of these features could be mapped and saved within the 02_Mapping folder in a new folder called RS_02, RS_03, etc.

### DCEs
The Data Capture Event features to map are the structure or beaver dam crests, thalwegs, and the inundated area and type. These features represent a snapshot of your project area in time and should be mapped seperately for each different image or time of interest.

##### DCE 1
All features that need to be mapped for the first DCE were created when you ran the Project Builder script in [Step 2](https://riverscapes.github.io/inundation/Documentation/Step2_createproject.html) and are located in the **02_Mapping/DCE_01 folder** of your project folder.

##### Subsequent DCEs
For additional DCEs you can provide a new image and create new blank DCE shapefiles using the Create_DCE script in [Step 3b](https://riverscapes.github.io/inundation/Documentation/Step3_Mapping/Step3b_newDCE.html). 

Reasons for which you might want to create a 2nd, 3rd, etc DCE:
- to map changes in inundation at different flows
- to track changes in inundation over time 
- using imagery from the same date but from a different source (e.g. to make a comparison between UAV acquired imagery and NAIP imagery)
- to compare outputs from two different mappers