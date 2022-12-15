Using DiaBloS: Some Practical Examples
======================================

This package provides some examples, as a way to demonstrate some of the capabilities that this program has. These
examples are contained in '.dat' files, located in the 'Examples' folder, and are executed as any file saved by the user.

----------------
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

    This is exemplified as the addition of a step of amplitude 1 and a sinusoidal starting at :math:`\phi_0 = \pi/2` at time :math:`t_0 = 0`. Then an example comparing the integration process and the exact curve can be done.

:Graph composition:

    Graph 1:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) A Sine block with an initial angle of :math:`\pi/4` to form :math:`\cos(t)`.
        #) An Adder block to form :math:`y(t)` defined above with the previous two blocks.
        #) A Scope block to observe the result of the operation.

    Graph 2:
        #) A Sine block to form :math:`\sin(t)`, the base function that will be integrated.
        #) An Integrator block using the RK45 method and initial condition set in zero.
        #) A Scope block to observe the result of the operation.


---------------------
Vectorial integration
---------------------

:Description: This example shows a integration with the RK45 method, but the inputs and outputs are vectors instead of
    scalar values.

:Demonstration:

    The Step block has support for vector outputs of the type:

        #) Vectorial = [a, b, c, d].
        #) Matrix = [[a, b], [c, d]]
        #) 3DoF matrix = [[[a, b], [c, d]], [[e, f], [g, h]]]

    A graph is formed representing a simple feedback system, consisting of an integrator connected in feedback. The input
    values are defined by two vector sources which are added together. This value is used for a feedback system represented
    by the following transfer function:

    .. math:: y(t) = e^{-t} \ast u(t) \leftrightarrow \frac{Y(s)}{U(s)} = \frac{1}{s+1}

    It should be noted that for this case, the initial conditions of the Integrator block must be of the same dimensions
    as its input. Since for this case it will be a vector of two elements, the initial conditions must be defined as
    :math:`[0.0, 0.0]`, if you want to start at zero for both.

:Graph Composition:

    #) A Step up block with amplitude :math:`[1.5, 2.0]` delayed in :math:`5` seconds.
    #) Another Step up block with amplitude :math:`[1.0, 0.5]` and no delay.
    #) An Adder block to add the outputs of both blocks.
    #) Another Adder block to subtract the output of the previous block with the output of the Integrator block.
    #) An Integrator block using the RK45 method to obtain the integration of the Adder's output with initial conditions set in :math:`[0.0, 0.0]`.
    #) A Scope block to observe the result of the operation.


--------------
Gaussian noise
--------------

:Description: This example shows a vectorial output (2 signals) with added noise.

:Demonstration:

    The Noise block allows the creation of Gaussian noise for simulation effects. It only requires defining :math:`mu`
    and :math:`sigma` and then adding the result to the target signal.

    The graph to be shown is a system where the Step block's amplitude is :math:`[5.0, -2.5]`, separates the vector into
    two independent signals, adding a Gaussian noise to each.

:Graph Composition:

    #) A Step up block with amplitude :math:`[5.0, -2.5]` delayed in :math:`2.5` seconds.
    #) A Demultiplexer block to split the vector from the Step block and treat each element as an independent signal.
    #) Two Noise blocks with :math:`\mu = 0` and :math:`\sigma = 1` to produce gaussian noise.
    #) Two Gain block with gain of :math:`0.5` to attenuate the signal amplitude from the noise blocks.
    #) Two Adder blocks to add the noise ouput to each signal coming from the Demultiplexer.
    #) A Scope block to observe the result of the operation.


Signal products
---------------

:Description: This example shows element-wise products between vectors and a scalar signal and a vector.

:Demonstration:

    The Sigproduct block is used to multiply the values of each iteration between different signals. Defining :math:`y_1`
    and :math:`y_2`, as two output signals from two different blocks, the following signal multiplications can be observed:

        #) Scalar with scalar: If :math:`y_1 = a` and :math:`y_2 = b` then :math:`y_3 = a\, b`.

        #) Scalar with vector: If :math:`y_1 = a` and :math:`y_2 = [b, c]` then :math:`y_3 = [a\, b, a\, c]`.

        #) Vector with vector: If :math:`y_1 = [a, b]` and :math:`y_2 = [c, d]` then :math:`y_3 = [a, c, b, b, d]`.

    An example graph is shown where the multiplication between three different sources is observed, based on the three
    types of multiplication described above.

