Introduction
============

Diablos es una herramienta de programacion de bloques. (Señales)

Esta herramienta se presenta como una alternativa open source dependiente completamente de librerias disponibles en Python y pip.

Este manual está enfocado en mostrar y explicar el uso de la interfaz, como también las bases para poder desarrollar nuevas funciones.

Capabilities of the DiaBloS package
-----------------------------------

Existen librerias de python que se enfocan en esto, pero solo se basan en las conexiones y no la interfaz, como tampoco el poder ejecutarlos.
Tambien otros que requieren el uso de herramientas externas a python, requiriendo compilacion extra, generando un sin fin de archivos sólo para poder ejecutar un sistema realimentado básico.

Target audience for the DiaBloS package
---------------------------------------

Usuarios de python
control, ecuaciones diferenciales, personas enfocadas en el desarrollo de alternativas de programacion visual

System requirements
-------------------

This library requires Python 3.9.7 or later

Background information and Reference Material
---------------------------------------------

Hoy en día se utilizan cada vez más herramientas de software basadas en la programación diagramática visual [citas]. Estas herramientas tienen la ventaja de facilitar al usuario la implementación de modelos de sistemas complejos, permitiendo visualizar las interacciones entre subcomponentes del sistema.  Ejemplos de estas herramientas pueden encontrar desde sistemas adoptados por la industria como LabView de National Instruments [],  Simulink de Mathworks []. Incluso existen herramientas para el desarrollo del pensamiento computacional y habilidades STEM que emplean programas de programación basados en diagramas de bloques como Lego EV3 [...].  Sin embargo, no existen librerías abiertas para el desarrollo de este tipo de herramientas.  Tampoco existe una exposición detallada de las metodologías para procesar diagramas de bloques y ejecutar los modelos que representan, ya que en general los software existentes utilizan metodologías propietarias.  Por esta razón, la contribución del presente trabajo es el planteamiento de los algoritmos principales para el procesamiento de diagramas de bloques y el desarrollo de una librería de software abierta para Python que se pone a disposición de la comunidad para ser empleada tanto como herramienta de cómputo, como base para el desarrollo de otros sistemas de modelación gráfica basada en diagramas de bloques, así como una herramienta educativa que puede ser útil en cursos de modelación y simulación de sistemas dinámicos.