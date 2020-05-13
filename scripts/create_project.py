import os
import arcpy
import sys

# Make folder function 
# copied from pyBRAT SupportingFunctions.py
def make_folder(path_to_location, new_folder_name):
    """
    Makes a folder and returns the path to it
    :param path_to_location: Where we want to put the folder
    :param new_folder_name: What the folder will be called
    :return: String
    """
    newFolder = os.path.join(path_to_location, new_folder_name)
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
    return newFolder

def make_project(project_path):
    """
    Creates project folders
    :param project_path: where we want project to be located
    """

# set workspace to desired project location
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = project_path

    if not os.path.exists(project_path):
        os.mkdir(project_path)

    # build project folder structure in project path
    # inputs folders
    inputs_folder = make_folder(project_path, "01_Inputs")

    image_folder = make_folder(inputs_folder, "01_Imagery")
    make_folder(image_folder, "AP_01")
    make_folder(image_folder, "AP_02")
    make_folder(image_folder, "AP_03")

    topo_folder = make_folder(inputs_folder, "02_Topo")
    make_folder(topo_folder, "DEM_01")

    context_folder = make_folder(inputs_folder, "03_Context")
    make_folder(context_folder, "BRAT_01")
    make_folder(context_folder, "VBET_01")

    # mapping folder
    # DCE and RS folders are created when a DCE is made
    make_folder(project_path, "02_Mapping")

    # analysis folder
    analysis_folder = make_folder(project_path, "03_Analysis")
    make_folder(analysis_folder, "CDs")
    make_folder(analysis_folder, "Summary")

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('srs_template', help='path to a shapefile with desired output coordinate system', type=str)
    parser.add_argument('project_path', help='path to output folder', type=str)
    args = parser.parse_args()

    make_project(project_path)

#project_path = r"C:\Users\karen\Box\0_ET_AL\NonProject\etal_Drone\2019\Inundation_sites\Utah\rock_creek_b\rock_creek_b"
make_project(project_path)