:Graph Composition:

    #) A Step up block with amplitude :math:`5.0` delayed in :math:`1` second.
    #) Another Step up block with amplitued :math:`[2.0, -3.0]` with no delay.
    #) A Step down block with amplitude :math:`[0.75, 1.5]` delayed in :math:`2` seconds.
    #) A Multiplexer block to append the Step blocks' outputs in one simple vector.
    #) A Terminator block to finish the branch of the graph that will not be plotted.
    #) Two Sigproduct blocks, one to multiply the output of the first and second Step blocks, and another to multiply the output of the second and third Step blocks.
    #) Two Scope blocks to observe the results of the operations.


-----------
Export data
-----------

:Description: This example shows how signal data can be exported in '.npz' format.

:Demonstration:

    The Export block is used to save data of signals created during the simulation. It is enough to add this block and
    define the labels within the settings of this block.

    In particular, the function for exporting data consists of two parts:

        #) Data acquisition: During the simulation, the block will accumulate data in ordered vectors, each associated with a label. associated to a label. If labels have not been previously defined, or if they are not enough to cover all the vectors to be created, the block will vectors to be created, the system adds default names to complete the list. A matrix is then created a matrix is then created that will append the values added by each simulation loop.

        #) Data conversion: At the end of the simulation, all the vectors of the Export blocks are taken (if there are more than one), and all the data is assembled. more than one), and a larger matrix is assembled, which will be exported as .npz by means of the numpy library.

    After completing a simulation process, a .npz file will be created and found inside the 'saves' folder, with the same
    name as the savefile (by default 'data.npz'). Note that this example only exports the files. Being able to read them
    can be done with Python, Excel or similar.

:Graph Composition:

    #) A Step up block with amplitude :math:`1` and no delay.
    #) A Sine block with an initial angle of :math:`\pi/4` to form :math:`\cos(t)`.
    #) An Adder block to form :math:`1+\cos(t)` with the previous two blocks.
    #) A Multiplexer block to produce a 2D vector with the Step block's output as first element and :math:`1+\cos(t)` (Adder block's output) as second element.
    #) An Export block to save the data from the Multiplexer block and then export it as a file in .npz format.


External source
---------------

:Description: This example shows an external function implemented as a source block.

:Demonstration:

    The Block block associates user-defined functions to give more options for graph simulation.

    The only parameter needed to modify is the function name (and ``.py`` file) located in the ``usermodels`` folder. After
    loading this, the block acquires the data defined in the file to change, number of inputs, outputs, block type and
    color.

    For this case, it is important to define the block inputs as :math:`0` and the block type as :math:`0` (source).

    Details on how to create such functions can be found in :ref:`developer:usermodel functions`.

:Graph Composition:

    #) An External block linked to the external usermodel function ``my_function_src.py``.
    #) Two Scope blocks to observe the outputs of the External block.


------------------
External Z-process
------------------

:Description: This example shows an external function implemented as a Z-process block.

:Demonstration:

    The Block block associates user-defined functions to give more options for graph simulation.

    The only parameter needed to modify is the function name (and ``.py`` file) located in the ``usermodels`` folder. After
    loading this, the block acquires the data defined in the file to change, number of inputs, outputs, block type and
    color.

    For this case, it is important to define the block type as :math:`2` (z-process).

    Details on how to create such functions can be found in :ref:`developer:usermodel functions`.

:Graph Composition:

    #) A Step up block with amplitude :math:`1` and no delay.
    #) An External block linked to the external usermodel function ``my_function_pcs.py``.
    #) A Scope block to observe the result of the operation.


-------------------------------
External integrator (N-process)
-------------------------------

:Description: This example shows an external function implemented as a N-process block. In this case, an integrator
    using the same RK45 method already implemented in the Integrator block.

    The Block block associates user-defined functions to give more options for graph simulation.

    The only parameter needed to modify is the function name (and ``.py`` file) located in the ``usermodels`` folder. After
    loading this, the block acquires the data defined in the file to change, number of inputs, outputs, block type and
    color.

    For this case, it is important to define the block type as :math:`1` (n-process).

    Details on how to create such functions can be found in :ref:`developer:usermodel functions`, details on how the RK45 integration method works, see :ref:`developer:graph simulation algorithm`.

:Graph Composition:

    #) A Step up block with amplitude :math:`1` and no delay.
    #) An External block linked to the external usermodel function ``external_rk45.py``.
    #) A Scope block to observe the result of the operation.


