Tilings GUI
===========

A graphical interface for `Tilings`_.

Install and run
---------------

.. code:: sh

   pip install tilingsgui
   tilingsgui

Note for Linux
~~~~~~~~~~~~~~

Pyperclip requires clipboard tools that might not come pre-installed.

.. code:: sh

   sudo apt-get install xclip

Without them the app still works but pasting won’t.

Known issues
------------
* Exporting places the json in the package directory.

Report a bug
~~~~~~~~~~~~
Along with the description of the bug, please provide a json of the tiling which is exportable in the gui.

User manual
-----------

Summary
~~~~~~~
* |add_point| Point insertion
* |add_custom| Permutation insertion
* |export| Export
* |factor| Factor
* |factor_int| Factor with interleaving
* |fusion_c| Fusion with column set
* |fusion_r| Fusion with row set
* |fusion_comp_c| Component fusion with column set
* |fusion_comp_r| Component fusion with row set
* |htc| Highlight hovered cell
* |move| Move
* |obstr_trans| Obstruction transitivity
* |place_east| East placement
* |place_north| North placement
* |place_south| South placement
* |place_west| West placement
* |pplace_east| East partial placement
* |pplace_north| North partial placement
* |pplace_south| South partial placement
* |pplace_west| West partial placement
* |pretty| Pretty points
* |undo| Undo
* |redo| Redo
* |rowcolsep| Row column separation
* |sequence| Sequece
* |shading| Shading
* |show_cross| Show crossing
* |show_local| Show localized
* |str| Print
* |verification| Verification

Tiling input
~~~~~~~~~~~~
The input box directly above the tiling canvas can be used to create an initial tiling. It accepts both strings and json, using ``from_string`` and ``from_json`` respectively. A right click activates it. To confirm your input, press enter or click away from the text box. Escape cancels the input. Right clicking when activated will paste whatever is on the clipboard.

**Example**:
The following two inputs are two ways of producing the same initial tiling.

.. code::

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
There are two types of factorization, factor |factor| and factor with interleaving |factor_int|. In both cases they are applied to the cell that is clicked. Two active cells are in the same factor if they are in the same row or column, or they share an obstruction or a requirement. For factoring with interleaving, two non-empty cells are in the same factor if they share an obstruction or a requirement.

Place points
~~~~~~~~~~~~
By clicking a point of a requirement, we pass its gridded permutation along with its index within it to ``place_point_of_gridded_permutation`` and the direction set by the button chosen, east |place_east|, north |place_north|, south |place_south| or west |place_west|.

.. code:: python

   def place_point_of_gridded_permutation(
           self, gp: GriddedPerm, idx: int, direction: int
       ) -> "Tiling":
           """
           Return the tiling where the directionmost occurrence of the idx point
           in the gridded permutaion gp is placed.
           """

Partially place points
~~~~~~~~~~~~~~~~~~~~~~
By clicking a point of a requirement, we pass its gridded permutation along with its index within it to ``partial_place_point_of_gridded_permutation`` and the direction set by the button chosen, east |pplace_east|, north |pplace_north|, south |pplace_south| or west |pplace_west|.

.. code:: python

    def partial_place_point_of_gridded_permutation(
        self, gp: GriddedPerm, idx: int, direction: int
    ) -> "Tiling":
        """
        Return the tiling where the directionmost occurrence of the idx point
        in the gridded permutaion gp is placed. The point is placed onto its
        own row or own column depending on the direction.
        """

Fusion
~~~~~~
Let ``c_r`` and ``c_c`` be the row and column respectively of the clicked cell. There are 4 types of fusions available. Fusion with ``row=c_r``, |fusion_r|, fusion with ``col=c_c``, |fusion_c|, component fusion with ``row=c_r``, |fusion_comp_r|, and component fusion with ``col=c_c``, |fusion_comp_c|. If the fusion are invalid, then exceptions are caught and nothing happens. 

Fusion:

.. code:: python

   """
   Fuse the tilings.
   If `row` is not `None` then `row` and `row+1` are fused together.
   If `col` is not `None` then `col` and `col+1` are fused together.
   """

Component fusion:

.. code:: python

   """
   Fuse the tilings in such a way that it can be unfused by drawing a line between skew/sum-components.
   If `row` is not `None` then `row` and `row+1` are fused together.
   If `col` is not `None` then `col` and `col+1` are fused together.
   """

Undo and redo
~~~~~~~~~~~~~
Given that there are previously drawn tilings, then undo, |undo|, will redraw the one before the last action. If you wish to revert the undo, you can use redo, |redo|. There is a limit on how many tilings are stored in memory.

Row column separation
~~~~~~~~~~~~~~~~~~~~~
|rowcolsep| splits the row and columns of a tilings using the inequalities implied by the length two obstructions.

Obstruction transitivity
~~~~~~~~~~~~~~~~~~~~~~~~
|obstr_trans| adds length 2 obstructions to the tiling using transitivity over positive cells.

Export
~~~~~~
Export, |export|, will store the current tiling in memory and upon closing the app, will add all stored tilings in the session to ``./export/history.json``. There is a session limit so the file become too large. If the session limit is reached, than adding more will remove the oldest. The format of the json can be seen below with time and tiling values empty.

