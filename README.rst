==================================================================================
<SimuSnide> - A graphical programming library/tool for dynamical systems in Python
==================================================================================

.. note::

    Work in progress.

.. contents::

INSTALLATION
============

You will need the following packages::

    - pygame (>=2.1.2)
    - numpy (>=1.22.3)
    - matplotlib (>=3.5.2)
    - tqdm (>=4.64.0)
    - pyqtgraph (>=0.12.3)

To install the packages you can use pip (recommended)::

    pip install pygame numpy matplotlib tk tqdm pyqtgraph

You will also need these packages, but they should come with Python 3.9.7 by default::

    - os
    - importlib
    - json
    - tkinter (tk)
    - functools
    - copy
    - time


KEYS, SHORTCUTS AND TIPS
========================

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

Diagram simulation
------------------

Before executing the diagram, beware of the following issues or the simulation won't start:

1) All ports from all blocks must be connected.
#) Beware of algebraic loops in the diagram.
#) If working with vectors, be sure all parameters/arguments will be consistent with their inputs and outputs.

Some Block arguments
--------------------

1) Specific argument values::

    Step.type: 'up', 'down'
    Integrator.method: 'FWD_RECT', 'BWD_RECT', 'TUSTIN', 'RK45'

#) Value arguments can be written in the following ways (if allowed)::

    Gain.gain: a
    Gain.gain: [[a, b],[c, d]] *with {a,b,c,d} = float/int type.


#) Nametype arguments::

    Scope.labels: "name,name2,..." (without quotation marks)
    Export.str_name: "name,name2,name3,..." (without quotation marks)


Loading external .py functions
------------------------------

This tool allows external loading of functions by using the block "Block".

1) The name of the file and main function (executing function) must be the same.
#) The file must be inside the 'external' folder.
#) The '_init_' function is used to assign parameters/arguments, block type, input/output values and color.
#) Libraries used to execute that block in particular must be added in that '.py' file only.
#) There are two examples to help program these blocks 'my_function_src' and 'my_function_mid'.
#) There are two simulation examples to execute these files, 'external_source.dat' and 'external_middle.dat'.

FIRST EXPERIENCE
================

1) Press 'Load' or 'Ctrl+A' to open a file
#) Go to saves/ folder and open basic-example.dat.
#) You will see a simple diagram with one Step block and one Scope block
#) Optional: Press "Dyn Plot" to enable the dynamic plot mode.
#) Press 'Simulate' or 'Ctrl+E' to execute the graph.
#) A pop-up will appear letting you change some values before executing.
#) Optional: Change the simulation time.
#) Optional: Change the sampling rate.
#) Optional: Change the window size for the dynamic plot.
#) Accept your changes.
#) Save the diagram. (Could be with the same filename or a different one).
#) The program will start reading and executing the diagram showing a bar in the terminal.
