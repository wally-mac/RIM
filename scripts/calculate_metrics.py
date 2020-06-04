# Import system modules
import arcpy
from arcpy import env
import os
import argparse
import numpy
import csv
from loghelper import Logger
from create_project import make_folder
arcpy.env.overwriteOutput = True
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')


# User Inputs
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
out_folder = os.path.join(project_path, '03_Analysis')
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
def intWidth_fn(polygon, polyline):
    arrPoly = arcpy.da.FeatureClassToNumPyArray(polygon, ['SHAPE@AREA'])
    arrPolyArea = arrPoly['SHAPE@AREA'].sum()
    arrCL = arcpy.da.FeatureClassToNumPyArray(polyline, ['SHAPE@LENGTH'])
    arrCLLength = arrCL['SHAPE@LENGTH'].sum()
    intWidth = round(arrPolyArea / arrCLLength, 1)
    print "integrated width =", intWidth
    arcpy.AddField_management(polygon, 'intWidth', 'DOUBLE')
    with arcpy.da.UpdateCursor(polygon, ['intWidth']) as cursor:
        for row in cursor:
            row[0] = intWidth
            cursor.updateRow(row)

log.info('calculating integrated valley width...')
intWidth_fn(valley_bottom, os.path.join(RS_folder, "vb_centerline.shp"))
for DCE in DCE_list:
    log.info('calculating integrated wetted width...')
    intWidth_fn(os.path.join(DCE, 'inundation.shp'), os.path.join(DCE, 'thalwegs.shp'))

# Calculate total inundated area and percent and inundated area and percent by inundation type
def inun_fn(inun_poly, site_poly):
    # calculate inundation areas
    tot_arrPoly = arcpy.da.FeatureClassToNumPyArray(inun_poly, ['SHAPE@AREA', 'type'])
    tot_area = tot_arrPoly['SHAPE@AREA'].sum()
    ff_arrPoly = arcpy.da.FeatureClassToNumPyArray(inun_poly, ['SHAPE@AREA', 'type'], "type = 'free_flowing'")
    ff_area = ff_arrPoly['SHAPE@AREA'].sum()
    pd_arrPoly = arcpy.da.FeatureClassToNumPyArray(inun_poly, ['SHAPE@AREA', 'type'], "type = \'ponded'")
    pd_area = pd_arrPoly['SHAPE@AREA'].sum()
    ov_arrPoly = arcpy.da.FeatureClassToNumPyArray(inun_poly, ['SHAPE@AREA', 'type'], "type = \'overflow'")
    ov_area = ov_arrPoly['SHAPE@AREA'].sum()
    vb_arrArea = arcpy.da.FeatureClassToNumPyArray(site_poly, 'SHAPE@AREA')
    vb_area = vb_arrArea['SHAPE@AREA'].sum()
    # calculate inundation percents
    tot_pct = round((tot_area / vb_area) * 100, 1)
    print "% valley bottom inundation (all types) =", tot_pct
    ff_pct = round((ff_area / vb_area) * 100, 1)
    print "% free flowing =", ff_pct
    pd_pct = round((pd_area / vb_area) * 100, 1)
    print "% ponded =", pd_pct
    ov_pct = round((ov_area / vb_area) * 100, 1)
    print "% overflow =", ov_pct
    arcpy.AddField_management(inun_poly, 'tot_area', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'ff_area', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'pd_area', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'ov_area', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'vb_area', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'tot_pct', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'ff_pct', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'pd_pct', 'DOUBLE')
    arcpy.AddField_management(inun_poly, 'ov_pct', 'DOUBLE')
    with arcpy.da.UpdateCursor(inun_poly, ['tot_area', 'ff_area', 'pd_area', 'ov_area', 'vb_area', 'tot_pct', 'ff_pct', 'pd_pct', 'ov_pct']) as cursor:
        for row in cursor:
            row[0] = tot_area
            row[1] = ff_area
            row[2] = pd_area
            row[3] = ov_area
            row[4] = vb_area
            row[5] = tot_pct
            row[6] = ff_pct
            row[7] = pd_pct
            row[8] = ov_pct
            cursor.updateRow(row)

