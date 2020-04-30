import os
import argparse

# function to define folder with template shapefiles

def folder(output_path):
    
    inundation_template = os.path.join(output_path, 'inundation.shp')
    print(inundation_template)
    
    dam_crests_template = os.path.join(output_path, 'dam_crests.shp')
    print(dam_crests_template)

    valleybottom_template = os.path.join(output_path, 'valley_bottom.shp')
    print(valleybottom_template)

    vbcenterline_template = os.path.join(output_path, 'vb_centerline.shp')
    print(vbcenterline_template)

    thalwegs_template = os.path.join(output_path, 'thalwegs.shp')
    print(thalwegs_template)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('output_path', help='folder path with template shapefiles', type=str)
    args = parser.parse_args()
    
    folder(args.output_path)
    
if __name__ == "__main__":
   main()     

