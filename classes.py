import pygame                           # LGPL
import numpy as np                      # Liberal BSD
import copy                             # PSF
import time                             # PSF
import json                             # PSF
import tkinter as tk                    # BSD/PSF
import importlib                        # PSF
from tqdm import tqdm                   # MPLv2.0 MIT
from tkinter import ttk
from tkinter import filedialog
from matplotlib import pyplot as plt    # BSD
from scipy.integrate import solve_ivp   # BSD-3-Clause License
from functools import partial           # PSF
import os                               # PSF

class InitSim:
    """
    Class that manages the simulation interface and main functions
    """
    def __init__(self): #Clase que incluye todas las variables y funciones necesarias para la simulación
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720

        self.colors = {'black': (0,0,0),
                       'white': (255,255,255),
                       'red': (255,0,0),
                       'green': (0,255,0),
                       'blue': (0,0,255),
                       'yellow': (255,255,0),
                       'magenta': (255,0,255),
                       'cyan': (0,255,255),
                       'purple': (128,0,255)}

        self.FPS = 60

        self.base_blocks = []  # Lista de bloques base (lista)
        self.blocks_list = []  # Lista de bloques existente
        self.line_list = []    # Lista de lineas existente

        self.line_creation = 0              # Booleano (3 estados) para creación de una línea
        self.only_one = False               # Booleano para impedir que más de un bloque puede efectuar una operación
        self.enable_line_selection = False  # Booleano para indicar si es posible seleccionar una línea o no
        self.holding_CTRL = False           # Booleano para controlar el estado de la tecla CTRL

        self.l_width = 5        # Ancho de linea en modo seleccionado
        self.ls_width = 5       # Ancho separacion entre linea-bloque en modo seleccionado
        self.run_initialized = False

        self.filename = 'data.txt' # Nombre del archivo cargado o por defecto
        self.sim_time = 1.0     # Tiempo de simulación por defecto
        self.sim_dt = 0.01      # diferencia de tiempo para simulación (default: 10ms)

        self.execution_pauseplay = 'play'

    def main_buttons(self, zone):
        """
        Creates a button list with all the basic functions available
        """
        # Crea una lista con los botones básicos para manejar la simulación
        new = Button('New', (40, 10, 100, 40))
        load = Button('Load', (160, 10, 100, 40))
        save = Button('Save', (280, 10, 100, 40))
        #blocks = Button('Add block', (400, 15, 100, 40))
        sim = Button('Simulate', (400, 10, 100, 40))
        pauseplay = Button('_pauseplay_', (520, 10, 40, 40))

        self.buttons_list = [new, load, save, sim, pauseplay]
        self.button_margin = 80

    def display_buttons(self, zone):
        """
        Displays all the buttons on the screen
        """
        # Dibuja los botones en la pantalla
        for button in self.buttons_list:
            button.draw_button(zone)

    ##### ADD OR REMOVE BLOCKS AND LINES #####

    def add_block(self, block, m_pos=(0,0)):
        """
        Adds a block in the screen with a unique ID
        """
        # agrega bloque primero asignando una id al mismo con base en los otros bloques presentes
        id_list = []
        sid = 0

        for b_elem in self.blocks_list:
            if b_elem.b_type == block.b_type:
                id_list.append(int(b_elem.name[len(b_elem.b_type):]))
        id_list.sort()

        for i in range(len(id_list)):
            if i < id_list[i]:
                sid = i
                break
            else:
                sid = len(id_list)

        # creación del bloque a partir del id y datos del bloque base del cual se 'copia'
        #block_collision = (np.random.randint(0.25*self.SCREEN_WIDTH,0.75*self.SCREEN_WIDTH), np.random.randint(0.25*self.SCREEN_HEIGHT,0.75*self.SCREEN_HEIGHT), block.size[0], block.size[1])
        mouse_x = m_pos[0]
        mouse_y = m_pos[1]
        if mouse_y < self.button_margin:
            mouse_y = self.button_margin
        block_collision = (mouse_x, mouse_y, block.size[0], block.size[1])

        new_block = Block(block.b_type, sid, block_collision, block.b_color, block.ins, block.outs, block.run_ord, block.io_edit, block.fun_name, copy.deepcopy(block.params), block.external)
        self.blocks_list.append(new_block)

    def add_line(self, srcData, dstData):
        """
        Adds a line in the screen with a unique ID
        """
        # agrega línea primero asignando una id dependiendo de las líneas existentes
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

        # creación de la línea a partir del id, y data de origen y destino para la misma
        line = Line(sid, srcData[0], srcData[1], (srcData[2], dstData[2]), dstData[0], dstData[1])  # zorder sin utilizar todavia
        self.line_list.append(line)

    def remove_block_and_lines(self):
        """
        Removes the block from the list and the lines connected with it
        """
        # Se elimina la posibilidad de conectar otro bloque con el que se está a punto de eliminar
        self.line_creation = 0

        # remueve el bloque de la lista, retornando también una segunda lista con los valores eliminados para su utilización en la eliminación de líneas
        b_del = [x.name for x in self.blocks_list if x.selected == True]
        self.blocks_list = [x for x in self.blocks_list if not (x.selected == True)]

        if len(b_del) >= 1:
            self.line_list = [x for x in self.line_list if not self.check_line_block(x, b_del)]
        else:
            self.line_list = [x for x in self.line_list if x.selected == False]

    def check_line_block(self, line, b_del_list):
        """
        Checks if there are lines left from a removed BLOCK
        """
        # Comprueba si es que hay lineas a bloques recientemente eliminados
        if line.dstblock in b_del_list or line.srcblock in b_del_list:
            return True
        return False

    def check_line_port(self, line, block):
        """
        Checks if there are lines left from a removed PORT (of a block)
        """
        # Comprueba si es que hay lineas a puertos recientemente eliminados
        if line.srcblock == block.name and line.srcport > block.out_ports - 1:
            return True
        elif line.dstblock == block.name and line.dstport > block.in_ports - 1:
            return True
        else:
            return False

    def print_lines(self, zone):
        """
        Draws lines connecting blocks in the screen
        """
        # Dibuja las líneas a partir de una lista
        for line in self.line_list:
            line.draw_line(zone)

    def update_lines(self):
        """
        Updates lines according to the location of blocks if these changed place
        """
        # Actualiza la ubicación de las líneas a partir de la ubicación de los bloques
        for line in self.line_list:
            line.update_line(self.blocks_list)

    def blockScreen(self, zone):
        """
        Draws existing blocks in the screen
        """
        # Dibuja los bloques incluyendo al seleccionado
        for b_elem in self.blocks_list:
            if b_elem.selected == True:
                b_elem.draw_selected(zone)
            b_elem.draw_Block(zone)

    def port_availability(self, dst_line):
        """
        Checks if an input port is free to get connected with a line to another port
        """
        # Comprueba si es que el puerto a conectar está libre para ello
        for line in self.line_list:
            if line.dstblock == dst_line[0] and line.dstport == dst_line[1]:
                return False
        return True

    ##### BASE BLOCKS #####

    def base_blocks_init(self):
        """
        Initializes the list of blocks available to use (base blocks)
        """
        # Inicializa los bloques del menú, son estos los que se copian para generar los bloques y funciones.
        # Algunos datos se envían en forma de diccionarios para que se pueda observar qué es cada cosa
        # Los colores pueden definirse como strings (si es que están en self.colors) o directamente con los valores RGB en tupla.

        block = BaseBlocks("Block",'block',
                           {'inputs': 1, 'outputs': 1, 'run_ord': 2, 'io_edit': False}, {"filename": '<no filename>'},
                           'green', (120, 60), True)

        step = BaseBlocks("Step", 'step',
                              {'inputs': 0, 'outputs': 1, 'run_ord': 0, 'io_edit': False}, {'value': 1.0, 'delay': 0.0, 'type': 'up'},
                              'blue', (60, 60))

        gain = BaseBlocks("Gain", 'gain',
                          {'inputs': 1, 'outputs': 1, 'run_ord': 2, 'io_edit': False}, {'gain': 1.0},
                          'yellow', (60, 60))

        integrator = BaseBlocks("Integr", 'integrator',
                                {'inputs': 1, 'outputs': 1, 'run_ord': 1, 'io_edit': False}, {'init_conds': 0.0, 'method': 'FWD_RECT', '_init_start_': True},
                                'magenta', (80, 60))

        sumator = BaseBlocks("Sum", 'sumator',
                             {'inputs': 2, 'outputs': 1, 'run_ord': 2, 'io_edit': 'input'}, {'sign': "++"},
                             'cyan', (70, 50))

        sigproduct = BaseBlocks("SgProd", 'sigproduct',
                                   {'inputs': 2, 'outputs': 1, 'run_ord': 2, 'io_edit': 'input'}, {},
                                   'green', (70, 50))

        sine = BaseBlocks("Sine", 'sine',
                          {'inputs': 0, 'outputs': 1, 'run_ord': 0, 'io_edit': False}, {'amplitude': 1.0, 'omega': 1.0, 'init_angle': 0},
                          'purple', (60, 60))

        exponential = BaseBlocks("Exp", 'exponential',
                                 {'inputs': 1, 'outputs': 1, 'run_ord': 2, 'io_edit': False}, {'a': 1.0, 'b': 1.0},
                                 (255,0,128), (60, 60))  # a*e^bx

        ramp = BaseBlocks("Ramp", 'ramp',
                          {'inputs': 0, 'outputs': 1, 'run_ord': 0, 'io_edit': False}, {'slope': 1.0, 'delay': 0.0},
                          (255,127,0), (60, 60))

        noise = BaseBlocks("Noise", 'noise',
                           {'inputs': 0, 'outputs': 1, 'run_ord': 0, 'io_edit': False}, {'sigma': 1, 'mu': 0},
                           (100,175,50), (60, 60))

        testmo = BaseBlocks("TestMO", "test_MO",
                            {'inputs': 0, 'outputs': 2, 'run_ord': 0, 'io_edit': False}, {},
                            (0, 20, 60), (60, 60))

        mux = BaseBlocks("Mux", "mux",
                            {'inputs': 2, 'outputs': 1, 'run_ord': 2, 'io_edit': 'input'}, {},
                            (102, 51, 153), (60, 60))

        demux = BaseBlocks("Demux", "demux",
                            {'inputs': 1, 'outputs': 2, 'run_ord': 2, 'io_edit': 'output'}, {'output_shape': 2.0},
                            (102, 30, 153), (60, 60))

        terminator = BaseBlocks("Term", 'terminator',
                                {'inputs': 1, 'outputs': 0, 'run_ord': 3, 'io_edit': False}, {},
                                'red', (60, 60))

        scope = BaseBlocks("Scope", 'scope',
                           {'inputs': 1, 'outputs': 0, 'run_ord': 3, 'io_edit': False}, {'labels': 'default', '_init_start_': True},
                           (220, 20, 60), (60, 60))

        export = BaseBlocks("Export", "export",
                            {'inputs': 1, 'outputs': 0, 'run_ord': 3, 'io_edit': False}, {'str_name': 'default', '_init_start_': True},
                            (255,160,0), (70, 60))

        self.base_blocks = [step,sine,ramp,noise,integrator,gain,exponential,block,sumator,sigproduct,mux,demux,testmo,terminator,scope,export]

    def draw_base_blocks(self,zone):
        """
        Draws base blocks in the screen
        """
        # Dibuja los bloques del menú y la línea separadora
        pygame.draw.line(zone, self.colors['black'], [200, 60], [200, 710], 2)
        for i in range(len(self.base_blocks)):
            self.base_blocks[i].draw_baseblock(zone, i)

    def display_base_blocks_menu(self):
        # Función base para Tkinter de forma que se puedan cargar la lista de bloques
        root = tk.Tk()
        root.title('Blocks')
        for i in range(len(self.base_blocks)):
            tk.Button(root,
                      text=self.base_blocks[i].fun_name,
                      width=15,
                      command=lambda i=i: self.add_block(self.base_blocks[i])).grid(row=i, column=0, sticky=tk.W, pady=4)
        tk.Button(root, text='Ok', command=root.quit).grid(row=len(self.base_blocks)+1, column=0, sticky=tk.W, pady=4)
        tk.mainloop()
        root.destroy()
        return

        # separar por partes (usar run_ord)
        # agregar un contador si es necesario
        # La otra sería un: <nombre bloque> |<-| |<numero de bloques>| |->|

    ##### LOADING AND SAVING #####

    def save(self):
        """
        Saves blocks, lines and other data in a .txt
        """
        # Guarda los datos en diccionarios, exportados a un .txt
        root = tk.Tk()
        root.withdraw()

        file = filedialog.asksaveasfilename(initialfile=self.filename, filetypes=[('Text Files', '*.txt'),("All files", "*.*")])

        if file == '':
            return 1
        if file[-4:] != '.txt':
            file += '.txt'

        # Datos de InitSim
        init_dict = {
            "wind_width": self.SCREEN_WIDTH,
            "wind_height": self.SCREEN_HEIGHT,
            "fps": self.FPS,
            "only_one": self.only_one,
            "enable_line_sel": self.enable_line_selection,
            "sim_time": self.sim_time,
            "sim_dt": self.sim_dt
            }

        # Datos de Block
        blocks_dict = []
        for block in self.blocks_list:
            block_dict = {
                "type": block.b_type,
                "sid": block.sid,
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
                "run_ord": block.run_ord,
                "io_edit": block.io_edit,
                "fun_name": block.fun_name,
                "params": block.saving_params(),
                "external": block.external
            }
            blocks_dict.append(block_dict)

        # Datos de Line
        lines_dict = []
        for line in self.line_list:
            line_dict = {
                "name": line.name,
                "sid": line.sid,
                "srcblock": line.srcblock,
                "srcport": line.srcport,
                "dstblock": line.dstblock,
                "dstport": line.dstport,
                "zorder": line.zorder,
                "selected": line.selected
            }
            lines_dict.append(line_dict)

        main_dict = {"sim_data": init_dict, "blocks_data": blocks_dict, "lines_data": lines_dict}

        with open(file, 'w') as fp:
            json.dump(main_dict, fp, indent=4)

        self.filename = file.split('/')[-1] # Para conservar el nombre del archivo si es que se quiere guardar

        root.destroy()
        print("SAVED AS",file)

    def open(self):
        """
        Loads blocks, lines and other data from a .txt
        """
        # Abre el archivo .txt y carga los datos guardados para mostrarlos en pantalla
        root = tk.Tk()
        root.withdraw()

        file = filedialog.askopenfilename(initialfile=self.filename, filetypes=[('Text Files', '*.txt'),("All files", "*.*")])
        if file == '':  # asksaveasfilename return `None` if dialog closed with "cancel".
            return
        root.destroy()

        self.filename = file.split('/')[-1] # Para conservar el nombre del archivo si es que se quiere guardar

        with open(file) as json_file:
            data = json.load(json_file)
        sim_data = data['sim_data']
        blocks_data = data['blocks_data']
        lines_data = data['lines_data']

        self.clear_all()
        self.update_sim_data(sim_data)
        for block in blocks_data:
            self.update_blocks_data(block)
        for line in lines_data:
            self.update_lines_data(line)

        print("LOADED FROM", file)

    def update_sim_data(self,data):
        """
        Updates information related with the main class variables saved in a file to the current simulation
        """
        # Reordena los datos de los diccionarios, para utilizarlos en las configuraciones de la simulación
        self.SCREEN_WIDTH = data['wind_width']
        self.SCREEN_HEIGHT = data['wind_height']
        self.FPS = data['fps']
        self.line_creation = 0
        self.only_one = data['only_one']
        self.enable_line_selection = data['enable_line_sel']
        self.sim_time = data['sim_time']
        self.sim_dt = data['sim_dt']

    def update_blocks_data(self,block_data):
        """
        Updates information related with all the blocks saved in a file to the current simulation
        """
        # Reordena los datos de los diccionarios, para utilizarlos creando un nuevo bloque
        block = Block(block_data['type'],
                      block_data['sid'],
                      (block_data['coords_left'],block_data['coords_top'],block_data['coords_width'],block_data['coords_height']),
                      block_data['b_color'],
                      block_data['in_ports'],
                      block_data['out_ports'],
                      block_data['run_ord'],
                      block_data['io_edit'],
                      block_data['fun_name'],
                      block_data['params'],
                      block_data['external'])
        block.height_base = block_data['coords_height_base']
        block.selected = block_data['selected']
        block.dragging = block_data['dragging']
        #block.loading_params(block_data['params'])
        self.blocks_list.append(block)

    def update_lines_data(self,line_data):
        """
        Updates information related with all the lines saved in a file to the current simulation
        """
        # Reordena los datos de los diccionarios, para utilizarlos creando una nueva línea
        line = Line(line_data['sid'],
                    line_data['srcblock'],
                    line_data['srcport'],
                    ((0,0), (0,0)),
                    line_data['dstblock'],
                    line_data['dstport'],
                    line_data['zorder'])  # zorder sin utilizar todavia
        line.selected = line_data['selected']
        line.update_line(self.blocks_list)
        self.line_list.append(line)

    def clear_all(self):
        """
        Cleans the screen from all blocks, lines and some main variables.
        """
        # Elimina todos los bloques, lineas y variables, haciendo que la interfaz vuelva a quedar en el estado inicial.
        self.blocks_list = []
        self.line_list = []
        self.line_creation = 0
        self.only_one = False
        self.enable_line_selection = False

    ##### DIAGRAM EXECUTION #####

    def execution_init_time(self):
        """
        Creates a pop-up to ask for execution time and sampling time
        """
        # Por medio de un popup window, determina el tiempo a simular y el muestreo de este para los datos (ejecutar).
        master = tk.Tk()
        master.title('Simulate')

        # Tiempo de simulación
        tk.Label(master, text="Simulation Time").grid(row=0)
        entry = tk.Entry(master)
        entry.grid(row=0, column=1)
        entry.insert(10, self.sim_time)

        # Muestreo de simulación
        tk.Label(master, text="Sampling Time").grid(row=1)
        entry2 = tk.Entry(master)
        entry2.grid(row=1, column=1)
        entry2.insert(10, self.sim_dt)

        tk.Button(master, text='Accept', command=master.quit).grid(row=2, column=1, sticky=tk.W, pady=4)
        tk.mainloop()

        try:
            self.sim_time = float(entry.get())
            self.sim_dt = float(entry2.get())
            master.destroy()
            return self.sim_time
        except:
            return -1

    def execution_init(self):
        """
        Initializes the graph execution
        """
        # Inicializa los parametros y bloques para la simulación del sistema, además de hacer la primera iteración de calculo
        self.execution_fun = Functions_call()
        self.time_step = 0
        self.timeline = np.array([self.time_step])

        self.execution_time = self.execution_init_time()

        # Para cancelar la simulación antes de correrla (habiendo presionado X en el pop up)
        if self.execution_time == -1:
            self.run_initialized = False
            return

        # Obligar a guardar antes de ejecutar (para no perder el diagrama)
        if self.save() == 1:
            return

        # Actualización de módulos importados (funciones externas)
        for block in self.blocks_list:
            missing_file_flag = block.reload_external_data()
            if missing_file_flag == 1:
                return

        # Chequeo de entradas y salidas:
        if self.check_diagram_integrity() == 1:
            return

        # Generación de lista para chequeo de cómputo de funciones
        self.global_computed_list = [{'name': x.name, 'computed_data': x.computed_data, 'hierarchy': x.hierarchy}
                                for x in self.blocks_list]
        self.reset_execution_data()
        self.execution_time_start = time.time()

        print("*****EXECUTION*****")
        # Inicialización de la barra de progreso
        self.pbar = tqdm(desc='SIMULATION PROGRESS', total=int(self.execution_time/self.sim_dt), unit=' itr')

        # Comprobar la existencia de loops algebraicos (pt1)
        check_loop = self.count_computed_global_list()

        # Comprobar la existencia de integradores que usen Runge-Kutta 45 e inicializar contador
        self.rk45_len = self.count_rk45_ints()
        self.rk_counter = 0

        for block in self.blocks_list:
            children = {}
            out_value = {}
            if block.run_ord == 0:
                # Se ejecuta la función (se diferencia entre función interna y externa primero)
                if block.external == True:
                    out_value = getattr(block.file_function, block.fun_name)(self.time_step, block.input_queue, block.params)
                else:
                    out_value = getattr(self.execution_fun, block.fun_name)(self.time_step, block.input_queue, block.params)
                block.computed_data = True
                block.hierarchy = 0
                self.update_global_list(block.name, 0, True)
                children = self.get_outputs(block.name)

            elif block.run_ord == 1:
                # Se ejecuta la función para únicamente entregar el resultado en memoria (se diferencia entre función interna y externa primero)
                if block.external == True:
                    out_value = getattr(block.file_function, block.fun_name)(self.time_step, block.input_queue, block.params, True, False, self.sim_dt)
                else:
                    out_value = getattr(self.execution_fun, block.fun_name)(self.time_step, block.input_queue, block.params, True, False, self.sim_dt)
                children = self.get_outputs(block.name)

            if 'E' in out_value.keys() and out_value['E'] == True:
                self.run_initialized = False            # Termina la ejecución de la simulación
                self.reset_memblocks()                  # Resetea la inicialización de los integradores (en caso que el error haya sido por vectores de distintas dimensiones
                print("*****EXECUTION STOPPED*****")
                return

            for mblock in self.blocks_list:
                is_child, tuple_list = self.children_recognition(mblock.name, children)
                if is_child == True:
                    # Se envian los datos a cada puerto necesario del bloque hijo
                    for tuple_child in tuple_list:
                        mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                        mblock.data_recieved += 1
                        block.data_sent += 1

        h_count = 1
        while (self.check_global_list() != True):
            for block in self.blocks_list:
                # Se ejecuta esta parte solo si la data recibida es igual al numero de puertos de entrada y el bloque no ha sido computado todavía
                if block.data_recieved == block.in_ports and block.computed_data != True:
                    # Se ejecuta la función (se diferencia entre función interna y externa primero)
                    if block.external == True:
                        out_value = getattr(block.file_function, block.fun_name)(self.time_step, block.input_queue, block.params)
                    else:
                        out_value = getattr(self.execution_fun, block.fun_name)(self.time_step, block.input_queue, block.params)

                    # Se comprueba que la función no haya entregado error:
                    if 'E' in out_value.keys() and out_value['E'] == True:
                        self.run_initialized = False    # Termina la ejecución de la simulación
                        self.reset_memblocks()        # Resetea la inicialización de los integradores (en caso que el error haya sido por vectores de distintas dimensiones
                        print("*****EXECUTION STOPPED*****")
                        return

                    # Se actualizan los flags de cómputo en la lista global como en el bloque mismo
                    self.update_global_list(block.name, h_count, True)
                    block.computed_data = True

                    # Se buscan los bloques que requieren los datos procesados de este bloque
                    children = self.get_outputs(block.name)
                    if block.run_ord not in [1,3]: #elementos que no entregan resultado a children (1 es cond. inicial)
                        for mblock in self.blocks_list:
                            is_child, tuple_list = self.children_recognition(mblock.name, children)
                            if is_child == True:
                                # Se envian los datos a cada puerto necesario del bloque hijo
                                for tuple_child in tuple_list:
                                    mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                                    mblock.data_recieved += 1
                                    block.data_sent += 1

            # Se compara el numero de bloques ejecutados de la etapa anterior. Si es cero, hay un loop algebraico
            if self.count_computed_global_list() == check_loop:
                print("ALGEBRAIC LOOP DETECTED")
                print("*****EXECUTION STOPPED*****")
                return
            else:
                check_loop = self.count_computed_global_list()

            h_count += 1

        self.max_hier = self.get_max_hierarchy()  # Se determina el valor más alto de jerarquía para las próximas iteraciones
        self.run_initialized = True
        self.rk_counter += 1
        # actualizar plots

    def execution_loop(self):
        """
        Continues with the execution sequence in loop until time runs out or an special event.
        """
        # Si el boton de play-pausa está en pausa, la simulación no corre hasta cambiar su estado
        if self.execution_pauseplay == 'pause':
            return

        # Después de inicializar, esta función es la que constantemente se repite en loop
        self.reset_execution_data()                                 # Se resetean los valores de ejecución cambiados en la etapa anterior

        # Avance de tiempo con Runge-kutta 45
        # 0.5 -> 2*self.rk45_ints | 1.0 -> 1+self.rk45_ints
        if self.rk45_len == True:
            self.rk_counter %= 4
            if self.rk_counter == 0 or self.rk_counter == 2:
                # Avance medio paso normal
                self.time_step += self.sim_dt/2
                self.pbar.update(1/2)                                 # Se actualiza la barra de progreso
                if self.rk_counter == 0:
                    self.timeline = np.append(self.timeline, self.time_step)

        # Avance de tiempo normal
        elif self.rk45_len == False:
            # Avance paso completo
            self.time_step += self.sim_dt                             # Se avanza sim_dt en la linea de tiempo de la ejecución
            self.pbar.update(1)                                       # Se actualiza la barra de progreso
            self.timeline = np.append(self.timeline, self.time_step)  # Se agrega este nuevo valor de tiempo a la escala de tiempo

        # Se ejecutan primero los bloques con memoria para obtener sólo el valor producido en la etapa anterior (no ejecutar la función primaria de estas)
        for block in self.blocks_list:
            if block.run_ord == 1:
                # Se define si el resultado debe acumularse en la memoria o no
                add_in_memory = True
                if self.rk45_len == True and self.rk_counter != 3:
                    add_in_memory = False

                # Se ejecuta la función para únicamente entregar el resultado en memoria (se diferencia entre función interna y externa primero)
                if block.external == True:
                    out_value = getattr(block.file_function, block.fun_name)(self.time_step, block.input_queue, block.params, True, add_in_memory)
                else:
                    out_value = getattr(self.execution_fun, block.fun_name)(self.time_step, block.input_queue, block.params, True, add_in_memory)

                # Se comprueba que la función no haya entregado error:
                if 'E' in out_value.keys() and out_value['E'] == True:
                    self.run_initialized = False    # Termina la ejecución de la simulación
                    self.reset_memblocks()        # Resetea la inicialización de los integradores (en caso que el error haya sido por vectores de distintas dimensiones
                    print("*****EXECUTION STOPPED*****")
                    return

                # Se buscan los bloques que requieren los datos procesados de este bloque
                children = self.get_outputs(block.name)
                for mblock in self.blocks_list:
                    is_child, tuple_list = self.children_recognition(mblock.name, children)
                    if is_child == True:
                        # Se envian los datos a cada puerto necesario del bloque hijo
                        for tuple_child in tuple_list:
                            mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                            mblock.data_recieved += 1
                            block.data_sent += 1

            # Para los bloques terminales que guardan datos, se les indica si se está en un instante de tiempo normal o intermedio
            elif block.run_ord == 3:
                if self.rk45_len == True and self.rk_counter != 0:
                    block.params['skip'] = True

        # Se ejecutan todos los bloques de acuerdo al orden de jerarquía definido en la primera iteración
        for hier in range(self.max_hier + 1):
            for block in self.blocks_list:
                # Se busca que el bloque tenga el grado de jerarquia para ejecutarlo (y que cumpla con los otros requisitos anteriores)
                if block.hierarchy == hier and (block.data_recieved == block.in_ports or block.in_ports == 0) and block.computed_data != True:
                    # Se ejecuta la función (se diferencia entre función interna y externa primero)
                    if block.external == True:
                        out_value = getattr(block.file_function, block.fun_name)(self.time_step, block.input_queue, block.params)
                    else:
                        out_value = getattr(self.execution_fun, block.fun_name)(self.time_step, block.input_queue, block.params)

                    # Se comprueba que la función no haya entregado error:
                    if 'E' in out_value.keys() and out_value['E'] == True:
                        self.run_initialized = False    # Termina la ejecución de la simulación
                        self.reset_memblocks()          # Resetea la inicialización de los integradores (en caso que el error haya sido por vectores de distintas dimensiones
                        print("*****EXECUTION STOPPED*****")
                        return

                    # Se actualizan los flags de cómputo en la lista global como en el bloque mismo
                    self.update_global_list(block.name,0)
                    block.computed_data = True

                    # Se buscan los bloques que requieren los datos procesados de este bloque
                    children = self.get_outputs(block.name)
                    if block.run_ord not in [1,3]: # elementos que no entregan resultado a children (1 es cond. inicial)
                        for mblock in self.blocks_list:
                            is_child, tuple_list = self.children_recognition(mblock.name, children)
                            if is_child == True:
                                # Se envian los datos a cada puerto necesario del bloque hijo
                                for tuple_child in tuple_list:
                                    mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                                    mblock.data_recieved += 1
                                    block.data_sent += 1
            hier += 1

        # Se comprueba si que el tiempo total de simulación (ejecución) ha sido superado para finalizar con el loop.
        if self.time_step >= self.execution_time: # seconds
            self.run_initialized = False                        # Se finaliza el loop de ejecución
            self.pbar.close()                                   # Se finaliza la barra de progreso
            print("SIMULATION TIME:", round(time.time() - self.execution_time_start, 5), 'SECONDS')  # Se imprime el tiempo total tomado

            #Scope
            self.plotScope()

            #Export
            self.exportData()

            # Resetea la inicializacion de los bloques con ejecuciones iniciales especiales (para que puedan ser ejecutados correctamente en la proxima simulación)
            self.reset_memblocks()
            print("*****EXECUTION DONE*****")

        self.rk_counter += 1


    def children_recognition(self, block_name, children_list):
        """
        For a block, checks all the blocks that are connected to its outputs and sends a list with them.
        """
        # Compara el block_name (de blocks_list) y lo busca en children_list, si está entrega un True y una lista con diccionarios que contienen los puertos de salida y llegada para parent and child.
        child_ports = []
        for child in children_list:
            if block_name in child.values():
                child_ports.append(child)
        if child_ports == []:
            return False, -1
        return True, child_ports

    def update_global_list(self, block_name, h_value, h_assign=False):
        """
        Updates the global execution list
        """
        # Actualiza la lista global que controla los loops en la ejecución
        # h_assign se utiliza para asignar el grado de jerarquía unicamente en la primera iteración
        for elem in self.global_computed_list:
            if elem['name'] == block_name:
                if h_assign == True:
                    elem['hierarchy'] = h_value
                elem['computed_data'] = True

    def check_global_list(self):
        """
        Checks if there are no blocks of a graph left unexecuted
        """
        # Comprueba que no queden bloques sin ejecutar en la simulación
        for elem in self.global_computed_list:
            if elem['computed_data'] == False:
                return False
        return True

    def count_computed_global_list(self):
        """
        Counts the number of already computed blocks of a graph
        """
        # Cuenta el número de bloques ya ejecutados durante la simulación
        return len([x for x in self.global_computed_list if x['computed_data'] == True])

    def reset_execution_data(self):
        """
        Resets the execution state for all the blocks of a graph
        """
        # Devuelve al estado inicial varios parametros tanto de los bloques, con de la lista global que controla los loops de ejecución
        for i in range(len(self.blocks_list)):
            self.global_computed_list[i]['computed_data'] = False
            self.blocks_list[i].computed_data = False
            self.blocks_list[i].data_recieved = 0
            self.blocks_list[i].data_sent = 0
            self.blocks_list[i].input_queue = {}
            self.blocks_list[i].hierarchy = self.global_computed_list[i]['hierarchy']

    def get_max_hierarchy(self):
        """
        Finds in the global execution list the max value in hierarchy
        """
        # Busca el grado de jerarquía más alto (o bajo?) para determinar el número de forloop necesario para correr el codigo
        maxValue = 0
        for elem in self.global_computed_list:
            if elem['hierarchy'] >= maxValue:
                maxValue = elem['hierarchy']
        return maxValue

    def get_outputs(self, block_name):
        """
        Finds all the blocks that need a "block_name" result as input
        """
        # A partir de las conexiones de las líneas entre puertos, busca cuales son los que necesitan a "block_name de input"
        # retorna una lista de diccionarios con los puertos de salida para block_name, como los bloques y puertos de llegada
        neighs = []
        for line in self.line_list:
            if line.srcblock == block_name:
                neighs.append({'srcport': line.srcport, 'dstblock': line.dstblock, 'dstport': line.dstport})
        return neighs

    def get_neighbors(self, block_name):
        """
        Finds all the connected blocks to "block_name"
        """
        # A partir de las conexiones de las líneas entre puertos, busca cuales son los que tienen a "block_name" de output o input
        # retorna una lista de bloques
        n_inputs = []
        n_outputs = []
        for line in self.line_list:
            if line.srcblock == block_name:
                n_outputs.append({'srcport': line.srcport, 'dstblock': line.dstblock, 'dstport': line.dstport})
            if line.dstblock == block_name:
                n_inputs.append({'dstport': line.dstport, 'srcblock': line.dstblock, 'srcport': line.srcport})
        return n_inputs, n_outputs

    def check_diagram_integrity(self):
        """
        Checks if the graph diagram doesn't have blocks with ports unconnected before the simulation execution
        """
        # Comprueba que el diagrama no tiene puertos sin conectar antes de ejecutar la simulación
        print("*****Checking diagram integrity*****")
        error_trigger = False
        for block in self.blocks_list:
            inputs, outputs = self.get_neighbors(block.name)
            if block.in_ports == 1 and len(inputs) < block.in_ports:
                print("ERROR. UNLINKED INPUT IN BLOCK:",block.name)
                error_trigger = True
            elif block.in_ports > 1:
                in_vector = np.zeros(block.in_ports)
                for tupla in inputs:
                    in_vector[tupla['dstport']] += 1
                finders = np.where(in_vector == 0)
                if len(finders[0]) > 0:
                    print("ERROR. UNLINKED INPUT(S) IN BLOCK:",block.name,"PORT(S):",finders[0])
                    error_trigger = True
            if block.out_ports == 1 and len(outputs) < block.out_ports:
                print("ERROR. UNLINKED OUTPUT PORT:",block.name)
                error_trigger = True
            elif block.out_ports > 1:
                out_vector = np.zeros(block.out_ports)
                for tupla in outputs:
                    out_vector[tupla['srcport']] += 1
                finders = np.where(out_vector == 0)
                if len(finders[0]) > 0:
                    print("ERROR. UNLINKED OUTPUT(S) IN BLOCK:",block.name,"PORT(S):",finders[0])
                    error_trigger = True
        if error_trigger == True:
            return 1
        print("NO ISSUES FOUND IN DIAGRAM")
        return 0

    def count_rk45_ints(self):
        """
        Checks all integrators and looks if there's at least one that use 'RK45' as integration method
        """
        for block in self.blocks_list:
            if block.b_type == 'Integr' and block.params['method'] == 'RK45':
                return True
        return False

    def reset_memblocks(self):
        """
        Resets the "_init_start_" parameter to all blocks
        """
        # Reestablece todos los bloques del sistema que contengan instrucciones especiales para su primera ejecución
        for block in self.blocks_list:
            if '_init_start_' in block.params.keys():
                block.params['_init_start_'] = True

    def plotScope(self):
        """
        Plots the data saved in Scope blocks
        """
        # Grafica los datos obtenidos de los bloques Scope
        scope_counter = 0
        for block in self.blocks_list:
            if block.b_type == 'Scope':
                if scope_counter == 0:
                    plt.figure()
                plt.plot(self.timeline, block.params['vector'], label=block.params['vec_labels'])
                scope_counter += 1
        if scope_counter > 0:
            plt.xlabel('Time [s]')
            plt.legend()
            plt.show()

    def exportData(self):
        """
        Exports the data saved in Export blocks
        """
        # Reune los vectores a guardar y se exportan en formato .npz
        vec_dict = {}
        export_toggle = False
        for block in self.blocks_list:
            if block.b_type == 'Export':
                export_toggle = True
                labels = block.params['vec_labels']
                vector = block.params['vector']
                if block.params['vec_dim'] == 1:
                    vec_dict[labels] = vector
                elif block.params['vec_dim'] > 1:
                    for i in range(block.params['vec_dim']):
                        vec_dict[labels[i]] = vector[:,i]
        if export_toggle == True:
            np.savez('saves/' + self.filename[:-4], t = self.timeline, **vec_dict)
            print("DATA EXPORTED TO",'saves/' + self.filename[:-4] + '.npz')

        '''# Formato a guardar: .csv
        export_mtx = self.timeline
        head = 't'
        for block in self.blocks_list:
            if block.b_type == 'Export':
                vector = block.params['vector']
                export_mtx = np.column_stack((export_mtx, vector))
                head += ',' + block.params['vector_name']
        np.savetxt(self.filename[:-4] + '_exported.csv', export_mtx, delimiter=",", header=head)#'''


