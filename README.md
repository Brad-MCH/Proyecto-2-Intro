## Documentación

### Tabla de Contenidos

1. [Introducción](#1-introducción)  
2. [Descripción del Problema](#2-descripción-del-problema)  
3. [Análisis de Resultados](#3-análisis-de-resultados)  
4. [Dificultades Encontradas](#4-dificultades-encontradas)  
5. [Bitácora de Actividades](#5-bitácora-de-actividades)  
6. [Estadística de Tiempos](#6-estadística-de-tiempos)  
7. [Conclusión](#7-conclusión)  
8. [Literatura o Fuentes Consultadas](#8-literatura-o-fuentes-consultadas)  
9. [Opinión de los Creadores del Juego](#9-opinión-de-los-creadores-del-juego) 

---

### 1. Introducción

Este proyecto consiste en el desarrollo de un videojuego estilo dungeon en pixel art llamado **Dungeonfall**, diseñado como parte del curso de *Introducción a la Programación* en el Tecnológico de Costa Rica.  
El objetivo principal fue aplicar los conocimientos adquiridos en programación, diseño de interfaces gráficas y lógica de juego utilizando Python y la librería `pygame`.  

---

### 2. Descripción del Problema

El problema planteado consistía en desarrollar una aplicación interactiva que integrara múltiples conceptos vistos durante el curso, tales como estructuras de datos, manejo de archivos, control de flujo, programación orientada a objetos y trabajo con interfaces gráficas.  
El reto adicional era diseñar un sistema jugable y funcional que simulara un entorno con enemigos, armas, niveles, lógica de daño, y una interfaz amigable.  

---

### 3. Análisis de Resultados

El juego final incluye un sistema de selección de personajes, movimiento libre en un mapa con obstáculos, enemigos con IA simple, efectos visuales, ataques, sistema de explosiones y daño, uso de pociones, y avance de niveles.  
Además, se implementó un sistema de puntuación que se guarda en un archivo `scores.txt` y se muestra al final del juego como una *leaderboard*.  
En términos de funcionamiento, el juego es estable y jugable en su totalidad.

---

### 4. Dificultades Encontradas

Durante el desarrollo surgieron varios retos clave:

- **Sincronización de estados del juego** (menú, pausa, juego, gane, derrota), lo cual requirió una arquitectura clara.
- **Control del score**, evitando duplicaciones al guardar y errores al mostrar el leaderboard.
- **Manejo de colisiones** entre el jugador, enemigos, y explosiones.
- **Diseño visual completo en pygame**, sin depender de interfaces externas como `tkinter`.
- **Depuración de errores con múltiples sprites y animaciones**, especialmente en interacciones entre bombas y enemigos.

Cada obstáculo se resolvió aplicando pruebas, impresión de estados (`print()`), simplificación de lógica, y modularización del código.

---

### 5. Bitácora de Actividades

| Días | Actividad | Detalles |
|-----|-----------|----------|
| 1 | Creación del entorno de desarrollo | Instalación de pygame, creación de archivos base |
| 2-3 | Implementación del mapa | Carga de mapas desde CSV, diseño de tiles |
| 4-6 | Movimiento del jugador y colisiones | Rectángulos de colisión, animaciones |
| 7-8 | Enemigos y ataque básico | Sprites de enemigos, sistema de daño |
| 9-11 | Sistema de bombas y explosiones | Explosión en cruz, daño en área, animación |
| 12 | Interfaces y menú | Pantallas de inicio, pausa y final |
| 13 | Leaderboard | Entrada de nombre, guardado de puntaje, lectura de `scores.txt` |
| 14 | Pruebas finales y correcciones | Ajuste de bugs y estética visual |

---

### 6. Estadística de Tiempos

| Tipo de Actividad | Tiempo Estimado (hrs) |
|-------------------|------------------------|
| Programación y lógica del juego | 22 h |
| Diseño gráfico y animaciones | 6 h |
| Pruebas y depuración | 5 h |
| Documentación y presentación | 3 h |
| **Total Aproximado** | **36 h** |

---

### 7. Conclusión

El desarrollo de **Dungeonfall** permitió aplicar múltiples conceptos clave de programación en un entorno práctico y creativo.  
A través del proyecto se reforzaron habilidades como la organización del código, el pensamiento algorítmico, la resolución de errores y la integración de componentes visuales e interactivos.  
El resultado final es un juego funcional, estable y entretenido, que demuestra la capacidad adquirida para construir proyectos integrales usando Python.

---

### 8. Literatura o Fuentes Consultadas

- [Documentación de pygame](https://www.pygame.org/docs/)
- Foros de Stack Overflow
- Videos tutoriales de YouTube sobre diseño de videojuegos en Python
- Imágenes y sprites obtenidos de OpenGameArt y itch.io


### 9. Opinión de los Creadores del Juego

> *"Nos sentimos emocionados durante el desarrollo de este proyecto. Era una experiencia completamente nueva y resultó muy gratificante trabajar en ella.  
Aunque nos hubiese gustado contar con más tiempo para pulir detalles y mejorar ciertos aspectos técnicos y visuales, estamos satisfechos con el resultado final.  
Fue una experiencia divertida, desafiante y muy enriquecedora."*
