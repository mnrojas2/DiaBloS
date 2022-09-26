Using DiaBloS: Developer's Guide
================================

Class and function hierarchy
----------------------------

Explicar con diagramas la relacion entre funciones principales

aqui va un diagrama de jerarquia::

    main_execution()
        --main classes--
        initsim
            --UI--
            add_block
            remove_block
            add_line
            remove_lines

            --settings--
            save
            open
            other settings
            canvas resolution
            canvas fps

            --execution--
            execution_init
            execution_loop
            other auxiliar functions

        blocks
            --internal--
            inputs
            outputs
            parameters
            function (internal/external)
            --ui--
            color

        lines
            --internal--
            start
            end
            --ui--
            color
            trajectory

        functions
            --execution--
            input/output functions

        --auxiliar classes--
        tkWidget
        menublocks
        signal_plot

How does the software work (UI level)
-------------------------------------

Explicar el loop de simulacion con las funciones para crear/destruir bloques::

    init canvas
    initsim
    loop
        event -> check inputs
            k&m input -> init_sim.functions
        update canvas

How to change some settings (resolution, fps, canvas color)
-----------------------------------------------------------

-Cambiar en InitSim/archivo de guardado

-initsim.__init__()

How does it work the run simulation function
--------------------------------------------

Explicar el loop de ejecucion del grafo, inicial y loop, con tambien los casos para detenerlo de golpe (diagrama)

poner la explicacion vista con el profe::

    Based on paper

    2 steps, init and loop

    init:
        -sort blocks according to computability.
        -start with source blocks.
        -spread initial conditions for blocks that use it (integrator).
        -check what blocks can be computed, compute them and spread its outputs to other uncomputed blocks.
        Then assign the order position to that block for the next step.

    loop:
        -spread output from blocks with initial conditions.
        -execute every block in the other already defined in the previous part, then spread outputs to other uncomputed blocks.

    stop:
        -wait until the time variable reaches the limit.
        -press STOP button in the interface.

How does RK45 integration works
-------------------------------

Explicar las cosas que hacen que funcione el RK45

poner la explicacion vista con el profe (todavia no vista)::

    definir dT

    T -> T0, T0, T0.5, T0.5, T1, T1, T1.5, T1.5, T2, ...

    -Definir periodo Delta T como el intervalo entre loops. O sea, después de inicializar, se debe esperar un tiempo DT, ejecutar el loop, otro DT, el loop, otro DT y así.
    -Definir caso integrador normal (caso con condiciones iniciales) generalizado
    -Definir caso para un sistema con un único integrador con realimentación, donde el integrador forma parte del circuito cerrado
    -Definir que el sistema visto desde el integrador se puede entender como que la salida del integrador es un 'x', y la entrada
    -Definir reglas del runge kutta k1, k2, k3, k4

    k1 = DT * f(t,x)
    k2 = DT * f(t + DT/2, x + k1/2)
    k3 = DT * f(t + DT/2, x + k2/2)
    k4 = DT * f(t + DT, x + k3)
    k = 1/6 * (k1 + 2*k2 + 2*k3 + k4)

    y = y(-1) + k
    t = t(-1) + h

    -init
    count_ki = 0
    T0.0 -> init conds (calcula k1)
    move DT/2
    -in loop
    count_ki = 1
    T0.5 -> k1 (calcula k2)
    count_ki = 2
    T0.5 -> k2 (calcula k3)
    move DT/2
    count_ki = 3
    T1.0 -> k3 (calcula k4 y k)
    count_ki = 0
    T1.0 -> k4 = k (calcula k1)
    move DT/2
    count_ki = 1
    T1.5 -> k1 (calcula k2)
    count_ki = 2
    T1.5 -> k2 (calcula k3)
    move DT/2
    count_ki = 3
    T2.0 -> k3 (calcula k4 y k)
    count_ki = 0
    T2.0 -> k4 = k (calcula k1)

Explain how the data is sent from one block to another (filetype)
-----------------------------------------------------------------

Mencionar el como funciona lo de los diccionarios::

    return {0: np.array(dato), 1: np.array([dato1,dato2])}


.. _usermodel-function:

Creating new functions
----------------------

Como desarrollar nuevas funciones de usuario (ver templates)::

    # filename: my_function.py
    """import libraries"""

    def my_function(time, inputs, params):
        """function code, either source, process or drain"""
        return {0: variable_output, 1: variable_output, ..., 'E': True/False}

Funcion inicialización::

    def _init_():
        io_data = { # parameters for the block containing the function
            'inputs': input_number,
            'outputs': output_number,
            'run_ord': block_order_number,
            'color': color_string_or_rgb_triplet
        }
        params = {} # parameters defined before use them in the function
        return io_data, params

Testing a new function
----------------------

-Se recomienda utilizar el bloque "Block" y el template para definir funciones y sus parámetros iniciales con "__init__()"

-Definir entradas, salidas, parametros

-Crear un sistema simple donde la salida de esta nueva funcion fuese a un scope o exportdata

-Agregar la entrada que se deba recibir por medio de los bloques (puertos)

-Analizar los resultados y comprobar externamente si funciona como se espera

-Usar bloque "block" para probar la funcion externa

Preventing crashes
------------------

Agregar casos de excepcion retornando una 'E'. De ese modo, la simulacion podrá detener la ejecucion sin terminar el
programa repentinamente::

    except:
        return {'E': True}
