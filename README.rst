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

Known issues
-----------
* Pressing enter adds an additional char to input boxes on macs

Report a bug
~~~~~~~~~~~
Along with the description of the bug, please provide a json of the tiling which is exportable in the gui.

User manual
-----------

Tiling input
~~~~~~~~~~~
The input box directly above the tiling canvas can be used to create an initial tiling. It accepts both strings and json, using ``from_string`` and ``from_json`` respectively. A right click activates it. To confirm your input, press enter or click away from the text box. Escape cancels the input. Right clicking when activated will paste whatever is on the clipboard.

**Example**:
The following two inputs are two ways of producing the same initial tiling.

.. code:: none

   1432_12345
   
   {"class_module": "tilings.tiling", "comb_class": "Tiling", "obstructions": [{"patt": [0, 3, 2, 1], "pos": [[0, 0], [0, 0], [0, 0], [0, 0]]}, {"patt": [0, 1, 2, 3, 4], "pos": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]}], "requirements": [], "assumptions": []}
   
The initial tiling in question would be the following.

.. code:: sh

   +-+
   |1|
   +-+
   1: Av(0321, 01234)
   

Cell insertion
~~~~~~~~~~~~~~
To insert a permutation into a single cell, one can choose either to add a point, |add_point|, or a custom permutation, |add_custom|. For the latter, the latest confirmed input in the text box above the button grid is used. The text box works just like the one for inputting tilings. It uses ``to_standard`` to convert the input to a permutation. After having selected the permutation to insert, then clicking a cell will insert it. Left click inserts it as a requirement while a right click inserts it as a obstruction, using ``add_single_cell_requirement`` and ``add_single_cell_obstruction`` respectively.

Factor
~~~~~~
|factor| |factor_int|

Place points
~~~~~~~~~~~~
|place_east| |place_north| |place_south| |place_west|

Partially place points
~~~~~~~~~~~~~~~~~~~~~~
|pplace_east| |pplace_north| |pplace_south| |pplace_west|

Fusion
~~~~~~
|fusion_r| |fusion_c|
|fusion_comp_r| |fusion_comp_c| 

Undo and redo
~~~~~~~~~~~~~
Given that there are previously drawn tilings, then undo, |undo|, will redraw the one before the last action. If you wish to revert the undo, you can use redo, |redo|. There is a limit on how many tilings are stored in memory.

Row column separation
~~~~~~~~~~~~~~~~~~~~~
|rowcolsep|

Obstruction transitivity
~~~~~~~~~~~~~~~~~~~~~~~~
|obstr-trans|

Export
~~~~~~
|export|

Print
~~~~~
|str|

Sequence
~~~~~~~~
|sequence|

Shading
~~~~~~~
|shading|

Pretty points
~~~~~~~~~~~~~
|pretty|

Show localized
~~~~~~~~~~~~~~
With localized shown, |show_local|, requirements and obstructions that are contained in a single cell are shown. Without it they are not.

Show crossing
~~~~~~~~~~~~~
With crossing shown, |show_cross|, requirements and obstructions that reach across different cells are shown. Without it they are not.

Highlight hovered cell
~~~~~~~~~~~~~~~~~~~~~~
Turning on the hovered cell highlighting, |htc|, obstructions in the hovered cell are colored differently.

Verification
~~~~~~~~~~~~
Given a tiling ``t``, the verification button, |verification|, will produce the following result.

.. code:: python

   [
      BasicVerificationStrategy().verified(t),
      DatabaseVerificationStrategy().verified(t),
      ElementaryVerificationStrategy().verified(t),
      InsertionEncodingVerificationStrategy().verified(t),
      LocallyFactorableVerificationStrategy().verified(t),
      LocalVerificationStrategy(no_factors=False).verified(t),
      MonotoneTreeVerificationStrategy().verified(t),
      OneByOneVerificationStrategy().verified(t)
   ]

An example output is shown below.

.. code:: sh

   BasicVerificationStrategy             : True
   DatabaseVerificationStrategy          : False
   ElementaryVerificationStrategy        : False
   InsertionEncodingVerificationStrategy : True
   LocallyFactorableVerificationStrategy : False
   LocalVerificationStrategy             : True
   MonotoneTreeVerificationStrategy      : False
   OneByOneVerificationStrategy          : True


.. _Tilings: https://github.com/PermutaTriangle/Tilings
.. _Poetry: https://python-poetry.org/docs/#installation

.. |add_point| image:: resources/img/svg/add_point.svg
   :scale: 200 %
   :alt: img-error

.. |add_custom| image:: resources/img/svg/add_custom.svg
   :scale: 200 %
   :alt: img-error

.. |export| image:: resources/img/svg/export.svg
   :scale: 200 %
   :alt: img-error

.. |factor| image:: resources/img/svg/factor.svg
   :scale: 200 %
   :alt: img-error

.. |factor_int| image:: resources/img/svg/factor_int.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_c| image:: resources/img/svg/fusion_c.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_comp_c| image:: resources/img/svg/fusion_comp_c.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_comp_r| image:: resources/img/svg/fusion_comp_r.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_r| image:: resources/img/svg/fusion_r.svg
   :scale: 200 %
   :alt: img-error

.. |htc| image:: resources/img/svg/htc.svg
   :scale: 200 %
   :alt: img-error

.. |move| image:: resources/img/svg/move.svg
   :scale: 200 %
   :alt: img-error

.. |obstr-trans| image:: resources/img/svg/obstr-trans.svg
   :scale: 200 %
   :alt: img-error

.. |place_east| image:: resources/img/svg/place_east.svg
   :scale: 200 %
   :alt: img-error

.. |place_north| image:: resources/img/svg/place_north.svg
   :scale: 200 %
   :alt: img-error

.. |place_south| image:: resources/img/svg/place_south.svg
   :scale: 200 %
   :alt: img-error

.. |place_west| image:: resources/img/svg/place_west.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_east| image:: resources/img/svg/pplace_east.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_north| image:: resources/img/svg/pplace_north.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_south| image:: resources/img/svg/pplace_south.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_west| image:: resources/img/svg/pplace_west.svg
   :scale: 200 %
   :alt: img-error

.. |pretty| image:: resources/img/svg/pretty.svg
   :scale: 200 %
   :alt: img-error

.. |redo| image:: resources/img/svg/redo.svg
   :scale: 200 %
   :alt: img-error

.. |rowcolsep| image:: resources/img/svg/rowcolsep.svg
   :scale: 200 %
   :alt: img-error

.. |sequence| image:: resources/img/svg/sequence.svg
   :scale: 200 %
   :alt: img-error

.. |shading| image:: resources/img/svg/shading.svg
   :scale: 200 %
   :alt: img-error

.. |show_cross| image:: resources/img/svg/show_cross.svg
   :scale: 200 %
   :alt: img-error

.. |show_local| image:: resources/img/svg/show_local.svg
   :scale: 200 %
   :alt: img-error

.. |str| image:: resources/img/svg/str.svg
   :scale: 200 %
   :alt: img-error

.. |undo| image:: resources/img/svg/undo.svg
   :scale: 200 %
   :alt: img-error

.. |verification| image:: resources/img/svg/verification.svg
   :scale: 200 %
   :alt: img-error
