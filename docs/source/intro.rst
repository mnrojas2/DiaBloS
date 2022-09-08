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

Nowadays, more and more software tools based on visual diagrammatic programming are being used. These tools have the
advantage of facilitating the user the implementation of complex system models, allowing to visualize the interactions
between subcomponents of the system. Examples of these tools can be found from industry-adopted systems such as LabView
from National Instruments or Simulink from Mathworks. There are also tools for the development of computational thinking
and STEM skills that employ programming programs based on block diagrams such as Lego EV3. However, there are no open
libraries for the development of this type of tools, nor is there a detailed exposition of the methodologies for
processing block diagrams and executing the models they represent, since in general the existing software uses
proprietary methodologies. For this reason, the contribution of the present work is the approach of the main algorithms
for the processing of block diagrams and the development of an open software library for Python that is made available
to the community to be used both as a computational tool and as a basis for the development of other graphical modeling
systems based on block diagrams, as well as an educational tool that can be useful in courses of modeling and simulation
of dynamic systems.