Using DiaBloS: Some Practical Examples
======================================

This package provides some examples, as a way to demonstrate some of the capabilities that this program has. These
examples are contained in '.dat' files, located in the 'Examples' folder, and are executed as any file saved by the user.

Sine integration
----------------

:Description: This example shows the process for integrating a sinusoidal signal, using the RK45 method and then
    comparing the result with the mathematically correct curve.

:Demonstration: The math expression for the process is the following

    .. math:: y(t) = \int_0^t A\,\sin(\omega\,t + \phi_0) dt

    calculating the integral rigorously, we arrive at the following expression:

    .. math:: y(t) = 1 + A\,\cos(\omega\,t + \phi_0)

    rewriting :math:`\cos(\theta)` as :math:`\sin(\theta + \pi/2)`:

    .. math:: y(t) = 1 + A\,\sin(\omega\,t + \phi_0 + \pi/2)

    if :math:`A = 1`, :math:`\omega = 1` y :math:`\phi_0 = 0`, the resulting expression for :math:`y(t)` is:

    .. math:: y(t) = 1 + \sin(t + pi/2)

    This is exemplified as the addition of a step of amplitude 1 and a sinusoidal starting at :math:`\phi_0 = \pi/2` at time :math:`t_0 = 0`.

:Graph composition:

    Graph 1:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) A Sine block with an initial angle of :math:`\pi/4` to form :math:`\cos(t)`.
        #) A Sumator block to form :math:`y(t)` defined above with the previous two blocks.
        #) A Scope block to observe the result of the operation.

    Graph 2:
        #) A Sine block to form :math:`\sin(t)`, the base function that will be integrated.
        #) An Integrator block using the RK45 method and initial condition set in zero.
        #) A Scope block to observe the result of the operation.


Vectorial integration
---------------------

:Description: This example shows a integration with the RK45 method, but the inputs and outputs are vectors instead of
    scalar values.

:Demonstration:

    El sistema funciona a partir de considerar ciertos elementos del string como vectores
    El modelo busca corchetes []
    vector de una dimension seria v1D = [a,b]
    vector de dos dimensiones seria v2D = [[a,b],[c,d]] o [a,b;c,d]
    vector de 3 dimensiones v3D = [[[a,b],[c,d]],[[e,f],[g,h]]]
    el uso de espacios no importa v = [3.9     ,   343] -> v = [3.9, 343]

    Ejemplo consta de dos bloques Step que contiene un vector de 2 elementos en vez de un solo valor, sumados.
    Este valor se utiliza para un sistema en realimentación representado por la función de transferencia:

    .. math:: y(t) = e^{-t} \ast u(t) \leftrightarrow \frac{Y(s)}{U(s)} = \frac{1}{s+1}

:Graph Composition:

    #) A Step up block with amplitude :math:`[1.5, 2.0]` delayed in :math:`5` seconds.
    #) Another Step up block with amplitude :math:`[1.0, 0.5]` and no delay.
    #) A Sumator block to add the outputs of both blocks.
    #) Another Sumator block to subtract the output of the previous block with the output of the Integrator block.
    #) An Integrator block using the RK45 method to obtain the integration of the previous operation's result.
    #) A Scope block to observe the result of the operation.


Gaussian noise
--------------

:Description: This example shows a vectorial output (2 signals) with added noise.

:Demonstration:

    Block step output is a vector of 2 dimensions to the rest of the system.
    Demux splits that 2d signal into 2 signals.
    Each signal gets added gaussian noise (mu = 0, sigma = 1), then get downscaled by 0.5x with a gain block.
    Both sum outputs are scoped.

:Graph Composition:

    #) A Step up block with amplitude :math:`[5.0, -2.5]` delayed in :math:`2.5` seconds.
    #) A Demux block to split the vector from the Step block and treat each element as an independent signal.
    #) Two Noise blocks with :math:`\mu = 0` and :math:`\sigma = 1` to produce gaussian noise.
    #) Two Gain block with gain of :math:`0.5` to attenuate the signal amplitude from the noise blocks.
    #) Two Sumator blocks to add the noise ouput to each signal coming from the Demux.
    #) A Scope block to observe the result of the operation.


Signal products
---------------

:Description: This example shows element-wise products between vectors and a scalar signal and a vector.

:Demonstration:

    3 bloques step, uno escalar 2 vectorial
    1-2 se multiplican, 2-3 se multiplican
    Luego se muestran los resultados con los bloques scope
    Si se quiere ver las salidas de los bloques step, se puede reemplazar el terminator con el bloque scope

:Graph Composition:

    #) A Step up block with amplitude :math:`5.0` delayed in :math:`1` second.
    #) Another Step up block with amplitued :math:`[2.0, -3.0]` with no delay.
    #) A Step down block with amplitude :math:`[0.75, 1.5]` delayed in :math:`2` seconds.
    #) A Mux block to append the Step blocks' outputs in one simple vector.
    #) A Terminator block to finish the branch of the graph that will not be plotted.
    #) Two Sigproduct blocks, one to multiply the output of the first and second Step blocks, and another to multiply the output of the second and third Step blocks.
    #) Two Scope blocks to observe the results of the operations.


Export data
-----------

:Description: This example shows how signal data can be exported in '.npz' format.

:Demonstration:

    Se requiere agregar el bloque Export
    El sistema se define en dos partes,
    parte 1 se dedica a juntar los valores recibidos en una matriz
    parte 2 se dedica a juntar todos los vectores de los distintos scope para exportar

    El modelo de grafos consta de un Step block y un Sin block como cos(x)
    Lo que recibe el bloque Export es un vector (mux) del step en el primer elemento y un 1+cos(x) en el segundo

    Cabe destacar que este ejemplo solo exporta los archivos. El poder leerlos se puede hacer con python mismo o excel.

