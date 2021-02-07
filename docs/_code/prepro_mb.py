import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import oggm
from oggm import cfg, tasks
from oggm.utils import get_demo_file
from oggm import workflow

# Set up the input data for this example
cfg.initialize()
cfg.PATHS['working_dir'] = oggm.utils.get_temp_dir('oggmcontrib_mb')
cfg.PATHS['dem_file'] = get_demo_file('srtm_oetztal.tif')
cfg.PATHS['climate_file'] = get_demo_file('histalp_merged_hef.nc')
cfg.set_intersects_db(get_demo_file('rgi_intersect_oetztal.shp'))

# Set up the run parameters
cfg.PARAMS['baseline_climate'] = 'CUSTOM'
cfg.PARAMS['run_mb_calibration'] = True
cfg.PARAMS['border'] = 80
cfg.PARAMS['use_multiprocessing'] = True

# Glacier directory for Hintereisferner in Austria
entity = gpd.read_file(get_demo_file('Hintereisferner_RGI5.shp')).iloc[0]
gdir = oggm.GlacierDirectory(entity)

# The usual OGGM preprecessing
tasks.define_glacier_region(gdir, entity=entity)
workflow.gis_prepro_tasks(gdir)
workflow.climate_tasks(gdir)
workflow.inversion_tasks(gdir)
tasks.init_present_time_glacier(gdir)
