Introduction
============

DiaBloS (Diagram Block Simulator) is a block programming tool, focused on the simulation of systems represented as
ordinary differential equations.

This tool is presented as an open source alternative independent of software or libraries external to Python, since it
only relies on packages already provided by Python, or available through pip.

This manual is separated into two parts: A novice's guide, which explains how to use the library, mainly focused on the
interface, and a programmer's guide, focused on explaining the hierarchy of functions and the most important algorithms,
with the idea of making it easier for other people to contribute to the project.

Capabilities of the DiaBloS package
-----------------------------------

DiaBloS es capaz de:

-Relate independent functions and obtaining results as a whole.

-Integrate and derivate signals.

-Produce step responses, such as ramp responses, for systems of ordinary difference (differential) equations.

-Generate signals with Gaussian distribution noise.

-Create feedback systems.

-Plot signals, both traditionally and dynamically (in active simulation time).

-Export signal data in .npz format.

-Saving and loading block systems created in .dat format.

-Vector data handling.

-Routing multiple signals into a single output vector and vice versa.

Existen librerias de python que se enfocan en esto, pero solo se basan en las conexiones y no la interfaz, como tampoco
el poder ejecutarlos. Tambien otros que requieren el uso de herramientas externas a python, requiriendo compilacion
extra, generando un sin fin de archivos sólo para poder ejecutar un sistema realimentado básico.

Target audience for the DiaBloS package
---------------------------------------

Usuarios de python
control, ecuaciones diferenciales, personas enfocadas en el desarrollo de alternativas de programacion visual

System requirements
-------------------

This library requires Python 3.9.7 or later

Background information and Reference Material
---------------------------------------------

Hoy en día se utilizan cada vez más herramientas de software basadas en la programación diagramática visual [citas].
Estas herramientas tienen la ventaja de facilitar al usuario la implementación de modelos de sistemas complejos,
permitiendo visualizar las interacciones entre subcomponentes del sistema.  Ejemplos de estas herramientas pueden
encontrar desde sistemas adoptados por la industria como LabView de National Instruments [],  Simulink de Mathworks [].
Incluso existen herramientas para el desarrollo del pensamiento computacional y habilidades STEM que emplean programas
de programación basados en diagramas de bloques como Lego EV3 [...].  Sin embargo, no existen librerías abiertas para
el desarrollo de este tipo de herramientas.  Tampoco existe una exposición detallada de las metodologías para procesar
diagramas de bloques y ejecutar los modelos que representan, ya que en general los software existentes utilizan
metodologías propietarias.  Por esta razón, la contribución del presente trabajo es el planteamiento de los algoritmos
principales para el procesamiento de diagramas de bloques y el desarrollo de una librería de software abierta para
Python que se pone a disposición de la comunidad para ser empleada tanto como herramienta de cómputo, como base para
el desarrollo de otros sistemas de modelación gráfica basada en diagramas de bloques, así como una herramienta educativa
que puede ser útil en cursos de modelación y simulación de sistemas dinámicos.