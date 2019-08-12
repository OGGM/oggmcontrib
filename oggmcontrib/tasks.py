""" Tasks available in the oggmcontrib package

"""
import logging
import warnings
import numpy as np
import netCDF4
import pandas as pd
import geopandas as gpd
import shapely.geometry as shpg
import salem
from scipy.ndimage import binary_erosion
from scipy.ndimage.morphology import distance_transform_edt

from oggm.utils import entity_task

# Module logger
log = logging.getLogger(__name__)


def distance_from_border(gdir,  sqrt=False):
    """Computes a normalized distance from border mask.

    It is a bit cleverer than just taking the glacier outlines: we also
    consider where the glacier has neighbors.

    Parameters
    ----------
    gdir : oggm.GlacierDirectory
        the working glacier directory
    sqrt : bool, optional
        whether the square root of the distance mask should be used or not

    Returns
    -------
    the distance
    """

    # Variables
    grids_file = gdir.get_filepath('gridded_data')
    with netCDF4.Dataset(grids_file) as nc:
        glacier_mask = nc.variables['glacier_mask'][:]

    # Glacier exterior including nunataks
    erode = binary_erosion(glacier_mask)
    glacier_ext = glacier_mask ^ erode
    glacier_ext = np.where(glacier_mask == 1, glacier_ext, 0)

    # Intersects between glaciers
    gdfi = gpd.GeoDataFrame(columns=['geometry'])
    if gdir.has_file('intersects'):
        # read and transform to grid
        gdf = gdir.read_shapefile('intersects')
        salem.transform_geopandas(gdf, gdir.grid, inplace=True)
        gdfi = pd.concat([gdfi, gdf[['geometry']]])

    dx = gdir.grid.dx

    # Here we check which grid points are on ice divides
    # Probably not the fastest way to do this, but it works
    dist = np.array([])
    jj, ii = np.where(glacier_ext)
    for j, i in zip(jj, ii):
        dist = np.append(dist, np.min(gdfi.distance(shpg.Point(i, j))))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        pok = np.where(dist <= 1)
    glacier_ext_intersect = glacier_ext * 0
    glacier_ext_intersect[jj[pok], ii[pok]] = 1

    # Scipy does the job
    dis_from_border = 1 + glacier_ext_intersect - glacier_ext
    dis_from_border = distance_transform_edt(dis_from_border) * dx
    dis_from_border[np.where(glacier_mask == 0)] = np.NaN

    # Square?
    if sqrt:
        dis_from_border = np.sqrt(dis_from_border)

    # We normalize and return
    return dis_from_border / np.nansum(dis_from_border)


# An entity task decorator is what allows this task to work like other
# OGGM tasks. What's happening inside is your job!
# Here we document our task by saying that it will write in the gridded_data
# file, but this is not required
@entity_task(log, writes=['gridded_data'])
def distributed_vas_thickness(gdir, sqrt=False):
    """Compute a thickness map of the glacier using very simple rules.

    The rules are:
    - the volume of the glacier is obtained from Volume Area Scaling (VAS)
    - the glacier gets thicker as a function of the distance to the outlines.

    Parameters
    ----------
    gdir : oggm.GlacierDirectory
        the working glacier directory
    sqrt : bool, optional
        whether the square root of the distance mask should be used or not
    """

    # Variables
    dis_from_border = distance_from_border(gdir,
                                           sqrt=sqrt)

    # VAS volume in m3
    inv_vol = 0.034 * (gdir.rgi_area_km2**1.375)
    inv_vol *= 1e9

    # Naive thickness
    dx = gdir.grid.dx
    thick = dis_from_border * inv_vol

    # Conserve volume
    thick *= inv_vol / np.nansum(thick * dx**2)

    # Write - we add it to existing netCDF file
    grids_file = gdir.get_filepath('gridded_data')
    with netCDF4.Dataset(grids_file, 'a') as nc:
        vn = 'vas_distributed_thickness'
        if vn in nc.variables:
            v = nc.variables[vn]
        else:
            v = nc.createVariable(vn, 'f8', ('y', 'x', ))
        v.units = 'm'
        v.long_name = 'Local ice thickness'
        v[:] = thick

    return thick
