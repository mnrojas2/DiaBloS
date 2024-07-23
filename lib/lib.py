"""
lib.py - Contains all the core functions and classes for the simulation and execution of the graphs.
"""

import pygame                           # LGPL
import numpy as np                      # Liberal BSD
import copy                             # PSF
import time                             # PSF
import json                             # PSF
import tkinter as tk                    # BSD/PSF
import importlib                        # PSF
import os                               # PSF

from tqdm import tqdm                   # MPLv2.0 MIT
from tkinter import filedialog

import sys                              # PSF
import pyqtgraph as pg                  # MIT
from lib.functions import *

sys.path.append('./usermodels/')


class DSim:
    """
    Class that manages the simulation interface and main functions.

    :param SCREEN_WIDTH: The width of the window
    :param SCREEN_HEIGHT: The height of the window
    :param canvas_top_limit: Top limit where blocks and lines must be drawn.
    :param canvas_left_limit: Left limit where blocks and lines must be drawn.
    :param colors: List of predefined colors for elements that show in the canvas.
    :param fps: Base frames per seconds for pygame's loop.
    :param l_width: Width of the line when a block or a line is selected.
    :param ls_width: Space between a selected block and the line that indicates the former is selected.
    :param filename: Name of the file that was recently loaded. By default is 'data.dat'.
    :param sim_time: Simulation time for graph execution.
    :param sim_dt: Simulation sampling time for graph execution.
    :param plot_trange: Width in number of elements that must be shown when a graph is getting executed with dynamic plot enabled.
    :type SCREEN_WIDTH: int
    :type SCREEN_HEIGHT: int
    :type canvas_top_limit: int
    :type canvas_left_limit: int
    :type colors: dict
    :type fps: int
    :type l_width: int
    :type ls_width: int
    :type filename: str
    :type sim_time: float
    :type sim_dt: float
    :type plot_trange: int

    """

    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        self.canvas_top_limit = 60
        self.canvas_left_limit = 200

        self.colors = {'black': (0, 0, 0),
                       'red': (255, 0, 0),
                       'green': (0, 255, 0),
                       'blue': (0, 0, 255),
                       'yellow': (255, 255, 0),
                       'magenta': (255, 0, 255),
                       'cyan': (0, 255, 255),
                       'purple': (128, 0, 255),
                       'orange': (255, 128, 0),
                       'aqua': (0, 255, 128),
                       'pink': (255, 0, 128),
                       'lime_green': (128, 255, 0),
                       'light_blue': (0, 128, 255),
                       'dark_red': (128, 0, 0),
                       'dark_green': (0, 128, 0),
                       'dark_blue': (0, 0, 128),
                       'dark_gray': (64, 64, 64),
                       'gray': (128, 128, 128),
                       'light_gray': (192, 192, 192),
                       'white': (255, 255, 255)}

        self.FPS = 60

        self.l_width = 5                    # Line width in selected mode
        self.ls_width = 5                   # Line-block spacing width in selected mode

        self.filename = 'data.dat'          # Saved Filename by default
        self.sim_time = 1.0                 # Default simulation time
        self.sim_dt = 0.01                  # Base sampling time for simulation (Default: 10ms)
        self.plot_trange = 100              # Window width for dynamic plot (Default: 100 samples)

        self.menu_blocks = []               # List of base blocks
        self.blocks_list = []               # List of blocks
        self.line_list = []                 # List of lines

        self.line_creation = 0              # Boolean (3 states) for creation of a line
        self.only_one = False               # Boolean to prevent more than one block from being able to perform an operation
        self.enable_line_selection = False  # Boolean to indicate whether it is possible to select a line or not
        self.holding_CTRL = False           # Boolean to control the state of the CTRL key
        self.execution_initialized = False  # Boolean to indicate if the graph was executed at least once
        self.ss_count = 0                   # Screenshot counter
        
        self.execution_pause = False        # Boolean indicating whether execution was paused at some point in time or not
        self.execution_stop = False         # Boolean indicating whether the execution was completely stopped or not
        self.dynamic_plot = False           # Boolean indicating whether the plot is displayed dynamically advancing or not

    def main_buttons_init(self):
        """
        :purpose: Creates a button list with all the basic functions available
        """
        new =  Button('_new_',     ( 40, 10, 40, 40))
        load = Button('_load_',    (100, 10, 40, 40))
        save = Button('_save_',    (160, 10, 40, 40))
        sim =  Button('_play_',    (220, 10, 40, 40))
        pause = Button('_pause_',  (280, 10, 40, 40))
        stop = Button('_stop_',    (340, 10, 40, 40))
        rplt = Button('_plot_',    (400, 10, 40, 40), active=False)
        capt = Button('_capture_', (460, 10, 40, 40))

        self.buttons_list = [new, load, save, sim, pause, stop, rplt, capt]

    def display_buttons(self, zone):
        """
        :purpose: Displays all the buttons on the screen.
        :param zone: Pygame's layer where the figure is drawn.
        """
        pygame.draw.line(zone, self.colors['black'], [200, 60], [1260, 60], 2)
        for button in self.buttons_list:
            button.draw_button(zone)

    def set_color(self, color):
        """
        :purpose: Defines color for an element drawn in pygame.
        :param color: The color in string or rgb to set.
        :type color: str/(float, float, float)
        """
        if type(color) == str:
            try:
                return self.colors[color]
            except:
                return self.colors['gray']
        elif type(color) == tuple or list:
            return color

    def screenshot(self, zone):
        """
        :purpose: Takes a capture of the screen with all elements seen on display.
        :param zone: Pygame's layer where the figures, lines and buttons are drawn.
        """
        filename = self.filename[:-4]
        pygame.image.save(zone, "captures/"+filename+'-'+str(self.ss_count)+".png")
        self.ss_count += 1

    ##### ADD OR REMOVE BLOCKS AND LINES #####

    def add_block(self, block, m_pos=(0, 0)):
        """
        :purpose: Function that adds a block to the interface, with a unique ID.
        :description: From a visible list of MenuBlocks objects, a complete Block instance is created, which is available for editing its parameters or connecting to other blocks.
        :param block: Base-block containing the base parameters for each type of block.
        :param m_pos: Coordinates (x, y) to locate the upper left corner of the future block.
        :type block: BaseBlock class
        :type m_pos: tuple
        :bugs: Under a wrongly configured MenuBlock, the resulting block may not have the correct qualities or parameters.
        """
        id_list = []
        sid = 0

        for b_elem in self.blocks_list:
            if b_elem.block_fn == block.block_fn:
                id_list.append(int(b_elem.name[len(b_elem.block_fn):]))
        id_list.sort()

        for i in range(len(id_list)):
            if i < id_list[i]:
                sid = i
                break
            else:
                sid = len(id_list)

        # Creation of the block from the id and data of the base block from which it is 'copied'
        mouse_x = m_pos[0]
        mouse_y = m_pos[1]
        block_collision = (mouse_x, mouse_y, block.size[0], block.size[1])

        new_block = DBlock(block.block_fn, sid, block_collision, block.b_color, block.ins, block.outs, block.b_type, block.io_edit, block.fn_name, copy.deepcopy(block.params), block.external)
        self.blocks_list.append(new_block)

    def add_line(self, srcData, dstData):
        """
        :purpose: Function that adds a line to the interface, with a unique ID.
        :description: Based on the existence of one or more blocks, this function creates a line between the last selected ports.
        :param srcData: Triplet containing 'block name', 'port number', 'port coordinates' of an output port (starting point for the line).
        :param dstData: Triplet containing 'block name', 'port number', 'port coordinates' of an input port (finish point for the line).
        :type srcData: triplet
        :type dstData: triplet
        """
        id_list = []
        sid = 0

        for line in self.line_list:
            id_list.append(int(line.name[4:]))
        id_list.sort()

        for i in range(len(id_list)):
            if i < id_list[i]:
                sid = i
                break
            else:
                sid = len(id_list)

        # Creation of the line from the id, and source and destination data for the line
        line = DLine(sid, srcblock=srcData[0], srcport=srcData[1], dstblock=dstData[0], dstport=dstData[1], points=(srcData[2], dstData[2]))
        self.line_list.append(line)

    def remove_block_and_lines(self):
        """
        :purpose: Function to remove blocks or lines.
        :description: Removes a block or a line depending on whether it is selected or not.
        :notes: Lines associated to a block being removed are also removed.
        """
        self.line_creation = 0

        # Removes the block from the list, returning also a second list with the deleted values for use in line deletion
        b_del = [x.name for x in self.blocks_list if x.selected]
        self.blocks_list = [x for x in self.blocks_list if not x.selected]

        if len(b_del) >= 1:
            self.line_list = [x for x in self.line_list if not self.check_line_block(x, b_del)]
        else:
            self.line_list = [x for x in self.line_list if not x.selected]

    def check_line_block(self, line, b_del_list):
        """
        :purpose: Checks if a line is connected to one or more removed blocks.
        :param line: Line object.
        :param b_del_list: List of recently removed blocks.
        """
        if line.dstblock in b_del_list or line.srcblock in b_del_list:
            return True
        return False

    def check_line_port(self, line, block):
        """
        :purpose: Checks if there are lines left from a removed port (associated to a block).
        :param line: Line object.
        :param block: Block object.
        """
        if line.srcblock == block.name and line.srcport > block.out_ports - 1:
            return True
        elif line.dstblock == block.name and line.dstport > block.in_ports - 1:
            return True
        else:
            return False

    def display_lines(self, zone):
        """
        :purpose: Draws lines connecting blocks in the screen.
        :param zone: Pygame's layer where the figure is drawn.
        """
        for line in self.line_list:
            line.draw_line(zone)

    def update_lines(self):
        """
        :purpose: Updates lines according to the location of blocks if these changed place.
        """
        for line in self.line_list:
            line.update_line(self.blocks_list)

    def display_blocks(self, zone):
        """
        :purpose: Draws blocks defined in the main list on the screen.
        :param zone: A layer in a pygame canvas where the figure is drawn.
        """
        for b_elem in self.blocks_list:
            b_elem.draw_Block(zone)

    def port_availability(self, dst_line):
        """
        :purpose: Checks if an input port is free to get connected with a line to another port.
        :param dst_line: The name of a Line object.
        :type dst_line: str
        """
        for line in self.line_list:
            if line.dstblock == dst_line[0] and line.dstport == dst_line[1]:
                return False
        return True

    ##### MENU BLOCKS #####

    def menu_blocks_init(self):
        """
        :purpose: Function that initializes all types of blocks available in the menu.
        :description: From the MenuBlocks class, base blocks are generated for the functions already defined in lib.functions.py. Then they are accumulated in a list so that they are available in the interface menu.
        """
        # block_fn, fn_name, {# inputs, # output, execution hierarchy}, {<specific argument/parameters>}, color, (width, height), allows_io_change

        # source-type blocks
        step = MenuBlocks(block_fn="Step", fn_name='step',
                        io_params={'inputs': 0, 'outputs': 1, 'b_type': 0, 'io_edit': False}, ex_params={'value': 1.0, 'delay': 0.0, 'type': 'up', 'pulse_start_up': True, '_init_start_': True},
                        b_color='blue', coords=(60, 60))

        ramp = MenuBlocks(block_fn="Ramp", fn_name='ramp',
                        io_params={'inputs': 0, 'outputs': 1, 'b_type': 0, 'io_edit': False}, ex_params={'slope': 1.0, 'delay': 0.0},
                        b_color='light_blue', coords=(60, 60))

        sine = MenuBlocks(block_fn="Sine", fn_name='sine',
                        io_params={'inputs': 0, 'outputs': 1, 'b_type': 0, 'io_edit': False}, ex_params={'amplitude': 1.0, 'omega': 1.0, 'init_angle': 0},
                        b_color='cyan', coords=(60, 60))

        noise = MenuBlocks(block_fn="Noise", fn_name='noise',
                        io_params={'inputs': 0, 'outputs': 1, 'b_type': 0, 'io_edit': False}, ex_params={'sigma': 1, 'mu': 0},
                        b_color='purple', coords=(60, 60))


        # N-process-type blocks
        integrator = MenuBlocks(block_fn="Integr", fn_name='integrator',
                        io_params={'inputs': 1, 'outputs': 1, 'b_type': 1, 'io_edit': False}, ex_params={'init_conds': 0.0, 'method': 'FWD_EULER', '_init_start_': True},
                        b_color='magenta', coords=(80, 60))


        # Z-process-type blocks
        derivative = MenuBlocks(block_fn="Deriv", fn_name='derivative',
                        io_params={'inputs': 1, 'outputs': 1, 'b_type': 2, 'io_edit': False}, ex_params={'_init_start_': True},
                        b_color=(255, 0, 200), coords=(80, 60))

        adder = MenuBlocks(block_fn="Sum", fn_name='adder',
                        io_params={'inputs': 2, 'outputs': 1, 'b_type': 2, 'io_edit': 'input'}, ex_params={'sign': "++"},
                        b_color='lime_green', coords=(70, 50))

        sigproduct = MenuBlocks(block_fn="SgProd", fn_name='sigproduct',
                        io_params={'inputs': 2, 'outputs': 1, 'b_type': 2, 'io_edit': 'input'}, ex_params={},
                        b_color='green', coords=(70, 50))

        gain = MenuBlocks(block_fn="Gain", fn_name='gain',
                        io_params={'inputs': 1, 'outputs': 1, 'b_type': 2, 'io_edit': False}, ex_params={'gain': 1.0},
                        b_color=(255, 216, 0), coords=(60, 60))

        exponential = MenuBlocks(block_fn="Exp", fn_name='exponential',
                        io_params={'inputs': 1, 'outputs': 1, 'b_type': 2, 'io_edit': False}, ex_params={'a': 1.0, 'b': 1.0},
                        b_color='yellow', coords=(60, 60))  # a*e^bx

        mux = MenuBlocks(block_fn="Mux", fn_name="mux",
                        io_params={'inputs': 2, 'outputs': 1, 'b_type': 2, 'io_edit': 'input'}, ex_params={},
                        b_color=(190, 0, 255), coords=(60, 60))

        demux = MenuBlocks(block_fn="Demux", fn_name="demux",
                        io_params={'inputs': 1, 'outputs': 2, 'b_type': 2, 'io_edit': 'output'}, ex_params={'output_shape': 1},
                        b_color=(170, 0, 255), coords=(60, 60))


        # Terminal-type blocks
        terminator = MenuBlocks(block_fn="Term", fn_name='terminator',
                        io_params={'inputs': 1, 'outputs': 0, 'b_type': 3, 'io_edit': False}, ex_params={},
                        b_color=(255, 106, 0), coords=(60, 60))

        scope = MenuBlocks(block_fn="Scope", fn_name='scope',
                        io_params={'inputs': 1, 'outputs': 0, 'b_type': 3, 'io_edit': False}, ex_params={'labels': 'default', '_init_start_': True},
                        b_color='red', coords=(60, 60))

        export = MenuBlocks(block_fn="Export", fn_name="export",
                        io_params={'inputs': 1, 'outputs': 0, 'b_type': 3, 'io_edit': False}, ex_params={'str_name': 'default', '_init_start_': True},
                        b_color='orange', coords=(70, 60))


        # External/general use block
        external = MenuBlocks(block_fn="External", fn_name='external',
                        io_params={'inputs': 1, 'outputs': 1, 'b_type': 2, 'io_edit': False}, ex_params={"filename": '<no filename>'},
                        b_color='light_gray', coords=(120, 60), external=True)

        self.menu_blocks = [step, ramp, sine, noise, integrator, derivative, adder, sigproduct, gain, exponential, mux, demux, terminator, scope, export, external]

    def display_menu_blocks(self, zone):
        """
        :purpose: Draws MenuBlocks objects in the screen.
        :param zone: Pygame's layer where the figure is drawn.
        """
        pygame.draw.line(zone, self.colors['black'], [200, 60], [200, 710], 2)
        for i in range(len(self.menu_blocks)):
            self.menu_blocks[i].draw_menublock(zone, pos=i)

    ##### LOADING AND SAVING #####

    def save(self, autosave=False):
        """
        :purpose: Saves blocks, lines and other data in a .dat file.
        :description: Obtaining the location where the file is to be saved, all the important data of the DSim class, each one of the blocks and each one of the lines, are copied into dictionaries, which will then be loaded to the external file by means of the JSON library.
        :param autosave: Flag that defines whether the process to be performed is an autosave or not.
        :type autosave: bool
        :notes: This function is executed automatically when you want to simulate, so as not to lose unsaved information.
        """
        if not autosave:
            root = tk.Tk()
            root.withdraw()

            file = filedialog.asksaveasfilename(initialdir=__file__[:-10]+'saves/', initialfile=self.filename, filetypes=[('Data Files', '*.dat'), ("All files", "*.*")])

            if file == '':
                return 1
            if file[-4:] != '.dat':
                file += '.dat'
        else: # Option for when a graph is going to run
            if '_AUTOSAVE' not in self.filename:
                file = 'saves/'+self.filename[:-4]+'_AUTOSAVE.dat'
            else:
                file = 'saves/'+self.filename

        # DSim data (Simulator interface)
        init_dict = {
            "wind_width": self.SCREEN_WIDTH,
            "wind_height": self.SCREEN_HEIGHT,
            "fps": self.FPS,
            "only_one": self.only_one,
            "enable_line_sel": self.enable_line_selection,
            "sim_time": self.sim_time,
            "sim_dt": self.sim_dt,
            "sim_trange": self.plot_trange
            }

        # Blocks parameters data
        blocks_dict = []
        for block in self.blocks_list:
            block_dict = {
                "block_fn": block.block_fn,
                "sid": block.sid,
                "username": block.username,
                "coords_left": block.left,
                "coords_top": block.top,
                "coords_width": block.width,
                "coords_height": block.height,
                "coords_height_base": block.height_base,
                "in_ports": block.in_ports,
                "out_ports": block.out_ports,
                "dragging": block.dragging,
                "selected": block.selected,
                "b_color": block.b_color,
                "b_type": block.b_type,
                "io_edit": block.io_edit,
                "fn_name": block.fn_name,
                "params": block.saving_params(),
                "external": block.external
            }
            blocks_dict.append(block_dict)

        # Line parameters data
        lines_dict = []
        for line in self.line_list:
            line_dict = {
                "name": line.name,
                "sid": line.sid,
                "srcblock": line.srcblock,
                "srcport": line.srcport,
                "dstblock": line.dstblock,
                "dstport": line.dstport,
                "points": line.points,
                "cptr": line.cptr,
                "selected": line.selected
            }
            lines_dict.append(line_dict)

        main_dict = {"sim_data": init_dict, "blocks_data": blocks_dict, "lines_data": lines_dict}

        with open(file, 'w') as fp:
            json.dump(main_dict, fp, indent=4)

        if not autosave:
            self.filename = file.split('/')[-1]  # Keeps the name of the file if you want to save it again later
            root.destroy()

        print("SAVED AS", file)

    def open(self):
        """
        :purpose: Loads blocks, lines and other data from a .dat.
        :description: Starting from the .dat file, the data saved in the dictionaries are unpacked, updating the data in DSim, creating new blocks and lines, leaving the canvas and the configurations as they were saved before.
        :notes: The name of the loaded file is saved in the system, in order to facilitate the saving of data in it (overwriting it).
        """
        root = tk.Tk()
        root.withdraw()

        file = filedialog.askopenfilename(initialdir=__file__[:-10], initialfile=self.filename, filetypes=[('Data Files', '*.dat'), ("All files", "*.*")])
        if file == '':  # asksaveasfilename return `None` if dialog closed with "cancel".
            return
        root.destroy()

        with open(file) as json_file:
            data = json.load(json_file)
        sim_data = data['sim_data']
        blocks_data = data['blocks_data']
        lines_data = data['lines_data']

        self.clear_all()
        self.update_sim_data(sim_data)
        self.ss_count = 0
        for block in blocks_data:
            self.update_blocks_data(block)
        for line in lines_data:
            self.update_lines_data(line)

        self.filename = file.split('/')[-1]  # Keeps the name of the file if you want to save it again later

        print("LOADED FROM", file)

    def update_sim_data(self, data):
        """
        :purpose: Updates information related with the main class variables saved in a file to the current simulation.
        :param data: Dictionary with DSim parameters.
        :type data: dict
        """
        self.SCREEN_WIDTH = data['wind_width']
        self.SCREEN_HEIGHT = data['wind_height']
        self.FPS = data['fps']
        self.line_creation = 0
        self.only_one = data['only_one']
        self.enable_line_selection = data['enable_line_sel']
        self.sim_time = data['sim_time']
        self.sim_dt = data['sim_dt']
        self.plot_trange = data['sim_trange']

    def update_blocks_data(self, block_data):
        """
        :purpose: Updates information related with all the blocks saved in a file to the current simulation.
        :param block_data: Dictionary with Block object id, parameters, variables, etc.
        :type block_data: dict
        """
        block = DBlock(block_fn=block_data['block_fn'],
                      sid=block_data['sid'],
                      coords=(block_data['coords_left'], block_data['coords_top'], block_data['coords_width'], block_data['coords_height_base']),
                      color=block_data['b_color'],
                      in_ports=block_data['in_ports'],
                      out_ports=block_data['out_ports'],
                      b_type=block_data['b_type'],
                      io_edit=block_data['io_edit'],
                      fn_name=block_data['fn_name'],
                      params=block_data['params'],
                      external=block_data['external'],
                      username=block_data['username'])
        block.height = block_data['coords_height']
        block.selected = block_data['selected']
        block.dragging = block_data['dragging']
        self.blocks_list.append(block)

    def update_lines_data(self, line_data):
        """
        :purpose: Updates information related with all the lines saved in a file to the current simulation.
        :param line_data: Dictionary with Line object id, parameters, variables, etc.
        :type line_data: dict
        """
        line = DLine(sid=line_data['sid'],
                    srcblock=line_data['srcblock'],
                    srcport=line_data['srcport'],
                    dstblock=line_data['dstblock'],
                    dstport=line_data['dstport'],
                    points=line_data['points'],
                    cptr=line_data['cptr'])
        line.selected = line_data['selected']
        line.update_line(self.blocks_list)
        self.line_list.append(line)

    def clear_all(self):
        """
        :purpose: Cleans the screen from all blocks, lines and some main variables.
        """
        self.blocks_list = []
        self.line_list = []
        self.line_creation = 0
        self.only_one = False
        self.enable_line_selection = False
        self.buttons_list[6].active = False  # Disable plot button
        self.ss_count = 0
        self.filename = 'data.dat'
        self.sim_time = 1.0
        self.sim_dt = 0.01
        self.plot_trange = 100
        self.dynamic_plot = False


    ##### DIAGRAM EXECUTION #####

    def execution_init_time(self):
        """
        :purpose: Creates a pop-up window to ask for graph simulation setup values.
        :description: The first step in order to be able to perform a network simulation, is to have the execution data. These are mainly simulation time and sampling period, but we also ask for variables needed for the graphs.
        """
        master = tk.Tk()
        master.title('Simulate')

        # Simulation time
        tk.Label(master, text="Simulation Time").grid(row=0)
        entry = tk.Entry(master)
        entry.grid(row=0, column=1)
        entry.insert(10, self.sim_time)

        # Simulation sample rate
        tk.Label(master, text="Sampling Time").grid(row=1)
        entry2 = tk.Entry(master)
        entry2.grid(row=1, column=1)
        entry2.insert(10, self.sim_dt)

        # Window width for pyqtgraph plots in real time
        tk.Label(master, text="Time range Plot").grid(row=2)
        entry3 = tk.Entry(master)
        entry3.grid(row=2, column=1)
        entry3.insert(10, self.plot_trange)

        # Dynamic plot in real time
        tk.Label(master, text="Dynamic Plot:").grid(row=3)
        r = tk.IntVar()
        tk.Checkbutton(master, variable=r).grid(row=3, column=1)

        tk.Button(master, text='Accept', command=master.quit).grid(row=8, column=1, sticky=tk.W, pady=4)
        tk.mainloop()

        try:
            self.sim_time = float(entry.get())
            self.sim_dt = float(entry2.get())
            self.plot_trange = float(entry3.get())
            self.dynamic_plot = r.get()
            master.destroy()
            return self.sim_time
        except:
            return -1

    def execution_init(self):
        """
        :purpose: Initializes the graph execution.
        :description: This is the first stage of the graph simulation, where variables and vectors are initialized, as well as testing to verify that everything is working properly. A previous autosave is done, as well as a block connection check and possible algebraic loops. If everything goes well, we continue with the loop stage.
        """

        # The class containing the functions for the execution is called
        self.execution_function = DFunctions()
        self.execution_stop = False                         # Prevent execution from stopping before executing in error
        self.time_step = 0                                  # First iteration of the time which will be incrementing self.sim_dt seconds
        self.timeline = np.array([self.time_step])          # List containing the value of all past iterations

        # Some parameters are initialized including the maximum simulation time.
        self.execution_time = self.execution_init_time()

        # To cancel the simulation before running it (having pressed X in the pop up)
        if self.execution_time == -1 or len(self.blocks_list) == 0:
            self.execution_initialized = False
            return

        # Force save before executing (so as not to lose the diagram)
        if self.save(True) == 1:
            return

        print("*****INIT NEW EXECUTION*****")

        # Updating imported modules (external functions)
        for block in self.blocks_list:
            missing_file_flag = block.reload_external_data()
            if missing_file_flag == 1:
                return
            # Note to self: podria agregar aqui el dato del sim_dt a todos los bloques...

        # Check in and check out of each block of the diagram
        if not self.check_diagram_integrity():
            return

        # Generation of a checklist for the computation of functions
        self.global_computed_list = [{'name': x.name, 'computed_data': x.computed_data, 'hierarchy': x.hierarchy}
                                for x in self.blocks_list]
        self.reset_execution_data()
        self.execution_time_start = time.time()

        print("*****EXECUTION START*****")

        # Initialization of the progress bar
        self.pbar = tqdm(desc='SIMULATION PROGRESS', total=int(self.execution_time/self.sim_dt), unit=' itr')

        # Check the existence of algebraic loops (part 1)
        check_loop = self.count_computed_global_list()

        # Check for integrators using Runge-Kutta 45 and initialize counter
        self.rk45_len = self.count_rk45_ints()
        self.rk_counter = 0

        # The block diagram starts with looking for source type blocks
        for block in self.blocks_list:
            children = {}
            out_value = {}
            if block.b_type == 0:
                # The function is executed (differentiate between internal and external function first)
                if block.external:
                    try:
                        out_value = getattr(block.file_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params)
                    except:
                        print("ERROR FOUND IN EXTERNAL FUNCTION",block.file_function)
                        self.execution_failed()
                        return
                else:
                    out_value = getattr(self.execution_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params)
                block.computed_data = True
                block.hierarchy = 0
                self.update_global_list(block.name, h_value=0, h_assign=True)
                children = self.get_outputs(block.name)

            elif block.b_type == 1:
                # The function is executed to only deliver the result to memory (a distinction is made between internal and external function first)
                if block.external:
                    try:
                        out_value = getattr(block.file_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params, output_only=True, next_add_in_memory=False, dtime=self.sim_dt)
                    except:
                        print("ERROR FOUND IN EXTERNAL FUNCTION", block.file_function)
                        self.execution_failed()
                        return
                else:
                    out_value = getattr(self.execution_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params, output_only=True, next_add_in_memory=False, dtime=self.sim_dt)
                children = self.get_outputs(block.name)

            if 'E' in out_value.keys() and out_value['E']:
                self.execution_failed()
                return

            for mblock in self.blocks_list:
                is_child, tuple_list = self.children_recognition(block_name=mblock.name, children_list=children)
                if is_child:
                    # Data is sent to each required port of the child block
                    for tuple_child in tuple_list:
                        mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                        mblock.data_recieved += 1
                        block.data_sent += 1

        # The diagram continues to be executed through the following blocks
        h_count = 1
        while not self.check_global_list():
            for block in self.blocks_list:
                # This part is executed only if the received data is equal to the number of input ports and the block has not been computed yet.
                if block.data_recieved == block.in_ports and not block.computed_data:
                    # The function is executed (differentiate between internal and external function first)
                    if block.external:
                        try:
                            out_value = getattr(block.file_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params)
                        except:
                            print("ERROR FOUND IN EXTERNAL FUNCTION", block.file_function)
                            self.execution_failed()
                            return
                    else:
                        out_value = getattr(self.execution_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params)

                    # It is checked that the function has not delivered an error
                    if 'E' in out_value.keys() and out_value['E']:
                        self.execution_failed()
                        return

                    # The computed_data booleans are updated in the global list as well as in the block itself
                    self.update_global_list(block.name, h_value=h_count, h_assign=True)
                    block.computed_data = True

                    # The blocks that require the processed data from this block are searched.
                    children = self.get_outputs(block.name)
                    if block.b_type not in [1, 3]:  # Elements that do not deliver a result to children (1 is initial cond.)
                        for mblock in self.blocks_list:
                            is_child, tuple_list = self.children_recognition(block_name=mblock.name, children_list=children)
                            if is_child:
                                # Data is sent to each required port of the child block
                                for tuple_child in tuple_list:
                                    mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                                    mblock.data_recieved += 1
                                    block.data_sent += 1

            # The number of executed blocks from the previous stage is compared. If it is zero, there is an algebraic loop.
            if self.count_computed_global_list() == check_loop:
                print("ALGEBRAIC LOOP DETECTED")
                print("*****EXECUTION STOPPED*****")
                return
            else:
                check_loop = self.count_computed_global_list()

            h_count += 1

        # The highest hierarchy value is determined for the next iterations
        self.max_hier = self.get_max_hierarchy()
        self.execution_initialized = True
        self.rk_counter += 1

        # Enable the plot button if there is at least one scope
        for block in self.blocks_list:
            if block.block_fn == 'Scope':
                self.buttons_list[6].active = True

        # The dynamic plot function is initialized, if the Boolean is active
        self.dynamic_pyqtPlotScope(step=0)

    def execution_loop(self):
        """
        :purpose: Continues with the execution sequence in loop until time runs out or an special event stops it.
        :description: This is the second stage of the network simulation. Here the reading of the complete graph will be done cyclically until the time is up, the user indicates that it is finished (by pressing Stop) or simply until one of the blocks gives error. At the end, the data saved in blocks like 'Scope' and 'External_data', will be exported to other libraries to perform their functions.
        """
        if self.execution_pause:
            return

        # After initialization, this function is the one that is constantly looped back to
        self.reset_execution_data()                                 # The execution values changed in the previous step are reset

        # Time progress with Runge-kutta 45
        # 0.5 -> 2*self.rk45_ints | 1.0 -> 1+self.rk45_ints
        if self.rk45_len:
            self.rk_counter %= 4
            if self.rk_counter == 1 or self.rk_counter == 3:
                # Normal half-step feed rate
                self.time_step += self.sim_dt/2
                self.pbar.update(1/2)                                 # Progress bar is updated
            if self.rk_counter == 0:
                self.timeline = np.append(self.timeline, self.time_step)

        # Normal time progress
        elif not self.rk45_len:
            # Full step advance
            self.time_step += self.sim_dt                             # sim_dt is progressed on the execution timeline
            self.pbar.update(1)                                       # Progress bar is updated
            self.timeline = np.append(self.timeline, self.time_step)  # This new time value is added to the time scale

        # The blocks with memory are executed first to obtain only the value produced in the previous stage (do not execute the primary function of these blocks).
        for block in self.blocks_list:
            if block.b_type == 1:
                # Defines whether or not the result is to be accumulated in memory
                add_in_memory = True
                if self.rk45_len and self.rk_counter != 3:
                    add_in_memory = False

                # The function is executed to only deliver the result to memory (a distinction is made between internal and external function first)
                if block.external:
                    try:
                        out_value = getattr(block.file_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params, output_only=True, next_add_in_memory=add_in_memory)
                    except:
                        print("ERROR FOUND IN EXTERNAL FUNCTION", block.file_function)
                        self.execution_failed()
                        return
                else:
                    out_value = getattr(self.execution_function, block.fn_name)(time=self.time_step, inputs=block.input_queue, params=block.params, output_only=True, next_add_in_memory=add_in_memory)

                # It is checked that the function has not delivered an error
                if 'E' in out_value.keys() and out_value['E']:
                    self.execution_failed()
                    return

                # The blocks that require the processed data from this block are searched
                children = self.get_outputs(block.name)
                for mblock in self.blocks_list:
                    is_child, tuple_list = self.children_recognition(mblock.name, children)
                    if is_child:
                        # Data is sent to each required port of the child block
                        for tuple_child in tuple_list:
                            mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                            mblock.data_recieved += 1
                            block.data_sent += 1

            # For terminal blocks that store data, it is indicated whether they are in a normal or intermediate time instant
            if self.rk45_len and self.rk_counter != 0:
                block.params['_skip_'] = True

        # All blocks are executed according to the hierarchy order defined in the first iteration
        for hier in range(self.max_hier + 1):
            for block in self.blocks_list:
                # The block must have the degree of hierarchy to execute it (and meet the other requirements above)
                if block.hierarchy == hier and (block.data_recieved == block.in_ports or block.in_ports == 0) and not block.computed_data:
                    # The function is executed (differentiate between internal and external function first)
                    if block.external:
                        try:
                            out_value = getattr(block.file_function, block.fn_name)(self.time_step, block.input_queue, block.params)
                        except:
                            print("ERROR FOUND IN EXTERNAL FUNCTION", block.file_function)
                            self.execution_failed()
                            return
                    else:
                        out_value = getattr(self.execution_function, block.fn_name)(self.time_step, block.input_queue, block.params)

                    # It is checked that the function has not delivered an error
                    if 'E' in out_value.keys() and out_value['E']:
                        self.execution_failed()
                        return

                    # The computed_data booleans are updated in the global list as well as in the block itself
                    self.update_global_list(block.name, h_value=0)
                    block.computed_data = True

                    # The blocks that require the processed data from this block are searched
                    children = self.get_outputs(block.name)
                    if block.b_type not in [1, 3]:  # Elements that do not deliver a result to children (1 is initial cond.)
                        for mblock in self.blocks_list:
                            is_child, tuple_list = self.children_recognition(block_name=mblock.name, children_list=children)
                            if is_child:
                                # Data is sent to each required port of the child block
                                for tuple_child in tuple_list:
                                    mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                                    mblock.data_recieved += 1
                                    block.data_sent += 1
            hier += 1

        # The dynamic plot function is called to save the new data, if active
        self.dynamic_pyqtPlotScope(step=1)

        # It is checked if the total simulation (execution) time has been exceeded to end the loop
        if self.time_step > self.execution_time + self.sim_dt:  # seconds
            self.execution_initialized = False                  # The execution loop is terminated
            self.pbar.close()                                   # The progress bar ends
            print("SIMULATION TIME:", round(time.time() - self.execution_time_start, 5), 'SECONDS')  # The total time taken is printed

            # Export
            self.export_data()

            # Scope
            if not self.dynamic_plot:
                self.pyqtPlotScope()

            # Resets the initialization of the blocks with special initial executions (so that they can be executed correctly in the next simulation)
            self.reset_memblocks()
            print("*****EXECUTION DONE*****")

        elif self.execution_stop:
            self.execution_stop = False

            self.execution_initialized = False  # The execution loop is terminated
            self.pbar.close()  # The progress bar is finished

            # Resets the boolean for the initialization of the blocks with special initial executions (so that they can be executed correctly in the next simulation)
            self.reset_memblocks()
            print("*****EXECUTION STOPPED*****")

        self.rk_counter += 1

    def execution_failed(self):
        """
        :purpose: If an error is found while executing the graph, this function stops all the processes and resets values to the state before execution.
        """
        self.execution_initialized = False   # Finishes the simulation execution
        self.reset_memblocks()               # Restores the initialization of the integrators (in case the error was due to vectors of different dimensions).
        self.pbar.close()                    # Finishes the progress bar
        print("*****EXECUTION STOPPED*****")

    def check_diagram_integrity(self):
        """
        :purpose: Checks if the graph diagram doesn't have blocks with ports unconnected before the simulation execution.
        :description: This function is only used to check that the network is properly connected. All ports must be connected without exception. In case something is disconnected, a warning is printed indicating where the problem is and returns to the main function indicating that it cannot continue.
        :return: 0 if there are no errors, 1 if there are errors.
        :rtype: int
        """
        print("*****Checking diagram integrity*****")
        error_trigger = False
        for block in self.blocks_list:
            inputs, outputs = self.get_neighbors(block.name)
            
            if block.in_ports == 1 and len(inputs) < block.in_ports:
                print("ERROR. UNLINKED INPUT IN BLOCK:", block.name)
                error_trigger = True
            elif block.in_ports > 1:
                in_vector = np.zeros(block.in_ports)
                for tupla in inputs:
                    in_vector[tupla['dstport']] += 1
                finders = np.where(in_vector == 0)
                if len(finders[0]) > 0:
                    print("ERROR. UNLINKED INPUT(S) IN BLOCK:", block.name, "PORT(S):", finders[0])
                    error_trigger = True
                    
            if block.out_ports == 1 and len(outputs) < block.out_ports:
                print("ERROR. UNLINKED OUTPUT PORT:", block.name)
                error_trigger = True
            elif block.out_ports > 1:
                out_vector = np.zeros(block.out_ports)
                for tupla in outputs:
                    out_vector[tupla['srcport']] += 1
                finders = np.where(out_vector == 0)
                if len(finders[0]) > 0:
                    print("ERROR. UNLINKED OUTPUT(S) IN BLOCK:", block.name, "PORT(S):", finders[0])
                    error_trigger = True
                    
        if error_trigger:
            return False
        print("NO ISSUES FOUND IN DIAGRAM")
        return True

    def count_rk45_ints(self):
        """
        :purpose: Checks all integrators and looks if there's at least one that use 'RK45' as integration method.
        """
        for block in self.blocks_list:
            if block.block_fn == 'Integr' and block.params['method'] == 'RK45':
                return True
            elif block.block_fn == 'External' and 'method' in block.params.keys() and block.params['method'] == 'RK45':
                return True
        return False

    def update_global_list(self, block_name, h_value, h_assign=False):
        """
        :purpose: Updates the global execution list.
        :param block_name: Block object name id.
        :param h_value: Value in graph hierarchy.
        :param h_assign: Flag that defines if the block gets assigned with h_value or not.
        :type block_name: str
        :type h_value: int
        :type h_assign: bool
        """
        # h_assign is used to assign the degree of hierarchy only in the first iteration.
        for elem in self.global_computed_list:
            if elem['name'] == block_name:
                if h_assign:
                    elem['hierarchy'] = h_value
                elem['computed_data'] = True

    def check_global_list(self):
        """
        :purpose: Checks if there are no blocks of a graph left unexecuted.
        """
        for elem in self.global_computed_list:
            if not elem['computed_data']:
                return False
        return True

    def count_computed_global_list(self):
        """
        :purpose: Counts the number of already computed blocks of a graph.
        """
        return len([x for x in self.global_computed_list if x['computed_data']])

    def reset_execution_data(self):
        """
        :purpose: Resets the execution state for all the blocks of a graph.
        """
        for i in range(len(self.blocks_list)):
            self.global_computed_list[i]['computed_data'] = False
            self.blocks_list[i].computed_data = False
            self.blocks_list[i].data_recieved = 0
            self.blocks_list[i].data_sent = 0
            self.blocks_list[i].input_queue = {}
            self.blocks_list[i].hierarchy = self.global_computed_list[i]['hierarchy']

    def get_max_hierarchy(self):
        """
        :purpose: Finds in the global execution list the max value in hierarchy.
        """
        max_val = 0
        for elem in self.global_computed_list:
            if elem['hierarchy'] >= max_val:
                max_val = elem['hierarchy']
        return max_val

    def get_outputs(self, block_name):
        """
        :purpose: Finds all the blocks that need a "block_name" result as input.
        :param block_name: Block object name id.
        :type block_name: str
        """
        # Returns a list of dictionaries with the outgoing ports for block_name, as well as the incoming blocks and ports
        neighs = []
        for line in self.line_list:
            if line.srcblock == block_name:
                neighs.append({'srcport': line.srcport, 'dstblock': line.dstblock, 'dstport': line.dstport})
        return neighs

    def get_neighbors(self, block_name):
        """
        :purpose: Finds all the connected blocks to "block_name".
        :param block_name: Block object name id.
        :type block_name: str
        """
        # Returns two lists of blocks, for blocks connected through lines where the current block is destination or source
        n_inputs = []
        n_outputs = []
        for line in self.line_list:
            if line.srcblock == block_name:
                n_outputs.append({'srcport': line.srcport, 'dstblock': line.dstblock, 'dstport': line.dstport})
            if line.dstblock == block_name:
                n_inputs.append({'dstport': line.dstport, 'srcblock': line.dstblock, 'srcport': line.srcport})
        return n_inputs, n_outputs

    def children_recognition(self, block_name, children_list):
        """
        :purpose: For a block, checks all the blocks that are connected to its outputs and sends a list with them.
        :param block_name: Block object name id.
        :param children_list: List of dictionaries with blocks data that require the output of block 'block_name'.
        :type block_name: str
        :type children_list: list
        """
        child_ports = []
        for child in children_list:
            if block_name in child.values():
                child_ports.append(child)
        if child_ports == []:
            return False, -1
        return True, child_ports

    def reset_memblocks(self):
        """
        :purpose: Resets the "_init_start_" parameter in all blocks.
        """
        for block in self.blocks_list:
            if '_init_start_' in block.params.keys():
                block.params['_init_start_'] = True

    def plot_again(self):
        """
        :purpose: Plots the data saved in Scope blocks without needing to execute the simulation again.
        """
        try:
            scope_lengths = [len(x.params['vector']) for x in self.blocks_list if x.block_fn == 'Scope']
            if scope_lengths[0] > 0:
                self.pyqtPlotScope()
            else:
                print("ERROR: NOT ENOUGH SAMPLES TO PLOT")
        except:
            print("ERROR: GRAPH HAS NOT BEEN SIMULATED YET")
            return

    def export_data(self):
        """
        :purpose: Exports the data saved in Export blocks in .npz format.
        :description: This function is executed after the simulation has finished or stopped. It looks for export blocks, which have some vectors saved with signal outputs from previous blocks. Then it merge all vectors in one big matrix, which is exported with the time vector to a .npz file, formatted in a way it is ready for graph libraries.
        """
        vec_dict = {}
        export_toggle = False
        for block in self.blocks_list:
            if block.block_fn == 'Export':
                export_toggle = True
                labels = block.params['vec_labels']
                vector = block.params['vector']
                if block.params['vec_dim'] == 1:
                    vec_dict[labels] = vector
                elif block.params['vec_dim'] > 1:
                    for i in range(block.params['vec_dim']):
                        vec_dict[labels[i]] = vector[:, i]
        if export_toggle:
            np.savez('saves/' + self.filename[:-4], t=self.timeline, **vec_dict)
            print("DATA EXPORTED TO", 'saves/' + self.filename[:-4] + '.npz')

    # Pyqtgraph functions
    def pyqtPlotScope(self):
        """
        :purpose: Plots the data saved in Scope blocks using pyqtgraph.
        :description: This function is executed while the simulation has stopped. It looks for Scope blocks, from which takes their 'vec_labels' parameter to get the labels of each vector and the 'vector' parameter containing the vector (or matrix if the input for the Scope block was a vector) and initializes a SignalPlot class object that uses pyqtgraph to show a graph.
        """
        labels_list = []
        vector_list = []
        for block in self.blocks_list:
            if block.block_fn == 'Scope':
                b_labels = block.params['vec_labels']
                labels_list.append(b_labels)
                b_vectors = block.params['vector']
                vector_list.append(b_vectors)

        if labels_list != [] and len(vector_list) > 0:
            self.plotty = SignalPlot(self.sim_dt, labels_list, len(self.timeline))
            self.plotty.loop(new_t=self.timeline, new_y=vector_list)

    def dynamic_pyqtPlotScope(self, step):
        """
        :purpose: Plots the data saved in Scope blocks dynamically with pyqtgraph.
        :description: This function is executed while the simulation is running, starting after all the blocks were executed in the first loop. It looks for Scope blocks, from which takes their 'labels' parameter and initializes a SignalPlot class object that uses pyqtgraph to show a graph. Then for each loop completed, it calls those Scope blocks again to get their vectors and update the graph with the new information.
        """
        if not self.dynamic_plot:
            return

        if step == 0:  # init
            labels_list = []
            for block in self.blocks_list:
                if block.block_fn == 'Scope':
                    b_labels = block.params['vec_labels']
                    labels_list.append(b_labels)

            if labels_list != []:
                self.plotty = SignalPlot(self.sim_dt, labels_list, self.plot_trange)

        elif step == 1: # loop
            vector_list = []
            for block in self.blocks_list:
                if block.block_fn == 'Scope':
                    b_vectors = block.params['vector']
                    vector_list.append(b_vectors)
            if len(vector_list) > 0:
                self.plotty.loop(new_t=self.timeline, new_y=vector_list)
            else:
                self.dynamic_plot = False
                print("DYNAMIC PLOT: OFF")