------------------------------
External derivator (Z-process)
------------------------------

:Description: This example shows an external function implemented as a Z-process block. In this case a variable
    step-size derivator (direct feedthrough function).

:Demonstration:

    The Block block associates user-defined functions to give more options for graph simulation.

    The only parameter needed to modify is the function name (and ``.py`` file) located in the ``usermodels`` folder. After
    loading this, the block acquires the data defined in the file to change, number of inputs, outputs, block type and
    color.

    For this case, it is important to define the block type as :math:`2` (z-process).

    Details on how to create such functions can be found in :ref:`developer:usermodel functions`.

:Graph Composition:

    #) A Ramp block with slope :math:`1` and no delay.
    #) An External block linked to the external usermodel function ``external_derivative.py``.
    #) A Scope block to observe the result of the operation.


---------------------
Convergent ODE system
---------------------

:Description: This example shows the same convergent ODE system implemented in three different ways.

:Demonstration:

    A particular ordinary differential equation is used as an example:

    .. math:: \ddot{y} + 0.4\,\dot{y} + y = u

    if :math:`x_1 = y` and :math:`x_2 = \dot{y}` this ODE can be represented in vector form as:

    .. math:: X' &= f(X,U)\\
        \begin{bmatrix}
        \dot{x}_1 \\ \dot{x}_2
        \end{bmatrix}
        &=
        \begin{bmatrix}
        x_2 \\ -x_1 -0.4\, x_2 + u
        \end{bmatrix}

    and in the same time, it can be converted to a matrix system of the type :math:`X'= A\,X + B\,U`.

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

    So three instances of this problem are created to simulate:

    #) Using an external function, where value :math:`U` and vector :math:`X=[x_1, x_2]` are received, to deliver :math:`\dot{X} = f(X,U)`.

    #) Using gain and adder blocks to form the matrix notation (:math:`X'= A,X + B,U`) before integrating it.

    #) Using the non-vector system definition, first by calculating :math:`ddot{y}`, then integrate it to find :math:`dot{y}` and then integrate once again to find :math:`y`.

:Graph Composition:

    Graph 1:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) An External block linked to the external user model function ``ode_system_conv.py``.
        #) An Integrator block using the RK45 method to obtain the integration of the previous operation's result.
        #) A Scope block to observe the output of the Integrator block.
        #) An Export block to save the data from the Integrator block and then export it as a file in .npz format.

    Graph 2:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) A Gain block to multiply the output of the Step block with the vector :math:`B = [0.0, 1.0]` producing :math:`BU`.
        #) A Gain block to multiply the output vector of the Integrator block with the matrix :math:`A = [[0.0, 1.0], [-1.0, -0.4]]` producing :math:`AX`.
        #) An Adder block to add the output of both Gain blocks, producing :math:`AX+BU`.
        #) An Integrator block using the RK45 method to obtain :math:`X` from the Adder block's output, and initial conditions set in :math:`[0.0, 0.0]`.
        #) A Scope block to observe the output of the Integrator block.
        #) An Export block to save the data from the Integrator block and then export it as a file in .npz format.

    Graph 3:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) An Integrator block that integrates the value of the Adder block's output to obtain :math:`x_2`.
        #) A Gain block to multiply :math:`x_2` by :math:`-0.4` and be used in the Adder block as future input.
        #) Another Integrator block that integrates :math:`x_2` to get :math:`x_1`.
        #) Another Gain block used to multiply :math:`x_1` by :math:`-1` and be used in the Adder block as future input.
        #) An Adder block that adds the result of both Gain blocks and the Step block's output to get :math:`\dot{x}_2`.
        #) A Multiplexer block to produce a vector with the output values of the Integrator blocks.
        #) A Scope block to observe the output of the Multiplexer block.
        #) An Export block to save the data from the Multiplexer block and then export it as a file in .npz format.

-------------------
Critical ODE system
-------------------

:Description: This example shows the same critical ODE system implemented in three different ways, compared to the exact curve.

