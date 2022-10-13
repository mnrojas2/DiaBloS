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
        :examples: See example in :ref:`examples:vectorial integration`, :ref:`examples:gaussian noise` and :ref:`examples:signal products`.

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
        :examples: See example in :ref:`examples:external derivator`.

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
        :examples: See example in :ref:`examples:sine integration`.

        """
        return {0: np.array(params['amplitude']*np.sin(params['omega']*time + params['init_angle']))}


    def noise(self, time, inputs, params):
        """
        Gaussian noise function

        :purpose: Function returns a normal random noise.
        :description: This is a source type function. It produces a gaussian random value of mean mu and variance sigma**2.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['mu']: Mean value of the noise.
        :param params['sigma']: Standard deviation value of the noise.
        :type time: float
        :type inputs: dict
        :type params['sigma']: float
        :type params['mu']: float
        :return: Gaussian random value of mean mu and variance sigma**2.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:gaussian noise`

        """
        return {0: np.array(params['sigma'] ** 2 * np.random.randn() + params['mu'])}


    def gain(self, time, inputs, params):
        """
        Gain function

        :purpose: Function that scales an input by a factor.
        :description: This is a process type function. It returns the same input, but scaled by a user-defined factor. This input can be either scalar or vector, as well as the scaling factor.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['gain']: Scaling value of the input. Can be a scalar value, or a matrix (only for vector multiplication).
        :type time: float
        :type inputs: dict
        :type params['gain']: float/numpy.ndarray
        :return: The input value, scaled by the 'gain' factor.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:gaussian noise` and :ref:`examples:feedback system implementations`.

        """
        return {0: np.array(np.dot(params['gain'], inputs[0]))}


    def exponential(self, time, inputs, params):
        """
        Exponential function

        :purpose: Function that returns the value of an exponential from an input.
        :description: This is a process type function. It takes the input value, and calculates the exponential of it, with scaling factors for the base as well as the exponent.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['a']: Scaling factor for the base of the exponential.
        :param params['b']: Scaling factor for the exponent of the exponential.
        :type time: float
        :type inputs: dict
        :type params['a']: float
        :type params['b']: float
        :return: The exponential of the input value.
        :rtype: numpy.ndarray

        """
        return {0: np.array(params['a']*np.exp(params['b']*inputs[0]))}


    def sumator(self, time, inputs, params):
        """
        Sumator function

        :purpose: Function that returns the sum of two or more inputs.
        :description: This is a process type function. It takes each input value and associates it with a sign (positive or negative), and then adds or subtracts them in an auxiliary variable. The function supports both scalar and vector operations.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['sign']: String that contains all the signs associated to each input value (or vector). It should be noted that in case of having less symbols than vectors, the function will assume that the remaining symbols will add up.
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :type time: float
        :type inputs: dict
        :type params['sign']: str
        :type params['_name_']: str
        :return: The sum of all inputs.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:gaussian noise`, :ref:`examples:export data` and :ref:`examples:feedback system implementations`.
        :notes: This function returns 'Error' if the dimensions of any of the entries are not equal.

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

        :purpose: Function that returns the multiplication by elements of two or more inputs.
        :description: This is a process type function. It takes each input value and multiplies it with a base value (or vector).
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :type time: float
        :type inputs: dict
        :return: The multiplication of all inputs.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:signal products`.
        :notes: Unlike the sumator function, this one does not check if the inputs have the same dimensions, since there may be occasions where the result needed may be something larger.
        :limitations: The function does not check that the result has the desired dimensions, so it is a job to be done by the user.

        """
        mult = 1.0
        for i in range(len(inputs)):
            mult *= inputs[i]
        return {0: mult}


    def mux(self, time, inputs, params):
        """
        Multiplexer function

        :purpose: Function that concatenates several values or vectors.
        :description: This is a process type function. It concatenates each of its entries in such a way as to obtain a vector equal to the sum product of the number of entries by the number of dimensions of each one. The order of the values is given by the order of the block entries.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :type time: float
        :type inputs: dict
        :return: The vector with all values sorted in a single dimension ((a,1) with a>=1).:rtype: numpy.ndarray
        :examples: See example in :ref:`examples:signal products`, :ref:`examples:export data` and :ref:`examples:feedback system implementations`.

        """
        array = np.array(inputs[0])
        for i in range(1, len(inputs)):
            array = np.append(array, inputs[i])
        return {0: array}


    def demux(self, time, inputs, params):
        """
        Demultiplexer function

        :purpose: Function that splits an input vector into two or more.
        :description: This is a process type function. It takes the input vector and splits it into several smaller equal vectors, depending on the number of outputs.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['output_shape']: Value defining the number of dimensions with which each output will have.
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.
        :param params['_outputs_']: Auxiliary parameter delivered by the associated block, for identification of available outputs.
        :type time: float
        :type inputs: dict
        :type params['output_shape']: float
        :type params['_name_']: str
        :type params['_outputs_']: float
        :return: A given number of outputs, with each output having equal dimensions.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:gaussian noise`.
        :notes: This function returns 'Error' if the number of values in the input vector is not enough to get all the outputs at the required dimensions. It also returns a 'Warning' if the vector is larger than required, truncating the values that are not taken.

        """
        # Check input dimensions first
        if len(inputs[0]) / params['output_shape'] < params['_outputs_']:
            print("ERROR: Not enough inputs or wrong output shape in", params['_name_'])
            return {'E': True}

        elif len(inputs[0]) / params['output_shape'] > params['_outputs_']:
            print("WARNING: There are more elements in vector for the expected outputs. System will truncate. Block", params['_name_'])

        outputs = {}
        for i in range(params['_outputs_']):
            if int(params['output_shape']) == 1:
                outputs[i] = inputs[0][i]
            else:
                outputs[i] = inputs[0][int(params['output_shape'])*i: int(params['output_shape'])*(i+1)]
        return outputs


    def integrator(self, time, inputs, params, output_only=False, next_add_in_memory=True, dtime=0.01):
        """
        Integrator function

        :purpose: Function that integrates the input signal.
        :description: This is a process type function. It takes the input signal and adds it to an internal variable, weighted by the sampling time. It allows 4 forms of integration, the most complex being the Runge Kutta 45 method.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['init_conds']: Value that contains the initial conditions for the integrator.
        :param params['method']: ['FWD_RECT/BWD_RECT/TUSTIN/RK45'] String that contains the method of integration to use.
        :param params['dtime']: Auxiliary variable that contains the sampling time that the simulation is using (fixed step integration).
        :param params['mem']: Variable containing the sum of all data, from start to lapse 'time'.
        :param params['mem_list']: Vector containing the last values of 'mem'.
        :param params['mem_len']: Variable defining the number of elements contained in 'mem_list'.
        :param params['nb_loop']: Auxiliary variable indicating the current step of the RK45 method.
        :param params['RK45_Klist']: Auxiliary vector containing the last values of K1,K2,K3,K4 (RK45 method).
        :param params['add_in_memory']: Auxiliary variable indicating when the input value is added to 'mem', as well as returning an auxiliary result (method RK45).
        :param params['aux']: Auxiliary variable containing the sum of 'mem' above, with half a simulation step (method RK45)
        :param params['_init_start_']: Auxiliary parameter used by the system to perform special functions in the first simulation loop.
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
        :type params['_name_']: str
        :return: The accumulated value of all inputs since step zero weighted by the sampling time.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:sine integration` and :ref:`examples:feedback system implementations`.
        :notes: The 'init_conds' parameter must be set by the user if the input has more than one dimension. You can define a vector value as [a,b,...], with a and b scalar values.

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

        :purpose: Function that obtains the derivative of a signal.
        :description: This is a process type function. It takes the input value and the value of the current time, then takes the difference of these with their previous and obtains the slope.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['t_old']: Previous value of the variable time.
        :param params['i_old']: Previous value of the entry.
        :param params['_init_start_']: Auxiliary parameter used by the system to perform special functions in the first simulation loop.:type time: float
        :type inputs: dict
        :type params['t_old']: float
        :type params['i_old']: float
        :type params['_init_start_']: bool
        :return: The slope between the previous value and the current value.
        :rtype: numpy.ndarray
        :notes: ...

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

        :purpose: Function that terminates with the signal.
        :description: This is a drain type function. It takes any input value and does nothing with it. This function is useful for terminating signals that will not be plotted.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :type time: float
        :type inputs: dict
        :return: A value set in zero.
        :rtype: numpy.ndarray
        :examples: See example in :ref:`examples:signal products`.

        """
        return {0: np.array([0.0])}


    def export(self, time, inputs, params):
        """
        Block to save and export block signals

        :purpose: Function that accumulates values over time for later export to .npz.
        :description: This is a drain type function. It takes the input value and concatenates it to a vector. If the input has more than one dimension, the function concatenates so that the saving vector has the corresponding dimensions as a function of time.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['str_name']: String supplied by the user with the names of the input values separated by comma: ("value1,value2,value3,...")
        :param params['vec_dim']: Value defined by the function that gets the number of dimensions of the input.
        :param params['vec_labels']: Vector produced by the function that gets the name for each element of the saving vector.
        :param params['vector']: Vector that accumulates the input values of the block.
        :param params['_init_start_']: Auxiliary parameter used by the system to perform special functions in the first simulation loop.
        :param params['_skip_']: Auxiliary parameter used by the system to indicate when not to save the input value (RK45 half steps).
        :param params['_name_']: Auxiliary parameter delivered by the associated block, for error identification.:type time: float
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
        :examples: See example in :ref:`examples:export data` and :ref:`examples:feedback system implementations`.
        :notes: If not enough labels are detected for 'vec_labels', the function adds the remaining labels using '_name_' and a number depending on the number of missing names.

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

        :purpose: Function that accumulates values over time to plot them with pyqtgraph both later and during the simulation.
        :description: This is a drain type function. It takes the input value and concatenates it to a vector. If the input has more than one dimension, the function concatenates in such a way that the saving vector has the corresponding dimensions as a function of time.
        :param time: Value indicating the current period in the simulation.
        :param inputs: Dictionary that provides one or more entries for the function (if applicable).
        :param params['labels']: String supplied by the user with the names of the input values separated by comma: ("value1,value2,value3,...")
        :param params['vec_dim']: Value defined by the function that gets the number of dimensions of the input.
        :param params['vec_labels']: Vector produced by the function that gets the name for each element of the saving vector.
        :param params['vector']: Vector that accumulates the input values of the block.
        :param params['_init_start_']: Auxiliary parameter used by the system to perform special functions in the first simulation loop.
        :param params['_skip_']: Auxiliary parameter used by the system to indicate when not to save the input value (RK45 half steps).
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
        :examples: See example in :ref:`examples:sine integration`, :ref:`examples:signal products`, :ref:`examples:gaussian noise`.
        :notes: If not enough labels are detected for 'vec_labels', the function adds the remaining ones using '_name_' and a number depending on the number of missing names.

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
