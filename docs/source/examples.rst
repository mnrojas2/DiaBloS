Using DiaBloS: Some Practical Examples
======================================

Algunos ejemplos de la herramienta en funcionamiento:

Sine integration
----------------

:Description: This example shows the process for integrating a sinusoidal signal, using two different integration
    methods (Forward Euler and Runge Kutta 45) and then comparing the results with the mathematically correct curve.
:Explanation: The math expression for the process is the following

    .. math:: y(t) = \int_0^t A\,\sin(\omega\,t + \phi_0) dt

    calculating the integral rigorously, we arrive at the following expression:

    .. math:: y(t) = 1 + A\,\cos(\omega\,t + \phi_0)

    rewriting :math:`\cos(\theta)` as :math:`\sin(\theta + \pi/2)`:

    .. math:: y(t) = 1 + A\,\sin(\omega\,t + \phi_0 + \pi/2)

    if :math:`A = 1`, :math:`\omega = 1` y :math:`\phi_0 = 0`, the resulting expression for :math:`y(t)` is:

    .. math:: y(t) = 1 + \sin(t + pi/2)

    This is exemplified as the sum of a step of amplitude 1 and a sinusoidal starting at :math:`\phi_0 = \pi/2` at time :math:`t_0 = 0`.

    El problema, también compara dos métodos de integración disponibles a utilizar...

    #. Metodo Forward: El más simple, consiste en ir sumando un valor equivalente a la multiplicación del valor nuevo por el tiempo de muestreo

    .. math:: y(t) \approx y(k) = \sum_{k=0}^K f(k,x) \cdot \Delta T

    #. Metodo Runge Kutta 45: Este metodo es más complejo, pero más exacto...

    .. math:: y(t) \approx (k_1 + 2k_2 + 2k_3 +k_4) \Delta T

    donde

    .. math:: k_1 &= \Delta T \cdot f\left(t,x\right) \\
        k_2 &= \Delta T \cdot f\left(t + \frac{\Delta T}{2}, x + \frac{k_1}{2}\right) \\
        k_3 &= \Delta T \cdot f\left(t + \frac{\Delta T}{2}, x + \frac{k_2}{2}\right) \\
        k_4 &= \Delta T \cdot f\left(t + \Delta T, x + k_3\right)


:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

:Important details: no c

Vectorial integration
---------------------

Integracion vectorial, comparando métodos de integracion runge-kutta y forward euler.

:description: Este ejemplo muestra un ejemplo de integración RK45, donde los valores utilizados por el sistema son vectores.

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play


Export data
-----------

Exportar datos proveniente de un vector muxxeado (step y cos(x))

:description: Este ejemplo muestra el cómo se pueden exportar datos, a partir de una entrada vectorial. Cabe destacar que una segunda parte del proceso requeriría tomar los datos exportados y desempacarlos utilizando otro código de python con apoyo de la librería numpy

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

External source
---------------

Ejemplo de funcion tipo fuente, implementada con una funcion externa

:description: Ejemplo de cómo crear una función source básica con código externo.

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

External process
----------------

Ejemplo de funcion tipo proceso, implementada con una funcion externa

:description: Ejemplo de cómo crear una función proceso simple, de forma de demostrar las capacidades del programa de trabajar con implementaciones externas.

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

External delay
--------------

Ejemplo de funcion tipo memoria, implementada con una funcion externa

:description: Ejemplo de cómo trabajar con datos guardados, de forma externa como un plus.

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

External integrator
-------------------

Ejemplo de integracion runge-kutta45

:description: Ejemplo de cómo implementar la parte interna del proceso de integración rungekutta, como función externa

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

External derivator
------------------

Ejemplo de derivacion de paso variable (paso constante no sirve)

:description: ejemplo de derivación como funcion externa

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

Feedback system three ways
--------------------------

Ejemplo de sistema con feedback, implementado de 3 maneras distintas (funcion externa, funcion vectorial, funcion escalar)

:description: Ejemplo integral que asocia varias funciones para poder comparar 3 métodos distintos para implementar un sistema de ecuaciones diferenciales, incluyendo el exportar tales datos a .npz

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

.. Nombre
.. Descripcion
.. Explicacion del proceso (o de las razones de pq se hizo asi)
.. Detalles importantes del ejemplo en particular
.. Que se puede modificar, o para que se puede usar el ejemplo.
.. bugs
