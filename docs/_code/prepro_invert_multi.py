# Read in the RGI file
rgi_file = get_demo_file('rgi_oetztal.shp')
rgidf = gpd.read_file(rgi_file)

# Use multiprocessing to apply the OGGM tasks and the new task to all glaciers
from oggm import workflow
gdirs = workflow.init_glacier_regions(rgidf)
workflow.execute_entity_task(tasks.glacier_masks, gdirs)
# Yes, also your new task!
workflow.execute_entity_task(distributed_vas_thickness, gdirs)
