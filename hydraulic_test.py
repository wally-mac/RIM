import arcpy
import os
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')

def extract_hyd(folder, raster, inundation):

    arcpy.env.workspace = folder

    arcpy.env.overwriteOutput = True

    # dissolve inundation shapefile
    arcpy.Dissolve_management(inundation, os.path.join(folder, 'in_diss.shp'), dissolve_field='type')

    # zonal statistics as table
    #arcpy.sa.ZonalStatisticsAsTable(os.path.join(folder, 'in_diss.shp'), 'type', raster, os.path.join(folder, 'ZS_Table'))

    # make feature layer from inundation to make masks of inundation types to extract raster by inundation type

    arcpy.MakeFeatureLayer_management(os.path.join(folder, 'in_diss.shp'), 'inun')

    # select FF
    arcpy.SelectLayerByAttribute_management('inun', 'NEW_SELECTION', "type = 'free_flowing'")
    # extract by mask
    FF = arcpy.sa.ExtractByMask(raster, 'inun')
    FF.save(os.path.join(folder, 'FF.tif'))

    # select OV
    arcpy.SelectLayerByAttribute_management('inun', 'NEW_SELECTION', "type = 'overflow'")
    # extract by mask
    OV = arcpy.sa.ExtractByMask(raster, 'inun')
    OV.save(os.path.join(folder, 'OV.tif'))

    # select all flowing (OV and FF)
    arcpy.SelectLayerByAttribute_management('inun', 'ADD_TO_SELECTION', "type = 'free_flowing'")
    # extract by mask
    FLOW = arcpy.sa.ExtractByMask(raster, 'inun')
    FLOW.save(os.path.join(folder, 'FLOW.tif'))

        # select FF
    arcpy.SelectLayerByAttribute_management('inun', 'NEW_SELECTION', "type = 'ponded'")
    # extract by mask
    PD = arcpy.sa.ExtractByMask(raster, 'inun')
    PD.save(os.path.join(folder, 'PD.tif'))

folder = r"C:\Users\karen\Box\Thesis_sites\17070204\lower_owens\hydraulics_compare\LO2\2013"
raster = 'WSE.tif'
inundation = 'inundation.shp'

extract_hyd(folder, raster, inundation)

