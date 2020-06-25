Tilings GUI
===========

A graphical interface for `Tilings`_.

Install and run
---------------

With poetry
~~~~~~~~~~~

Start by installing `Poetry`_. You can add it to path and if you prefer,
make it create virtual environments in the project directory.

.. code:: sh

   source $HOME/.poetry/env
   poetry config virtualenvs.in-project true

Then run.

.. code:: sh

   poetry install

You can use the ``--no-dev`` flag to avoid installing dev dependencies.
Finally run

.. code:: sh

   poetry run tilingsgui

Without poetry
~~~~~~~~~~~~~~

Alternatively the dependencies can be installed manually.

.. code:: sh

   pip install tilings
   pip install pyglet
   pip install pyperclip

Then run

.. code:: sh

   python -m tilingsgui.main

Note for Linux
~~~~~~~~~~~~~~

Pyperclip requires clipboard tools that might not come pre-installed.

.. code:: sh

   sudo apt-get install xclip

Without them the app still works but pasting won’t.

User manual
-----------

Basis input
~~~~~~~~~~~

Cell insertion
~~~~~~~~~~~~~~
img test.... |add_custom| ...sadfsadf

Factor
~~~~~~

Place points
~~~~~~~~~~~~

Partially place points
~~~~~~~~~~~~~~~~~~~~~~

Fusion
~~~~~~

Undo and redo
~~~~~~~~~~~~~

Row column separation
~~~~~~~~~~~~~~~~~~~~~

Obstruction transitivity
~~~~~~~~~~~~~~~~~~~~~~~~

Export
~~~~~~

Sequence
~~~~~~~~

Shading
~~~~~~~

Pretty points
~~~~~~~~~~~~~

Show localized
~~~~~~~~~~~~~~

Show crossing
~~~~~~~~~~~~~

Highlight hovered cell
~~~~~~~~~~~~~~~~~~~~~~

.. _Tilings: https://github.com/PermutaTriangle/Tilings
.. _Poetry: https://python-poetry.org/docs/#installation

.. |add_point| image:: resources/img/svg/add_point.svg
   :scale: 100 %
   :alt: img-error

.. |add_custom| image:: resources/img/svg/add_custom.svg
   :scale: 100 %
   :alt: img-error

.. |export| image:: resources/img/svg/export.svg
   :scale: 100 %
   :alt: img-error

.. |factor| image:: resources/img/svg/factor.svg
   :scale: 100 %
   :alt: img-error

.. |factor_int| image:: resources/img/svg/factor_int.svg
   :scale: 100 %
   :alt: img-error

.. |fusion_c| image:: resources/img/svg/fusion_c.svg
   :scale: 100 %
   :alt: img-error

.. |fusion_comp_c| image:: resources/img/svg/fusion_comp_c.svg
   :scale: 100 %
   :alt: img-error

.. |fusion_comp_r| image:: resources/img/svg/fusion_comp_r.svg
   :scale: 100 %
   :alt: img-error

.. |fusion_r| image:: resources/img/svg/fusion_r.svg
   :scale: 100 %
   :alt: img-error

.. |htc| image:: resources/img/svg/htc.svg
   :scale: 100 %
   :alt: img-error

.. |move| image:: resources/img/svg/move.svg
   :scale: 100 %
   :alt: img-error

.. |obstr-trans| image:: resources/img/svg/obstr-trans.svg
   :scale: 100 %
   :alt: img-error

.. |place_east| image:: resources/img/svg/place_east.svg
   :scale: 100 %
   :alt: img-error

.. |place_north| image:: resources/img/svg/place_north.svg
   :scale: 100 %
   :alt: img-error

.. |place_south| image:: resources/img/svg/place_south.svg
   :scale: 100 %
   :alt: img-error

.. |place_west| image:: resources/img/svg/place_west.svg
   :scale: 100 %
   :alt: img-error

.. |pplace_east| image:: resources/img/svg/pplace_east.svg
   :scale: 100 %
   :alt: img-error

.. |pplace_north| image:: resources/img/svg/pplace_north.svg
   :scale: 100 %
   :alt: img-error

.. |pplace_south| image:: resources/img/svg/pplace_south.svg
   :scale: 100 %
   :alt: img-error

.. |pplace_west| image:: resources/img/svg/pplace_west.svg
   :scale: 100 %
   :alt: img-error

.. |pretty| image:: resources/img/svg/pretty.svg
   :scale: 100 %
   :alt: img-error

.. |redo| image:: resources/img/svg/redo.svg
   :scale: 100 %
   :alt: img-error

.. |rowcolsep| image:: resources/img/svg/rowcolsep.svg
   :scale: 100 %
   :alt: img-error

.. |sequence| image:: resources/img/svg/sequence.svg
   :scale: 100 %
   :alt: img-error

.. |shading| image:: resources/img/svg/shading.svg
   :scale: 100 %
   :alt: img-error

.. |show_cross| image:: resources/img/svg/show_cross.svg
   :scale: 100 %
   :alt: img-error

.. |show_local| image:: resources/img/svg/show_local.svg
   :scale: 100 %
   :alt: img-error

.. |str| image:: resources/img/svg/str.svg
   :scale: 100 %
   :alt: img-error

.. |undo| image:: resources/img/svg/undo.svg
   :scale: 100 %
   :alt: img-error

.. |verification| image:: resources/img/svg/verification.svg
   :scale: 100 %
   :alt: img-error
