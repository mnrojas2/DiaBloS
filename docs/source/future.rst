Topics for Further Improvement
==============================

.. What can be done in the future?

#. Support for other similar processes (closer to Modellica).
    -right now this algorithm only works with input-output signals (reference paper), but no other types of systems that can be described as graphs, like mass balance systems or electric grids.

#. Threading
    -right now this library works with everything under the same whileloop. So anything that can affect the execution loop also affects the interface fps, so it's necessary for the future that both loops can be happening in parallel. (separate UI from graph reading and executing process).

#. Use PyQT -> Change license according to rules.
    -right now the package works acceptable with pygame only, but to make this a better option for the user, it is necessary to remade to remade the interface using PyQT5 or another similar alternative. It's important to consider this as changing the license from MIT to GPL, due to the requirements of some UI libraries.

#. More support for special functions
    -Add support to functions that require different clocks, or elements not implemented yet, like an option to set parameters through inputs with data from other blocks.