---
title: Protocol
weight: 1
---

This page outlines the protocol implemented in Bartelt 2021 Masters thesis

## Overview

For each site, the protocol can be broken into 3 main steps:

- Imagery Acquisition
- Mapping Features
- Calculating Metrics

![flow_chart]({{ site.baseurl }}/assets/images/flow_chart_tiny.png)

## Imagery Acquisition

1. Use Drone deploy (or similar software) to [create a flight plan](https://support.dronedeploy.com/docs/desktopplanning) covering the full length and lateral extent of the site or project area
2. Field visit to collect imagery
3. Follow the instructions [here](https://www.agisoft.com/pdf/PS_1.3%20-Tutorial%20(BL)%20-%20Orthophoto,%20DEM%20(GCPs).pdf) to upload and process the drone photos and generate a 2cm orthomosaic

## Map Features

### Create RIM Project

### Map Riverscape Context Features

#### Map Valley Bottom

#### Derive Valley Bottom Centerline

### Map and Attribute Structurally Forced Features

#### Map Dam Crests

Beaver dam crests represent the top of the dam, and beavers tend to construct them at a constant elevation, such that when the dam is maintained and full, water spills over the contour of the crest evenly. Digitize the beaver dam crest for each beaver dam by tracing the polyline representing a contour at the crest elevation of the dam (note, if topography is available, these dam crests should connect to cells of equal elevation on the digital elevation model at each end of the crest).

#### Attribute "dam state" and "crest type"

For each digitized dam crest you will determine two categorical attributes that together help characterize dam condition and beaver dam activity:

- dam state
- crest type

Dam state refers to the condition of the dam and whether it was intact, breached, or blown out at the time of the survey based on definitions by Hafen et al. (2020). For the crest type attribute you will determine the length of the crest that was actively ponding flow at the time of the survey.