for DCE in DCE_list:
    log.info('calculating inundation area and percent...')
    print "calculating inundation percents for", DCE, "..."
    inun_fn(os.path.join(DCE, 'inundation.shp'), os.path.join(RS_folder, 'valley_bottom.shp'))

# Calculate dam crest metrics
def dam_crests_fn(crests_line, CL_line):
    # Calculate valley length
    arrCL = arcpy.da.FeatureClassToNumPyArray(CL_line, ['SHAPE@LENGTH'])
    arrCL_len = arrCL['SHAPE@LENGTH'].sum()
    
    # Calculate dam crest to valley length ratio
    crestArr = arcpy.da.FeatureClassToNumPyArray(crests_line, ['SHAPE@LENGTH'])
    crest_lenArr = crestArr['SHAPE@LENGTH'].sum()
    crest_CL_rat = round(crest_lenArr / arrCL_len, 1)
    print "dam crest length (all) : valley length =", crest_CL_rat
    # active dam crest to valley length ratio
    act_crestArr = arcpy.da.FeatureClassToNumPyArray(crests_line, ['SHAPE@LENGTH', 'crest_type'], "crest_type = 'active'")
    act_crest_len = act_crestArr['SHAPE@LENGTH'].sum()
    act_crest_rat = round(act_crest_len / arrCL_len, 1)
    print "active dam crest length : valley length =", act_crest_rat
    # intact dam crest to valley length ratio
    intact_crestArr = arcpy.da.FeatureClassToNumPyArray(crests_line, ['SHAPE@LENGTH', 'dam_state'], "dam_state = 'intact'")
    intact_crest_len = intact_crestArr['SHAPE@LENGTH'].sum()
    intact_crest_rat = round(intact_crest_len / arrCL_len, 1)
    print "intact dam crest length : valley length =", intact_crest_rat

    # Calculate number of dams and dam density
    # Make a layer from the feature class
    arcpy.CopyFeatures_management(crests_line, os.path.join(project_path, 'tmp_dams.shp'))
    tmp_dams = os.path.join(project_path, 'tmp_dams.shp')
    arcpy.MakeFeatureLayer_management(tmp_dams, os.path.join(project_path, 'damsCount_lyr'))
    # Delete identical dam_ID so there is just 1 row per dam
    arcpy.DeleteIdentical_management(os.path.join(project_path, 'damsCount_lyr'), 'dam_id')
    # all dams
    dams_num = int(arcpy.GetCount_management(os.path.join(project_path, 'damsCount_lyr')).getOutput(0))
    print "number of dams =", dams_num
    # dam density in dams/km
    dam_dens = round((dams_num / arrCL_len) * 1000, 1)
    print "dam density (dams/km) =", dam_dens
    # intact
    arcpy.SelectLayerByAttribute_management(os.path.join(project_path, 'damsCount_lyr'), 'NEW_SELECTION', "dam_state = 'intact'")
    intact_num = int(arcpy.GetCount_management(os.path.join(project_path, 'damsCount_lyr')).getOutput(0))
    print "number of intact dams =", intact_num
    # breached
    arcpy.SelectLayerByAttribute_management(os.path.join(project_path, 'damsCount_lyr'), 'NEW_SELECTION', "dam_state = 'breached'")
    breached_num = int(arcpy.GetCount_management(os.path.join(project_path, 'damsCount_lyr')).getOutput(0))
    print "number of breached dams =", breached_num
    # blown_out
    arcpy.SelectLayerByAttribute_management(os.path.join(project_path, 'damsCount_lyr'), 'NEW_SELECTION', "dam_state = 'blown-out'")
    blown_out_num = int(arcpy.GetCount_management(os.path.join(project_path, 'damsCount_lyr')).getOutput(0))
    print "number of blown out dams =", blown_out_num
    # delete temporary dams layer
    arcpy.Delete_management(tmp_dams)

    # Add values to dam_crests attribute table
    arcpy.AddField_management(crests_line, 'width', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'dams_num', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'dam_dens', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'intact_num', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'breach_num', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'blown_num', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'ratio_all', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'ratio_act', 'DOUBLE')
    arcpy.AddField_management(crests_line, 'ratio_int', 'DOUBLE')
    
    with arcpy.da.UpdateCursor(crests_line, ['width', 'dams_num', 'dam_dens', 'intact_num', 'breach_num', 'blown_num', 'ratio_all', 'ratio_act', 'ratio_int', 'SHAPE@LENGTH']) as cursor:
        for row in cursor:
            row[0] = row[9]
            row[1] = dams_num
            row[2] = dam_dens
            row[3] = intact_num
            row[4] = breached_num
            row[5] = blown_out_num
            row[6] = crest_CL_rat
            row[7] = act_crest_rat
            row[8] = intact_crest_rat
            cursor.updateRow(row)

