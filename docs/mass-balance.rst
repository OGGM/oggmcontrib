.. _mass-balance:

Adding a mass-balance model
---------------------------

In this exemple, we demonstrate how to provide an independant mass-balance
model to OGGM. The example code can be found in `oggmcontrib/mbmod.py`_.

In order to be used by the dynamical model, the mass-balance model must comply
to a relatively simple interface:

- it must return the mass-balance as a function of time and altitude
- it must comply yo the units needed by the ice dynamics model: meters of ice
  per second

The time-step at which the dynamical model requires mass-balance is a user
parameter, and the current default is at annual time steps. Previous studies
and experience shows that coupling the ice dynamics and mass-balance models
at more frequent time steps is not necessary. **It doesn't mean, however,
that the mass-balance model cannot compute the mass-balance at shorter time
intervals:** the interface just has to integrate the mass-balance over a year
before giving it to the dynamical model.

In the provided example, we compute a linear mass-balance profile
as a function of a randomly chosen equilibrium line altitude.

.. _oggmcontrib/mbmod.py: https://github.com/OGGM/oggmcontrib/blob/master/oggmcontrib/mbmod.py


Apply our new model to Hintereisferner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython:: python
   :suppress:

   fpath = "_code/prepro_mb.py"
   with open(fpath) as f:
      code = compile(f.read(), fpath, 'exec')
      exec(code)

Let's apply the standard OGGM workflow to our glacier:

.. literalinclude:: _code/prepro_mb.py

This was all OGGM stuff. Now, let's define our own model for this glacier:


.. ipython:: python

    from oggmcontrib.mbmod import RandomLinearMassBalance
    mbmod = RandomLinearMassBalance(gdir, seed=0, sigma_ela=200)

The ELA will vary randomly with a standard deviation of 200 m. What does that
mean for the glacier? Let's compute the specific mass-balance integrated over
the flowline glacier:

.. ipython:: python

    heights, widths = gdir.get_inversion_flowline_hw()
    smb = mbmod.get_specific_mb(heights, widths, year=np.arange(50))
    plt.figure(figsize=(7, 4));
    plt.plot(smb, label='Specific MB (mm we yr$^{-1}$)');
    @savefig plot_smb_ts.png width=80%
    plt.legend();

These are variations in the same order of magnitude as observed
`in the last 60+ years`_, with the difference that they are rather positive,
not negative.

.. _in the last 60+ years: http://wgms.ch/products_ref_glaciers/hintereisferner-alps/

Let's give this mass-balance model to the OGGM glacier dynamics model and run
it for 300 years:

.. ipython:: python

   from oggm.core.flowline import flowline_model_run
   flowline_model_run(gdir, mb_model=mbmod, ys=0, ye=300);

The model stored its output in standard NetCDF files. Let's just have a look
a it!

.. ipython:: python

    import xarray as xr
    ds = xr.open_dataset(gdir.get_filepath('model_diagnostics'))
    (ds.volume_m3 * 1e-9).plot();
    plt.ylabel('Glacier volume (km$^{3}$)');
    @savefig plot_volume_ts.png width=80%
    plt.title('Volume of Hintereisferner under random mass-balance forcing');
