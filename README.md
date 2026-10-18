# Space Invaders - Vibecoding Edition
**Actividad:** Vibecoding Guiado (Semana 2)  
**Proyecto:** Desarrollo de Mini-Juego con IA como Copiloto  
**Lenguaje:** Python 3 (Tkinter)  

---

## 🎯 Objetivo del Proyecto
Aplicar técnicas de **vibecoding** y **prompt engineering** para desarrollar un mini-juego funcional en 2D inspirado en el clásico *Space Invaders*, empleando la IA como copiloto de programación, iterando sobre su comportamiento y validando de manera crítica el código generado.

---

## 🚀 Requisitos de Ejecución
El proyecto fue construido utilizando la librería estándar gráfica de Python (`tkinter`), por lo que **no requiere instalar dependencias externas**.

### Instrucciones para ejecutar:
1. Clonar el repositorio:
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
2. Ejecutar el juego:
   ```bash
   python main.py
   ```

### 🎮 Controles:
* `Flecha Izquierda` / `Flecha Derecha`: Mover la nave lateralmente de manera fluida.
* `Barra Espaciadora`: Disparar láseres (con tiempo de recarga / cooldown).
* `R`: Reiniciar la partida al perder (Game Over).

---

## 🧠 Evidencia de Vibecoding y Prompts Utilizados

### Prompt 1: Generación de la Base Funcional
* **Prompt exacto enviado a la IA:**
  > *"Crea un mini-juego estilo Space Invaders en Python usando únicamente tkinter. La ventana debe ser de 600x700 px con fondo negro. Debe incluir una nave espacialen la parte inferior controlada con las flechas izquierda y derecha, capacidad de disparar láseres hacia arriba con la barra espaciadora, y una formación de 3 filas de alienígenas y naves aliens que se desplacen horizontalmente y bajen un paso al tocar el borde de la pantalla."*
* **Qué se pidió:** La arquitectura elemental de renderizado y el bucle principal de juego mediante`.
* **Justificación / Refinamiento:** Se requirió explícitamente usar `tkinter` para eliminar la necesidad de librerías externas pesadas (como `pygame`), asegurando portabilidad inmediata en cualquier entorno con Python instalado.

---

### Prompt 2: Iteración y Mejora (Jugabilidad y Progresión)
* **Prompt exacto enviado a la IA:**
  > *"Mejora el juego: 1) Agrega un panel superior con puntaje, vidas (iniciando en 3) y número de oleada. 2) Haz que los alienígenas bajen y que las naves aliens disparen proyectiles hacia abajo de manera aleatoria. 3) Si el jugador destruye a todos los alienígenas, genera una nueva oleada con mayor velocidad de desplazamiento. 4) Haz que los aliens (tipo marcianos), naves aliens (tipo platillos) y la nave principal (como el halcon milenario) tengan dichos aspectos"*
* **Qué se pidió:** Implementación de mecánicas de riesgo/recompensa, proyectiles enemigos y escalabilidad de dificultad por oleadas.
* **Por qué se ajustó:** La versión inicial era estática; los enemigos no contraatacaban ni existía un sentido de progreso o reto.

---

### Prompt 3: Depuración, Fluidez de Controles y UX
* **Prompt exacto enviado a la IA:**
  > *"Se detecto un problema: Si la tecla epaciadora se mantiene presionada debe ser  capaz de disparar en rafaga pero agrega un tiempo de enfriamiento de 300ms entre disparos para que no sea una rafaga infinita"*
* **Qué se pidió:** Corrección de la respuesta de entrada del teclado.
* **Por qué se ajustó:** La experiencia de usuario (*feel* de los controles) era deficiente con enlaces de eventos simples.

---

## 🛠️ Iteración y Mejora Destacada
* **Cambio principal:** Desacoplamiento de la captura de eventos del teclado mediante un buffer/set de teclas activas, junto con el control de cadencia de tiro basado en `time.time()`.
* **Impacto visible:** Desplazamiento ultra fluido a ~33 FPS sin micro-interrupciones y balance en el sistema de combate.

---

## 🔍 Validación del Resultado y Pruebas Realizadas

### Metodología de validación:
1. **Prueba de colisión:** Se comprobó que el algoritmo de colisión por caja delimitadora (*Bounding Box*) eliminara con precisión al alienígena impactado y removiera el proyectil del jugador en el mismo tick.
2. **Prueba de daño y vidas:** Se permitió deliberadamente el impacto de proyectiles enemigos para verificar el decremento secuencial de vidas de 3 a 0 y la posterior activación del estado *Game Over*.
3. **Prueba de avance de oleada:** Al vaciar la matriz de invasores, se verificó el incremento del contador de oleada, la bonificación de +50 puntos y el aumento del multiplicador de velocidad horizontal.
4. **Prueba de reinicio rápido:** Tras el *Game Over*, al pulsar 'R' se validó el vaciado del canvas, la limpieza de listas de proyectiles y el reinicio de contadores a su estado por defecto.

### Error o limitación identificada y corregida:
* **Fallo:** En las primeras pruebas, las listas en memoria de `balas_jugador` y `balas_enemigas` crecían indefinidamente fuera de los bordes de la pantalla, lo que a largo plazo degradaba el rendimiento por acumulación de elementos no visibles.
* **Solución aplicada:** Se implementaron filtros por comprensión de listas      liberando memoria en cada cuadro.

---

## 📝 Reflexión Final

### 1. ¿Qué se aprendió usando la IA como copiloto?
El desarrollo mediante *vibecoding* demostró que la productividad aumenta exponencialmente al delegar la escritura de código repetitivo (configuración de canvas, geometrías y bucles `after()`), permitiendo enfocar el tiempo y criterio en la arquitectura lógica, la experiencia de usuario y la depuración de casos límite.

### 2. Ventajas y límites del Vibecoding:
* **Ventajas:** Rapidez para pasar de una idea abstracta a un ejecutable funcional en minutos; facilidad para solicitar refactorizaciones y paletas visuales modernas sin fricción.
* **Límites:** La IA no siempre anticipa la latencia de entrada de hardware ni optimiza la recolección de basura por cuenta propia si no se le instruye con precisión técnica.

### 3. Comprensión del código y áreas a reforzar:
* **Comprendido con solidez:** Arquitectura orientada a objetos (POO) en Python, gestión de eventos asíncronos en entornos GUI, manipulación de listas mutables y matemáticas vectoriales para detección de colisiones 2D.
* **Áreas a reforzar:** Implementación de audio procedural nativo y optimización avanzada de renderizado con doble búfer.
