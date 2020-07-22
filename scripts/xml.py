import argparse
import sys
import os
from settings import ModelConfig

cfg = ModelConfig('http://xml.riverscapes.xyz/Projects/XSD/V1/RSContext.xsd')

def create_project(huc, output_dir, site_name, image_date):

    project_name = site_name
    project = RSProject(cfg, output_dir)
    project.create(project_name, 'RIM')

    project.add_project_meta({
        'HUC{}'.format(len(huc)): str(huc),
        'site_name': site_name,
        'date_created': datetime.datetime.now().isoformat()
    })

    inputs = project.XMLBuilder.add_sub_element(project.XMLBuilder.root, 'Inputs')
    realizations = project.XMLBuilder.add_sub_element(project.XMLBuilder.root, 'Realizations')
    rs_context = project.XMLBuilder.add_sub_element(realizations, 'RS_Context', None, {
        'id': 'RS_01',
        'evidence_used': 'DEM, hillshade, vegetation',
        'Mapper': mapper,
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version
    })
    dce = project.XMLBuilder.add_sub_element(realizations, 'DCE', None, {
        'id': 'DCE_01',
        'image_date': image_date
        'dateCreated': datetime.datetime.now().isoformat(),
        'guid': str(uuid.uuid1()),
        'productVersion': cfg.version
    })
    project.XMLBuilder.add_sub_element(dce, 'Name', image_date)

    project.XMLBuilder.write()
    return project, realization