class Block(InitSim):
    """
    Class to initialize, mantain and modify function blocks
    """
    # Clase para inicializar y mantener a los bloques
    def __init__(self, b_type, sid, coords, color, in_ports=1, out_ports=1, run_ord=2, io_edit=True, fun_name='block', params={}, external=False):
        super().__init__()
        self.name = b_type + str(sid)   # Nombre del bloque
        self.b_type = b_type            # Tipo de bloque
        self.sid = sid                  # id del bloque
        self.b_color = self.set_color(color) # color del bloque
        self.left = coords[0]           # Coordenada ubicación línea izquierda
        self.top = coords[1]            # Coordenada ubicación línea superior
        self.width = coords[2]          # Ancho bloque
        self.height = coords[3]         # Altura bloque
        self.fun_name = fun_name        # Nombre función asociada para ejecución
        self.params = self.loading_params(params) # Parámetros asociados a la función
        self.init_params_list = list(self.params.keys()) # Lista de parámetros iniciales/editables
        self.external = external

        self.port_radius = 8            # Radio del circulo para el dibujado de los puertos
        self.height_base = self.height  # Variable que conserva valor de altura por defecto
        self.in_ports = in_ports        # Variable que contiene el número de puertos de entrada
        self.out_ports = out_ports      # Variable que contiene el número de puertos de salida

        # Datos básicos del bloque para identificación en funciones.
        self.params.update({'_name_': self.name,'_inputs_': self.in_ports ,'_outputs_': self.out_ports})

        self.rectf = pygame.rect.Rect(self.left - self.port_radius, self.top, self.width + 2 * self.port_radius,
                                      self.height)  # Rect que define la colisión del bloque

        self.in_coords = []             # Lista que contiene coordenadas para cada puerto de entrada
        self.out_coords = []            # Lista que contiene coordenadas para cada puerto de salida
        self.io_edit = io_edit          # Variable que determina si el número de inputs y outputs puede cambiarse.
        self.update_Block()             # Ubica las coordenadas de los puertos actualizando también el tamaño del bloque

        self.run_ord = run_ord          # Posición de prioridad al correr la simulación
        self.dragging = False           # Booleano para determinar si el bloque se está moviendo
        self.selected = False           # Booleano para determinar si el bloque está seleccionado en el plano

        # Variables para la inicialización de texto para cada bloque (nombre)
        self.font_size = 24             # Tamaño del texto
        self.text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.text.render(self.name, True, self.colors['black'])

        # Variables para simulacion
        self.hierarchy = -1             # Indica el nivel de jerarquía para ejecutar durante la simulación
        self.data_recieved = 0          # Variable que indica cuando datos se han recibido para calcular la función
        self.computed_data = False      # Flag que indica si la función asociada al bloque ha sido ejecutada
        self.data_sent = 0              # Variable que indica a cuantos bloques se ha enviado el resultado de la función
        self.input_queue = {}           # Diccionario el cual almacena los datos que llegan desde otros bloques

    def update_Block(self):
        # Actualiza ubicación y dimensiones del bloque como también definir la de los puertos
        self.in_coords = []
        self.out_coords = []

        # En caso que el número de puertos sea muy grande, se redimensiona el bloque
        port_height = max(self.out_ports, self.in_ports) * self.port_radius * 2
        if port_height > self.height:
            self.height = port_height + 10
        elif port_height < self.height_base:
            self.height = self.height_base
        elif port_height < self.height:
            self.height = port_height + 10
        self.rectf.update((self.left - self.port_radius, self.top, self.width + 2 * self.port_radius, self.height))

        # Se ubican los puertos de forma simétrica en ambos lados
        if self.in_ports > 0:
            for i in range(self.in_ports):
                port_in = (self.left, self.top + self.height * (i + 1) / (self.in_ports + 1))
                self.in_coords.append(port_in)
        if self.out_ports > 0:
            for j in range(self.out_ports):
                port_out = (self.left + self.width, self.top + self.height * (j + 1) / (self.out_ports + 1))
                self.out_coords.append(port_out)

    def draw_Block(self, zone):
        # Dibuja el bloque y los puertos
        pygame.draw.rect(zone, self.b_color, (self.left, self.top, self.width, self.height))
        for port_in_location in self.in_coords:
            pygame.draw.circle(zone, self.colors['black'], port_in_location, self.port_radius)

        for port_out_location in self.out_coords:
            pygame.draw.circle(zone, self.colors['black'], port_out_location, self.port_radius)

    def draw_selected(self, zone):
        # Dibuja linea de selección en torno a un bloque.
        pygame.draw.line(zone, self.colors['black'], (self.left - self.ls_width, self.top - self.ls_width),
                         (self.left + self.width + self.ls_width, self.top - self.ls_width), self.l_width)
        pygame.draw.line(zone, self.colors['black'], (self.left - self.ls_width, self.top - self.ls_width),
                         (self.left - self.ls_width, self.top + self.height + self.ls_width), self.l_width)
        pygame.draw.line(zone, self.colors['black'], (self.left + self.width + self.ls_width, self.top + self.height + self.ls_width),
                         (self.left + self.width + 5, self.top - self.ls_width), self.l_width)
        pygame.draw.line(zone, self.colors['black'], (self.left + self.width + self.ls_width, self.top + self.height + self.ls_width),
                         (self.left - self.ls_width, self.top + self.height + self.ls_width), self.l_width)
        zone.blit(self.text_display, (self.left + 0.5 * (self.width - self.text_display.get_width()), self.top - 25))
        if self.external == True:
            self.function_display = self.text.render(self.params['filename'], True, self.colors['black'])
            zone.blit(self.function_display,(self.left + 0.5 * (self.width - self.function_display.get_width()), self.top + self.height + 15))

    def set_color(self, color):
        # Define el color del bloque a partir de un string o directamente de una tupla con los valores RGB
        if type(color) == str:
            return self.colors[color]
        elif type(color) == tuple or list:
            return color

    def port_collision(self, m_coords):
        # Observa si el mouse toca alguno de los puertos de un bloque. Retorna una tupla con el tipo de puerto y su id.
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

    def relocate_Block(self, new_coords):  # new_coords = (left,top)
        # Función simple para reubicar el bloque en el plano, requiere coordenadas de la esquina superior izquierda
        self.left = new_coords[0]
        self.top = new_coords[1]
        self.update_Block()

    def resize_Block(self, new_coords):  # new_dims = (width,height)
        # Función simple para redimensionar el bloque en el plano, requiere ancho y altura ingresado como tupla
        self.width = new_coords[0]
        self.height = new_coords[1]
        self.update_Block()

    def change_port_numbers(self):
        # Funcion que habilita un pop up con la opción de cambiar el numero de entrada o salida a un bloque
        # Esta definido por 3 estados en el que se permite editar solo inputs, solo output o ambos
        if self.io_edit == 'both':
            # Se pueden editar inputs y outputs
            io_widget = Tk_widget(self.name, {'inputs': self.in_ports, 'outputs': self.out_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.in_ports = int(new_io['inputs'])
                self.out_ports = int(new_io['outputs'])
                io_widget.destroy()

        elif self.io_edit == 'input':
            # Solo se pueden editar inputs
            io_widget = Tk_widget(self.name, {'inputs': self.in_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.in_ports = int(new_io['inputs'])
                io_widget.destroy()

        elif self.io_edit == 'output':
            # Solo se pueden editar outputs
            io_widget = Tk_widget(self.name, {'outputs': self.out_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.out_ports = int(new_io['outputs'])
                io_widget.destroy()

        self.update_Block()

        # para actualizar los datos en los parametros hacia las funciones
        self.params['_inputs_'] = self.in_ports
        self.params['_outputs_'] = self.out_ports

    def saving_params(self):
        # Actualizar funcion para aceptar los arrays como corresponde
        # Guarda únicamente los parámetros definidos inicialmente, no los agregados durante la ejecución
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
        # Cargar los datos desde el .txt, transformando las listas en np.ndarrays.
        try:
            for key in new_params.keys():
                if isinstance(new_params[key], list):
                    new_params[key] = np.array(new_params[key])
            return new_params
        except:
            return new_params

    def change_params(self):
        # Se cambian los valores de los parametros para cada bloque a partir del diccionario con la lista completa de parametros y la lista que indica que se puede editar
        if self.params == {}:
            return

        ed_dict = {}
        non_ed_dict = {}

        for key in self.params.keys():
            if key in self.init_params_list and not (key[0] == key[-1] == '_'):
                ed_dict[key] = self.params[key]
            else:
                non_ed_dict[key] = self.params[key]

        if ed_dict == {}:
            return

        widget_params = Tk_widget(self.name, ed_dict)
        new_inputs = widget_params.get_values()

        if new_inputs != {}:
            new_inputs.update(non_ed_dict)
            self.params = new_inputs
            widget_params.destroy()

    def load_external_data(self):
        # Carga la funcion desde un archivo .py externo
        if self.external == False:
            return

        full_module_name = self.params['filename']
        try:
            self.file_function = importlib.import_module(full_module_name)
            importlib.reload(self.file_function)
        except:
            print(self.name, "ERROR: NO MODULE FUNCTION",full_module_name,"WAS FOUND")
            return

        file_dir = dir(self.file_function)
        fun_list, fn_params = self.file_function._init_()

        if hasattr(self.file_function, full_module_name):
            pass
        else:
            print(self.name, "ERROR: NO FUNCTION",full_module_name,"WAS FOUND IN THE MODULE",full_module_name)
            print("THE MAIN FUNCTION MUST HAVE THE SAME NAME AS THE FILE")
            self.params['filename'] = '<no filename>'
            return

        self.params.update(fn_params)
        self.run_ord = fun_list['run_ord']
        self.in_ports = fun_list['inputs']
        self.out_ports = fun_list['outputs']
        self.fun_name = full_module_name
        self.update_Block()
        print("MODULE FUNCTION:", full_module_name, "WAS LOADED")

    def reload_external_data(self):
        # Actualiza unicamente los parametros de la funcion del archivo externo
        if self.external == False:
            return 0

        if self.params['filename'] == '<no filename>':
            print("ERROR: NO EXTERNAL FUNCTION IS DEFINED FOR",self.name)
            return 1

        #Si no existe un import previo de la función, se intenta cargar a partir del nombre de archivo asignado al bloque
        if not hasattr(self, 'file_function'):
            full_module_name = self.params['filename']
            self.file_function = importlib.import_module(full_module_name)
        else:
            importlib.reload(self.file_function)

        fun_list, fn_params = self.file_function._init_()
        self.params.update(fn_params)
        return 0
        # falta caso bloque con memoria (a lo integrador)


class Line(InitSim):
    """
    Class to initialize and maintain lines that connect blocks
    """
    # Clase para la inicialización y mantención de las líneas
    def __init__(self, sid, srcblock, srcport, points, dstblock, dstport, zorder=0):
        super().__init__()
        self.name = "Line" + str(sid)       # Nombre de la línea
        self.sid = sid                      # id de la línea
        self.srcblock = srcblock            # Nombre del bloque de origen
        self.srcport = srcport              # ID del puerto de origen del bloque
        self.points = points                # puntos de vertice para la línea(?) ((a,b),(c,d),(e,f),...)
        self.dstblock = dstblock            # Nombre del bloque de origen
        self.dstport = dstport              # ID del puerto de origen del bloque
        self.zorder = zorder                # ID de prioridad al momento de dibujar el bloque
        self.selected = False               # Indica estado de selección en pantalla

    def draw_line(self,zone):
        # Dibuja la línea con los datos del init
        for i in range(len(self.points) - 1):
            if self.selected == True:
                line_width = 5
            else:
                line_width = 2
            pygame.draw.line(zone, self.colors['black'], self.points[i], self.points[i + 1], line_width)

    def update_line(self, block_list):
        # Actualiza el valor de la línea según la ubicación y tamaño del bloque
        for block in block_list:
            if block.name == self.srcblock:
                startline = block.out_coords[self.srcport]
            if block.name == self.dstblock:
                endline = block.in_coords[self.dstport]
        self.points = (startline, endline)

    def collision(self, m_coords):
        # Determinar colisión entre línea y posición de un click
        min_dst = 10
        line_A = np.array(self.points[0])
        line_B = np.array(self.points[1])
        m_coords = np.array(m_coords)

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

        if distance_to_line > min_dst:
            return False
        else:
            return True

    def __str__(self):
        # Imprime en la consola, el nombre de la línea, su origen y destino
        return self.name + ": From " + str(self.srcblock) + ", port " + str(self.srcport) + " to " + str(
            self.dstblock) + ", port " + str(self.dstport)


class BaseBlocks(InitSim):
    """
    Class to create and show basic blocks used as a mark to generate functional blocks in the user interface
    """
    # Produce un "boton" para generar bloques con las caracteristicas indicadas
    def __init__(self,b_type, fun_name, io_params, ex_params, b_color, coords, external=False):
        super().__init__()
        self.b_type = b_type
        self.fun_name = fun_name
        self.ins = io_params['inputs']
        self.outs = io_params['outputs']
        self.run_ord = io_params['run_ord']
        self.io_edit = io_params['io_edit']
        self.params = ex_params                           # parametros de ejecución en simulación
        self.b_color = self.set_color(b_color)            # Color caracteristico del bloque
        self.size = coords                                # Dimensiones del bloque
        self.external = external

        self.font_size = 24  # Tamaño del texto
        self.text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.text.render(self.fun_name, True, self.colors['black'])

    def draw_baseblock(self,zone, pos):
        # Dibuja el bloque
        self.collision = pygame.rect.Rect(40, 60 + 40*pos, 30, 30)
        pygame.draw.rect(zone, self.b_color, self.collision)
        zone.blit(self.text_display, (90, 70 + 40*pos))

    def set_color(self, color):
        # Define el color del bloque a partir de un string o directamente de una tupla con los valores RGB
        if type(color) == str:
            return self.colors[color]
        elif type(color) == tuple:
            return color


class Button(InitSim):
    """
    Class to create and show buttons in the user interface
    """
    # Produce un boton con texto
    def __init__(self, name, coords):
        super().__init__()
        self.name = name                                                            # Nombre que se mostrará en el botón
        self.coords = coords                                                        # Ubicación del botón
        self.collision = pygame.rect.Rect(coords)                                   # Colisión del botón
        self.pressed = False
        self.font_size = 24  # Tamaño del texto
        self.font_text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.font_text.render(name, True, self.colors['black']) # Render del botón

    def draw_button(self, zone):
        # Dibuja el boton en la pantalla, con su nombre en el centro
        if self.pressed == True:
            color = (64, 64, 64)
        else:
            color = (128, 128, 128)
        pygame.draw.rect(zone, color, self.collision)
        if not (self.name[0] == self.name[-1] == '_'):
            zone.blit(self.text_display, (self.collision.left + 0.5 * (self.collision.width - self.text_display.get_width()),
                                 self.collision.top + 0.5 * (self.collision.height - self.text_display.get_height())))
        elif self.name == '_pauseplay_':
            pygame.draw.polygon(zone, self.colors['black'], ( (self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.25 * self.collision.height),(self.collision.left + 0.25 * self.collision.width, self.collision.top + 0.75 * self.collision.height),(self.collision.left + 0.5 * self.collision.width, self.collision.top + 0.5 * self.collision.height) ))
            pygame.draw.rect(zone, self.colors['black'], (self.collision.left + 0.5 * self.collision.width, self.collision.top + 0.25 * self.collision.height, 4, 0.5 * self.collision.height))
            pygame.draw.rect(zone, self.colors['black'], (self.collision.left + 0.5 * self.collision.width + 8, self.collision.top + 0.25 * self.collision.height, 4, 0.5 * self.collision.height))

    def set_color(self, color):
        # Define el color del bloque a partir de un string o directamente de una tupla con los valores RGB
        if type(color) == str:
            return self.colors[color]
        elif type(color) == tuple:
            return color

    def change_color(self):
        if self.pressed == True:
            self.color = self.color_pressed
        else:
            self.color = self.color_base


class Tk_widget:
    """
    Class used to create popup windows for changing data, like ports and parameters.
    """
    # Clase para poder producir los pop up windows para modificar datos
    def __init__(self, name, params):
        self.params = params
        self.params_names = list(params.keys())
        self.n = len(self.params_names)
        self.master = tk.Tk()
        self.master.title(name+' parameters')
        self.entry_widgets = [self.create_entry_widget(x) for x in range(self.n)]
        tk.Button(self.master, text='Ok', command=self.master.quit).grid(row=self.n+1, column=0, sticky=tk.W, pady=4)
        tk.mainloop()

    def create_entry_widget(self, x):
        # Crea una nueva línea que permite editar datos
        new_widget = tk.Entry(self.master)
        tk.Label(self.master, text=self.params_names[x]).grid(row=x, column = 0)
        new_widget.grid(row = x, column= 1)

        # Diferenciar entre np.nparray y otros para convertir correctamente a string.
        value = self.params[self.params_names[x]]
        if isinstance(value, np.ndarray):
            new_widget.insert(0, np.array2string(value, separator=','))
        else:
            new_widget.insert(0, str(value))
        return new_widget

    def get_values(self):
        # Entrega un diccionario con los datos obtenidos de la ventana
        try:
            dict = {}
            for i in range(len(self.entry_widgets)):
                dato = str(self.entry_widgets[i].get())

                # convertir a np.ndarray
                if dato[0] == '[' and dato[-1] == ']':
                    dato = self.string_to_vector(dato)
                # convertir a float
                elif dato.replace('.', '', 1).replace('-', '', 1).isdigit():
                    dato = float(dato)
                # convertir a booleano
                elif dato == 'True' or dato == 'true':
                    dato = True
                elif dato == 'False' or dato == 'false':
                    dato = False

                dict[self.params_names[i]] = dato
            return dict
        except:
            return {}

    def string_to_vector(self, string):
        # convierte el dato guardado de un string a un array. Soporta el uso de espacios y corchetes, separa unicamente valores con comas.
        # primero se buscan las dimensiones del array eliminando todos los números
        string_shape = string
        for char in string_shape:
            if char not in "[],;":
                string_shape = string_shape.replace(char, '')

        # unicamente soporte para matrices de 3 dimensiones shape = (a,b,c)
        first_dim = int(string_shape.count(']],[[') + 1)
        second_dim = int((string_shape.count('],[') - string_shape.count(']],[[')) / first_dim + 1)
        third_dim = int((string_shape.count(',') - string_shape.count('],[')) / (first_dim * second_dim) + 1)
        shape = [first_dim, second_dim, third_dim]

        while True:
            if (shape[0] == 1 and len(shape) == 1) or shape[0] != 1:
                break
            else:
                shape = shape[1:]

        # del string se eliminan todos los valores que no sean comas o números
        for char in "[] ":
            string = string.replace(char, '')
        string = string.replace(';', ',')

        # se transforma el string resultante a un np.ndarray ajustando las dimensiones de acuerdo a lo calculado en shape
        array = np.fromstring(string, dtype=float, sep=',')
        dim = np.prod(shape)
        if len(array) == dim:
            array = array.reshape(shape)
            return array
        else:
            print("MATRIX DIMENSIONS ARE INCORRECT")
            return ""

    def destroy(self):
        # Finaliza la ventana
        self.master.destroy()


class Functions_call:
    """
    Class to contain all the default functions available to work with in the simulation interface
    """
    #Funciones utilizadas durante la ejecución del sistema

    def step(self, time, inputs, params):
        """
        Step source function
        """
        # Funcion escalón base
        if params['type'] == 'up':
            change = True if time < params['delay'] else False
        elif params['type'] == 'down':
            change = True if time > params['delay'] else False
        else:
            print("ERROR: 'type' not defined correctly in", params['_name_'])
            return {'E': True}

        if change == True:
            return {0: 0*abs(np.array(params['value']))}
        elif change == False:
            return {0: np.array(params['value'])}


    def ramp(self, time, inputs, params):
        """
        Ramp source function
        """
        # Funcion rampa
        if params['slope'] == 0:
            return {0: 0}
        elif params['slope'] > 0:
            return {0: np.maximum(0,params['slope']*(time - params['delay']))}
        elif params['slope'] < 0:
            return {0: np.array(np.minimum(0, params['slope'] * (time - params['delay'])))}


    def sine(self, time, inputs, params):
        """
        Sinusoidal source function
        """
        # Funcion sinusoidal
        return {0: np.array(params['amplitude']*np.sin(params['omega']*time + params['init_angle']))}


    #vector
    def gain(self, time, inputs, params):
        """
        Gain function
        """
        # Funcion ganancia
        return {0: np.array(np.dot(params['gain'],inputs[0]))}


    #vector
    def exponential(self, time, inputs, params):
        """
        Exponential function
        """
        # Funcion exponencial

        return {0: np.array(params['a']*np.exp(params['b']*inputs[0]))}


    def sumator(self, time, inputs, params):
        """
        Sumator function
        """
        # Funcion sumador
        for i in range(len(inputs)-1):
            if inputs[i].shape != inputs[i+1].shape:
                print("ERROR: Dimensions don't fit in", params['_name_'])
                return {'E': True}

        if len(params['sign']) < len(inputs):
            params['sign'] += (len(inputs)-len(params['sign']))*'+'

        suma = np.zeros(inputs[0].shape)
        for i in range(len(inputs)):
            if params['sign'][i] == '+':
                suma += inputs[i]
            elif params['sign'][i] == '-':
                suma -= inputs[i]
            else:
                print("ERROR: Symbols not defined in", params['_name_'])
                return {'E': True}
        return {0: suma}


    def sigproduct(self, time, inputs, params):
        """
        Element-wise product between signals
        """
        # Funcion producto punto
        mult = 1.0
        for i in range(len(inputs)):
            mult *= inputs[i]
        return {0: mult}


    def block(self, time, inputs, params):
        """
        Generic block function - no actual use
        """
        # Funcion bloque generico (No hace nada sin un archivo externo)
        return {0: np.array(inputs[0])}


    def terminator(self, time, inputs, params):
        """
        Signal terminator function
        """
        # Funcion terminator
        return {0: np.array([0.0])}


    def noise(self, time, inputs, params):
        """
        Normal noise function
        """
        # Funcion noise (agrega ruido a la señal)
        return {0: np.array(params['sigma']**2*np.random.randn() + params['mu'])}


    def mux(self, time, inputs, params):
        """
        Multiplexer function
        """
        # Funcion mux
        array = np.array(inputs[0])
        for i in range(1, len(inputs)):
            array = np.append(array, inputs[i])
        return {0: array}


    def demux(self, time, inputs, params):
        """
        Demultiplexer function
        """
        # Funcion demux

        # Primero se comprueba que las dimensiones del vector son suficientes para el demux. Entrega Error o Warning según largo.
        if len(inputs[0]) / params['output_shape'] < params['_outputs_']:
            print("ERROR: Not enough inputs or wrong output shape in", params['_name_'])
            return {'E': True}

        elif len(inputs[0]) / params['output_shape'] > params['_outputs_']:
            print("WARNING: There are more elements in vector for the expected outputs. System will truncate. Block", params['_name_'])

        outputs = {}
        for i in range(params['_outputs_']):
            outputs[i] = inputs[0][int(params['output_shape'])*i : int(params['output_shape'])*(i+1)]
        return outputs


    # bloques tipo memoria
    def integrator(self, time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
        """
        Integrator function
        """
        # Funcion integrador
        if params['_init_start_'] == True:
            params['dtime'] = dtime
            params['mem'] = np.array(params['init_conds'])
            params['mem_list'] = [np.zeros(params['mem'].shape)]
            params['mem_len'] = 5.0 # Agregar otros largos dependiendo del metodo
            params['_init_start_'] = False

            if params['method'] == 'RK45':
                params['nb_loop'] = 0
                params['RK45_Klist'] = [0, 0, 0, 0]  # K1, K2, K3, K4

            params['add_in_memory'] = True # Para entregar valores de output_only al principio

        if output_only == True:
            old_add_in_memory = params['add_in_memory']
            params['add_in_memory'] = next_add_in_memory  # Actualizar para siguiente loop
            if old_add_in_memory == True:
                return {0: params['mem']}
            else:
                return {0: params['aux']}
        else:
            # Comprueba que los vectores de llegada tengan las mismas dimensiones que el vector memoria.
            if params['mem'].shape != inputs[0].shape:
                print("ERROR: Dimension Error in initial conditions in", params['_name_'])
                params['_init_start_'] = True
                return {'E': True}

            # Se entrega el valor antes de agregar, por lo que se guarda antes de cambiar
            mem_old = params['mem']

            # Se integra según método escogido
            # Forward euler
            if params['method'] == 'FWD_RECT':
                if params['add_in_memory'] == True:
                    params['mem'] += params['dtime'] * inputs[0]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * inputs[0])
                    return {0: params['aux']}

            # Backwards euler
            elif params['method'] == 'BWD_RECT':
                if params['add_in_memory'] == True:
                    params['mem'] += params['dtime'] * params['mem_list'][-1]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * params['mem_list'][-1])
                    return {0: params['aux']}

            # Tustin
            elif params['method'] == 'TUSTIN':
                if params['add_in_memory'] == True:
                    params['mem'] += 0.5*params['dtime'] * (inputs[0] + params['mem_list'][-1])
                else:
                    params['aux'] = np.array(params['mem'] + 0.25 * params['dtime'] * (inputs[0] + params['mem_list'][-1]))
                    return {0: params['aux']}

            # Runge-Kutta 45
            elif params['method'] == 'RK45':
                K_list = params['RK45_Klist']
                K_list[params['nb_loop']] = params['dtime'] * inputs[0]     # Calculo de K1, K2, K3 o K4
                params['RK45_Klist'] = K_list
                K1, K2, K3, K4 = K_list

                if params['nb_loop'] == 0:
                    params['nb_loop'] += 1
                    params['aux'] = np.array(params['mem'] + 0.5 * K1)
                    return {0: params['aux']}
                elif params['nb_loop'] == 1:
                    params['nb_loop'] += 1
                    params['aux'] = np.array(params['mem'] + 0.5 * K2)
                    return {0: params['aux']}
                elif params['nb_loop'] == 2:
                    params['nb_loop'] += 1
                    params['aux'] = np.array(params['mem'] + K3)
                    return {0: params['aux']}
                elif params['nb_loop'] == 3:
                    params['nb_loop'] = 0
                    params['mem'] += (1 / 6) * (K1 + 2 * K2 + 2 * K3 + K4)

            aux_list = params['mem_list']
            aux_list.append(inputs[0])
            if len(aux_list) > params['mem_len']: # 5 solo por probar, dependería del método de integración
                aux_list = aux_list[-5:]
            params['mem_list'] = aux_list

            return {0: mem_old}


    def export(self, time, inputs, params):
        """
        Block to save and export block signals
        """
        #Funcion exportar datos
        # Para evitar guardar datos en los intervalos intermedios de RK45
        if 'skip' in params.keys() and params['skip'] == True:
            params['skip'] = False
            return {0: inputs[0]}
        # Iniciar el vector de guardado
        if params['_init_start_'] == True:
            aux_vector = np.array([inputs[0]])
            try:
                params['vec_dim'] = len(inputs[0])
            except:
                params['vec_dim'] = 1

            labels = params['str_name']
            if labels == 'default':
                labels = params['_name_'] + '-0'
            labels = labels.replace(' ', '').split(',')
            if len(labels) < params['vec_dim']:
                for i in range(params['vec_dim'] - len(labels)):
                    labels.append(params['_name_'] + '-' + str(params['vec_dim'] + i - 1))
            elif len(labels) > params['vec_dim']:
                labels = labels[:params['vec_dim']]
            if len(labels) == params['vec_dim'] == 1:
                labels = labels[0]
            params['vec_labels'] = labels
            params['_init_start_'] = False
        else:
            aux_vector = params['vector']
            aux_vector = np.concatenate((aux_vector, [inputs[0]]))
        params['vector'] = aux_vector
        return {0: inputs[0]}


    def scope(self, time, inputs, params):
        """
        Function to plot block signals
        """
        # Funcion graficar datos (MatPlotLib)
        # Para evitar guardar datos en los intervalos intermedios de RK45
        if 'skip' in params.keys() and params['skip'] == True:
            params['skip'] = False
            return {0: inputs[0]}
        # Iniciar el vector de guardado
        if params['_init_start_'] == True:
            aux_vector = np.array([inputs[0]])
            try:
                params['vec_dim'] = len(inputs[0])
            except:
                params['vec_dim'] = 1

            labels = params['labels']
            if labels == 'default':
                labels = params['_name_'] + '-0'
            labels = labels.replace(' ','').split(',')
            if len(labels) < params['vec_dim']:
                for i in range(params['vec_dim'] - len(labels)):
                    labels.append(params['_name_'] + '-' + str(params['vec_dim'] + i - 1))
            elif len(labels) > params['vec_dim']:
                labels = labels[:params['vec_dim']]
            if len(labels) == params['vec_dim'] == 1:
                labels = labels[0]
            params['vec_labels'] = labels
            params['_init_start_'] = False
        else:
            aux_vector = params['vector']
            aux_vector = np.concatenate((aux_vector, [inputs[0]]))
        params['vector'] = aux_vector
        return {0: inputs[0]}


    # bloques con multiples salidas
    def test_MO(self, time, inputs, params):
        return {0: np.array([1,5]), 1: np.array([-1])}
