import numpy as np

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
