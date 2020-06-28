import arcpy
import os
from create_project import make_folder


arcpy.Dissolve_management(r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\TEST\Bear_river_BRAT.shp", r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\TEST\dissolve.shp", '', 'MEAN')