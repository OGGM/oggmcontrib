.. image:: _static/logo.png

|

This repository shows how you can develop
an external module for OGGM and keep control over it without having to
put your code on the main OGGM repository.

Why would I want to do that?
----------------------------

Ideally, we would have your module added to the main codebase: this ensures
consistency of the code and continuous testing. However, there are several
reasons why making your own repository could be useful:

- complying to OGGM's strict testing rules can be annoying, especially in the
  early stages of development of a model
- with you own repository you have full control on it's development while
  still being able to use the OGGM workflow and multiprocessing capabilities
- with an external module the users who will use your model *will* have
  to download it from here and you can make sure that correct attribution
  is made to your work, i.e. by specifying that using this module requires a
  reference to a specific scientific publication
- if your funding agency requires you to have your own public website
- etc.

Before writing your own module we recommend to contact us to discuss the best
path to follow in your specific case.

How does this module work?
--------------------------

This module is a template. It implements two very simple use cases:
- adding a new "bed inversion" task based on volume-area-scaling but using the
  OGGM preprocessing workflow
- using a custom mass-balance model and apply it to OGGM's ice-dynamics model

You can install this custom module with:

     pip install git+https://github.com/OGGM/dummy-module.git

However, what you'd probably like to do is to `fork <https://help.github.com/articles/fork-a-repo/>`_ this repository and use
it as a template for your own project. You can install it locally with

    pip install -e .


Get in touch
------------

- View the source code `on GitHub`_.
- Report bugs or share your ideas on the `issue tracker`_.
- Improve the model by submitting a `pull request`_.
- Or you can always send us an `e-mail`_ the good old way.

.. _e-mail: info@oggm.org
.. _on GitHub: https://github.com/OGGM/oggm
.. _issue tracker: https://github.com/OGGM/oggm/issues
.. _pull request: https://github.com/OGGM/oggm/pulls
