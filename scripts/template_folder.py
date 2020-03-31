import os
import argparse

# function to define folder with template shapefiles

def template_folder(template_path):
    
    inundation_template = os.path.join(template_path, 'inundation.shp')
    print(inundation_template)
    
    dam_crests_template = os.path.join(template_path, 'dam_crests.shp')
    print(dam_crests_template)

    valleybottom_template = os.path.join(template_path, 'valley_bottom.shp')
    print(valleybottom_template)

    vbcenterline_template = os.path.join(template_path, 'vb_centerline.shp')
    print(vbcenterline_template)

    thalwegs_template = os.path.join(template_path, 'thalwegs.shp')
    print(thalwegs_template)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('template_path', help='folder path with template shapefiles', type=str)
    args = parser.parse_args()
    
    template_folder(args.template_path)
    
if __name__ == "__main__":
   main()     

