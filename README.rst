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

On CMD or Terminal write::

    pip install pygame numpy matplotlib json tkinter tqdm pyqtgraph

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

Diagram simulation
------------------

Before executing the diagram, beware of the following issues or the simulation won't start:

1) All ports from all blocks must be connected.
#) Beware of algebraic loops in the diagram.
#) If working with vectors, be sure all parameters/arguments will be consistent with their inputs and outputs.


FIRST EXPERIENCE
----------------

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


Some Block arguments
--------------------

1) Specific argument values ::

    Step.type: 'up', 'down'
    Integrator.method: 'FWD_RECT', 'BWD_RECT', 'TUSTIN', 'RK45'

#) Value arguments can be written in the following ways (if allowed) ::

    Gain.gain: a
    Gain.gain: [[a, b],[c, d]]


#) Nametype arguments ::

    Scope.labels: "name,name2,..." (without quotation marks)
    Export.str_name: "name,name2,name3,..." (without quotation marks)

::
