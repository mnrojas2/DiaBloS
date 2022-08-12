Using DiaBloS: Basics
=====================

Interfaz
--------

Al cargar el programa por primera vez se ve asi::

.. image:: images/screenshot.png


+-----+-------------------------+
| Nro | Que es                  |
+=====+=========================+
| (1) | Barra de funciones      |
+-----+-------------------------+
| (a) | New                     |
+-----+-------------------------+
| (b) | Load                    |
+-----+-------------------------+
| (c) | Save                    |
+-----+-------------------------+
| (d) | Play simulation         |
+-----+-------------------------+
| (e) | Pause simulation        |
+-----+-------------------------+
| (f) | Stop simulation         |
+-----+-------------------------+
| (g) | Plot graph              |
+-----+-------------------------+
| (2) | Function list           |
+-----+-------------------------+
| (3) | Canva                   |
+-----+-------------------------+


#. How to add blocks.
    Para agregar bloques basta con drag and drop it en el canvas.
    <image>

#. How to remove blocks.
    Para remover bloques basta con drag and drop it fuera del canvas.
    También se puede seleccionar el bloque y presionar DEL.
    <image>

#. How to add lines.
    Para agregar lineas, se debe hacer click a los 2 puertos (entrada y salida) para generar una conexión entre los dos.
    <image>

#. How to remove lines.
    Para remover líneas, se debe seleccionar la línea y presionar DEL.

#. How to change line color.
    Una característica particular de las líneas es que se les puede cambiar el color. Para ello se debe seleccionar la línea y luego presionar UP_ARROW o DOWN_ARROW contínuamente hasta encontrar el color a escoger.

#. How to change parameters.
    Si el bloque contiene parametros de funcion editables, se puede abrir una ventana para modificarlos como RMB.
    Tener cuidado de utilizar los parametros correctos
    En algunos casos son strings, en otros booleanos, en otros floats (ints se convierten a float al momento de leer y guardar los datos).

#. How to change port numbers.
    Si el bloque permite cambiar el numero de puertos, se puede abrir una ventana con CTRL + RMB...

#. How to load/save files.
    El formato de guardado de estos archivos es .dat...
    Para guardar un archivo, basta con presionar en el ícono SAVE, donde se abrirá una ventana dando las opciones de ubicación y nombre de archivo.
    Para cargar un archivo, bsta con presionar en el ícono LOAD, donde se abrirá una ventana dando las opciones de ubicar el archivo por carpeta y nombre.
    Usar basic_example.dat

#. How to run simulation.
    Para correr la simulacion
    Se puede pausar y detener presionando PAUSE y STOP.

#. How to change the sampling rate.
    Para cambiar el período de muestreo de la simulacion...
    Importante considerar que el tiempo de simulación puede ser mayor con un período de muestreo más pequeño.

#. How to plot data.
    Para graficar las curvas de una simulacion
    Para graficar las curvas de una simulacion mientras está corriendo...
    Cambiar el ancho de la ventana de simulacion (se basa en puntos graficados mas que en tiempo)
    Para observar de nuevo el gráfico, u observarlo en todo el espacio, presionar el boton

#. How to export data.
    Para exportar data, el proceso es similar al de graficar las curvas.
    Primero se debe agregar un bloque EXPORT_DATA, el cual debe ser conectado a la salida del bloque del cual se quiere la señal a guardar.
    Se pueden renombrar los 'labels' para poder identificar cada uno de los vectores. Si no se llamarán de forma predefinida como 'ExportData-<numero>', donde 'n' corresponde a la ubicación de la variable a lo largo del vector inicial.

#. How to load user-made functions.
    DiaBloS permite la carga de funciones externas, creadas por el usuario.
    Una explicacion en detalle se puede ver en la seccion xxxx
    Para cargar este tipo de funciones, se debe agregar un bloque Block, donde el único parámetro que tiene para modificar es el de agregar el nombre del archivo (y función) ubicado en la carpeta 'usermodels/'.

#. Some shortcuts
    ::

        Ctrl + E: Run
        Ctrl + S: Save
        Ctrl + A: Load
        Ctrl + N: New