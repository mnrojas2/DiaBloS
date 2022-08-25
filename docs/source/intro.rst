Introduction
============

Diablos es una herramienta de programacion de bloques. (Señales)

Esta herramienta se presenta como una alternativa open source independiente de software o librerias externas a Python,
todos los paquetes necesarios ya los provee Python o pip.

Este manual está dedicado a explicar las aplicaciones básicas al usuario, como también explicar el proceso algoritmico
del mismo, de forma que sirva como base para la mantención de este paquete, como la creación de nuevas funciones.

Capabilities of the DiaBloS package
-----------------------------------

DiaBloS es capaz de:

-relacionar funciones y obtener resultados
-integrar y derivar señales
-Producir respuestas al escalon como a la rampa para sistemas de ecuaciones de diferencia (diferenciales) ordinarias
-Ejemplificar con sistemas de control realimnetado
-graficar señales, tanto de forma tradicional como de forma dinámica
-exportar datos en formato .npz
-cargar y guardar archivos de datos con las conexiones
-trabajar vectorialmente los valores
-asociar y disasociar señales en forma de vectores

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