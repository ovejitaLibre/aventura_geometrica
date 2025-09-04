# aventura_geometrica
Juega mientras aprendes.

Un minijuego creado con PyGame donde un circulo puede dibujar figuras geométricas o moverse en modo dibujo libre, mientras evita enemigos que se mueven por la pantalla.

# Características

- Menú inicial para elegir:
  - Dibujar Triángulo
  - Dibujar Cuadrado
  - Dibujar Círculo
  - Dibujo libre (controlado por el jugador con las flechas)
- En modo libre, cada 10 segundos aparece un nuevo enemigo.
- Opción de **activar/desactivar dibujo** con la tecla `ENTER`.
- En modo automático, se puede pausar y reanudar con `ENTER`.esto con el fin de que el jugador, pueda pausar el circulo para evitar chocar con el enemigo.
- Si el circulo blanco choca con un enemigo → **PERDISTE**.
- Si termina de dibujar una figura → **¡ERES EL MEJOR**.

#Controles

- `← ↑ ↓ →` : Mover al circulo.
- `ENTER` : Alternar entre **dibujar / no dibujar**.  
  - En modo libre: activa o desactiva el trazo.  
  - En modo figura: pausa o reanuda el dibujo automático.
- `ESPACIO` : En el menú, inicia **dibujo libre**.
- `1` : En el menú, dibujar un **Triángulo**.
- `2` : En el menú, dibujar un **Cuadrado**.
- `3` : En el menú, dibujar un **Círculo**.
- `ESC` : Salir del juego.

#Requisitos

- Python 3.8 o superior
- [PyGame](https://www.pygame.org/)  

Instalación de PyGame:
```bash
pip install pygame