:Graph Composition:

    #) A Step up block with amplitude :math:`1` and no delay.
    #) A Sine block with an initial angle of :math:`\pi/4` to form :math:`\cos(t)`.
    #) A Sumator block to form :math:`1+\cos(t)` with the previous two blocks.
    #) A Mux block to produce a 2D vector with the Step block's output as first element and :math:`1+\cos(t)` (Sumator block's output) as second element.
    #) An Export block to save the data from the Mux block and then export it as a file in .npz format.


External source
---------------

:Description: This example shows an external function implemented as a source block.

:Demonstration:

    Bloque solo requiere las salidas
    Necesario definir bien el parametro que dice que es source
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra

:Graph Composition:

    #) An External block linked to the external usermodel function 'my_function_src.py'.
    #) Two Scope blocks to observe the outputs of the External block.

External Z-process
------------------

:Description: This example shows an external function implemented as a Z-process block.

:Demonstration:

    Necesario definir bien el parametro que dice que es process
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra

:Graph Composition:

    #) A Step up block with amplitude :math:`1` and no delay.
    #) An External block linked to the external usermodel function 'my_function_pcs.py'.
    #) A Scope block to observe the result of the operation.


External integrator (N-process)
-------------------------------

:Description: This example shows an external function implemented as a N-process block. In this case, an integrator
    using the same RK45 method already implemented in the Integrator block.

    Necesario definir bien el parametro que dice que es integrador
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra

:Graph Composition:

    #) A Step up block with amplitude :math:`1` and no delay.
    #) An External block linked to the external usermodel function 'external_rk45.py'.
    #) A Scope block to observe the result of the operation.


External derivator
------------------

:Description: This example shows an external function implemented as a Z-process block. In this case a variable
    step-size derivator (direct feedthrough function).

:Demonstration:

    Necesario definir bien el parametro que dice que es progress
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra

:Graph Composition:

    #) A Ramp block with slope :math:`1` and no delay.
    #) An External block linked to the external usermodel function 'external_derivative.py'.
    #) A Scope block to observe the result of the operation.


ODE system
----------

:Description: This example shows the same ODE system implemented in three different ways.

:Demonstration:

    Se utiliza un sistema en particular de ecuaciones diferenciales ordinarias como ejemplo:

    .. math:: \ddot{y} + 0.4\,\dot{y} + y = u

    si :math:`x_1 = y` y :math:`x_2 = \dot{y}` el sistema se puede representar de forma vectorial como:

    .. math:: X' &= f(X,U)\\
        \begin{bmatrix}
        \dot{x}_1 \\ \dot{x}_2
        \end{bmatrix}
        &=
        \begin{bmatrix}
        x_2 \\ -x_1 -0.4\, x_2 + u
        \end{bmatrix}

    y a su vez, se puede convertir a un sistema matricial del tipo :math:`X'= A\,X + B\,U`

    .. math::
        \begin{bmatrix}
        \dot{x}_1 \\ \dot{x}_2
        \end{bmatrix}
        &=
        \begin{bmatrix}
        0 & 1 \\ -1 & -0.4
        \end{bmatrix}
        \begin{bmatrix}
        x_1 \\ x_2
        \end{bmatrix}
        +
        \begin{bmatrix}
        0 \\ 1
        \end{bmatrix}
        u

    Entonces se crean 3 instancias de este problema para simular:

    #) Utilizando una función externa, se recibe u y el vector x, para entregar x'.

    #) Utilizando bloques gain y sum para conseguir un x'.

    #) Utilizando la definción del sistema no vectorial, calcular primero ddot{y}, para luego integrarlo, definir dot{y} y volver a integrarlo para encontrar {y}.

:Graph Composition:

    Graph 1:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) An External block linked to the external usermodel function 'axbu.py'.
        #) An Integrator block using the RK45 method to obtain the integration of the previous operation's result.
        #) A Scope block to observe the output of the Integrator block.
        #) An Export block to save the data from the Integrator block and then export it as a file in .npz format.

    Graph 2:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) A Gain block to multiply the output of the Step block with the vector :math:`B = [0.0, 1.0]` producing :math:`BU`.
        #) A Gain block to multiply the output vector of the Integrator block with the matrix :math:`A = [[0.0, 1.0], [-1.0, -0.4]]` producing :math:`AX`.
        #) A Sumator block to add the output of both Gain blocks, producing :math:`AX+BU`.
        #) An Integrator block using the RK45 method to obtain :math:`X` from the Sumator block's output, and initial conditions set in :math:`[0.0, 0.0]`.
        #) A Scope block to observe the output of the Integrator block.
        #) An Export block to save the data from the Integrator block and then export it as a file in .npz format.

    Graph 3:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) An Integrator block that integrates the value of the Sumator block's output to obtain :math:`x_2`.
        #) A Gain block to multiply :math:`x_2` by :math:`-0.4` and be used in the Sumator block as future input.
        #) Another Integrator block that integrates :math:`x_2` to get :math:`x_1`.
        #) Another Gain block used to multiply :math:`x_1` by :math:`-1` and be used in the Sumator block as future input.
        #) A Sumator block that adds the result of both Gain blocks and the Step block's output to get :math:`\dot{x}_2`.
        #) A Mux block to produce a vector with the output values of the Integrator blocks.
        #) A Scope block to observe the output of the Mux block.
        #) An Export block to save the data from the Mux block and then export it as a file in .npz format.

.. raw:: latex

    \newpage