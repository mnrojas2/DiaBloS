Using DiaBloS: Begginer's Guide
===============================

Interface
---------

After loading the package, a window similar like the following figure will show::

.. image:: images/screenshot.png


+-----+-------------------------+
| Nro | What is it              |
+=====+=========================+
| (1) | Bar function            |
+-----+-------------------------+
| (a) | NEW                     |
+-----+-------------------------+
| (b) | LOAD                    |
+-----+-------------------------+
| (c) | SAVE                    |
+-----+-------------------------+
| (d) | PLAY Simulation         |
+-----+-------------------------+
| (e) | PAUSE Simulation        |
+-----+-------------------------+
| (f) | STOP Simulation         |
+-----+-------------------------+
| (g) | PLOT Graph              |
+-----+-------------------------+
| (h) | Screen CAPTURE          |
+-----+-------------------------+
| (2) | Blocks Menu             |
+-----+-------------------------+
| (3) | Canvas                  |
+-----+-------------------------+


#. How to remove all elements in the canvas.
    To remove all elements, press the NEW icon (1a).

#. How to add blocks.
    To add a block, drag and drop any block from the Block Menu (2) to the canvas (3).

    <image>

#. How to remove blocks.
    To remove a block, drag and drop it outside the canvas. Also you can select it with LMB, then press the DELETE key.

    <image>

#. How to add lines.
    To add a line, click on two block ports to generate a link between both.

    It's important to note that a link between ports only can be created if one port is labeled as input (ports located
    at the left side of a block) and the other is labeled as output (ports located at the left side of a block).

    Also, if an input port has already a link with another port you cannot create another link. However this restriction
    does not apply to output ports.

    Each port in the blocks has a unique identification. The input ports are always on the left side of the blocks,
    while the output ports are on the right side of the blocks. Between ports of the same type, they are differentiated
    according to their position from top to bottom starting from zero. e.g, a 3-input Adder block has inputs identified
    as :math:`i = {0, 1, 2}` and a single output identified as :math:`o = {0}`.

    <image>

#. How to remove lines.
    To remove a line select it with LMB, then press the DELETE key.

    When blocks are removed, the associated lines are also removed, in order to free connections that no longer make
    logical sense (input or output port does not exist).

    <image>

#. How to change color of the line.
    A particular feature of the lines is that you can change their color. To do this, select the line and then press
    the UP_ARROW or DOWN_ARROW keys continuously until you find the color to choose.

#. How to change parameters.
    If the block contains editable function parameters, you can open a window to modify them by pressing RMB on the block.

    It is important to be careful to enter the parameters in the correct formats. These can be strings, boolean (as
    text), or floats (ints are converted to floats).

#. How to change port numbers.
    If a block allows changing the number of ports, a window can be opened with CTRL + RMB, with one or more entries to
    change the number of inputs and outputs, written as ints.

#. How to load/save files.
    The saving format of these files is .dat. It can be opened with any text editor to look and edit its data as wanted.

    To save a file, just click on the SAVE icon (1c), where a window will open giving the options of saving location
    and file name.

    <image>

    To load a file, just click on the LOAD icon (1b), which will open a window giving the options to locate the file by
    folder and file name.

    <image>

#. How to run simulation.
    To run the simulation, first press the PLAY icon (1d). A window will appear, to set the simulation time, the
    sampling time, as well as settings for the signal plotting: the size of the window in dynamic mode, and activate or
    deactivate the dynamic mode. Then press OK and the simulation will start and continue running until the sampling
    time is reached or stopped by pressing the STOP icon (1f).

    The process can be paused by pressing the PAUSE icon (1e). To restart it back, just press the PAUSE icon a second time.

    <image>

#. How to plot data.
    To plot the curves of a simulation it is necessary to add Scope blocks and connect them to the output signals to be
    observed.

    The Scope block contains a single parameter called 'labels' which is used to name the signal(s) to be plotted. If
    this parameter is not changed, the observed signals will be named by default as 'Scope-<n>', where 'n' corresponds
    to the location of the variable within the input vector to the Scope block.

    In addition, dynamic plotting (plotting the data while the simulation is running), can be enabled or disabled.
    To do this, when starting a simulation (by pressing the PLAY icon (1d)), there is an option that allows enabling
    this feature as another that allows changing the size of the moving window that will show the plotted values over
    time.

    If the simulation is finished, the graph with all the data can be seen by pressing the PLOT icon (1g). If dynamic
    plotting has been performed, first close the first window with the resulting graph and then reopen it by pressing
    the PLOT button.

    <image>

#. How to export data.
    To export data, the process is similar to plotting.

    First an EXPORT block must be added, which must be connected to the output of the block from which the signal is
    wanted to be saved.

    The labels can be renamed to identify each of the vectors. Otherwise they will be called by default as
    'ExportData-<n>', where 'n' corresponds to the location of the variable within the input vector to the Export block.

    <image>

#. How to load user-made functions.
    DiaBloS allows the loading of external functions, created by the user.

    To load these type of functions, a Block block must be added, where the only parameter to modify is the name of the
    file, that contains the user-made function, located in the 'usermodels/' folder.

    If the upload is correct, the block will update its name at the bottom, the ports and the color in the canvas. If
    something went wrong, the program will indicate that the function name does not exist or something wrong was found
    during the process.

    More details about how to create these types of functions are available in
    :ref:`"Creating new functions"<developer:creating new functions>` section from developer's guide.

#. How to take a capture of the canvas.
    Press the CAPTURE icon (1h) to take a capture of the screen. These get saved in the 'captures/' folder.

#. Some shortcuts
    ::

        Ctrl + N: New
        Ctrl + A: Load
        Ctrl + S: Save
        Ctrl + E: Play Simulation
        Ctrl + P: Take Capture

First Experience
----------------

#. Load the interface.

#. Press the OPEN icon.

#. Go to examples/ and open basic_example.dat.

#. You will see something like the following picture::

    .. image:: images/screenshot.png

#. Select the blue block (Step) and open the parameters' menu pressing RMB over the block.

#. Change the "value" parameter from "1.0" to "2.5" and change the "delay" parameter to "5.0" seconds, then press OK.

#. Select the red block (Scope) and open the parameters' menu pressing RMB over the block.

#. Change the "labels" parameter from "default" to "step", then press OK.

#. Press the PLAY icon to open the simulation pop-up window.

#. Change the "Simulation time" parameter to "10.0" (seconds).

#. Set "Dynamic Plot" as ON, then press OK.

#. Wait until the simulation is done.

#. Close the plot window.

#. Press the PLOT icon to open the plot window to observe the complete graph.

#. You will see something like the following picture::

    .. image:: images/screenshot.png


.. raw:: latex

    \newpage