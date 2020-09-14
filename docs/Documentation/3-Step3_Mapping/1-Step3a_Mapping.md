---
title: Step 3a - Mapping
weight: 1
---

## Context Features

### Valley bottom
##### Background
[Wheaton et al., 2015](https://www.researchgate.net/publication/281321324_Geomorphic_Mapping_and_Taxonomy_of_Fluvial_Landforms) defined the valley bottom as the active channel(s) and contemporary floodplain. The spatial extent of the valley bottom represents the area that could plausibly flood during the contemporary flow regime. The margins or lateral extent of the valley bottom will be a confining margin, which are hillslope, fans, or terraces ([Wheaton et al., 2015](https://www.researchgate.net/publication/281321324_Geomorphic_Mapping_and_Taxonomy_of_Fluvial_Landforms)). 

![ValleyBottom]({{ site.baseurl }}/assets/images/oblique_valleyBottom-02.jpg)

##### Mapping
During [Step 2](https://riverscapes.github.io/inundation/Documentation/Step2_createproject.html) an empty valley bottom shapefile was created in the **02_Mapping/RS_01 folder** of your project folder and is called **valley_bottom.shp**
###### Useful resources and lines of evidence for identifying the valley bottom extent
When mapping the valley bottom it is beneficial to use all available lines of evidence including observations made in the field, a DEM, aerial photos, google earth, contour maps, hillshades, etc. The upstream and downstream edge of your valley bottom polygon will determine the longitudinal extent of you project area.
### Valley bottom centerline
##### Mapping
During [Step 2](https://riverscapes.github.io/inundation/Documentation/Step2_createproject.html) an empty valley bottom centerline shapefile was created in the **02_Mapping/RS_01 folder** of your project folder and is called **vb_centerline.shp**

The valley bottom centerline can be manually digitized or created using the ArcGIS [Polygon to Centerline Tool](https://www.arcgis.com/home/item.html?id=bc642731870740aabf48134f90aa6165)

## DCE Features

The Data Capture Event features to map are the structure or beaver dam crests, thalwegs, and the inundation types. These features are a snapshot in time and should be mapped seperately for each different image or time period of interest.

### Dam or structure crests
During [Step 2](https://riverscapes.github.io/inundation/Documentation/Step2_createproject.html) an empty structures shapefile was created in the **02_Mapping/DCE_01 folder** of your project folder and is called **dam_crests.shp**

For each beaver dam you will trace the crest of the beaver dam and will determine whether the dam is intact, breached, or blown out. You will then give each dam a unique dam ID and then determine the portion or length of the dam that is or is not actively structurally forcing flow at the time the image was taken.
#### Dam state
The dam state of each beaver dam is either intact, breached, or blown_out as defined below by [Hafen, 2017](https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=7648&context=etd). 

- **intact** - a dam from which pond is fully maintained upstream of the dam
- **breached** - a dam where partial removal or loss of material from the dam crest results in a lowering of the pond water surface elevation
- **blown_out** - a dam where enough of the dam is breached or damaged such that the dam no longer backs up water

The dam state for each dam should be entered in the dam_state attribute field of the shapefile as "intact", "breached", or "blown_out".

#### Dam ID
Number each dam in the dam_id attribute field so that when you split the crest of each dam to describe the crest type the correct dam number is retained

#### Crest type
For each dam crest, split the dam into the length of the crest that is or is not structurally forcing backwater upstream of the dam. To do this, use the split tool in the editor and populate the crest_type attribute field as either "active" or "inactive"

- **active** - the portion of the dam that is actively backing up water upstream of the dam
- **inactive** - the portion of the dam that is not actively backing up water upstream of the dam

### Thalwegs

#### Thalweg type

### Inundation 

#### Inundation type

![InundationType]({{ site.baseurl }}/assets/images/07052020inundation_typespng-01.png)

