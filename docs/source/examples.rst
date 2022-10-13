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

Integracion vectorial, utilizando el método de integracion runge-kutta.

:description: Este ejemplo muestra un ejemplo de integración RK45, donde los valores utilizados por el sistema son vectores.

:explanation:

    El sistema funciona a partir de considerar ciertos elementos del string como vectores
    El modelo busca corchetes []
    vector de una dimension seria v1D = [a,b]
    vector de dos dimensiones seria v2D = [[a,b],[c,d]] o [a,b;c,d]
    vector de 3 dimensiones v3D = [[[a,b],[c,d]],[[e,f],[g,h]]]
    el uso de espacios no importa v = [3.9     ,   343] -> v = [3.9, 343]


Gaussian Noise
--------------

Un ejemplo que muestra la modelación de ruido en un sistema step.

:description: Este ejemplo muestra el cómo se puede agregar ruido a las señales, simplemente sumando un bloque ruido a
    la señal original. Además se aprovecha de mostrar el cómo separar las señales un vector por medio del bloque demux.

:explanation:

    Block step output is a vector of 2 dimensions to the rest of the system.
    Demux splits that 2d signal into 2 signals.
    Each signal gets added gaussian noise (mu = 0, sigma = 1), then get downscaled by 0.5x with a gain block.
    Both sum outputs are scoped.


Signal products
---------------

Multiplicación de datos con el bloque sigprod. Tanto escalar por vector, como vector por vector (multiplicación por elementos).

:descripcion: Este ejemplo muestra el cómo se pueden multiplicar señales provenientes de distintas fuentes, sean estas escalares o vectoriales.

:explanation:

    3 bloques step, uno escalar 2 vectorial
    1-2 se multiplican, 2-3 se multiplican
    Luego se muestran los resultados con los bloques scope
    Si se quiere ver las salidas de los bloques step, se puede reemplazar el terminator con el bloque scope

Export data
-----------

Exportar datos proveniente de un vector muxxeado (step y cos(x))

:description: Este ejemplo muestra el cómo se pueden exportar datos, a partir de una entrada vectorial. Cabe destacar
    que una segunda parte del proceso requeriría tomar los datos exportados y desempacarlos utilizando otro código de
    python con apoyo de la librería numpy

:explanation:

    Se requiere agregar el bloque Export
    El sistema se define en dos partes,
    parte 1 se dedica a juntar los valores recibidos en una matriz
    parte 2 se dedica a juntar todos los vectores de los distintos scope para exportar

External source
---------------

Ejemplo de funcion tipo fuente, implementada con una funcion externa

:description: Ejemplo de cómo crear una función source básica con código externo.

:explanation:

    Bloque solo requiere las salidas
    Necesario definir bien el parametro que dice que es source
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


External process
----------------

Ejemplo de funcion tipo proceso, implementada con una funcion externa

:description: Ejemplo de cómo crear una función proceso simple, de forma de demostrar las capacidades del programa de trabajar con implementaciones externas.

:explanation:

    Necesario definir bien el parametro que dice que es process
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


External integrator
-------------------

Ejemplo de integracion runge-kutta45

:description: Ejemplo de cómo implementar la parte interna del proceso de integración rungekutta, como función externa

:explanation:

    Necesario definir bien el parametro que dice que es integrador
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


External derivator
------------------

Ejemplo de derivacion de paso variable (paso constante no sirve)

:description: ejemplo de derivación como funcion externa

:explanation:

    Necesario definir bien el parametro que dice que es progress
    En la simulacion es necesario cargar el bloque "Bloque" para cargar externos
    La funcion de carga, se dedica de ajustar los puertos y parametros del bloque para que corra


Feedback system implementations
-------------------------------

Ejemplo de sistema con feedback, implementado de 3 maneras distintas (funcion externa, funcion vectorial, funcion escalar)

:description: Ejemplo integral que asocia varias funciones para poder comparar 3 métodos distintos para implementar un sistema de ecuaciones diferenciales, incluyendo el exportar tales datos a .npz

:explanation:

    Este ejemplo en forma de resumen la mayoria de los ejemplos vistos anteriormente, pero en conjunto para un sistema realimentado
    modo 1 funcion externa x' = Ax + Bu
    modo 2 funcion vectorial con uso de gains para hacer el Ax + Bu
    modo 3 funcion escalar con uso de más de un integrador (explicar parte matematica)