for DCE in DCE_list:
    dam_crests_fn(os.path.join(DCE, 'dam_crests.shp'), os.path.join(RS_folder, 'vb_centerline.shp'))

# Pull attributes from BRAT table

# Estimate bankfull with Beechie equation

# Estimate Error for inundation area

# Add data to csv
for DCE in DCE_list:
    # create output folder
    split = os.path.split(DCE)
    tail = split[1]
    print tail
    output = os.path.join(out_folder, tail)

    # valley bottom 
    nparr = arcpy.da.FeatureClassToNumPyArray(os.path.join(RS_folder, 'valley_bottom.shp'), ['*'])
    field_names = [f.name for f in arcpy.ListFields(os.path.join(RS_folder, 'valley_bottom.shp'))]
    fields_str = ','.join(str(i) for i in field_names)
    numpy.savetxt(output + '/' + '01_Metrics' + '/' + 'valley_bottom' + '_metrics.csv', nparr, fmt="%s", delimiter=",", header=str(fields_str), comments='')
    # valley bottom centerline
    nparr = arcpy.da.FeatureClassToNumPyArray(os.path.join(RS_folder, 'vb_centerline.shp'), ['*'])
    field_names = [f.name for f in arcpy.ListFields(os.path.join(RS_folder, 'vb_centerline.shp'))]
    fields_str = ','.join(str(i) for i in field_names)
    numpy.savetxt(output + '/' + '01_Metrics' + '/' + 'vb_centerline' + '_metrics.csv', nparr, fmt="%s", delimiter=",", header=str(fields_str), comments='')
    # thalweg
    nparr = arcpy.da.FeatureClassToNumPyArray(os.path.join(DCE, 'thalwegs.shp'), ['*'])
    field_names = [f.name for f in arcpy.ListFields(os.path.join(DCE, 'thalwegs.shp'))]
    fields_str = ','.join(str(i) for i in field_names)
    numpy.savetxt(output + '/' + '01_Metrics' + '/' + 'thalwegs' + '_metrics.csv', nparr, fmt="%s", delimiter=",", header=str(fields_str), comments='')
    # inundation
    nparr = arcpy.da.FeatureClassToNumPyArray(os.path.join(DCE, 'inundation.shp'), ['*'])
    field_names = [f.name for f in arcpy.ListFields(os.path.join(DCE, 'inundation.shp'))]
    fields_str = ','.join(str(i) for i in field_names)
    numpy.savetxt(output + '/' + '01_Metrics' + '/' + 'inundation' + '_metrics.csv', nparr, fmt="%s", delimiter=",", header=str(fields_str), comments='')
    # dam crests
    nparr = arcpy.da.FeatureClassToNumPyArray(os.path.join(DCE, 'dam_crests.shp'), ['*'])
    field_names = [f.name for f in arcpy.ListFields(os.path.join(DCE, 'dam_crests.shp'))]
    fields_str = ','.join(str(i) for i in field_names)
    numpy.savetxt(output + '/' + '01_Metrics' + '/' + 'dam_crests' + '_metrics.csv', nparr, fmt="%s", delimiter=",", header=str(fields_str), comments='')

# Make plots

# Make table 







