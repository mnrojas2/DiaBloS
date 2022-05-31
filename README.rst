SimuSnide
=========

INSTALLATION
============

You will need the following packages (pip installation recommended):

- pygame
- numpy
- matplotlib
- json
- tkinter
- tqdm
- pyqtgraph
- functools

On CMD or Terminal write::

pip install pygame numpy matplotlib json tkinter tqdm pyqtgraph functools

::

KEYS AND SHORTCUTS
==================

Basics
------

1) Ctrl + N: New
#) Ctrl + A: Open
#) Ctrl + G: Save
#) Ctrl + E: Simulate

Blocks
------

1) RMB over block menu (left list): Create a block
#) Ctrl + RMB over block: Input/Output menu (if applicable)
#) Ctrl + LMB over block: Parameters/Attributes menu
#) LMB over block: move the block

Tips:

a) Input dots (drain ports) are always on the left side of the block
#) Output dots (source ports) are always on the right side of the block
#) To delete a block, first select it with LMB, then press DEL.

Lines
-----

1) Press LMB on two block ports to create a line.
2) While selected you can change the colorline with UP_arrow or DOWN_arrow

Tips:

a) Beware these ports can only connect if one of them is a source port and the other one a drain port.
#) A drain port can only connect with one source port, but you can connect multiple drain ports to the same source port.
#) To delete a line, first select it with LMB, then press DEL.

FIRST EXPERIENCE
----------------

1) Load data.txt to see a basic graph
#) Press 'Simulate' or 'Ctrl+E' to execute the graph

