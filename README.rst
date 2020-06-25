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
asdfa |add_custom| adsfsadf

.. |add_custom| image:: resources/img/svg/add_custom.svg
   :scale: 100 %
   :alt: img-error
   :align: middle

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