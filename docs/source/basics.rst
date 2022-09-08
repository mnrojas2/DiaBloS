Using DiaBloS: Begginer's Guide
===============================

Interface
---------

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
| (3) | Canvas                  |
+-----+-------------------------+


#. How to clean the canvas.
    Para eliminar todos los bloques y líneas del canvas, presionar el botón NEW o la combinación de teclas Ctrl + N.

#. How to add blocks.
    Para agregar bloques basta con drag and drop them in the canvas.

    <image>

#. How to remove blocks.
    Para remover bloques basta con drag and drop it fuera del canvas.
    También se puede seleccionar el bloque con LMB y presionar DEL.

    <image>

#. How to add lines.
    Para agregar lineas, se debe hacer click a los 2 puertos (entrada y salida) para generar una conexión entre los
    dos bloques.

    Cabe destacar que presionar 2 puertos del mismo tipo no creará una línea entre ellas.

    Cabe destacar también que si un puerto de entrada ya tiene una línea conectada, no conectará más líneas a ese puerto.
    Para el caso del puerto de salida, esta restricción no aplica.

    <image>

#. How to remove lines.
    Para remover líneas, se debe seleccionar la línea y presionar DEL.

    Cuando se remueven bloques, también se remueven las líneas asociadas a este, de forma de liberar las conexiones
    que ya no tienen sentido lógico (puerto de entrada o salida no existe).

    <image>

#. How to change line color.
    Una característica particular de las líneas es que se les puede cambiar el color. Para ello se debe seleccionar
    la línea y luego presionar UP_ARROW o DOWN_ARROW contínuamente hasta encontrar el color a escoger.

#. How to change parameters.
    Si el bloque contiene parametros de funcion editables, se puede abrir una ventana para modificarlos presionando RMB
    sobre el bloque.

    Es importante tener cuidado de ingresar los parámetros en los formatos correctos. Estos pueden ser strings,
    booleanos (como texto), o floats (ints se convierten a floats).

#. How to change port numbers.
    Si el bloque permite cambiar el numero de puertos, se puede abrir una ventana con CTRL + RMB, con una o más entradas
    para cambiar el número de inputs y outputs, escritos como ints.

#. How to load/save files.
    El formato de guardado de estos archivos es .dat.

    Para guardar un archivo, basta con presionar en el ícono SAVE o la combinación de teclas Ctrl + S, donde se abrirá
    una ventana dando las opciones de ubicación y nombre de archivo.

    <image>

    Para cargar un archivo, bsta con presionar en el ícono LOAD o la combinación de teclas Ctrl + A, donde se abrirá
    una ventana dando las opciones de ubicar el archivo por carpeta y nombre.

    <image>

#. How to run simulation.
    Para ejecutar la simulacion, primero presionar el botón PLAY o la combinación de teclas Ctrl + E. Aparecerá una
    ventana, para ajustar el tiempo de simulación, el tiempo de muestreo, como también configuraciones para el graficado
    de las señales: el tamaño de la ventana en modo dinámico y activar o desactivar el modo dinámico. Luego se presiona
    aceptar y la simulación iniciará y continuará corriendo hasta que se alcance el tiempo de muestro o se detenga con
    el botón STOP.

    Se puede pausar presionando el botón PAUSE. Para reiniciar, basta con presionar el mismo botón PAUSE una segunda vez.

    <image>

#. How to plot data.
    Para graficar las curvas de una simulacion es necesario agregar bloques Scope y conectarlos a las señales de salida
    que se quieren observar.

    El bloque Scope contiene un solo parámetro llamado 'labels' el cual es utilizado para darle nombre a la (o las)
    señal(es) que se quieren graficar. Si este parámetro no se cambia, las señales observadas se llamarán de forma
    predefinida como 'Scope-<numero>', donde 'n' corresponde a la ubicación de la variable a lo largo del vector inicial.

    Además se puede activar o desactivar el graficado dinámico, es decir, graficar los datos mientras la simulación está
    corriendo. Para ello, al iniciar una simulación (presionando PLAY o haciendo la combinación de teclas Ctrl+E),
    se puede cambiar tanto el uso o no de esta herramienta durante la ejecución de la simulación como también el tamaño
    de la ventana móvil que mostrará los valores graficados en el tiempo (basado en puntos graficados mas que en tiempo).

    En caso de haber finalizado la simulación, se puede observar el gráfico presionando el botón PLOT. En caso que se
    haya realizado un graficado dinámico, primero cerrar la primera ventana con el gráfico resultante, para luego
    reabrirlo presionando con el botón PLOT.

    <image>

#. How to export data.
    Para exportar data, el proceso es similar al de graficar las curvas.

    Primero se debe agregar un bloque EXPORT, el cual debe ser conectado a la salida del bloque del cual se quiere
    la señal a guardar.

    Se pueden renombrar los 'labels' para poder identificar cada uno de los vectores. Si no se llamarán de forma
    predefinida como 'ExportData-<numero>', donde 'n' corresponde a la ubicación de la variable a lo largo del vector
    inicial.

    <image>

#. How to load user-made functions.
    DiaBloS permite la carga de funciones externas, creadas por el usuario. Una explicacion en detalle se puede ver en
    la seccion xxxx CITE

    Para cargar este tipo de funciones, se debe agregar un bloque Block, donde el único parámetro que tiene para
    modificar es el de agregar el nombre del archivo (y función) ubicado en la carpeta 'usermodels/'.

    Si la carga es correcta, el bloque actualizará su nombre en la parte inferior, los puertos y el color en el canvas.
    Si hay algo que salió mal, el programa indicará que el nombre de la función no existe o se encontró algo erróneo
    durante el proceso.

#. Some shortcuts
    ::

        Ctrl + E: Run (Simulate)
        Ctrl + S: Save
        Ctrl + A: Load
        Ctrl + N: New


First Experience
----------------

#. Load the interface.

#. Press OPEN icon or press Ctrl + A.

#. Go to examples/ and open basic_example.dat.

#. You will see something like the following picture::

    .. image:: images/screenshot.png

#. Select the blue block (Step)

#. Press RMB over the block

#. Change the ... to ...

#. Add a delay of 5 seconds

#. Select the red block (Scope)

#. Press RMB over the block

#. Change the ... to ...

#. Press PLAY to open the simulation popup

#. Change Simulation time to 10 seconds

#. Set Dynamic Plot as ON

#. Press OK.