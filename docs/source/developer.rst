Developing for DiaBloS
======================

Explain main functions and classes
----------------------------------

Explicar con diagramas la relacion entre funciones principales

How does the software work (UI level)
-------------------------------------

Explicar el loop de simulacion con las funciones para crear/destruir bloques

How to change some settings (resolution, fps, canvas color)
-----------------------------------------------------------

Cambiar en InitSim/archivo de guardado

How does it work the run simulation function
--------------------------------------------

Explicar el loop de ejecucion del grafo, inicial y loop, con tambien los casos para detenerlo de golpe (diagrama)

How does RK45 integration works
-------------------------------

Explicar las cosas que hacen que funcione el RK45

Explain how the data is sent from one block to another (filetype)
-----------------------------------------------------------------

Mencionar el como funciona lo de los diccionarios::

    return {0: np.array(dato), 1: np.array([dato1,dato2])}


How to add new functions
------------------------

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

How to test a new function
--------------------------

Usar bloque "block" para probar la funcion externa

How to prevent crashes
----------------------

Agregar casos de excepcion retornando una 'E'. De ese modo, la simulacion podrá detener la ejecucion sin terminar el programa repentinamente::

    except:
        return {'E': True}