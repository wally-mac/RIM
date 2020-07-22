# Name:     GDAL DEM Geographic
#
# Author:   Philip Bailey
#
# Date:     9 October 2019
#
# Purpose:  Perform GDAL DEM operations on rasters that are in geographic coordinates
#           by first calculating the z-factor using the haversine equation.
#
#           https://gdal.org/programs/gdaldem.html
#           https://rosettacode.org/wiki/Haversine_formula#Python
#           https://www.esri.com/arcgis-blog/products/product/imagery/setting-the-z-factor-parameter-correctly/
# -------------------------------------------------------------------------------
import argparse
import os
from math import radians, cos, sin, asin, sqrt, degrees
import gdal
from lib.loghelper import Logger


def gdal_dem_geographic(dem_raster, output_raster, operation):
    """Perform GDAL DEM operation on raster in geographic coordinates

    Arguments:
        dem_raster {string} -- Path to DEM raster
        output_raster {string} -- Path to output raster that will get created
        operation {string} -- GDAL DEM operation: hillshade,slope,color-relief,TRI,TPI,roughness
    """
    log = Logger('GDAL DEM')

    zfactor = __get_zfactor(dem_raster)
    log.info("Creating '{}' raster from: {}".format(operation, dem_raster))
    gdal.DEMProcessing(output_raster, dem_raster, operation, scale=zfactor, creationOptions=["COMPRESS=DEFLATE"])


def __get_zfactor(dem):
    """Calculate the Z factor for a raster by measuring the height of a raster
    in degrees and then use the haversine to calculate the same length in metres.
    The result is the ratio of these two numbers.

    Arguments:
        dem {string} -- Raster path

    Returns:
        float -- Z factor to be used by the GDAL DEM operation
    """

    src = gdal.Open(dem)
    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    src = None

    length_km = haversine(uly, ulx, lry, ulx)
    length_deg = uly - lry
    zfactor = (length_km * 1000) / length_deg
    src = None
    return zfactor


def haversine(lat1, lon1, lat2, lon2):
    """[summary]
    Great circle distance calculation
    https://rosettacode.org/wiki/Haversine_formula#Python
    Arguments:
        lat1 {[type]} -- [description]
        lon1 {[type]} -- [description]
        lat2 {[type]} -- [description]
        lon2 {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    R = 6372.8  # Earth radius in kilometers

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))

    return R * c


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('dem', help='Input DEM raster path', type=argparse.FileType('r'))
    parser.add_argument('output', help='Output raster', type=str)
    parser.add_argument('operation', help='hillshade,slope,color-relief,TRI,TPI,roughness')
    args = parser.parse_args()

    gdal_dem_geographic(args.dem.name, args.output, args.operation)


if __name__ == '__main__':
    main()
