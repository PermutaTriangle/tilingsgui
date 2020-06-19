============
Tilings GUI
============

***************
Install and run
***************
.. code:: bash

       # Setup poetry 
       curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
       source $HOME/.poetry/env
       poetry config virtualenvs.in-project true

       # Install dependencies
       poetry install

       # Run
       poetry run tilingsgui

or if you have all dependencies installed,

.. code:: bash

       python -m tilingsgui.main

***************
Dependencies
***************
* pyglet
* tilings
* pyperclip