class DBlock(DSim):
    """
    Class to initialize, mantain and modify function blocks.

    :param block_fn: Block name, defined according to the available blocks created in DSim.
    :param sid: Unique identification for the created block.
    :param coords: List with tuples that contain the location and size of the block in the canvas.
    :param color: String or triplet that defines the color of the block in the canvas.
    :param in_ports: Number of inputs for the block.
    :param out_ports: Number of outputs for the block.
    :param b_type: Variable for block type identification (0: source, 1: N_process, 2: Z_process, 3: drain).
    :param io_edit: Variable that defines if a block can change the number of its input ports and/or output ports.
    :param fn_name: Function name, function associated to the block. That function defined in the Functions class.
    :param params: Dictionary with function-related parameters.
    :param external: Parameter that set a block with an external function (not defined in Functions class).
    :param username: String that contains the name of the block previously assigned by the user
    :type block_fn: str
    :type sid: int
    :type coords: list
    :type color: str/triplet
    :type in_ports: int
    :type out_ports: int
    :type b_type: int
    :type io_edit: str
    :type fn_name: str
    :type params: dict
    :type external: bool
    :type username: str

    """
    def __init__(self, block_fn, sid, coords, color, in_ports=1, out_ports=1, b_type=2, io_edit=True, fn_name='block', params={}, external=False, username=''):
        super().__init__()
        self.name = block_fn + str(sid)   # Block name
        self.block_fn = block_fn          # Block type 
        self.sid = sid                    # Block ID
        self.username = self.name         # Block name assigned by the user
        if username != '':
            self.username = username

        self.left = coords[0]             # Location coordinate left border
        self.top = coords[1]              # Coordinate location top border
        self.width = coords[2]            # Block width
        self.height = coords[3]           # Block height
        self.height_base = self.height    # Variable retaining default height value

        self.b_color = self.set_color(color)  # Block color
        self.image = pygame.image.load('./lib/icons/' + self.block_fn + '.png')
        self.image = pygame.transform.scale(self.image, (self.height_base, self.height_base))

        self.fn_name = fn_name                              # Name of the associated function for execution
        self.params = self.loading_params(params)           # Parameters associated with the function
        self.init_params_list = list(self.params.keys())    # List of initial/editable parameters
        self.external = external                            # Boolean to know if associated function is external or not

        self.port_radius = 8            # Radius of the circle for the drawing of the ports
        self.in_ports = in_ports        # Variable containing the number of input ports
        self.out_ports = out_ports      # Variable containing the number of output ports


        # Basic block data for identification in functions.
        self.params.update({'_name_': self.name, '_inputs_': self.in_ports, '_outputs_': self.out_ports})

        self.rectf = pygame.rect.Rect(self.left - self.port_radius, self.top, self.width + 2 * self.port_radius,
                                      self.height)  # Rect defining the block collision

        self.in_coords = []             # List containing coordinates for each input port
        self.out_coords = []            # List containing coordinates for each output port
        self.io_edit = io_edit          # Boolean that determines whether the number of inputs and outputs can be changed
        self.update_Block()             # Locate the port coordinates by updating the block size as well

        self.b_type = b_type            # Block type/priority position when running simulation
        self.dragging = False           # Boolean to determine if block is moving
        self.selected = False           # Boolean to determine if the block is selected in the plane

        # Variables for text initialization for each block (name)
        self.font_size = 24             # Text size
        self.text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.text.render(self.username, True, self.colors['dark_gray'])

        # Variables for simulation execution
        self.hierarchy = -1             # Indicates the hierarchy level to execute during simulation
        self.data_recieved = 0          # Variable indicating when data has been received to calculate the function
        self.computed_data = False      # Boolean indicating whether the function associated with the block has been executed
        self.data_sent = 0              # Variable indicating how many blocks the result of the function has been sent to
        self.input_queue = {}           # Dictionary which stores data arriving from other blocks

    def update_Block(self):
        """
        :purpose: Updates location and size of the block, including its ports.
        :description: This function handles what is necessary to display the block on the screen. It draws the square of the block, draws the ports and places them depending on their quantity, and even extends or reduces the size of the block if the number of ports is not enough or too many. This function always acts when the block is updated, being much more important when it changes location.
        """
        self.in_coords = []
        self.out_coords = []

        # If the number of ports is too large, the block is resized
        port_height = max(self.out_ports, self.in_ports) * self.port_radius * 2
        if port_height > self.height:
            self.height = port_height + 10
        elif port_height < self.height_base:
            self.height = self.height_base
        elif port_height < self.height:
            self.height = port_height + 10
        self.rectf.update((self.left - self.port_radius, self.top, self.width + 2 * self.port_radius, self.height))

        # Ports are symmetrically located on both sides
        if self.in_ports > 0:
            for i in range(self.in_ports):
                port_in = (self.left, self.top + self.height * (i + 1) / (self.in_ports + 1))
                self.in_coords.append(port_in)
        if self.out_ports > 0:
            for j in range(self.out_ports):
                port_out = (self.left + self.width, self.top + self.height * (j + 1) / (self.out_ports + 1))
                self.out_coords.append(port_out)

    def draw_Block(self, zone):
        """
        :purpose: Draws block and its ports.
        :param zone: Pygame's layer where the figure is drawn.
        """
        pygame.draw.rect(zone, self.b_color, (self.left, self.top, self.width, self.height))

        # Load external icons
        zone.blit(self.image, (self.left + 0.5*(self.width-self.height_base), self.top + 0.5*(self.height - self.height_base)))

        for port_in_location in self.in_coords:
            pygame.draw.circle(zone, self.colors['black'], port_in_location, self.port_radius)

        for port_out_location in self.out_coords:
            pygame.draw.circle(zone, self.colors['black'], port_out_location, self.port_radius)
            
        # Draws text with original color
        if not self.selected:
            self.text_display = self.text.render(self.username, True, self.colors['dark_gray'])
            zone.blit(self.text_display, (self.left + 0.5 * (self.width - self.text_display.get_width()), self.top - 20))
        else:
            self.draw_selected(zone)

    def draw_selected(self, zone):
        """
        :purpose: Draws the black line indicating that the block is selected.
        :param zone: Pygame's layer where the figure is drawn.
        """
        # Draws colored text with more contrast
        self.text_display = self.text.render(self.username, True, self.colors['black'])
        zone.blit(self.text_display, (self.left + 0.5 * (self.width - self.text_display.get_width()), self.top - self.ls_width - 20))
        
        # Draws the selection line around a block
        pygame.draw.line(zone, self.colors['black'], (self.left - self.ls_width, self.top - self.ls_width),
                         (self.left + self.width + self.ls_width, self.top - self.ls_width), self.l_width)
        pygame.draw.line(zone, self.colors['black'], (self.left - self.ls_width, self.top - self.ls_width),
                         (self.left - self.ls_width, self.top + self.height + self.ls_width), self.l_width)
        pygame.draw.line(zone, self.colors['black'], (self.left + self.width + self.ls_width, self.top + self.height + self.ls_width),
                         (self.left + self.width + 5, self.top - self.ls_width), self.l_width)
        pygame.draw.line(zone, self.colors['black'], (self.left + self.width + self.ls_width, self.top + self.height + self.ls_width),
                         (self.left - self.ls_width, self.top + self.height + self.ls_width), self.l_width)
        
        if self.external:
            self.function_display = self.text.render(self.params['filename'], True, self.colors['black'])
            zone.blit(self.function_display, (self.left + 0.5 * (self.width - self.function_display.get_width()), self.top + self.height + 15))

    def port_collision(self, m_coords):
        """
        :purpose: Checks if a point collides with one of the ports of a block. Returns a tuple with the port type and port id.
        :param m_coords: Coordinates of mouse input.
        :type m_coords: tuple
        """
        for i in range(len(self.in_coords)):
            p_coords = self.in_coords[i]
            distance = np.sqrt((m_coords[0] - p_coords[0]) ** 2 + (m_coords[1] - p_coords[1]) ** 2)
            if distance <= self.port_radius:
                return ("i", i)
        for j in range(len(self.out_coords)):
            p_coords = self.out_coords[j]
            distance = np.sqrt((m_coords[0] - p_coords[0]) ** 2 + (m_coords[1] - p_coords[1]) ** 2)
            if distance <= self.port_radius:
                return ("o", j)
        return (-1, -1)

    def relocate_Block(self, new_coords):
        """
        :purpose: Relocates port.
        :param m_coords: New coordinates for the block (left, top).
        :type m_coords: tuple
        """
        # new_coords = (left,top)
        self.left = new_coords[0]
        self.top = new_coords[1]
        self.update_Block()

    def resize_Block(self, new_coords):
        """
        :purpose: Resizes block.
        :param m_coords: New parameters for block (width, height).
        :type m_coords: tuple
        """
        # new_dims = (width,height)
        self.width = new_coords[0]
        self.height = new_coords[1]
        self.update_Block()

    def change_port_numbers(self):
        """
        :purpose: Generates a pop-up window for the user to change number of input and/or output ports for the block.
        :description: Through the use of the TkWidget class, a pop-up window is created containing 2 parameters that can be changed by the user: inputs and outputs. After loading them, the 'update_Block' function is executed to adjust the size of the block and the position of its ports. It should be noted that whether the number of inputs or outputs can be changed depends on the type of block, which is differentiated within the function.
        """
        # It is defined by 3 states in which it is allowed to edit only inputs, only output or both.
        if self.io_edit == 'both':
            # Inputs and outputs can be edited
            io_widget = TkWidget(self.name, {'inputs': self.in_ports, 'outputs': self.out_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.in_ports = int(new_io['inputs'])
                self.out_ports = int(new_io['outputs'])
                io_widget.destroy()

        elif self.io_edit == 'input':
            # Only inputs can be edited
            io_widget = TkWidget(self.name, {'inputs': self.in_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.in_ports = int(new_io['inputs'])
                io_widget.destroy()

        elif self.io_edit == 'output':
            # Only outputs can be edited
            io_widget = TkWidget(self.name, {'outputs': self.out_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.out_ports = int(new_io['outputs'])
                io_widget.destroy()

        self.update_Block()

        # To maintain the data in the parameters for the functions
        self.params['_inputs_'] = self.in_ports
        self.params['_outputs_'] = self.out_ports

    def saving_params(self):
        """
        :purpose: Saves parameters only defined at initialization.
        """
        # Saves only the parameters initially defined, not those added during execution
        ed_dict = {}
        for key in self.params.keys():
            if key in self.init_params_list:
                if isinstance(self.params[key], np.ndarray):
                    arraylist = self.params[key]
                    ed_dict[key] = arraylist.tolist()
                else:
                    ed_dict[key] = self.params[key]
        return ed_dict

    def loading_params(self, new_params):
        """
        :purpose: Loads parameters from a dictionary list, converting lists in array vectors.
        :param new_params: Dictionary with parameters for block.
        """
        try:
            for key in new_params.keys():
                if isinstance(new_params[key], list):
                    new_params[key] = np.array(new_params[key])
            return new_params
        except:
            return new_params

    def change_params(self):
        """
        :purpose: Generates a pop-up window to change modifiable parameters only.
        :description: Through the use of the TkWidget class, a pop-up is created to modify parameters associated to the blocks. It should be noted that the only parameters that can be modified are those defined at the beginning (during the definition of the block in 'DSim.menu_blocks_init'), as well as those that do not start with '_' underscore. The function separates the parameters, they are shown to the user, returned to the system and all are put back together at the end.
        """
        
        # If the block has no parameters return to main function
        if self.params == {}:
            return

        ed_dict = {}            # List of editable parameters
        non_ed_dict = {}        # List of non editable parameters
        
        # Add username variable to change
        ed_dict['Name'] = self.username

        # Split all parameters between editable or not editable
        for key in self.params.keys():
            if key in self.init_params_list and not (key[0] == key[-1] == '_'):
                ed_dict[key] = self.params[key]
            else:
                non_ed_dict[key] = self.params[key]

        # If there are no editable parameters return to main function
        if ed_dict == {}:
            return

        # Create the window pop-up to change the parameters' values
        widget_params = TkWidget(self.name, ed_dict, external=self.external)
        new_inputs = widget_params.get_values()
        try:
            external_reset = new_inputs['_ext_reset_']
            new_inputs.pop('_ext_reset_')
        except:
            external_reset = False

        # Save new username and remove it from the dictionary
        if new_inputs['Name'] == '--':
            self.username = self.name
        else:
            self.username = new_inputs['Name']
        new_inputs.pop('Name')

        # Merge again the editable and non editable dictionaries and save them as the new parameters of the block
        if new_inputs != {}:
            new_inputs.update(non_ed_dict)
            self.params = new_inputs
        
        widget_params.destroy()

        # If the block type corresponds to an external type, update the external_reset boolean
        if self.external:
            self.load_external_data(params_reset=external_reset)

    def load_external_data(self, params_reset=False):
        """
        :purpose: Loads initialization data of a function located in a external python file.
        :description: Through the use of the importlib library, a .py file is imported from the 'usermodels' folder, from where the function parameters and the block parameters (input, output, block_type) are extracted, importing them to the existing block, modifying its qualities if necessary.
        """
        
        # If the block type does not correspond to an external type, return to main function
        if not self.external:
            return

        full_module_name = self.params['filename']
        io_params = {'_name_': self.name, '_inputs_': self.in_ports, '_outputs_': self.out_ports}
        try:
            self.file_function = importlib.import_module(full_module_name)
            importlib.reload(self.file_function)
        except:
            print(self.name, "ERROR: NO MODULE FUNCTION", full_module_name, "WAS FOUND")
            self.params = {'filename': '<no filename>'}
            self.init_params_list = list(self.params.keys())
            self.params.update(io_params)
            return

        fun_list, fn_params = self.file_function._init_()

        if not hasattr(self.file_function, full_module_name):
            print("ERROR: IN", self.name, "NO FUNCTION", full_module_name, "WAS FOUND IN THE MODULE", full_module_name)
            print("THE MAIN FUNCTION MUST HAVE THE SAME NAME AS THE FILE")
            self.params = {'filename': '<no filename>'}
            self.init_params_list = list(self.params.keys())
            self.params.update(io_params)
            return

        if not hasattr(self, 'external_old') or (hasattr(self, 'external_old') and (self.external_old != self.params['filename'] or params_reset)):
            self.external_old = self.params['filename']
            self.params = {'filename': self.params['filename']}
            self.params.update(fn_params)
            self.init_params_list = list(self.params.keys())

        self.b_type = fun_list['b_type']
        self.in_ports = fun_list['inputs']
        self.out_ports = fun_list['outputs']
        self.b_color = self.set_color(fun_list['color'])
        self.fn_name = full_module_name

        io_params = {'_name_': self.name, '_inputs_': self.in_ports, '_outputs_': self.out_ports}
        self.params.update(io_params)

        self.update_Block()
        print("MODULE FUNCTION:", full_module_name, "WAS LOADED")

        self.external_old = self.params['filename']

    def reload_external_data(self):
        """
        :purpose: Reloads the external function parameters.
        """
        if not self.external:
            return 0

        if self.params['filename'] == '<no filename>':
            print("ERROR: NO EXTERNAL FUNCTION IS DEFINED FOR", self.name)
            return 1

        # If there is no previous import of the function, an attempt is made to load from the file name assigned to the block
        if not hasattr(self, 'file_function'):
            full_module_name = self.params['filename']
            self.file_function = importlib.import_module(full_module_name)
        else:
            importlib.reload(self.file_function)

        return 0


class DLine(DSim):
    """
    Class to initialize and maintain lines that connect blocks.

    :param sid: Unique identification for the created line.
    :param srcblock: Block from where the line starts.
    :param srcport: Port of the block where the line starts.
    :param dstblock: Block to where the line ends.
    :param dstport: Port of the block where the line ends.
    :param points: List of tuples that defines the vertex of the trajectory of the line (if it's not a straight line).
    :param cptr: Variable used as a pointer to assign a color to the line. It depends on the 'colors' list defined in DSim.
    :type sid: int
    :type srcblock: int
    :type srcport: int
    :type dstblock: int
    :type dstport: int
    :type points: list
    :type cptr: int

    """
    def __init__(self, sid, srcblock, srcport, dstblock, dstport, points, cptr=0):
        super().__init__()
        self.name = "Line" + str(sid)       # Line name
        self.sid = sid                      # Line ID
        self.srcblock = srcblock            # Name of source block
        self.srcport = srcport              # Block source port ID
        self.dstblock = dstblock            # Destination block name
        self.dstport = dstport              # Block destination port ID

        # Variables for line creation
        self.total_srcports = srcport + 1
        self.total_dstports = dstport + 1
        self.srcbottom = points[0][1]
        self.dstbottom = points[0][1]

        self.points = self.trajectory(points)   # vertex points for the line(?) ((a,b),(c,d),(e,f),...)
        self.cptr = cptr                        # Priority ID when drawing the block

        self.selected = False                   # Indicates selection status on the interface

    def draw_line(self, zone):
        """
        :purpose: Draws line.
        :param zone: Pygame's layer where the figure is drawn.
        """
        for i in range(len(self.points) - 1):
            if self.selected:
                line_width = 5
            else:
                line_width = 2
            pygame.draw.line(zone, color=self.colors[list(self.colors.keys())[self.cptr]], start_pos=self.points[i], end_pos=self.points[i + 1], width=line_width)

    def trajectory(self, points):
        """
        :purpose: Generates segments to display a connection between blocks linked by a line.
        :param points: List with coordinates for each vertex of the line group.
        :type points: list
        """
        if len(points) > 2:
            return points
        start = points[0]
        finish = points[-1]

        h_src = 20*(self.total_srcports-self.srcport)               # 30: horizontal distance from the source port to the adjacent vertex
        h_dst = 20*(self.total_dstports-self.dstport)               # 30: horizontal distance from the destination port to the adjacent vertex
        v_dst = 20*(self.total_dstports-self.dstport)               # 50: vertical distance from the destination port to the adjacent vertex
        b_dst = 25*max(self.total_dstports, self.total_srcports)    # 60: distance between ports (covers normal block)

        # if both axes have 'x' or 'y' in common:
        if start[0] == finish[0] or (start[1] == finish[1] and start[0] < finish[0]):
            points = (start,
                      finish)
        # if the destination port is to the right of the source port:
        elif start[0] < finish[0]:
            points = (start,
                      (max(start[0]+10, finish[0] - h_dst), start[1]),
                      (max(start[0]+10, finish[0] - h_dst), finish[1]),
                      finish)
        # if the destination port is to the left of the source port and above or under the other:
        elif start[0] > finish[0] and np.abs(start[1] - finish[1]) > b_dst:
            points = (start,
                      (start[0] + h_src, start[1]),
                      (start[0] + h_src, int(0.5*(start[1]+finish[1]))),
                      (finish[0] - h_dst, int(0.5*(start[1]+finish[1]))),
                      (finish[0] - h_dst, finish[1]),
                      finish)
        # if the destination port is to the left of the source port and at a similar height:
        elif start[0] > finish[0] and np.abs(start[1] - finish[1]) <= b_dst:
            points = (start,
                      (start[0] + h_src, start[1]),
                      (start[0] + h_src, max(self.srcbottom, self.dstbottom) + v_dst),
                      (finish[0] - h_dst, max(self.srcbottom, self.dstbottom) + v_dst),
                      (finish[0] - h_dst, finish[1]),
                      finish)
        return points

    def update_line(self, block_list):
        """
        :purpose: Updates line from size and location of blocks.
        :description: The function searches in the canvas for the location of the input and output ports to which it is connected, then produces a new trajectory using the 'trajectory' function.
        """
        for block in block_list:
            if block.name == self.srcblock:
                startline = block.out_coords[self.srcport]
                self.total_srcports = block.out_ports
                self.srcbottom = block.top + block.height
            if block.name == self.dstblock:
                endline = block.in_coords[self.dstport]
                self.total_dstports = block.in_ports
                self.dstbottom = block.top + block.height
        self.points = self.trajectory((startline, endline))

    def collision(self, m_coords):
        """
        :purpose: Checks if there is collision between a point and the line.
        """
        min_dst = 10
        m_coords = np.array(m_coords)

        for i in range(len(self.points) - 1):
            line_A = np.array(self.points[i])       # Initial position
            line_B = np.array(self.points[i+1])     # Final position

            if all(line_A == m_coords) or all(line_B == m_coords):
                distance_to_line = 0.0
            elif np.arccos(np.dot((m_coords - line_A) / np.linalg.norm(m_coords - line_A),
                                  (line_B - line_A) / np.linalg.norm(line_B - line_A))) > np.pi / 2:
                distance_to_line = np.linalg.norm(m_coords - line_A)
            elif np.arccos(np.dot((m_coords - line_B) / np.linalg.norm(m_coords - line_B),
                                  (line_A - line_B) / np.linalg.norm(line_A - line_B))) > np.pi / 2:
                distance_to_line = np.linalg.norm(m_coords - line_B)
            else:
                distance_to_line = np.linalg.norm(np.cross(line_A - line_B, line_A - m_coords)) / np.linalg.norm(
                    line_B - line_A)

            if distance_to_line <= min_dst:
                return True
        return False

    def change_color(self, ptr):
        """
        :purpose: Pointer indicating which color is chosen from the color list defined in DSim.
        :param ptr: Value that adds or subtracts 1 depending of the user's input.
        :type ptr: int
        """
        # In hardcoded form, the last element corresponding to the white color is skipped (to avoid "invisible" lines).
        self.cptr += ptr
        if self.cptr < 0:
            self.cptr = len(list(self.colors.keys()))-2
        elif self.cptr == len(list(self.colors.keys()))-1:
            self.cptr = 0


class MenuBlocks(DSim):
    """
    Class to create and show basic blocks used as a mark to generate functional blocks in the user interface.

    :param block_fn: Block type, defined according to the available blocks created in DSim
    :param fn_name: Function name, function associated to the block type. That function defined in the Functions class.
    :param io_params: Dictionary with block-related parameters (input ports, output ports, b_type, edit inputs/outputs).
    :param ex_params: Dictionary with function-related parameters.
    :param b_color: String or triplet that defines the color of the block in the canvas.
    :param coords: List with tuples that contain the location and size of the block in the canvas.
    :param external: Parameter that set a block with an external function (not defined in Functions class).
    :type block_fn: str
    :type fn_name: str
    :type io_params: dict
    :type ex_params: dict
    :type b_color: str/triplet
    :type coords: list
    :type external: bool

    """
    # Produces a "button" to generate blocks with the indicated characteristics.
    def __init__(self, block_fn, fn_name, io_params, ex_params, b_color, coords, external=False):
        super().__init__()
        self.block_fn = block_fn
        self.fn_name = fn_name
        self.ins = io_params['inputs']
        self.outs = io_params['outputs']
        self.b_type = io_params['b_type']
        self.io_edit = io_params['io_edit']
        self.params = ex_params                           # Simulation execution parameters
        self.b_color = self.set_color(b_color)            # Characteristic color of the block
        self.size = coords                                # Simulation block dimensions (not this one)
        self.side_length = (30, 30)
        self.image = pygame.image.load('./lib/icons/' + self.block_fn + '.png')
        self.image = pygame.transform.scale(self.image, self.side_length)
        self.external = external

        self.font_size = 24                               # Text size
        self.text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.text.render(self.fn_name, True, self.colors['black'])

    def draw_menublock(self, zone, pos):
        """
        :purpose: Draws the menu block.
        """
        self.collision = pygame.rect.Rect(40, 80 + 40*pos, self.side_length[0], self.side_length[1])
        pygame.draw.rect(zone, color=self.b_color, rect=self.collision)
        zone.blit(self.image, (40, 80 + 40*pos))
        zone.blit(self.text_display, (90, 90 + 40*pos))


class Button(DSim):
    """
    Class to create and show buttons in the user interface.

    :param name: Name of the variable associated to the button.
    :param coords: Coordinates of the button in the canvas.
    :param active: Boolean that indicates the state of the function associated to the button.
    :type name: str
    :type coords: list
    :type active: bool

    """
    def __init__(self, name, coords, active=True):
        super().__init__()
        self.name = name                                                            # Name of the button
        self.coords = coords                                                        # Button location
        self.collision = pygame.rect.Rect(coords)                                   # Button collision
        self.pressed = False
        self.active = active
        self.font_size = 24                                                         # Text size
        self.font_text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.font_text.render(self.name, True, self.colors['black']) # Button render

    def draw_button(self, zone):
        """
        :purpose: Draws the button.
        """
        if not self.active:
            text_color = self.colors['gray']
            text_color2 = (255, 160, 160)
            bg_color = (240, 240, 240)
        else:
            text_color = self.colors['black']
            text_color2 = self.colors['red']
            if self.pressed:
                bg_color = self.colors['gray']
            else:
                bg_color = self.colors['light_gray']

        pygame.draw.rect(zone, color=bg_color, rect=self.collision)
        if not (self.name[0] == self.name[-1] == '_'):
            zone.blit(self.text_display, (self.collision.left + 0.5 * (self.collision.width - self.text_display.get_width()),
                                 self.collision.top + 0.5 * (self.collision.height - self.text_display.get_height())))

        elif self.name == '_new_':
            pygame.draw.polygon(zone, color=text_color, points=(
                (self.collision.left + 0.3 * self.collision.width, self.collision.top + 0.25 * self.collision.height),
                (self.collision.left + 0.3 * self.collision.width, self.collision.top + 0.75 * self.collision.height),
                (self.collision.left + 0.7 * self.collision.width, self.collision.top + 0.75 * self.collision.height),
                (self.collision.left + 0.7 * self.collision.width, self.collision.top + 0.4 * self.collision.height),
                (self.collision.left + 0.55 * self.collision.width, self.collision.top + 0.25 * self.collision.height)
            ), width=2)

        elif self.name == '_load_':
            pygame.draw.polygon(zone, color=text_color, points=(
                (self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height),
                (self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.75 * self.collision.height),
                (self.collision.left + 0.75 * self.collision.width, self.collision.top + 0.75 * self.collision.height),
                (self.collision.left + 0.75 * self.collision.width, self.collision.top + 0.35 * self.collision.height),
                (self.collision.left + 0.45 * self.collision.width, self.collision.top + 0.35 * self.collision.height),
                (self.collision.left + 0.35 * self.collision.width, self.collision.top + 0.25 * self.collision.height),
            ), width=2)

        elif self.name == '_save_':
            pygame.draw.rect(zone, color=text_color, rect=(
                self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height,
                0.5*self.collision.width, 0.5*self.collision.height), width=2)
            pygame.draw.rect(zone, color=text_color, rect=(
                self.collision.left + 0.375 * self.collision.width, self.collision.top + 0.5 * self.collision.height,
                0.25 * self.collision.width, 0.25 * self.collision.height), width=2)

        elif self.name == '_play_':
            pygame.draw.polygon(zone, color=text_color, points=(
            (self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height),
            (self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.75 * self.collision.height),
            (self.collision.left + 0.75 * self.collision.width, self.collision.top + 0.5 * self.collision.height)))

        elif self.name == '_pause_':
            pygame.draw.rect(zone, color=text_color, rect=(self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height, 8, 0.5 * self.collision.height))
            pygame.draw.rect(zone, color=text_color, rect=(self.collision.left + 0.25 * self.collision.width + 12, self.collision.top + 0.25 * self.collision.height, 8, 0.5 * self.collision.height))

        elif self.name == '_stop_':
            pygame.draw.rect(zone, color=text_color, rect=(self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height, 0.5 * self.collision.width, 0.5 * self.collision.height))

        elif self.name == '_plot_':
            pygame.draw.line(zone, color=text_color2,
                             start_pos=[self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.75 * self.collision.height],
                             end_pos=[self.collision.left + 0.45 * self.collision.width, self.collision.top + 0.4 * self.collision.height], width=2)
            pygame.draw.line(zone, color=text_color2,
                             start_pos=[self.collision.left + 0.45 * self.collision.width, self.collision.top + 0.4 * self.collision.height],
                             end_pos=[self.collision.left + 0.55 * self.collision.width, self.collision.top + 0.65 * self.collision.height], width=2)
            pygame.draw.line(zone, color=text_color2,
                             start_pos=[self.collision.left + 0.55 * self.collision.width, self.collision.top + 0.65 * self.collision.height],
                             end_pos=[self.collision.left + 0.75 * self.collision.width, self.collision.top + 0.25 * self.collision.height], width=2)
            pygame.draw.line(zone, color=text_color,
                             start_pos=[self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height],
                             end_pos=[self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.75 * self.collision.height], width=2)
            pygame.draw.line(zone, color=text_color,
                             start_pos=[self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.75 * self.collision.height],
                             end_pos=[self.collision.left + 0.75 * self.collision.width, self.collision.top + 0.75 * self.collision.height], width=2)

        elif self.name == '_capture_':
            pygame.draw.rect(zone, text_color, (
                self.collision.left + 0.2 * self.collision.width, self.collision.top + 0.25 * self.collision.height,
                0.6 * self.collision.width, 0.5 * self.collision.height), 2)
            pygame.draw.rect(zone, text_color, (
                self.collision.left + 0.3 * self.collision.width, self.collision.top + 0.15 * self.collision.height,
                0.15 * self.collision.width, 0.15 * self.collision.height), 2)
            pygame.draw.rect(zone, text_color, (
                self.collision.left + 0.375 * self.collision.width, self.collision.top + 0.25 * self.collision.height,
                0.25 * self.collision.width, 0.15 * self.collision.height), 2)
            pygame.draw.circle(zone, text_color, (
                self.collision.left + 0.5 * self.collision.width, self.collision.top + 0.55 * self.collision.height), 5, 2)

class TkWidget:
    """
    Class used to create popup windows for changing data, like ports and parameters.

    :param name: Name of the source (class, block, line, element that calls this class function).
    :param params: Parameters of the source to display in the popup window.
    :type name: str
    :type params: dict

    """
    def __init__(self, name, params, external=False):
        self.params = params
        self.params_names = list(params.keys())
        self.n = len(self.params_names)
        self.external = external

        self.master = tk.Tk()
        self.master.title(name+' parameters')
        self.entry_widgets = [self.create_entry_widget(x) for x in range(self.n)]

        self.external_toggle()

        tk.Button(self.master, text='Ok', command=self.master.quit).grid(row=self.n+1, column=0, sticky=tk.W, pady=4)
        tk.mainloop()

    def create_entry_widget(self, x):
        """
        :purpose: Creates a new entry for the widget.
        """
        new_widget = tk.Entry(self.master)
        tk.Label(self.master, text=self.params_names[x]).grid(row=x, column=0)
        new_widget.grid(row=x, column=1)

        # Differentiate between np.nparray and others to convert variables or lists to strings.
        value = self.params[self.params_names[x]]
        if isinstance(value, np.ndarray):
            new_widget.insert(0, np.array2string(value, separator=','))
        else:
            new_widget.insert(0, str(value))
        return new_widget

    def get_values(self):
        """
        :purpose: Gets values in a dictionary after the pop-up window is closed.
        """
        try:
            dicty = {}
            for i in range(len(self.entry_widgets)):
                dato = str(self.entry_widgets[i].get())

                if self.params_names[i] != 'Name':
                    # If the string value is empty, the previously existing data is kept.
                    if dato == '':
                        dato = self.params[self.params_names[i]]
                    # Convert to np.ndarray
                    elif dato[0] == '[' and dato[-1] == ']':
                        dato = self.string_to_vector(dato)
                        if type(dato) == str:
                            dato = self.params[self.params_names[i]]
                    # Convert to float
                    elif dato.replace('.', '', 1).replace('-', '', 1).isdigit():
                        dato = float(dato)
                    # Convert to boolean
                    elif dato == 'True' or dato == 'true':
                        dato = True
                    elif dato == 'False' or dato == 'false':
                        dato = False
                
                else:
                    # If the string value is empty, the previously existing data is kept.
                    if dato == '':
                        dato = self.params[self.params_names[i]]

                dicty[self.params_names[i]] = dato

            # If block type is External, get if the parameters must be reset or not
            if self.external:
                dicty['_ext_reset_'] = self.ext_check.get()

            return dicty
        except:
            return {}

    def string_to_vector(self, string):
        """
        :purpose: Converts the string into an array vector.
        :description: This function takes the resulting string and checks whether or not it corresponds to a vector. The function supports receiving up to a three-dimensional array.
        """
        # Supports the use of spaces and square brackets, separates values with commas only.
        # The first step is getting the dimensions of the array by eliminating all the numbers.
        string_shape = string
        for char in string_shape:
            if char not in "[],;":
                string_shape = string_shape.replace(char, '')

        # Beware there is only support for 3-dimensional shaped matrices = (a,b,c)
        first_dim = int(string_shape.count(']],[[') + 1)
        second_dim = int((string_shape.count('],[') - string_shape.count(']],[[')) / first_dim + 1)
        third_dim = int((string_shape.count(',') - string_shape.count('],[')) / (first_dim * second_dim) + 1)
        shape = [first_dim, second_dim, third_dim]

        while True:
            if (shape[0] == 1 and len(shape) == 1) or shape[0] != 1:
                break
            else:
                shape = shape[1:]

        # The second step is removing all values other than commas or numbers from the string.
        for char in "[] ":
            string = string.replace(char, '')
        string = string.replace(';', ',')

        # The resulting string is transformed to an np.ndarray by adjusting the dimensions according to the shape calculation
        array = np.fromstring(string, dtype=float, sep=',')
        dim = np.prod(shape)
        if len(array) == dim:
            array = array.reshape(shape)
            return array
        else:
            print("MATRIX DIMENSIONS ARE INCORRECT")
            return ''

    def external_toggle(self):
        """
        :purpose: Creates a prompt to reset value parameters from a external block.
        """
        if self.external:
            self.ext_check = tk.IntVar()
            tk.Checkbutton(self.master, variable=self.ext_check).grid(row=self.n)
            tk.Label(self.master, text="Reset parameters").grid(row=self.n, column=1)

    def destroy(self):
        """
        :purpose: Finishes the window instance.
        """
        self.master.destroy()


class SignalPlot:
    """
    Class that manages the display of dynamic plots through the simulation.
    *WARNING: It uses pyqtgraph as base (MIT license, but interacts with PyQT5 (GPL)).*

    :param dt: Sampling time of the system.
    :param labels: List of names of the vectors.
    :param xrange: Maximum number of elements to plot in axis x.
    :type dt: float
    :type labels: list
    :type xrange: int

    """
    def __init__(self, dt, labels=['default'], xrange=100):
        self.dt = dt
        self.xrange = xrange*self.dt
        self.sort_labels(labels)

        self.app = pg.mkQApp("")
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.resize(1280, 720)
        self.win.setWindowTitle('Scope')

        pg.setConfigOptions(antialias=True)

        self.linelist = ['line' + str(i) for i in range(len(self.labels))]
        self.plot_win = self.win.addPlot(title='Dynamic Plot')
        self.legend = pg.LegendItem(offset=(0., 1.))
        self.legend.setParentItem(self.plot_win)

        for i in range(len(self.linelist)):
            self.__dict__[self.linelist[i]] = self.plot_win.plot([], [], label=self.labels[i], pen=self.pltcolor(i))
            self.legend.addItem(self.__dict__[self.linelist[i]], self.labels[i])

        self.plot_win.showGrid(x=True, y=True)

    def pltcolor(self, index, hues=9, hueOff=180, minHue=0, maxHue=360, val=255, sat=255, alpha=255):
        """
        :purpose: Assigns a color to a vector for plotting purposes.
        """
        third = (maxHue - minHue) / 3
        hues = int(hues)
        indc = int(index) // 3
        indr = int(index) % 3

        hsection = indr * third
        hrange = (indc * third / (hues // 3)) % third
        h = (hsection + hrange + hueOff) % 360
        return pg.hsvColor(h/360, sat/255, val/255, alpha/255)

    def plot_config(self, settings_dict={}):
        return

    def loop(self, new_t, new_y):
        """
        :purpose: Updates the time and scope vectors and plot them.
        """
        y = self.sort_vectors(new_y)

        if len(new_t)*self.dt >= self.xrange:
            self.plot_win.setXRange(new_t[-1] - self.xrange, new_t[-1])

        # Assign new vectors
        #pg.QtGui.QApplication.processEvents()

        for i in range(len(self.linelist)):
            plotline = getattr(self, self.linelist[i])
            if len(self.linelist) == 1:
                plotline.setData(new_t, y, name=self.labels[i], clear=True)
            else:
                plotline.setData(new_t, y[:, i], name=self.labels[i], clear=True)

    def sort_labels(self, labels):
        """
        :purpose: Rearranges the list if some elements are lists too.
        """
        self.labels = []
        for elem in labels:
            if isinstance(elem, str):
                self.labels += [elem]
            elif isinstance(elem, list):
                self.labels += elem

    def sort_vectors(self, ny):
        """
        :purpose: Rearranges all vectors in one matrix.
        """
        new_vec = ny[0]
        for i in range(1, len(ny)):
            new_vec = np.column_stack((new_vec, ny[i]))
        return new_vec

