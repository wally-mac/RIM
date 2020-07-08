import arcpy
import os
from arcpy import env
from create_project import make_folder
from arcpy.sa import *
from arcpy.da import *
arcpy.CheckOutExtension('Spatial')
arcpy.env.overwriteOutput = True


def BRAT_settings (folder, BRAT, BRAT_out, SP_cut, grad_cut):
    """
    folder: path to working folder
    BRAT: path to BRAT output file
    BRAT_out: what you want the name of the output BRAT file with the settings field to be called
    SP_cut: the streampower at which dams will fail
    grad_cut: the gradient cutoff between classic and steep setting
    """

    # make a copy of the input BRAT shapefile and save to an output folder
    out_folder = make_folder(folder, "Output")
    arcpy.CopyFeatures_management(BRAT, os.path.join(out_folder, BRAT_out))
    
    # make new field in output BRAT shapefile for settings
    arcpy.AddField_management(os.path.join(out_folder, BRAT_out), 'setting', "TEXT")

    # make setting type for areas where capacity is 0 "unsuitable"
    arcpy.MakeFeatureLayer_management(os.path.join(out_folder, BRAT_out), 'BRAT_noCap', "oCC_EX = 0")
    ## populate setting field
    with arcpy.da.UpdateCursor('BRAT_noCap', 'setting') as Ucursor:
        for Urow in Ucursor:
            Urow[0] = 'unsuitable'
            Ucursor.updateRow(Urow)


    # create feature layer or segments where capacity is greater than 0 to make selections
    arcpy.MakeFeatureLayer_management(os.path.join(out_folder, BRAT_out), 'BRAT_out', "oCC_EX > 0")

    # steeper setting
    ## gradient
    #arcpy.SelectLayerByAttribute_management('BRAT_out', 'NEW_SELECTION', '"iGeo_Slope" >= ' + grad_cut)
    ## SP
    #arcpy.SelectLayerByAttribute_management('BRAT_out', 'ADD_TO_SELECTION', '"iHyd_SPLow" <= ' + SP_cut)
    ## populate setting field
    with arcpy.da.UpdateCursor('BRAT_out', ['setting', 'iGeo_Slope', 'iHyd_SPLow'], """"iGeo_Slope" >= grad_cut AND "iHyd_SPLow" <= SP_cut""") as Ucursor:
        for Urow in Ucursor:
            Urow[0] = 'steep'
            Ucursor.updateRow(Urow)
    
    # floodplain setting
    ## gradient
    #arcpy.SelectLayerByAttribute_management('BRAT_out', 'NEW_SELECTION', '"iGeo_Slope" <= ' + grad_cut)
    ## SP
    #arcpy.SelectLayerByAttribute_management('BRAT_out', 'ADD_TO_SELECTION', '"iHyd_SPLow" >= ' + SP_cut)
    ## populate setting field
    with arcpy.da.UpdateCursor('BRAT_out', ['setting', 'iGeo_Slope', 'iHyd_SPLow'], """"iGeo_Slope" <= grad_cut AND "iHyd_SPLow" >= SP_cut""") as Ucursor:
        for Urow in Ucursor:
            Urow[0] = 'floodplain'
            Ucursor.updateRow(Urow)
    
    # "Classic" setting
    ## gradient
    #arcpy.SelectLayerByAttribute_management('BRAT_out', 'NEW_SELECTION', '"iGeo_Slope" <= ' + grad_cut)
    ## SP
    #arcpy.SelectLayerByAttribute_management('BRAT_out', 'ADD_TO_SELECTION', '"iHyd_SPLow" <= ' + SP_cut)
    ## populate setting field
    with arcpy.da.UpdateCursor('BRAT_out', ['setting', 'iGeo_Slope', 'iHyd_SPLow'], """"iGeo_Slope" <= grad_cut AND "iHyd_SPLow" <= SP_cut""") as Ucursor:
        for Urow in Ucursor:
            Urow[0] = 'classic'
            Ucursor.updateRow(Urow)
    

folder = r"C:\Users\a02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\all\BRAT\Utah\setting_test"
BRAT = r"C:\Users\a02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\all\BRAT\Utah\setting_test\Bear_river_BRAT.shp"
BRAT_out = 'oCC_EX_6_25.shp'
SP_cut = "25"
grad_cut = "0.06"

BRAT_settings(folder, BRAT, BRAT_out, SP_cut, grad_cut)