:Demonstration:

    A particular ordinary differential equation system is used vector form as an example:

    .. math:: X' &= f(X,U)\\
        \begin{bmatrix}
        \dot{x}_1 \\ \dot{x}_2
        \end{bmatrix}
        &=
        \begin{bmatrix}
        x_2 \\ -x_1 + u
        \end{bmatrix}

    and in the same time, it can be converted to a matrix system of the type :math:`X'= A\,X + B\,U`.

    .. math::
        \begin{bmatrix}
        \dot{x}_1 \\ \dot{x}_2
        \end{bmatrix}
        &=
        \begin{bmatrix}
        0 & 1 \\ -1 & 0
        \end{bmatrix}
        \begin{bmatrix}
        x_1 \\ x_2
        \end{bmatrix}
        +
        \begin{bmatrix}
        0 \\ 1
        \end{bmatrix}
        u

    Knowing that :math:`A` is the rotation matrix when :math:`\theta = 90^{\circ}`, and setting :math:`u = 1`, the equations can be rewritten as:

    .. math:: x_1 &= 1 - \cos(t) \\ x_2 &= \sin(t)

    So four instances of this problem are created to simulate:

    #) Using an external function as source, the exact value of the curves.

    #) Using an external function, where value :math:`U` and vector :math:`X=[x_1, x_2]` are received, to deliver :math:`\dot{X} = f(X,U)`.

    #) Using gain and adder blocks to form the matrix notation (:math:`X'= A,X + B,U`) before integrating it.

    #) Using the non-vector system definition, first by calculating :math:`\dot{x}_2`, then integrate it to find :math:`x_2 = \dot{x}_1` and then integrate once again to find :math:`x_1`.

:Graph Composition:

    Graph 1:
        #) An External block linked to the external user model function ``ode_exact_crit.py``.
        #) #) A Scope block to observe the output of the External block.

    Graph 2:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) An External block linked to the external user model function ``ode_system_crit.py``.
        #) An Integrator block using the RK45 method to obtain the integration of the previous operation's result.
        #) A Scope block to observe the output of the Integrator block.
        #) An Export block to save the data from the Integrator block and then export it as a file in .npz format.

    Graph 3:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) A Gain block to multiply the output of the Step block with the vector :math:`B = [0.0, 1.0]` producing :math:`BU`.
        #) A Gain block to multiply the output vector of the Integrator block with the matrix :math:`A = [[0.0, 1.0], [-1.0, -0.4]]` producing :math:`AX`.
        #) An Adder block to add the output of both Gain blocks, producing :math:`AX+BU`.
        #) An Integrator block using the RK45 method to obtain :math:`X` from the Adder block's output, and initial conditions set in :math:`[0.0, 0.0]`.
        #) A Scope block to observe the output of the Integrator block.
        #) An Export block to save the data from the Integrator block and then export it as a file in .npz format.

    Graph 4:
        #) A Step up block with amplitude :math:`1` and no delay.
        #) An Integrator block that integrates the value of the Adder block's output to obtain :math:`x_2`.
        #) A Gain block to multiply :math:`x_2` by :math:`-0.4` and be used in the Adder block as future input.
        #) Another Integrator block that integrates :math:`x_2` to get :math:`x_1`.
        #) Another Gain block used to multiply :math:`x_1` by :math:`-1` and be used in the Adder block as future input.
        #) An Adder block that adds the result of both Gain blocks and the Step block's output to get :math:`\dot{x}_2`.
        #) A Multiplexer block to produce a vector with the output values of the Integrator blocks.
        #) A Scope block to observe the output of the Multiplexer block.
        #) An Export block to save the data from the Multiplexer block and then export it as a file in .npz format.

-----------------
Watertank control
-----------------

:Description: This example shows the classic watertank control problem, trying to stabilize the height of the water using a PI control.

:Demonstration: ESPERAR A LOS CAMBIOS DE LA SECCION DE RESULTADOS DEL PAPER

:Graph composition:

    #) A Step block
    #) A Gain block (5)
    #) An Adder block
    #) An External block sqrt_pcs
    #) An Integrator block (PI)
    #) An Integrator block (h)
    #) An External block (sat_pcs)
    #) A Scope block

..
    ------------------------------------------------
    Differential traction robot model and controller
    ------------------------------------------------

    :Description: This example shows the modelling of a differential traction robot.

    :Demonstration: ESPERAR A LOS CAMBIOS DEL CONTROLADOR

    :Graph composition:

        #) An External block (square_robot/robot_torques)
        #) An Adder block (5)
        #) A Gain block (4)
        #) A SigProduct block
        #) An External block (sin_pcs/cos_pcs)
        #) A Multiplexer block (2)
        #) A Demultiplexer block
        #) An Integrator block (x)
        #) A Scope block
        #) An Export block

.. raw:: latex

    \newpage