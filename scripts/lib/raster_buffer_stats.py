# Name:     Raster buffer statistics
#
# Purpose:  Loops over all features in a feature class, buffers those features by
#           a distance and obtains the values from an underlying raster. The raster
#           values are reclassified using a column from a lookup CSV and then the
#           mean of the reclassified values is written back to the feature class.
#
# Author:   Philip Bailey
#
# Date:     15 May 2019
#
# Notes:    Raster extraction using polygon and Rasterio
#           https://gis.stackexchange.com/questions/260304/extract-raster-values-within-shapefile-with-pygeoprocessing-or-gdal
#
#           Rasterio projection and shapes not intersecting raster
#           https://gis.stackexchange.com/questions/303089/masking-geotiff-file-after-geojson-through-rasterio-input-shapes-do-not-overl
# -------------------------------------------------------------------------------
import argparse
import os
import sys
import traceback
import json
import csv
from lib.util import ProgressBar
from osgeo import ogr
from shapely.geometry import shape
from osgeo import osr
from lib.loghelper import Logger
import rasterio
from rasterio.mask import mask
import numpy as np
import gdal


def raster_buffer_stats(network, raster, buffer_dist, lookup, lookupcol, outputcol):
    """
    Loops over all features in a feature class, buffers those features by
    a distance and obtains the values from an underlying raster. The raster
    values are reclassified using a column from a lookup CSV and then the
    mean of the reclassified values is written back to the feature class.
    :param network: Polyline feature class
    :param raster: Raster whose values will be used
    :param buffer_dist: Distance to buffer features in the network feature class
    :param lookup: CSV file containing values to reclassify the raster
    :param lookupcol: column in the lookup CSV containing the values to be assigned to the raster
    :param outputcol: Attribute field that will be added to the network containing the results
    :return: None
    """

    log = Logger("Buffer Stats")
    log.info('Buffer {}m'.format(buffer_dist))
    log.info("Loading network from {0}".format(network))

    # Get the input NHD flow lines layer
    driver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = driver.Open(network, 1)
    inLayer = inDataSource.GetLayer()
    networkSRS = inLayer.GetSpatialRef()
    lyrDefn = inLayer.GetLayerDefn()

    # Load the vegetation lookup from CSV and then reclass the array values
    log.info('Reclassify veg from column "VALUE" to "{}" using {}'.format(lookupcol, lookup))
    reclass = load_reclassification(lookup, lookupcol)

    # Delete output column from network ShapeFile if it exists and then recreate it
    for fieldidx in range(0, lyrDefn.GetFieldCount()):
        if lyrDefn.GetFieldDefn(fieldidx).GetName().lower() == outputcol.lower():
            log.info('Deleting existing output field "{}" in network ShapeFile.'.format(outputcol))
            inLayer.DeleteField(fieldidx)
            break

    log.info('Creating output field "{}" in network ShapeFile.'.format(outputcol))
    inLayer.CreateField(ogr.FieldDefn(outputcol, ogr.OFTReal))

    # temporarily open the raster and verify that the spatial reference matches the Shape File
    rasterDS = gdal.Open(raster)
    rasterSRS = osr.SpatialReference(wkt=rasterDS.GetProjection())

    if not networkSRS.IsSame(rasterSRS):
        log.info('Raster spatial Reference: {}'.format(rasterSRS))
        log.info('Network spatial Reference: {}'.format(networkSRS))
        raise Exception('The network spatial reference are not the same.')

    rasterDS = None

    # Open the raster and then loop over all polyline features
    with rasterio.open(raster) as src:
        log.info('Looping over {:,} features in network ShapeFile...'.format(inLayer.GetFeatureCount()))

        progbar = ProgressBar(inLayer.GetFeatureCount(), 50, "Buffer Stats")
        counter = 0

        for feature in inLayer:
            counter += 1
            progbar.update(counter)
            # print('ReachID {}'.format(feature.GetField('ReachID')))

            # get a Shapely representation of the line and then buffer it
            featobj = json.loads(feature.ExportToJson())
            polyline = shape(featobj['geometry']) if not featobj["geometry"] is None else None
            polygon = polyline.buffer(buffer_dist)

            # retrieve an array for the cells under the polygon
            raw_raster, out_transform = mask(src, [polygon], crop=True)
            mask_raster = np.ma.masked_values(raw_raster, src.nodata)
            # print(mask_raster)

            # Reclass the raster to dam suitability. Loop over present values for performance
            for oldvalue in np.unique(mask_raster):
                if oldvalue is not np.ma.masked:
                    if oldvalue in reclass:
                        mask_raster[mask_raster == oldvalue] = reclass[oldvalue]
                    else:
                        log.warning('Missing vegetation reclassification for value {}'.format(oldvalue))
                        mask_raster[mask_raster == oldvalue] = np.nan

            # print(mask_raster)
            avg = mask_raster.mean() if mask_raster.sum() > 0 else 0
            feature.SetField(outputcol, avg)
            inLayer.SetFeature(feature)
        progbar.finish()

    log.info('Process completed successfully.')


def raster_buffer_stats2(polygons, raster):

    log = Logger('Buffer Stats')

    # Open the raster and then loop over all polyline features
    results = {}
    with rasterio.open(raster) as src:
        log.info('Looping over {:,} polygon features...'.format(len(polygons)))

        progbar = ProgressBar(len(polygons), 50, "Buffer Stats")
        counter = 0

        for reach_id, polygon in polygons.items():
            counter += 1
            progbar.update(counter)
            # print('ReachID {}'.format(feature.GetField('ReachID')))

            # retrieve an array for the cells under the polygon
            raw_raster, out_transform = mask(src, [polygon], crop=True)
            mask_raster = np.ma.masked_values(raw_raster, src.nodata)
            # print(mask_raster)

            mean = None
            maximum = None
            minimum = None

            if not mask_raster.mask.all():
                mean = mask_raster.mean()
                maximum = float(mask_raster.max())
                minimum = float(mask_raster.min())

            results[reach_id] = {'Mean': mean, 'Maximum': maximum, 'Minimum': minimum}
        progbar.finish()
    log.info('Process completed successfully.')
    return results


def main():
    # parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('network', help='Output network ShapeFile path', type=argparse.FileType('r'))
    parser.add_argument('vegraster', help='Original vegetation raster', type=argparse.FileType('r'))
    parser.add_argument('buffer', help='Distance in map units to buffer the network', type=int)
    parser.add_argument('lookupcsv', help='CSV file containing the vegetation lookup', type=argparse.FileType('r'))
    parser.add_argument('lookupcol', help='Column in the vegetation lookup CSV with the reclassification.', type=str)
    parser.add_argument('outputcol', help='Output attribute column that will be added to the network ShapeFile.', type=str)
    parser.add_argument('--verbose', help='(optional) verbose logging mode', action='store_true', default=False)

    args = parser.parse_args()

    # Initiate the log file
    logg = Logger("{} Veg Stats".format(args.buffer))
    logfile = os.path.join(os.path.dirname(args.network.name), "raster_buffer_stats.log")
    logg.setup(logPath=logfile, verbose=args.verbose)

    try:
        raster_buffer_stats(args.network.name, args.vegraster.name, args.buffer, args.lookupcsv.name, args.lookupcol, args.outputcol)

    except Exception as e:
        logg.error(e)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
