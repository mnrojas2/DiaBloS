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

-Cambiar en InitSim

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


Vector management
-----------------

Explicación de cómo se construyen los vectores.

vector: [a, b, c, d]
matrix: [[a, b], [c, d]]
3d-matrix: [[[a, b], [c, d]], [[e, f], [g, h]]]

TkWidget.string_to_vector(): proceso de conversion de vectores en string.

* En ambos procesos se eliminan los espacios, solo importan los valores numéricos, como los corchetes y espacios ('[', ']', ' ')
1) Se eliminan los valores numéricos y se observa el número de corchetes para determinar las dimensiones del potencial vector/matriz.
2) Se eliminan los corchetes, creando un único vector que se redimensiona con los valores resultantes del proceso anterior.
* Si el número de elementos en el vector no corresponde a las dimensiones del vector/matriz, se indica un error y se entrega un "''".


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

It is recommended to implement this function as an external-function type first, then add it to the Functions class.


#. First define inputs, outputs, running order and block color in the external function file "_init_" and implement the most simplified version of the function to add.

#. After that, create a simple graph diagram to test the new block. i.e: A Step block, connected to the external block (where the new function is implemented), connected to a Scope block.

#. If the system doesn't fail execution, add new elements to the external function being aware of not breaking the graph execution stability.

#. When everything is ok, add the new finished function to the Functions class and create a new MenuBlock in InitSim.menu_blocks_init(), using the parameters already defined in the external function "_init_" and defining block size and if the function allows change of inputs and/or outputs.

#. Test again the function in the simulation, this time replacing the External Block with the corresponding to the new implemented function.


Preventing crashes
------------------

Agregar casos de excepcion retornando una 'E'. De ese modo, la simulacion podrá detener la ejecucion sin terminar el
programa repentinamente::

    except:
        return {'E': True}
