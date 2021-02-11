---
title: Step 3a - Mapping
weight: 3
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
To characterize more dynamic hydrogeomorphic attributes such as planform changes (e.g. multithreadedness and sinuosity) that potentially occur between survey dates we mapped the location and type of thalwegs in the riverscape at the time of each survey. We mapped 4 thalweg types adapted from the Kramer-Anderson et al. Geomorphic Unit Tool (GUT - http://gut.riverscapes.xyz/); main, anabranch, split, and braid.
- **Main** – the thalweg that follows the deepest point of the primary anabranch
- **Anabranch** – thalwegs that follow the deepest point of a fully formed (i.e. has an active channel bed) secondary anabranch that is longer than 2 ocularly estimated bankfull channel widths
- **Split** – thalwegs that follow the deepest point of structurally forced sheetflow, or short secondary anabranches 
- **Braid** – thalwegs within the primary anabranch that are not the main thalweg and are not structurally forced by large wood or beaver dams. These typically depart and return from the main thalweg or an anabranch thalweg. 


#### Thalweg type
Attribute thalwegs to the following types:
- **Main** – the thalweg that follows the deepest point of the primary anabranch
- **Anabranch** – thalwegs that follow the deepest point of a fully formed (i.e. has an active channel bed) secondary anabranch that is longer than 2 ocularly estimated bankfull channel widths
- **Split** – thalwegs that follow the deepest point of structurally forced sheetflow, or short secondary anabranches 
- **Braid** – thalwegs within the primary anabranch that are not the main thalweg and are not structurally forced by large wood or beaver dams. These typically depart and return from the main thalweg or an anabranch thalweg. 
### Inundation 
Be sure to map inundation at a consistent zoom level (we typically use 1:250). To map inundation simply digitize a polygon around the wetted edge visible in the aerial imagery. Where vegetation or shadows obscure the waters edge, infer the wetted extent between visible boundaries. If possible, predict vegetated areas that will be difficult to see the inundation and spot check at the time of imagery collection.
#### Inundation type

Each inundation survey polygon was then broken into three flow type classes on a continuum from more lotic (free flowing) to more lentic (ponded, but still flowing). We defined these classes in Figure 5 as follows:
- **Free flowing** – not obstructed by a channel-spanning structural element
- **Overflow** – structurally-forced flow onto floodplain and/or otherwise expose in channel surfaces (e.g. bars)
- **Ponded** – structurally-forced backwater ponding upstream of a channel-spanning structural-element


![InundationType]({{ site.baseurl }}/assets/images/inun_types_tiny.png)

