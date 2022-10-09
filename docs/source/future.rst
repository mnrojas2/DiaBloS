Topics for Further Improvement
==============================

.. What can be done in the future?

#. Support for other similar processes.
    Right now this algorithm only works with input-output signals, but no other types of systems that can be described
    with graphs, like mass balance systems or electric grids or even distributed systems. So one thing that could be
    worked in the future are support for other graph represented systems.

#. Use of Threading, improve and simplify some processes.
    Right now this library works with everything under the same while loop. So anything that can affect the execution
    loop also affects the interface fps, so it's necessary for the future that both loops can be happening in parallel,
    essentially split the UI process from the graph executing process).

    Also, improve the versatility of some functions by using better methods to programming in python. e.g.: Use of \*args
    and \*\*kwargs to allow more specific parameters to some functions without affecting the readability and stability
    of others.

#. Use of PyQT5.
    Right now the package works with pygame only, in an acceptable way, but to make this a better option for the user,
    it is necessary to rework interface using PyQT5 or another similar alternative. It's important to consider
    this as changing the license from MIT to GPL, due to the requirements of some of these libraries.

#. More support for special functions.
    Add support to functions that require different clocks, or elements not implemented yet, like an option to set
    parameters through inputs with data from other blocks.