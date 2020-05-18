
# Import system modules
import arcpy
from arcpy import env
import os
import argparse
#from loghelper import Logger
from create_project import make_folder
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("spatial")


# Set project path
project_path = r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\mill_test_2020_05_07"

# Input the name of the folder of the desired RS Context shapefiles (the folder with the Valley Bottom polygon)
RS_folder_name = "RS_01"

# Input the name of the folder of the desired DCEs for the analysis
DCE1_name = "DCE_01"
DCE2_name = "DCE_02"

########

#log = Logger('set paths')

# Set internal paths
map_folder = os.path.join(project_path, '02_Mapping')
RS_folder = os.path.join(map_folder, RS_folder_name)
DCE1 = os.path.join(map_folder, DCE1_name)
DCE1 = os.path.join(map_folder, DCE1_name)

#log.info('paths set for DCEs of interest')

#######
# Calculate reach and valley slope with DEM, Thalweg, and VB_Centerline

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
    drop = ["el_max", "el_min", "length", "slope"]
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
        arcpy.Buffer_analysis(tmp_pts, tmp_buff, '10 Meters')
        # get min dem z value within each buffer
        arcpy.AddField_management(polyline, out_field, "DOUBLE")
        out_ZS = arcpy.sa.ZonalStatistics(tmp_buff, "FID", DEM, "MINIMUM", "NODATA")
        out_ZS.save(os.path.join(scratch, "out_ZS"))
        tmp_pts2 = os.path.join(scratch, 'tmp_pts2.shp')
        arcpy.sa.ExtractValuesToPoints(tmp_pts, os.path.join(scratch, "out_ZS"), tmp_pts2)
        # populate polyline with elevation value
        with arcpy.da.UpdateCursor(polyline, ["FID", "RASTERVALU"]) as cursor:
            for row in cursor
        

        # delete temp fcs, tbls, etc.
        items = [tmp_pts, tmp_buff]
        #for item in items:
            #arcpy.Delete_management(item)

    # run zSeg function for start/end of each network segment
    zSeg('START', 'el_max')
    zSeg('END', 'el_min')

    # calculate slope
    arcpy.AddField_management(polyline, "length", "DOUBLE")
    arcpy.CalculateField_management(polyline, "length", '!shape.length@meters!', "PYTHON_9.3")
    arcpy.AddField_management(polyline, "slope", "DOUBLE")
    with arcpy.da.UpdateCursor(polyline, ["el_max", "el_min", "length", "slope"]) as cursor:
        for row in cursor:
            row[3] = (abs(row[0] - row[1]))/row[2]
            if row[3] == 0.0:
                row[3] = 0.0001
            cursor.updateRow(row)


polyline=r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\mill_test_2020_05_07\02_Mapping\RS_01\vb_centerline.shp"
DEM=r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\mill_test_2020_05_07\01_Inputs\02_Topo\DEM_01\DEM.tif"
scratch=r"C:\Users\A02295870\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\Mill_Creek\mill_test_2020_05_07"

CL_attributes(polyline, DEM, scratch)