.. code:: JSON

  [
    {
      "session_time": "",
      "tilings": [
        {
          "tiling_time": "",
          "tiling": {}
        },
        {
          "tiling_time": "",
          "tiling": {}
        }
      ]
    },
    {
      "session_time": "",
      "tilings": [
        {
          "tiling_time": "",
          "tiling": {}
        }
      ]
    }
  ]

Print
~~~~~
Writing the current tiling to ``stdout``, |str|, will produce both the ``__str__`` and ``__repr__`` representation of the tiling. An example output is shown below.

.. code:: sh

   +-+-+-+
   | |●| |
   +-+-+-+
   |1| |1|
   +-+-+-+
   1: Av(021)
   ●: point
   Crossing obstructions:
   01: (0, 0), (2, 0)
   Requirement 0:
   0: (1, 1)

   Tiling(obstructions=(GriddedPerm(Perm((0,)), ((0, 1),)), GriddedPerm(Perm((0,)), ((1, 0),)), GriddedPerm(Perm((0,)), ((2, 1),)), GriddedPerm(Perm((0, 1)), ((0, 0), (2, 0))), GriddedPerm(Perm((0, 1)), ((1, 1), (1, 1))), GriddedPerm(Perm((1, 0)), ((1, 1), (1, 1))), GriddedPerm(Perm((0, 2, 1)), ((0, 0), (0, 0), (0, 0))), GriddedPerm(Perm((0, 2, 1)), ((2, 0), (2, 0), (2, 0)))), requirements=((GriddedPerm(Perm((0,)), ((1, 1),)),),), assumptions=())

Sequence
~~~~~~~~
The first few terms of the sequence of gridded permutations griddable on the current tiling can be written to ``stdout``, |sequence|, where for example the following tiling

.. code:: sh

   +-+-+-+-+
   | |●| | |
   +-+-+-+-+
   |1| |1| |
   +-+-+-+-+
   | | | |●|
   +-+-+-+-+
   | | |1| |
   +-+-+-+-+
   1: Av(021)
   ●: point
   Crossing obstructions:
   01: (0, 2), (2, 2)
   01: (2, 0), (2, 2)
   Requirement 0:
   0: (1, 3)
   Requirement 1:
   0: (3, 1)

would produce this output.

.. code:: sh

   [0, 0, 1, 3, 9, 28, 90, 297]

Shading
~~~~~~~
With shading on, |shading|, then a 1 restriction is not drawn as a point but rather as a filled cell.

Pretty points
~~~~~~~~~~~~~
With pretty points on, |pretty|, then 12 and 21 restrictions along with a 1 requirement within the same cell are drawn as a single point.

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

.. |add_point| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/add_point.svg
   :scale: 200 %
   :alt: img-error

.. |add_custom| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/add_custom.svg
   :scale: 200 %
   :alt: img-error

.. |export| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/export.svg
   :scale: 200 %
   :alt: img-error

.. |factor| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/factor.svg
   :scale: 200 %
   :alt: img-error

.. |factor_int| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/factor_int.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_c| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/fusion_c.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_comp_c| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/fusion_comp_c.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_comp_r| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/fusion_comp_r.svg
   :scale: 200 %
   :alt: img-error

.. |fusion_r| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/fusion_r.svg
   :scale: 200 %
   :alt: img-error

.. |htc| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/htc.svg
   :scale: 200 %
   :alt: img-error

.. |move| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/move.svg
   :scale: 200 %
   :alt: img-error

.. |obstr_trans| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/obstr_trans.svg
   :scale: 200 %
   :alt: img-error

.. |place_east| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/place_east.svg
   :scale: 200 %
   :alt: img-error

.. |place_north| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/place_north.svg
   :scale: 200 %
   :alt: img-error

.. |place_south| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/place_south.svg
   :scale: 200 %
   :alt: img-error

.. |place_west| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/place_west.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_east| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/pplace_east.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_north| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/pplace_north.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_south| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/pplace_south.svg
   :scale: 200 %
   :alt: img-error

.. |pplace_west| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/pplace_west.svg
   :scale: 200 %
   :alt: img-error

.. |pretty| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/pretty.svg
   :scale: 200 %
   :alt: img-error

.. |redo| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/redo.svg
   :scale: 200 %
   :alt: img-error

.. |rowcolsep| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/rowcolsep.svg
   :scale: 200 %
   :alt: img-error

.. |sequence| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/sequence.svg
   :scale: 200 %
   :alt: img-error

.. |shading| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/shading.svg
   :scale: 200 %
   :alt: img-error

.. |show_cross| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/show_cross.svg
   :scale: 200 %
   :alt: img-error

.. |show_local| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/show_local.svg
   :scale: 200 %
   :alt: img-error

.. |str| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/str.svg
   :scale: 200 %
   :alt: img-error

.. |undo| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/undo.svg
   :scale: 200 %
   :alt: img-error

.. |verification| image:: https://raw.githubusercontent.com/PermutaTriangle/tilingsgui/develop/tilingsgui/resources/img/svg/verification.svg
   :scale: 200 %
   :alt: img-error
