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

Python by itself does not provide a library to visually simulate dynamic system models, nor does it offer a visual
programming alternative to paid software, such as Simulink from Mathworks.

There are Python libraries created by the open source community that allow modeling interconnected dynamic systems,
such as SimuPy, as well as others that provide an interface to analyze models created and used by external programs,
such as PySimulator. However, none of these can produce these dynamic models visually, requiring direct
programming, or the use of external software to create these systems (like OpenModellica Simulator), and then
simulate in a Python environment.

DiaBloS provides a library that does not depend on external software for the simulation of dynamic systems, and provides
the necessary tools to be able to create dynamic systems, simulate and obtain graphs of their behavior over time,
without requiring major programming.

The package currently offers the following functionalities:

#. Interconnect functions to create more complex systems.

#. Integrate and derivate signals.

#. Produce step responses, such as ramp responses, for systems of ordinary difference (differential) equations.

#. Generate signals with Gaussian distribution noise.

#. Create feedback systems.

#. Plot signals, both traditionally and dynamically (in active simulation time).

#. Export signal data in .npz format.

#. Save and load created block systems in files formated as .dat.

#. Vector data handling.

#. Route multiple signals into a single output vector and vice versa (multiplexing).


Target audience for the DiaBloS package
---------------------------------------

DiaBloS is intended for mathematicians, physicists and practicing engineers. It is a tool designed to help students
understand processes associated with modeling dynamic systems, observe their physical behavior over time, as well as
develop solutions for control systems, visually, without the need to have a full understanding of how to code these
systems first.


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