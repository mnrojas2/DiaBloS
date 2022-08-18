"""
functions.py - Contains all the functions associated with the blocks in the simulation
"""

import numpy as np


class FunctionsCall:
    """
    Class to contain all the default functions available to work with in the simulation interface
    """

    def step(self, time, inputs, params):
        """
        Step source function

        :purpose: Function that returns a constant value over time.
        :description: This is a source type function, which is piecewise. It can be used to indicate the beginning or end of a branch of a network.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['value']: The value that the function returns. It can be a scalar (float) as well as a vector ([float, ...]).
        :param params['delay']: Indicates a point in time where the piecewise jump occurs.
        :param params['type']: ['up'/'down'] Indicates whether the jump is upward ('value') or downward (0).
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :type time: float
        :type inputs: dict
        :type params['value']: float/numpy.ndarray
        :type params['delay']: float
        :type params['type']: str
        :type params['_name_']: str
        :return: The value defined in 'value' or 0.
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        if params['type'] == 'up':
            change = True if time < params['delay'] else False
        elif params['type'] == 'down':
            change = True if time > params['delay'] else False
        else:
            print("ERROR: 'type' not correctly defined in", params['_name_'])
            return {'E': True}

        if change:
            return {0: 0*abs(np.array(params['value']))}
        else:
            return {0: np.array(params['value'])}

    def ramp(self, time, inputs, params):
        """
        Ramp source function

        :purpose: Function that returns a value that changes linearly over time.
        :description: This is a source type function, which is piecewise. The value changes linearly over time, and can increase or decrease.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['slope']: The value of the slope that the ramp has.
        :param params['delay']: Indicates a point in time where the start of the ramp happens.
        :type time: float
        :type inputs: dict
        :type params['slope']: float
        :type params['delay']: float
        :return: The value of the slope multiplied by the difference between 'time' and 'delay'.
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        if params['slope'] == 0:
            return {0: 0}
        elif params['slope'] > 0:
            return {0: np.maximum(0, params['slope']*(time - params['delay']))}
        elif params['slope'] < 0:
            return {0: np.array(np.minimum(0, params['slope'] * (time - params['delay'])))}

    def sine(self, time, inputs, params):
        """
        Sinusoidal source function

        :purpose: Function that returns a sinusoidal in time.
        :description: This is a source type function. It returns a sinusoidal with variation in the parameters of amplitude, frequency and initial angle.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['amplitude']: Amplitude value taken by the sinusoidal.
        :param params['omega']: Value in rad/s (2*pi*f) of the frequency taken by the sinusoidal.
        :param params['init_angle']: Value in radians of the angle taken by the sinusoidal at time zero.
        :type time: float
        :type inputs: dict
        :type params['amplitude']: float
        :type params['omega']: float
        :type params['init_angle']: float
        :return: A sinusoidal of amplitude 'amplitude', frequency 'omega' and initial angle 'init_angle'.
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        return {0: np.array(params['amplitude']*np.sin(params['omega']*time + params['init_angle']))}

    def noise(self, time, inputs, params):
        """
        Normal noise function

        :purpose: Function returns a normal random noise.
        :description: This is a source type function. It produces a normal random value of mean mu and variance sigma**2.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['mu']: Mean value of the noise.
        :param params['sigma']: Standard deviation value of the noise.
        :type time: float
        :type inputs: dict
        :type params['sigma']: float
        :type params['mu']: float
        :return: Normal random value of mean mu and variance sigma**2.
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        return {0: np.array(params['sigma'] ** 2 * np.random.randn() + params['mu'])}

    def gain(self, time, inputs, params):
        """
        Gain function

        :purpose: Funcion que escala una entrada por un factor.
        :description: Esta es una funcion tipo proceso. Retorna la misma entrada, pero escalada por un factor definido por el usuario. Esta entrada puede ser tanto escalar como vectorial, así como el factor de escalamiento.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['gain']: Valor de escalamiento de la entrada. Puede ser un valor escalar, o una matriz (solo para multiplicación vectorial).
        :type time: float
        :type inputs: dict
        :type params['gain']: float/numpy.ndarray
        :return: El valor de entrada, escalado por el factor 'gain'.
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        return {0: np.array(np.dot(params['gain'], inputs[0]))}

    def exponential(self, time, inputs, params):
        """
        Exponential function

        :purpose: Funcion que retorna el valor de una exponencial a partir de una entrada.
        :description: Esta es una funcion tipo proceso. Toma el valor de entrada, y le calcula la exponencial de la misma, con factores de escala para la base como al exponente.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['a']: Factor de escalamiento para la base de la exponencial.
        :param params['b']: Factor de escalamiento para el exponente de la exponencial.
        :type time: float
        :type inputs: dict
        :type params['a']: float
        :type params['b']: float
        :return: La exponencial del valor de la entrada.
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        return {0: np.array(params['a']*np.exp(params['b']*inputs[0]))}

    def sumator(self, time, inputs, params):
        """
        Sumator function

        :purpose: Funcion que retorna la suma de dos o más entradas.
        :description: Esta es una funcion tipo proceso. Toma cada valor de entrada y este lo asocia a un signo (positivo o negativo), para luego irlos sumando o restando en una variable auxiliar. La función soporta tanto operatoria escalar como vectorial.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['sign']: String que contiene todos los signos asociados a cada valor (o vector) de entrada. Cabe destacar que en caso de tener menos símbolos que vectores, la función asumirá que estos restantes sumarán.
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :type time: float
        :type inputs: dict
        :type params['sign']: str
        :type params['_name_']: str
        :return: La suma de todas las entradas.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: Esta función retorna 'Error' si es que las dimensiones de alguna de las entradas no son iguales.

        """
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

        :purpose: Funcion que retorna la multiplicación por elementos de dos o más entradas.
        :description: Esta es una funcion tipo proceso. Toma cada valor de entrada y los va multiplicando con un valor (o vector) base.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :type time: float
        :type inputs: dict
        :return: La multiplicación de todas las entradas.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: A diferencia de la función sumator, esta no comprueba que las entradas tengan las mismas dimensiones, puesto que se puede dar la ocasión donde el resultado necesitado puede ser algo de más dimensiones.
        :limitations: La función no comprueba que el resultado tenga las dimensiones deseadas, por lo que es un trabajo que debe realizar el usuario.

        """
        mult = 1.0
        for i in range(len(inputs)):
            mult *= inputs[i]
        return {0: mult}

    def block(self, time, inputs, params):
        """
        Generic block function for testing purposes
        """
        return {0: np.array(inputs[0])}

    def mux(self, time, inputs, params):
        """
        Multiplexer function

        :purpose: Funcion que la concatenación de varios valores o vectores.
        :description: Esta es una funcion tipo proceso. Concatena cada una de sus entradas de forma que se obtiene un vector igual a la suma producto del número de entradas por el número de dimensiones de cada una. El orden de los valores está dado por el orden de las entradas al bloque.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :type time: float
        :type inputs: dict
        :return: El vector con todos los valores ordenados en una sola dimensión ((a,1) con a>=1).
        :rtype: numpy.ndarray
        :examples: See example in ...

        """
        array = np.array(inputs[0])
        for i in range(1, len(inputs)):
            array = np.append(array, inputs[i])
        return {0: array}

    def demux(self, time, inputs, params):
        """
        Demultiplexer function

        :purpose: Funcion que retorna la suma de dos o más entradas.
        :description: Esta es una funcion tipo proceso. Toma cada valor de entrada y este lo asocia a un signo (positivo o negativo), para luego irlos sumando o restando en una variable auxiliar. La función soporta tanto operatoria escalar como vectorial.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['output_shape']: Valor que define el número de dimensiones con el cual cada salida tendrá.
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :param params['_outputs_']: Parámetro auxiliar entregado por el bloque asociado, para identificación de salidas disponibles.
        :type time: float
        :type inputs: dict
        :type params['output_shape']: float
        :type params['_name_']: str
        :type params['_outputs_']: float
        :return: Un número determinado de salidas, con cada una de ellas con dimensiones iguales.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: Esta función retorna 'Error' si es que el número de valores en el vector de entrada no es suficiente para obtener todas las salidas a las dimensiones requeridas. También retorna un 'Warning' en caso que el vector sea más grande que lo requerido, truncando los valores que no se alcanzan a tomar.
        :bugs: bugs

        """
        # Check input dimensions first
        if len(inputs[0]) / params['output_shape'] < params['_outputs_']:
            print("ERROR: Not enough inputs or wrong output shape in", params['_name_'])
            return {'E': True}

        elif len(inputs[0]) / params['output_shape'] > params['_outputs_']:
            print("WARNING: There are more elements in vector for the expected outputs. System will truncate. Block", params['_name_'])

        outputs = {}
        for i in range(params['_outputs_']):
            outputs[i] = inputs[0][int(params['output_shape'])*i: int(params['output_shape'])*(i+1)]
        return outputs

    def integrator(self, time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
        """
        Integrator function

        :purpose: Función que integra la señal de entrada.
        :description: Esta es una funcion tipo proceso. Toma la señal de entrada y la va sumando a una variable interna, ponderando por el tiempo de muestreo. Permite 4 formas de integración, siendo la más compleja el método Runge Kutta 45.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['init_conds']: Value that contains the initial conditions for the integrator
        :param params['method']: ['FWD_RECT/BWD_RECT/TUSTIN/RK45'] String that contains the method of integration to use.
        :param params['dtime']: Variable auxiliar que contiene el tiempo de muestreo que la simulación está utilizando (integración de paso fijo)
        :param params['mem']: Variable que contiene la suma de todos los datos, desde el inicio hasta el lapso 'time'.
        :param params['mem_list']: Vector que contiene los últimos valores de 'mem'
        :param params['mem_len']: Variable que define el número de elementos que contiene 'mem_list'
        :param params['nb_loop']: Variable auxiliar que indica el paso actual del método RK45
        :param params['RK45_Klist']: Vector auxiliar que contiene los últimos valores de K1,K2,K3,K4 (método RK45)
        :param params['add_in_memory']: Variable auxiliar que indica cuando el valor de entrada se suma a 'mem', como también retornar un resultado auxiliar (método RK45)
        :param params['aux']: Variable auxiliar que contiene la suma de 'mem' anterior, con medio paso de simulación (método RK45)
        :param params['_init_start_']: Parámetro auxiliar utilizado por el sistema para realizar funciones especiales en el primer loop de simulación.
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :type time: float
        :type inputs: dict
        :type params['init_conds']: numpy.ndarray
        :type params['method']: str
        :type params['dtime']: float
        :type params['mem']: numpy.ndarray
        :type params['mem_list']: numpy.ndarray
        :type params['mem_len']: float
        :type params['nb_loop']: int
        :type params['RK45_Klist']: numpy.ndarray
        :type params['add_in_memory']: bool
        :type params['aux']: numpy.ndarray
        :type params['_init_start_']: bool
        :type params['_name_']: Parámetro auxiliar entregado por el bloque asociado, para identificación de errores.
        :return: A value set in zero.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: El parámetro 'init_conds' debe ser ajustado por el usuario si la entrada tiene más de una dimensión. Se puede definir un valor vectorial como [a,b,...], con a y b valores escalares.

        """
        # Initialization (this step happens only in the first iteration)
        if params['_init_start_']:
            params['dtime'] = dtime
            params['mem'] = np.array(params['init_conds'])
            params['mem_list'] = [np.zeros(params['mem'].shape)]
            params['mem_len'] = 5.0
            params['_init_start_'] = False

            if params['method'] == 'RK45':
                params['nb_loop'] = 0
                params['RK45_Klist'] = [0, 0, 0, 0]  # K1, K2, K3, K4

            params['add_in_memory'] = True  # It defines if the saved value is sent to the next block or not

        if output_only:
            old_add_in_memory = params['add_in_memory']
            params['add_in_memory'] = next_add_in_memory  # Update for next loop
            if old_add_in_memory:
                return {0: params['mem']}
            else:
                return {0: params['aux']}
        else:
            # Checks if the new input vector dimensions match.
            if params['mem'].shape != inputs[0].shape:
                print("ERROR: Dimension Error in initial conditions in", params['_name_'])
                params['_init_start_'] = True
                return {'E': True}

            # The old value is saved
            mem_old = params['mem']

            # Integration process according to chosen method
            # Forward euler
            if params['method'] == 'FWD_RECT':
                if params['add_in_memory']:
                    params['mem'] += params['dtime'] * inputs[0]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * inputs[0])
                    return {0: params['aux']}

            # Backwards euler
            elif params['method'] == 'BWD_RECT':
                if params['add_in_memory']:
                    params['mem'] += params['dtime'] * params['mem_list'][-1]
                else:
                    params['aux'] = np.array(params['mem'] + 0.5 * params['dtime'] * params['mem_list'][-1])
                    return {0: params['aux']}

            # Tustin
            elif params['method'] == 'TUSTIN':
                if params['add_in_memory']:
                    params['mem'] += 0.5*params['dtime'] * (inputs[0] + params['mem_list'][-1])
                else:
                    params['aux'] = np.array(params['mem'] + 0.25 * params['dtime'] * (inputs[0] + params['mem_list'][-1]))
                    return {0: params['aux']}

            # Runge-Kutta 45
            elif params['method'] == 'RK45':
                K_list = params['RK45_Klist']
                K_list[params['nb_loop']] = params['dtime'] * inputs[0]     # K1, K2, K3 or K4
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
            if len(aux_list) > params['mem_len']:
                aux_list = aux_list[-5:]
            params['mem_list'] = aux_list

            return {0: mem_old}

    def derivative(self, time, inputs, params):
        """
        Derivative function

        :purpose: Función que obtiene la derivada de una señal.
        :description: Esta es una funcion tipo proceso. Toma el valor de entrada y el valor del tiempo actual, para luego tomar la diferencia de estos con sus valores anteriores y obtener la pendiente.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['t_old']: Valor anterior de la variable time.
        :param params['i_old']: Valor anterior de la entrada.
        :param params['_init_start_']: Parámetro auxiliar utilizado por el sistema para realizar funciones especiales en el primer loop de simulación.
        :type time: float
        :type inputs: dict
        :type params['t_old']: float
        :type params['i_old']: float
        :type params['_init_start_']: bool
        :return: La pendiente entre el valor anterior y el actual.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        if params['_init_start_']:
            params['t_old'] = time
            params['i_old'] = inputs[0]
            params['_init_start_'] = False
            return {0: 0.0}
        dt = time - params['t_old']
        di = inputs[0] - params['i_old']
        params['t_old'] = time
        params['i_old'] = inputs[0]
        return {0: np.array(di/dt)}

    def terminator(self, time, inputs, params):
        """
        Signal terminator function

        :purpose: Función que termina con la señal.
        :description: Esta es una funcion tipo fuga. Toma cualquier valor de entrada y no hace nada con este. Esta función es útil para darle término a señales que no se graficarán.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :type time: float
        :type inputs: dict
        :return: A value set in zero.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: notes
        :limitations: limitations
        :bugs: bugs

        """
        return {0: np.array([0.0])}

    def export(self, time, inputs, params):
        """
        Block to save and export block signals

        :purpose: Función que acumula valores en el tiempo para su posterior exportación a .npz.
        :description: Esta es una funcion tipo fuga. Toma el valor de entrada y lo concatena a un vector. Si la entrada tiene más de una dimensión, la función concatena de forma que el vector de guardado tenga las dimensiones correspondientes en función del tiempo.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['str_name']: String entregado por el usuario con los nombres de los valores de entrada separados por coma: ("value1,value2,value3,...")
        :param params['vec_dim']: Valor definido por la función que obtiene el número de dimensiones de la entrada.
        :param params['vec_labels']: Vector producido por la función que obtiene el nombre para cada elemento del vector de guardado.
        :param params['vector']: Vector que acumula los valores de entrada del bloque.
        :param params['_init_start_']: Parámetro auxiliar utilizado por el sistema para realizar funciones especiales en el primer loop de simulación.
        :param params['_skip_']: Parámetro auxiliar utilizado por el sistema para indicar cuando no se debe guardar el valor de entrada (pasos medios de RK45).
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :type time: float
        :type inputs: dict
        :type params['str_name']: str
        :type params['vec_dim']: float
        :type params['vec_labels']: numpy.ndarray
        :type params['vector']: numpy.ndarray
        :type params['_init_start_']: bool
        :type params['_skip_']: bool
        :type params['_name_']: str
        :return: A value set in zero.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: Si es que no se detectan suficientes labels para 'vec_labels', la función agrega los restantes utilizando '_name_' y un número dependiendo del de nombres faltantes.
        :limitations: limitations
        :bugs: bugs

        """
        # To prevent saving data in the wrong iterations (integration method RK45 in use)
        if '_skip_' in params.keys() and params['_skip_']:
            params['_skip_'] = False
            return {0: np.array([0.0])}
        # Initialization of the saving vector
        if params['_init_start_']:
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
        return {0: np.array([0.0])}

    def scope(self, time, inputs, params):
        """
        Function to plot block signals

        :purpose: Función que acumula valores en el tiempo para graficarlos con pyqtgraph tanto posteriormente como durante la simulación.
        :description: Esta es una funcion tipo fuga. Toma el valor de entrada y lo concatena a un vector. Si la entrada tiene más de una dimensión, la función concatena de forma que el vector de guardado tenga las dimensiones correspondientes en función del tiempo.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['labels']: String entregado por el usuario con los nombres de los valores de entrada separados por coma: ("value1,value2,value3,...")
        :param params['vec_dim']: Valor definido por la función que obtiene el número de dimensiones de la entrada.
        :param params['vec_labels']: Vector producido por la función que obtiene el nombre para cada elemento del vector de guardado.
        :param params['vector']: Vector que acumula los valores de entrada del bloque.
        :param params['_init_start_']: Parámetro auxiliar utilizado por el sistema para realizar funciones especiales en el primer loop de simulación.
        :param params['_skip_']: Parámetro auxiliar utilizado por el sistema para indicar cuando no se debe guardar el valor de entrada (pasos medios de RK45).
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :type time: float
        :type inputs: dict
        :type params['labels']: str
        :type params['vec_dim']: float
        :type params['vec_labels']: numpy.ndarray
        :type params['vector']: numpy.ndarray
        :type params['_init_start_']: bool
        :type params['_skip_']: bool
        :type params['_name_']: str
        :return: A value set in zero.
        :rtype: numpy.ndarray
        :examples: See example in ...
        :notes: Si es que no se detectan suficientes labels para 'vec_labels', la función agrega los restantes utilizando '_name_' y un número dependiendo del de nombres faltantes.
        :limitations: limitations
        :bugs: bugs

        """
        # To prevent saving data in the wrong iterations (integration method RK45 in use)
        if '_skip_' in params.keys() and params['_skip_']:
            params['_skip_'] = False
            return {0: np.array([0.0])}
        # Initialization of the saving vector
        if params['_init_start_']:
            aux_vector = np.array([inputs[0]])
            try:
                params['vec_dim'] = len(inputs[0])
            except:
                params['vec_dim'] = 1

            labels = params['labels']
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
        return {0: np.array([0.0])}
