import geopandas as gpd
import oggm
from oggm import cfg, tasks
from oggm.utils import get_demo_file

# Set up the input data for this example
cfg.initialize()
cfg.PATHS['working_dir'] = oggm.utils.get_temp_dir('oggm_wd')
cfg.PATHS['dem_file'] = get_demo_file('srtm_oetztal.tif')
cfg.set_intersects_db(get_demo_file('rgi_intersect_oetztal.shp'))

# Glacier directory for Hintereisferner in Austria
entity = gpd.read_file(get_demo_file('Hintereisferner_RGI5.shp')).iloc[0]
gdir = oggm.GlacierDirectory(entity)

# The usual OGGM preprecessing
tasks.define_glacier_region(gdir, entity=entity)
tasks.glacier_masks(gdir)
