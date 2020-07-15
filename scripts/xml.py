import os
import arcpy
import sys
import XMLBuilder
reload(XMLBuilder)
XMLBuilder = XMLBuilder.XMLBuilder

def write_xml(project_root, proj_name, huc_ID, image_destinations,
              dem_destinations, valley_bottom_destinations, beaver_dams_destinations):
    """
    Writes and populates the entire XML document for the project.
    :param project_path: The folder for the whole project
    :param proj_name: The name for the project given by the user
    :param huc_ID: The HUC ID given by the user

    :param image_destinations: A path to all image files
    :param dem_destinations: A path to all DEM files

    :param valley_bottom_destinations: A path to all valley bottom files

    :param beaver_dams_destinations: A path to all beaver dam files

    :return:
    """

    xml_file = project_root + "\project.rs.xml"
    if os.path.exists(xml_file):
        os.remove(xml_file)

    new_xml_file = XMLBuilder(xml_file, "Project", [("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance"),
                                                    ("xsi:noNamespaceSchemaLocation","https://raw.githubusercontent.com/Riverscapes/Program/master/Project/XSD/V1/Project.xsd")])
    if proj_name is None:
        proj_name = os.path.basename(project_root)
    new_xml_file.add_sub_element(new_xml_file.root, "Name", proj_name)
    new_xml_file.add_sub_element(new_xml_file.root, "ProjectType", "RIM")

    add_metadata(new_xml_file, huc_ID)

    add_inputs(project_root, new_xml_file, image_destinations,
               dem_destinations, valley_bottom_destinations, beaver_dams_destinations)

    new_xml_file.write()

def add_inputs(project_root, new_xml_file, image_destinations, dem_destinations, valley_bottom_destinations, beaver_dams_destinations, perennial_stream_destinations):
    """
    Calls write_xml_for_destination for each input and creates a sub element for inputs
    :param project_root: The folder for the whole project
    :param new_xml_file: The new XML file created in write_xml
    :param hist_veg_destinations: A path to all historic vegetation files
    :param network_destinations: A path to all network files
    :param dem_destinations: A path to all DEM files
    :param landuse_destinations: A path to all landuse files
    :param valley_bottom_destinations: A path to all valley bottom files
    :param road_destinations: A path to all road files
    :param rr_destinations: A path to all rail road files
    :param canal_destinations: A path to all canal files
    :param ownership_destinations: A path to all land ownership files
    :param beaver_dams_destinations: A path to all beaver dam files
    :param perennial_stream_destinations: A path to all perennial network files
    :return:
    """
    inputs_element = new_xml_file.add_sub_element(new_xml_file.root, "Inputs")

    write_xml_for_destination(network_destinations, new_xml_file, inputs_element, "Vector", "NETWORK", "Segmented Network", project_root)
    write_xml_for_destination(dem_destinations, new_xml_file, inputs_element, "Raster", "DEM", "DEM", project_root)

    write_xml_for_destination(valley_bottom_destinations, new_xml_file, inputs_element, "Vector", "VALLEY", "Valley Bottom", project_root)

    write_xml_for_destination(beaver_dams_destinations, new_xml_file, inputs_element, "Vector", "BEAVER_DAM", "Beaver Dam", project_root)
    write_xml_for_destination(perennial_stream_destinations, new_xml_file, inputs_element, "Vector", "PERENNIAL_STREAM", "Perennial Stream", project_root)

def write_xml_element_with_path(xml_file, base_element, xml_element_name, item_name, path, project_root, xml_id=None):
    """
    :param xml_file:
    :param base_element:
    :param xml_element_name:
    :param xml_id:
    :param item_name:
    :param path:
    :param project_root:
    :return:
    """
    if xml_id is None:
        new_element = xml_file.add_sub_element(base_element, xml_element_name, tags=[("guid", getUUID())])
    else:
        new_element = xml_file.add_sub_element(base_element, xml_element_name, tags=[("guid", getUUID()), ("id", xml_id)])

    xml_file.add_sub_element(new_element, "Name", item_name)
    relative_path = find_relative_path(path, project_root)
    xml_file.add_sub_element(new_element, "Path", relative_path)

def write_xml_for_destination(destination, new_xml_file, base_element, xml_element_name, xml_id_base, item_name,
                              project_root):
    """
    Adds all data for one destination into the XML doc
    :param destination: The destination for all of the data to be added
    :param new_xml_file: The new XML file created in write_xml
    :param base_element: The element that all of the data will be put into
    :param xml_element_name: The type of element, either "Vector" or "Raster"
    :param xml_id_base: The unique ID base for each input
    :param item_name: The item name for the input
    :param project_root: The folder containing all BRAT data, provided by the user
    :return:
    """
    for i in range(len(destination)):
        str_i = str(i + 1)
        if i < 10:
            str_i = '0' + str_i
        str_i = '_' + str_i
        write_xml_element_with_path(new_xml_file, base_element, xml_element_name, item_name,
                                    destination[i], project_root, xml_id_base + str_i)

    for i in range(len(destination)):
        str_i = str(i + 1)
        if i < 10:
            str_i = '0' + str_i
        str_i = '_' + str_i
        write_xml_element_with_path(new_xml_file, base_element, xml_element_name, item_name,
                                    destination[i], project_root, xml_id_base + str_i)

def add_metadata(new_xml_file, huc_ID):
    """
    Writes the metadata elements
    :param new_xml_file:
    :param huc_ID:
    :param watershed_name:
    :return:
    """
    metadata_element = new_xml_file.add_sub_element(new_xml_file.root, "MetaData")
    new_xml_file.add_sub_element(metadata_element, "Meta", huc_ID, [("name","HUCID")])
