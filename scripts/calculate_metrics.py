# Import system modules
import arcpy
from arcpy import env
import os
import argparse
from loghelper import Logger
from create_project import make_folder
arcpy.env.overwriteOutput = True
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')



# Set project path
project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\mill_test_2020_05_07"

# Input the name of the folder of the desired RS Context shapefiles (the folder with the Valley Bottom polygon)
RS_folder_name = "RS_01"

# Input the name of the folder of the desired DCEs for the analysis
DCE1_name = "DCE_01"
DCE2_name = "DCE_02"

########

log = Logger('set paths')

# Set internal paths
map_folder = os.path.join(project_path, '02_Mapping')
RS_folder = os.path.join(map_folder, RS_folder_name)
DCE1 = os.path.join(map_folder, DCE1_name)
DCE2 = os.path.join(map_folder, DCE2_name)
DEM = os.path.join(project_path, '01_Inputs', '02_Topo', 'DEM_01', 'DEM.tif')


# Create a list of DCEs 1 and 2
DCE_list = [DCE1, DCE2]


log.info('paths set for DCEs of interest and DEM')

#######

# Calculate reach and valley slope with DEM, Thalweg, and VB_Centerline
log = Logger('CL_attributes')
def CL_attributes(polyline, DEM, scratch):
    """
    calculates min and max elevation, length, slope for each flowline segment
    :param polyline: The output netwrok to add fields to.
    :param DEM: The DEM raster.
    :param midpoint_buffer: The buffer created from midpoints
    :param scratch: The current workspace
    """
    # if fields lready exist, delete them
    fields = [f.name for f in arcpy.ListFields(polyline)]
    drop = ["el_1", "el_2", "length", "slope"]
    for field in fields:
        if field in drop:
            arcpy.DeleteField_management(polyline, field)

    # function to attribute start/end elevation (dem z) to each flowline segment
    def zSeg(vertex_type, out_field):
        # create start/end points for each flowline reach segment
        tmp_pts = os.path.join(scratch, 'tmp_pts.shp')
        arcpy.FeatureVerticesToPoints_management(polyline, tmp_pts, vertex_type)
        # create 20 meter buffer around each start/end point
        tmp_buff = os.path.join(scratch, 'tmp_buff.shp')
        arcpy.Buffer_analysis(tmp_pts, tmp_buff, '20 Meters')
        # get min dem z value within each buffer
        arcpy.AddField_management(polyline, out_field, "DOUBLE")
        out_ZS = arcpy.sa.ZonalStatistics(tmp_buff, "FID", DEM, "MINIMUM", "NODATA")
        out_ZS.save(os.path.join(scratch, "out_ZS"))
        tmp_pts2 = os.path.join(scratch, 'tmp_pts2.shp')
        arcpy.sa.ExtractValuesToPoints(tmp_pts, os.path.join(scratch, "out_ZS"), tmp_pts2)
        # populate polyline with elevation value from out_ZS
        with arcpy.da.UpdateCursor(polyline, out_field) as Ucursor:
            for Urow in Ucursor:
                with arcpy.da.SearchCursor(tmp_pts2, 'RASTERVALU') as Scursor:
                    for Srow in Scursor:
                        Urow[0] = Srow[0]
                        Ucursor.updateRow(Urow)


        # delete temp fcs, tbls, etc.
        items = [tmp_pts, tmp_pts2, tmp_buff, out_ZS]
        for item in items:
            arcpy.Delete_management(item)

    # run zSeg function for start/end of each network segment
    log.info('extracting elevation at start of polyline...')
    zSeg('START', 'el_1')
    log.info('extracting elevation at end of polyline...')
    zSeg('END', 'el_2')

    # calculate slope
    log.info('calculating length...')
    arcpy.AddField_management(polyline, "length", "DOUBLE")
    arcpy.CalculateField_management(polyline, "length", '!shape.length@meters!', "PYTHON_9.3")
    log.info('calculating slope...')
    arcpy.AddField_management(polyline, "slope", "DOUBLE")
    with arcpy.da.UpdateCursor(polyline, ["el_1", "el_2", "length", "slope"]) as cursor:
        for row in cursor:
            row[3] = (abs(row[0] - row[1]))/row[2]
            if row[3] == 0.0:
                row[3] = 0.0001
            cursor.updateRow(row)
    log.info('added min and max elevation, length, and slope to polyline')
# Run CL_attributes for thalweg to get channel slope and valley bottom centerline to get valley slope 
# thalwegs for DCEs
log = Logger('DCE CL_attributes')
for DCE in DCE_list:
    CL_attributes(os.path.join(DCE, 'thalwegs.shp'), DEM, project_path)
    log.info('channel slope and length calculated')
# vb_centerline
log = Logger('RS CL_attributes')
CL_attributes(os.path.join(RS_folder, "vb_centerline.shp"), DEM, project_path)
log.info('valley slope and length calculated')



log = Logger('calculate attributes')
# Add and calculate fields for valley bottom shapefile
valley_bottom = os.path.join(RS_folder, 'valley_bottom.shp')
log.info('calculating valley area...')
arcpy.AddField_management(valley_bottom, 'area', 'DOUBLE')
fields = ['area', 'SHAPE@AREA']
with arcpy.da.UpdateCursor(valley_bottom, fields) as cursor:
    for row in cursor:
        row[0] = row[1]
        cursor.updateRow(row)

# Add and calculate fields for DCE shapefiles
for DCE in DCE_list:
    # inundation
    log.info('calculating inundatioin areas and perimeters...')
    inundation = os.path.join(DCE, 'inundation.shp')
    arcpy.AddField_management(inundation, 'area', 'DOUBLE')
    arcpy.AddField_management(inundation, 'perimeter', 'DOUBLE')
    fields = ['area', 'perimeter', 'SHAPE@AREA', 'SHAPE@LENGTH']
    with arcpy.da.UpdateCursor(inundation, fields) as cursor:
        for row in cursor:
            row[0] = row[2]
            row[1] = row[3]
            cursor.updateRow(row)
    # dam crests
    log.info('calculating dam crest lengths...')
    dam_crests = os.path.join(DCE, 'dam_crests.shp')
    arcpy.AddField_management(dam_crests, 'length', 'DOUBLE')
    fields = ['length', 'SHAPE@LENGTH']
    with arcpy.da.UpdateCursor(dam_crests, fields) as cursor:
        for row in cursor:
            row[0] = row[1]
            cursor.updateRow(row)








# Calculate integrated valley width and integrated wetted width
#def intWidth_fn(polygon, polyline):
    #arrPoly = arcpy.da.FeatureClassToNumPyArray(polygon, ['SHAPE@AREA'])
    #arrPolyArea = arrPoly['SHAPE@AREA'].sum()
    #arrCL = arcpy.da.FeatureClassToNumPyArray(polyline, ['SHAPE@LENGTH'])
    #arrCLLength = arrCL['SHAPE@LENGTH'].sum()
    #intWidth = round(arrPolyArea / arrCLLength, 1)
    #return intWidth











