.. _inversion-task:

Adding an ice thickness inversion task
======================================

This example illustrates the concept of `entity tasks`_ by implementing
a new task for the ice thickness inversion. We are therefore using
the OGGM preprocessing workflow only, and add our own tool on top of it.

The new task is called ``distributed_vas_thickness`` and is very simple:
with a baseline volume obtained from volume area scaling, we distribute the
local ice thickness so that the ice gets thicker as a function of the
distance to the boundaries, and so that the total volume is conserved.

The implementation can be found in `oggmcontrib/tasks.py`_. This module contains
two functions: a helper function called ``distance_from_border`` and the
actual task ``distributed_vas_thickness``.

Have a short look at the code in `oggmcontrib/tasks.py`_ before going on.

**Entity tasks** in OGGM allow only one single argument: a `GlacierDirectory`_
instance, which gives access to all the input files in the working directory.
Tasks can have as many keyword arguments as you wish, though. They can return
data (useful for testing), but in order to fit in the stop/restart workflow
of OGGM they should write their output in the working directory though. Here
we use an existing NetCDF file and add the output of our function to it.

The last element that makes of a function a real "entity task" for OGGM is the
addition of the ``@entity_task`` decorator on top of it. If you are not used
to python decorators, don't worry: just keep in mind that these decorators are
here for three major purposes:

- logging
- error handling (if your task raises an error on certain glaciers, OGGM might
  choose to ignore it if the user wants it that way)
- multi-processing (by complying to a certain syntax, tasks cn be sent to
  OGGM's task manager)

.. _entity tasks: http://oggm.readthedocs.io/en/latest/api.html#entity-tasks
.. _oggmcontrib/tasks.py: https://github.com/OGGM/oggmcontrib/blob/master/oggmcontrib/tasks.py
.. _GlacierDirectory: http://oggm.readthedocs.io/en/latest/generated/oggm.GlacierDirectory.html#oggm.GlacierDirectory


Apply our new task to a single glacier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython:: python
   :suppress:

   fpath = "_code/prepro_invert.py"
   with open(fpath) as f:
      code = compile(f.read(), fpath, 'exec')
      exec(code)

Let's use our usual test glacier for this:

.. literalinclude:: _code/prepro_invert.py

This was all OGGM stuff. Now let's use our new task on this preprocessed data:

.. ipython:: python
   :suppress:

   fpath = "_code/apply_invert_1.py"
   with open(fpath) as f:
      code = compile(f.read(), fpath, 'exec')
      exec(code)

.. literalinclude:: _code/apply_invert_1.py


And plot it:

.. ipython:: python

   plt.figure(figsize=(7, 4));
   plt.imshow(out_thick);
   @savefig plot_thick_1.png width=80%
   plt.colorbar(label='Thick [m]');


We can use the keyword arguments just like a regular function of course:

.. ipython:: python
   :suppress:

   fpath = "_code/apply_invert_2.py"
   with open(fpath) as f:
      code = compile(f.read(), fpath, 'exec')
      exec(code)

.. literalinclude:: _code/apply_invert_2.py

.. ipython:: python

   plt.figure(figsize=(7, 4));
   plt.imshow(out_thick);
   @savefig plot_thick_2.png width=80%
   plt.colorbar(label='Thick [m]');


Apply our new task in parallel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython:: python
   :suppress:

   fpath = "_code/prepro_invert_multi.py"
   with open(fpath) as f:
      code = compile(f.read(), fpath, 'exec')
      exec(code)

Let's go big, and apply our task to the selections of glaciers in the
Öztal Alps:

.. literalinclude:: _code/prepro_invert_multi.py

Define a simple function to plot them:

.. ipython:: python
   :suppress:

   fpath = "_code/invert_multi_plotfunc.py"
   with open(fpath) as f:
      code = compile(f.read(), fpath, 'exec')
      exec(code)

.. literalinclude:: _code/invert_multi_plotfunc.py


Let's go:

.. ipython:: python


   f, axs = plt.subplots(3, 3, figsize=(7, 7));
   for gdir, ax in zip(gdirs[:9], np.array(axs).flatten()):
      plot_inversion(gdir, ax)
   @savefig plot_thick_all.png width=100%
   plt.tight_layout();
