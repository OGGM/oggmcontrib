import netCDF4

def plot_inversion(gdir, ax):
    """Plot the VAS inversion for this glacier."""

    # Read the data
    grids_file = gdir.get_filepath('gridded_data')
    with netCDF4.Dataset(grids_file) as nc:
        thick = nc.variables['vas_distributed_thickness'][:]

    ax.imshow(thick)
