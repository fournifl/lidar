from pathlib import Path
import argparse
import geopandas as gpd
import yaml

def get_params():

    # construct an argument parser
    parser = argparse.ArgumentParser()

    # add argument to the parser
    parser.add_argument('config')

    # get arguments
    args = vars(parser.parse_args())
    config_file = args['config']
    with open(config_file, 'r') as yaml_file:
        params = yaml.safe_load(yaml_file)
    litto3d_path = Path(params['litto3d_path'])
    roi = Path(params['roi'])
    outdir = Path(params['outdir'])
    epsg_in = params['epsg_in']
    epsg_out = params['epsg_out']
    return litto3d_path, roi, outdir, epsg_in, epsg_out



# execution parameter
extract = True

# read yaml parameters
litto3d_path, roi_file, outdir, epsg_in, epsg_out = get_params()

# read roi
roi = gpd.read_file(roi_file)

# gather rasters

# apply roi

# save to ascii file


