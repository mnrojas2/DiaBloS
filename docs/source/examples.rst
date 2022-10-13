Using DiaBloS: Some Practical Examples
======================================

This package provides some examples, as a way to demonstrate some of the capabilities that this program has. These
examples are contained in '.dat' files, located in the 'Examples' folder, and are executed as any file saved by the user.

Sine integration
----------------

:Description: This example shows the process for integrating a sinusoidal signal, using the RK45 method and then
    comparing the result with the mathematically correct curve.

:Explanation: The math expression for the process is the following

    .. math:: y(t) = \int_0^t A\,\sin(\omega\,t + \phi_0) dt

    calculating the integral rigorously, we arrive at the following expression:

    .. math:: y(t) = 1 + A\,\cos(\omega\,t + \phi_0)

    rewriting :math:`\cos(\theta)` as :math:`\sin(\theta + \pi/2)`:

    .. math:: y(t) = 1 + A\,\sin(\omega\,t + \phi_0 + \pi/2)

    if :math:`A = 1`, :math:`\omega = 1` y :math:`\phi_0 = 0`, the resulting expression for :math:`y(t)` is:

    .. math:: y(t) = 1 + \sin(t + pi/2)

    This is exemplified as the sum of a step of amplitude 1 and a sinusoidal starting at :math:`\phi_0 = \pi/2` at time :math:`t_0 = 0`.

    Metodo Runge Kutta 45: Este metodo es más complejo, pero más exacto.

    .. math:: y(t) \approx (k_1 + 2k_2 + 2k_3 +k_4) \Delta T

    donde

    .. math:: k_1 &= \Delta T \cdot f\left(t,x\right) \\
        k_2 &= \Delta T \cdot f\left(t + \frac{\Delta T}{2}, x + \frac{k_1}{2}\right) \\
        k_3 &= \Delta T \cdot f\left(t + \frac{\Delta T}{2}, x + \frac{k_2}{2}\right) \\
        k_4 &= \Delta T \cdot f\left(t + \Delta T, x + k_3\right)


Vectorial integration
---------------------

:description: This example shows a integration with the RK45 method, but the inputs and outputs are vectors instead of
    scalar values.

:demonstration:

    El sistema funciona a partir de considerar ciertos elementos del string como vectores
    El modelo busca corchetes []
    vector de una dimension seria v1D = [a,b]
    vector de dos dimensiones seria v2D = [[a,b],[c,d]] o [a,b;c,d]
    vector de 3 dimensiones v3D = [[[a,b],[c,d]],[[e,f],[g,h]]]
    el uso de espacios no importa v = [3.9     ,   343] -> v = [3.9, 343]


Gaussian noise
--------------

:description: This example shows a vectorial output (2 signals) with added noise.

:demonstration:

    Block step output is a vector of 2 dimensions to the rest of the system.
    Demux splits that 2d signal into 2 signals.
    Each signal gets added gaussian noise (mu = 0, sigma = 1), then get downscaled by 0.5x with a gain block.
    Both sum outputs are scoped.


Signal products
---------------

:descripcion: This example shows element-wise products between vectors and a scalar signal and a vector.

:demonstration:

    3 bloques step, uno escalar 2 vectorial
    1-2 se multiplican, 2-3 se multiplican
    Luego se muestran los resultados con los bloques scope
    Si se quiere ver las salidas de los bloques step, se puede reemplazar el terminator con el bloque scope

Export data
-----------

:description: This example shows how signal data can be exported in '.npz' format.

:demonstration:

    Se requiere agregar el bloque Export
    El sistema se define en dos partes,
    parte 1 se dedica a juntar los valores recibidos en una matriz
    parte 2 se dedica a juntar todos los vectores de los distintos scope para exportar
    Cabe destacar que una segunda parte del proceso requeriría tomar los datos exportados y desempacarlos utilizando otro código de python con apoyo de la librería numpy

External source
---------------

:description: This example shows an external function implemented as a source block.

:demonstration:

    Bloque solo requiere las salidas
    Necesario definir bien el parametro que dice que es source
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


External Z-process
------------------

:description: This example shows an external function implemented as a Z-process block.

:demonstration:

    Necesario definir bien el parametro que dice que es process
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


External integrator
-------------------

:description: This example shows an external function implemented as a N-process block. In this case, an integrator
    using the same RK45 method already implemented in the Integrator block.

    Necesario definir bien el parametro que dice que es integrador
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


External derivator
------------------

:description: This example shows an external function implemented as a Z-process block. In this case a variable
    step-size derivator (direct feedthrough function).

:demonstration:

    Necesario definir bien el parametro que dice que es progress
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


ODE system
----------

:description: This example shows the same ODE system implemented in three different ways.

:demonstration:

    Este ejemplo en forma de resumen la mayoria de los ejemplos vistos anteriormente, pero en conjunto para un sistema realimentado
    modo 1 funcion externa x' = Ax + Bu
    modo 2 funcion vectorial con uso de gains para hacer el Ax + Bu
    modo 3 funcion escalar con uso de más de un integrador (explicar parte matematica)

