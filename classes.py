import pygame
import numpy as np
import time
import json
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import os

class InitSim:
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

        self.sim_dt = 0.01      # diferencia de tiempo para simulación (default: 10ms)

    def add_block(self, block, event_xy):
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
        mouse_x, mouse_y = event_xy
        block_collision = (np.random.randint(mouse_x + 200,mouse_x + 500), np.random.randint(mouse_y - 50, mouse_y + 50), block.size[0], block.size[1])
        new_block = Block(block.b_type, sid, block_collision, block.b_color, block.ins, block.outs, block.run_ord, block.io_edit, block.fun_name, block.params)
        self.blocks_list.append(new_block)

    def add_line(self, srcData, dstData):
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
        # remueve el bloque de la lista, retornando también una segunda lista con los valores eliminados para su utilización en la eliminación de líneas
        b_del = [x.name for x in self.blocks_list if x.selected == True]
        self.blocks_list = [x for x in self.blocks_list if not (x.selected == True)]

        if len(b_del) >= 1:
            self.line_list = [x for x in self.line_list if not self.check_line_block(x, b_del)]
        else:
            self.line_list = [x for x in self.line_list if x.selected == False]

    def check_line_block(self, line, b_del_list):
        # Comprueba si es que hay lineas a bloques recientemente eliminados
        if line.dstblock in b_del_list or line.srcblock in b_del_list:
            return True
        return False

    def check_line_port(self, line, block):
        # Comprueba si es que hay lineas a puertos recientemente eliminados
        if line.srcblock == block.name and line.srcport > block.out_ports - 1:
            return True
        elif line.dstblock == block.name and line.dstport > block.in_ports - 1:
            return True
        else:
            return False

    def print_lines(self, zone):
        # Dibuja las líneas a partir de una lista
        for line in self.line_list:
            line.draw_line(zone)

    def update_lines(self):
        # Actualiza la ubicación de las líneas a partir de la ubicación de los bloques
        for line in self.line_list:
            line.update_line(self.blocks_list)

    def blockScreen(self, zone):
        # Dibuja los bloques incluyendo al seleccionado
        for b_elem in self.blocks_list:
            if b_elem.selected == True:
                b_elem.draw_selected(zone)
            b_elem.draw_Block(zone)

    def port_availability(self, dst_line):
        # Comprueba si es que el puerto a conectar está libre para ello
        for line in self.line_list:
            if line.dstblock == dst_line[0] and line.dstport == dst_line[1]:
                return False
        return True

    def base_blocks_init(self):
        # Inicializa los bloques del menú, son estos los que se copian para generar los bloques y funciones.
        # Algunos datos se envían en forma de diccionarios para que se pueda observar qué es cada cosa
        # Los colores pueden definirse como strings (si es que están en self.colors) o directamente con los valores RGB en tupla.

        block = BaseBlocks("Block",'block',
                           {'inputs': 1, 'outputs': 1, 'run_ord': 2, 'io_edit': 'both'}, {"function_name": 'blocky'},
                           'green', (120, 60))

        step = BaseBlocks("Step", 'step',
                              {'inputs': 0, 'outputs': 1, 'run_ord': 0, 'io_edit': False}, {'value': 1.0, 'delay': 0.0, 'type': 'up'},
                              'blue', (60, 60))

        gain = BaseBlocks("Gain", 'gain',
                          {'inputs': 1, 'outputs': 1, 'run_ord': 2, 'io_edit': False}, {'gain': 1.0},
                          'yellow', (60, 60))

        integrator = BaseBlocks("Integr", 'integrator',
                                {'inputs': 1, 'outputs': 1, 'run_ord': 1, 'io_edit': False}, {'init_conds': 0.0, 'init_start': True},
                                'magenta', (80, 60))

        sumator = BaseBlocks("Sum", 'sumator',
                             {'inputs': 2, 'outputs': 1, 'run_ord': 2, 'io_edit': 'input'}, {'sign': "++"},
                             'cyan', (70, 50))

        multiplicator = BaseBlocks("Mult", 'multiplicator',
                                   {'inputs': 2, 'outputs': 1, 'run_ord': 2, 'io_edit': 'input'}, {'sign': "**"},
                                   'green', (70, 50))

        terminator = BaseBlocks("Term", 'terminator',
                                {'inputs': 1, 'outputs': 0, 'run_ord': 3, 'io_edit': False}, {},
                                'red', (60, 60))

        sine = BaseBlocks("Sine", 'sine',
                          {'inputs': 0, 'outputs': 1, 'run_ord': 0, 'io_edit': False}, {'amplitude': 1.0, 'omega': 2.0 * np.pi, 'init_angle': 0},
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

        scope = BaseBlocks("Scope", 'scope',
                           {'inputs': 1, 'outputs': 0, 'run_ord': 3, 'io_edit': 'input'}, {},
                           (220,20,60), (60, 60))

        testmo = BaseBlocks("TestMO", "test_MO",
                            {'inputs': 0, 'outputs': 2, 'run_ord': 0, 'io_edit': False}, {},
                            (0, 20, 60), (60, 60))

        self.base_blocks = [step,sine,ramp,noise,integrator,gain,exponential,block,sumator,multiplicator,terminator,scope,testmo]

    def draw_base_blocks(self,zone):
        # Dibuja los bloques del menú y la línea separadora
        pygame.draw.line(zone, self.colors['black'], [250, 0], [250, 720], 2)
        for i in range(len(self.base_blocks)):
            self.base_blocks[i].draw_baseblock(zone, i)

    def save(self):
        # Guarda los datos en diccionarios, exportados a un .txt
        root = tk.Tk()
        root.withdraw()

        file = tk.filedialog.asksaveasfilename(initialfile='data.txt', filetypes=[('Text Files', '*.txt'),("All files", "*.*")])
        if file == '':
            return

        # Datos de InitSim
        init_dict = {
            "wind_width": self.SCREEN_WIDTH,
            "wind_height": self.SCREEN_HEIGHT,
            "fps": self.FPS,
            "line_creation": self.line_creation,
            "only_one": self.only_one,
            "enable_line_sel": self.enable_line_selection,
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
                "params": block.params,
                "ed_params": block.ed_params_list
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
        print("GUARDADO")


    def open(self):
        # Abre el archivo .txt y carga los datos guardados para mostrarlos en pantalla
        root = tk.Tk()
        root.withdraw()

        file = tk.filedialog.askopenfilename(initialfile='data.txt', filetypes=[('Text Files', '*.txt'),("All files", "*.*")])
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
        for block in blocks_data:
            self.update_blocks_data(block)
        for line in lines_data:
            self.update_lines_data(line)
        print("CARGADO")

    def update_sim_data(self,data):
        # Reordena los datos de los diccionarios, para utilizarlos en las configuraciones de la simulación
        self.SCREEN_WIDTH = data['wind_width']
        self.SCREEN_HEIGHT = data['wind_height']
        self.FPS = data['fps']
        self.line_creation = data['line_creation']
        self.only_one = data['only_one']
        self.enable_line_selection = data['enable_line_sel']
        self.sim_dt = data['sim_dt']

    def update_blocks_data(self,block_data):
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
                      block_data['params'])
        block.height_base = block_data['coords_height_base']
        block.selected = block_data['selected']
        block.dragging = block_data['dragging']
        block.ed_params_list = block_data['ed_params']
        self.blocks_list.append(block)

    def update_lines_data(self,line_data):
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
        # Elimina todos los bloques, lineas y variables, haciendo que la interfaz vuelva a quedar en el estado inicial.
        self.blocks_list = []
        self.line_list = []
        self.line_creation = 0
        self.only_one = False
        self.enable_line_selection = False

    def execution_init_time(self):
        # Por medio de un popup window, determina el tiempo a simular (ejecutar).
        master = tk.Tk()
        master.title('Simulate')

        tk.Label(master, text="Simulation Time").grid(row=0)
        entry = tk.Entry(master)
        entry.grid(row=0, column=1)
        entry.insert(10, '1.0')

        tk.Button(master, text='Accept', command=master.quit).grid(row=1, column=1, sticky=tk.W, pady=4)
        tk.mainloop()

        try:
            time_exec = float(entry.get())
            master.destroy()
            return time_exec
        except:
            return -1

    def execution_init(self):
        # Inicializa los parametros y bloques para la simulación del sistema, además de hacer la primera iteración de calculo
        self.execution_fun = Functions_call()
        self.time_step = 0
        self.timeline = np.array([self.time_step])

        self.execution_time = self.execution_init_time()

        # Para cancelar la simulación antes de correrla (habiendo presionado X en el pop up)
        if self.execution_time == -1:
            self.run_initialized = False
            return

        ###########################
        # Falta un chequeo de errores por referencia circular. Sin eso, la simulación no puede partir.
        ###########################

        # Chequeo de entradas y salidas:
        if self.check_diagram_integrity() == 1:
            return

        self.global_computed_list = [{'name': x.name, 'computed_data': x.computed_data, 'hierarchy': x.hierarchy}
                                for x in self.blocks_list]
        self.reset_execution_data()
        self.execution_time_start = time.time()

        print("*****EXECUTION*****")

        self.plotterms = {}

        #AJUSTAR PROBLEMA PARA CASOS CON MULTIPLES SALIDAS

        for block in self.blocks_list:
            children = {}
            if block.run_ord == 0:
                #print(block.name, "Ejecutar función", block.fun_name, block.params)
                out_value = getattr(self.execution_fun, block.fun_name)(block.params, self.time_step, block.input_queue)
                block.computed_data = True
                block.hierarchy = 0
                self.update_global_list(block.name, 0, True)
                children = self.get_outputs(block.name)

            elif block.run_ord == 1:
                #print(block.name, "Enviar output_data")
                out_value = getattr(self.execution_fun, block.fun_name)(block.params, self.time_step, block.input_queue, True, self.sim_dt)
                #out_value se debe cambiar a formato lista o al menos diccionario
                self.update_global_list(block.name, 0, True)
                children = self.get_outputs(block.name)

                #resolver problema con coseno y seno

            #update for multiples outputs
            for mblock in self.blocks_list:
                is_child, tuple_child = self.children_recognition(mblock.name, children)
                #if mblock.name in children.values():
                if is_child == True:
                    #print("Enviar datito", out_value, "a", mblock.name)
                    #mblock.input_queue.append(out_value)
                    mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                    mblock.data_recieved += 1
                    block.data_sent += 1

        h_count = 1
        while (self.check_global_list() != True):
            for block in self.blocks_list:
                if block.data_recieved == block.in_ports and block.computed_data != True:
                    #print(block.name, "Ejecutar función", block.fun_name, block.params,"inputs:",block.input_queue)
                    out_value = getattr(self.execution_fun, block.fun_name)(block.params, self.time_step,block.input_queue)
                    self.update_global_list(block.name, h_count, True)
                    block.computed_data = True
                    children = self.get_outputs(block.name)
                    if block.run_ord not in [1,3]: #elementos que no entregan resultado a children (1 es cond. inicial)
                        for mblock in self.blocks_list:
                            is_child, tuple_child = self.children_recognition(mblock.name, children)
                            # if mblock.name in children.values():
                            if is_child == True:
                                #print("Enviar datito", out_value, "a", mblock.name)
                                mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                                mblock.data_recieved += 1
                                block.data_sent += 1
                    elif block.run_ord == 3:
                        #print("Rama terminada")
                        if 'Scope' in block.name:
                            self.plotterms[block.name] = [out_value[0]]
            h_count += 1
            #print("***************")

        self.max_hier = self.get_max_hierarchy()  # Se determina el valor más alto de hierarchy
        self.run_initialized = True

    def execution_loop(self):
        # Después de inicializar, esta función es la que constantemente se repite en loop
        self.reset_execution_data()                                 # Se resetean los valores de ejecución cambiados en la etapa anterior
        self.time_step += self.sim_dt                               # Se avanza sim_dt en la linea de tiempo de la ejecución
        self.timeline = np.append(self.timeline,self.time_step)     # Se agrega este nuevo valor de tiempo a la escala de tiempo

        # Se ejecutan primero los bloques con memoria para obtener sólo el valor producido en la etapa anterior (no ejecutar la función primaria de estas)
        for block in self.blocks_list:
            if block.run_ord == 1:
                #print(block.name, "Enviar output_data")
                out_value = getattr(self.execution_fun, block.fun_name)(block.params, self.time_step, block.input_queue, True)
                self.update_global_list(block.name, 0)
                children = self.get_outputs(block.name)
                for mblock in self.blocks_list:
                    is_child, tuple_child = self.children_recognition(mblock.name, children)
                    # if mblock.name in children.values():
                    if is_child == True:
                        #print("Enviar datito", out_value, "a", mblock.name)
                        # mblock.input_queue.append(out_value)
                        mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                        mblock.data_recieved += 1
                        block.data_sent += 1

        # Se ejecutan todos los bloques de acuerdo al orden de jerarquía definido en la primera iteración
        for hier in range(self.max_hier + 1):
            for block in self.blocks_list:
                if block.hierarchy == hier and (block.data_recieved == block.in_ports or block.in_ports == 0) and block.computed_data != True:
                    #print(block.name, block.hierarchy, "Ejecutar función", block.fun_name, block.params,"inputs:", block.input_queue)
                    out_value = getattr(self.execution_fun, block.fun_name)(block.params, self.time_step, block.input_queue)
                    self.update_global_list(block.name,0)
                    block.computed_data = True
                    children = self.get_outputs(block.name)
                    if block.run_ord not in [1,3]: # elementos que no entregan resultado a children (1 es cond. inicial)
                        for mblock in self.blocks_list:
                            is_child, tuple_child = self.children_recognition(mblock.name, children)
                            # if mblock.name in children.values():
                            if is_child == True:
                                #print("Enviar datito", out_value, "a", mblock.name)
                                # mblock.input_queue.append(out_value)
                                mblock.input_queue[tuple_child['dstport']] = out_value[tuple_child['srcport']]
                                mblock.data_recieved += 1
                                block.data_sent += 1
                    elif block.run_ord == 3:
                        #print("Rama terminada")
                        if 'Scope' in block.name:
                            self.plotterms[block.name].append(out_value[0])
            hier += 1

        # Se comprueba si que el tiempo total de simulación (ejecución) ha sido superado para finalizar con el loop.
        if self.time_step >= self.execution_time:#seconds
            self.run_initialized = False                        # Se finaliza el loop de ejecución
            print(time.time() - self.execution_time_start)      # Se imprime el tiempo total tomado

            ##########
            # Se grafican los datos guardados en los bloques TermX
            if len(self.plotterms) > 0:
                plt.figure()
                for key in self.plotterms.keys():
                    plt.plot(self.timeline, self.plotterms[key])
                plt.show()
                self.plotterms = {}
            ##########

            for block in self.blocks_list:
                if block.run_ord == 1:
                    block.params['init_start'] = True
                    print(block.params)

            print("EJECUCION TERMINADA")

    def children_recognition(self, block_name, children_list):
        # Compara el block_name (de blocks_list) y lo busca en children_list, si está entrega un True y un diccionario con los puertos necesarios correspondientes.
        for child in children_list:
            if block_name in child.values():
                return True, child
        return False, -1

    def update_global_list(self, block_name, h_value, h_assign=False):
        # Actualiza la lista global que controla los loops en la ejecución
        # h_assign se utiliza para asignar el grado de jerarquía unicamente en la primera iteración
        for elem in self.global_computed_list:
            if elem['name'] == block_name:
                if h_assign == True:
                    elem['hierarchy'] = h_value
                elem['computed_data'] = True

    def check_global_list(self):
        # Comprueba que no queden bloques sin ejecutar en la simulación
        for elem in self.global_computed_list:
            if elem['computed_data'] == False:
                return False
        return True

    def reset_execution_data(self):
        # Devuelve al estado inicial varios parametros tanto de los bloques, con de la lista global que controla los loops de ejecución
        for i in range(len(self.blocks_list)):
            self.global_computed_list[i]['computed_data'] = False
            self.blocks_list[i].computed_data = False
            self.blocks_list[i].data_recieved = 0
            self.blocks_list[i].data_sent = 0
            self.blocks_list[i].input_queue = {}
            self.blocks_list[i].hierarchy = self.global_computed_list[i]['hierarchy']

    def get_max_hierarchy(self):
        # Busca el grado de jerarquía más alto (o bajo?) para determinar el número de forloop necesario para correr el codigo
        maxValue = 0
        for elem in self.global_computed_list:
            if elem['hierarchy'] >= maxValue:
                maxValue = elem['hierarchy']
        return maxValue

    def get_outputs(self, block_name):
        # A partir de las conexiones de las líneas entre puertos, busca cuales son los que necesitan a "block_name de input"
        # retorna una lista de diccionarios con los puertos de salida para block_name, como los bloques y puertos de llegada
        neighs = []
        for line in self.line_list:
            if line.srcblock == block_name:
                neighs.append({'srcport': line.srcport, 'dstblock': line.dstblock, 'dstport': line.dstport})
        return neighs

    def get_neighbors(self, block_name):
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

class Block(InitSim):
    # Clase para inicializar y mantener a los bloques
    def __init__(self, b_type, sid, coords, color, in_ports=1, out_ports=1, run_ord=2, io_edit=True, fun_name='block', params={}):
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
        self.params = params            # Parámetros asociados a la función
        self.ed_params_list = list(self.params.keys()) # Lista de parámetros editables

        self.port_radius = 8            # Radio del circulo para el dibujado de los puertos
        self.height_base = self.height  # Variable que conserva valor de altura por defecto
        self.in_ports = in_ports        # Variable que contiene el número de puertos de entrada
        self.out_ports = out_ports      # Variable que contiene el número de puertos de salida

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

    def draw_Block(self, zone):
        # Dibuja el bloque y los puertos
        pygame.draw.rect(zone, self.b_color, (self.left, self.top, self.width, self.height))
        for port_in_location in self.in_coords:
            pygame.draw.circle(zone, self.colors['black'], port_in_location, self.port_radius)

        for port_out_location in self.out_coords:
            pygame.draw.circle(zone, self.colors['black'], port_out_location, self.port_radius)

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
            self.update_Block()

        elif self.io_edit == 'input':
            # Solo se pueden editar inputs
            io_widget = Tk_widget(self.name, {'inputs': self.in_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.in_ports = int(new_io['inputs'])
                io_widget.destroy()
            self.update_Block()

        elif self.io_edit == 'output':
            # Solo se pueden editar outputs
            io_widget = Tk_widget(self.name, {'outputs': self.out_ports})
            new_io = io_widget.get_values()
            if new_io != {}:
                self.out_ports = int(new_io['outputs'])
                io_widget.destroy()
            self.update_Block()

    def change_params(self):
        # Se cambian los valores de los parametros para cada bloque a partir del diccionario con la lista completa de parametros y la lista que indica que se puede editar
        if self.params == {}:
            return

        ed_dict = {}
        non_ed_dict = {}

        if self.run_ord == 1:
            print(vars(self))

        for key in self.params.keys():
            if key in self.ed_params_list:
                ed_dict[key] = self.params[key]
            else:
                non_ed_dict[key] = self.params[key]

        widget_params = Tk_widget(self.name, ed_dict)
        new_inputs = widget_params.get_values()
        if new_inputs != {}:
            for n_key in new_inputs.keys():
                if new_inputs[n_key] == 'True':
                    new_inputs[n_key] = True
                elif new_inputs[n_key] == 'False':
                    new_inputs[n_key] = False
            new_inputs.update(non_ed_dict)
            self.params = new_inputs
            widget_params.destroy()


class Line(InitSim):
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
    # Produce un "boton" para generar bloques con las caracteristicas indicadas
    def __init__(self,b_type, fun_name, io_params, ex_params, b_color, coords):
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

        self.font_size = 24  # Tamaño del texto
        self.text = pygame.font.SysFont(None, self.font_size)
        self.text_display = self.text.render(self.fun_name, True, self.colors['black'])

    def draw_baseblock(self,zone, pos):
        # Dibuja el bloque
        self.collision = pygame.rect.Rect(40,40+50*pos,40,40)
        pygame.draw.rect(zone, self.b_color, self.collision)
        zone.blit(self.text_display, (90, 50 + 50*pos))

    def set_color(self, color):
        # Define el color del bloque a partir de un string o directamente de una tupla con los valores RGB
        if type(color) == str:
            return self.colors[color]
        elif type(color) == tuple:
            return color


class Tk_widget:
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
        new_widget.insert(0, str(self.params[self.params_names[x]]))
        return new_widget

    def get_values(self):
        # Entrega un diccionario con los datos obtenidos de la ventana
        try:
            dict = {}
            for i in range(len(self.entry_widgets)):
                dict[self.params_names[i]] = self.entry_widgets[i].get()
            return dict
        except:
            return {}

    def destroy(self):
        # Finaliza la ventana
        self.master.destroy()


class Functions_call:
    #Funciones utilizadas durante la ejecución del sistema
    def __init__(self):
        self.dummy = 0

    def step(self, params, time, inputs):
        # Funcion escalón base
        if params['type'] == 'up':
            change = True if time < float(params['delay']) else False
        elif params['type'] == 'down':
            change = True if time > float(params['delay']) else False
        else:
            return 'error'

        if change == True:
            return {0: 0.0}
        elif change == False:
            return {0: float(params['value'])}

    def ramp(self, params, time, inputs):
        # Funcion rampa
        if float(params['slope']) == 0:
            return {0: 0}
        elif float(params['slope']) > 0:
            return {0: np.maximum(0,float(params['slope'])*(time - float(params['delay'])))}
        elif float(params['slope']) < 0:
            return {0: np.minimum(0, float(params['slope']) * (time - float(params['delay'])))}

    def sine(self, params, time, inputs):
        # Funcion sinusoidal
        return {0: float(params['amplitude'])*np.sin(float(params['omega'])*time + float(params['init_angle']))}

    def gain(self, params, time, inputs):
        # Funcion ganancia
        return {0: float(params['gain'])*inputs[0]}

    def exponential(self, params, time, inputs):
        # Funcion exponencial
        return {0: float(params['a'])*np.exp(float(params['b'])*inputs[0])}

    def sumator(self, params, time, inputs):
        # Funcion sumador
        suma = 0.0
        for i in range(len(inputs)):
            if params['sign'][i] == '+':
                suma += inputs[i]
            elif params['sign'][i] == '-':
                suma -= inputs[i]
            else:
                print("WRONG SYMBOLS")
                return 'error'
        return {0: suma}

    def multiplicator(self, params, time, inputs):
        # Funcion multiplicador
        mult = 1.0
        for i in range(len(inputs)):
            if params['sign'][i] == '*':
                mult *= inputs[i]
            elif params['sign'][i] == '/' and inputs[i] != 0:
                mult /= inputs[i]
            elif params['sign'][i] == '/' and inputs[i] == 0:
                print("DIV BY ZERO")
                return 'error'
            else:
                print("WRONG SYMBOLS")
                return 'error'
        return {0: mult}

    def block(self, params, time, inputs):
        # Funcion bloque generico (en pruebas)
        return {0: inputs[0]}

    def terminator(self, params, time, inputs):
        # Funcion terminator
        return {0: 0.0} #dejarlo en 0 como originalmente se tenía previsto

    def noise(self, params, time, inputs):
        # Funcion noise (agrega ruido a la señal)
        return {0: float(params['sigma'])**2*np.random.randn() + float(params['mu'])}

    # bloques tipo memoria
    def integrator(self, params, time, inputs, output_only=False, dtime=0.01):
        # Funcion integrador
        if params['init_start'] == True:
            params['init_start'] = False
            params['dtime'] = dtime
            params['memory'] = float(params['init_conds'])
            print(params['memory'])
        if output_only == True:
            return {0: float(params['memory'])}
        else:
            params['memory'] += inputs[0] * float(params['dtime'])
            return {0: float(params['memory'])}

    def scope(self, params, time, inputs):
        # Funcion scope (sin terminar)
        return {0: inputs[0]}

    def test_MO(self, params, time, inputs):
        return {0: 1, 1: -1}

        ## for multiple outputs
        #return {'0': 0.0, '1': 0.0}
        # in the execution loop:
        # dict.keys() -> for key in dict.keys() if children.port == key -> send it