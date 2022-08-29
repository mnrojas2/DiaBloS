Using DiaBloS: Some Practical Examples
======================================

Algunos ejemplos de la herramienta en funcionamiento:

Sine integration
----------------

:Description: Este ejemplo muestra el proceso para integrar una señal sinusoidal, utilizando dos métodos de integración
    distintos (Forward Euler y Runge Kutta 45) para luego comparar los resultados con la curva matemáticamente correcta.
:Math explanation: The math expression for the process is the following

    .. math:: y(t) = \int_0^t A\,\sin(\omega\,t + \phi_0) dt

    calculando la integral de forma rigurosa, se llega a la siguiente expresión:

    .. math:: y(t) = 1 + A\,\cos(\omega\,t + \phi_0)

    reescribiendo :math:`\cos(\theta)` como :math:`\sin(\theta + \pi/2)`:

    .. math:: y(t) = 1 + A\,\sin(\omega\,t + \phi_0 + \pi/2)

    si :math:`A = 1`, :math:`\omega = 1` y :math:`\phi_0 = 0`, el resultado de :math:`y(t)` queda como:

    .. math:: y(t) = 1 + \sin(t + pi/2)

    Lo cual se ejemplifica como la suma de un step de amplitud 1 y una sinusoidal que parte en :math:`\pi/2` en tiempo 0.

    El problema, muestra dos de los 4 métodos de integración disponibles...

    Forward euler consiste en simplemente tomar el valor anterior y extender un rectángulo...
    Runge Kutta consiste en un método más complejo... pero más exacto

:How to execute it:
    Despues de abirr el programa

    editar parametros

    presionar Play

:Important details: no c

.. Nombre
.. Descripcion
.. Explicacion del proceso (o de las razones de pq se hizo asi)
.. Detalles importantes del ejemplo en particular
.. Que se puede modificar, o para que se puede usar el ejemplo.
.. bugs

Vectorial integration
---------------------

Integracion vectorial, comparando métodos de integracion runge-kutta y forward euler.


Export data
-----------

Exportar datos proveniente de un vector muxxeado (step y cos(x))

External source
---------------

Ejemplo de funcion tipo fuente, implementada con una funcion externa

External process
----------------

Ejemplo de funcion tipo proceso, implementada con una funcion externa

External delay
--------------

Ejemplo de funcion tipo memoria, implementada con una funcion externa

External integrator
-------------------

Ejemplo de integracion runge-kutta45

External derivator
------------------

Ejemplo de derivacion de paso variable (paso constante no sirve)

Feedback system three ways
----------------------

Ejemplo de sistema con feedback, implementado de 3 maneras distintas (funcion externa, funcion vectorial, funcion escalar)

.. Nombre
.. Descripcion
.. Explicacion del proceso (o de las razones de pq se hizo asi)
.. Detalles importantes del ejemplo en particular
.. Que se puede modificar, o para que se puede usar el ejemplo.
.. bugs
