---
title: DCE Features
weight: 1
---

### DCE
The Data Capture Event features to map are the structure or beaver dam crests, thalwegs, and the inundation types. These features are a snapshot in time and should be mapped seperately for each different image or time period of interest.

#### Dam or structure crests
During Step 2 an empty structures shapefile was created in the **02_Mapping/DCE_01 folder** of your project folder and is called dam_crests.shp

For each beaver dam you will trace the crest of the beaver dam and will determine whether the dam is intact, breached, or blown out. You will then give each dam a unique dam ID and then determine the portion or length of the dam that is or is not actively structurally forcing flow at the time the image was taken.
##### Dam state
The dam state of each beaver dam is either intact, breached, or blown_out as defined below by [Hafen, 2017](https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=7648&context=etd). The dam state for each dam should be entered in the dam_state attribute field of the shapefile as "intact", "breached", or "blown_out".
- **intact** - a dam from which pond is fully maintained upstream of the dam
- **breached** - a dam where partial removal or loss of material from the dam crest results in a lowering of the pond water surface elevation
- **blown_out** - a dam where enough of the dam is breached or damaged such that the dam no longer backs up water
##### Dam ID
Number each dam in the dam_id attribute field so that when you split the crest of each dam to describe the crest type the correct dam number is retained
##### Crest type
For each dam crest, split the dam into the length of the crest that is or is not structurally forcing backwater upstream of the dam. To do this, use the split tool in the editor and populate the crest_type attribute field as either "active" or "inactive"
#### Thalwegs

##### Thalweg type

#### Inundation 

##### Inundation type

![InundationType]({{ site.baseurl }}/assets/images/07052020inundation_typespng-01.png)

