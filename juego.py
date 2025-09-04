import pygame, sys, random, math

# --- Configuración ---
pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Una aventura geometrica")

# Colores
LILA = (200, 162, 200)
BLANCO = (255, 255, 255)
ROJO = (220, 70, 70)
MORADO = (148, 0, 211)
GRIS = (30, 30, 30)
NEGRO = (0, 0, 0)

# Jugador
jugador_pos = [ANCHO//2, ALTO//2]
velocidad = 4
radio = 12
dibujando = True
paused = False

# Superficie para guardar el dibujo
canvas = pygame.Surface((ANCHO, ALTO))
canvas.fill(LILA)

# Fuente
FUENTE = pygame.font.SysFont("consolas", 26)

# Estados
MENU = "MENU"
JUGANDO = "JUGANDO"
GAME_OVER = "GAME_OVER"
GANASTE = "GANASTE"
estado = MENU
modo_libre = False

# Enemigos
class Enemigo:
    def __init__(self):
        self.r = 15
        self.x = random.randint(self.r, ANCHO-self.r)
        self.y = random.randint(self.r, ALTO-self.r)
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])
    def mover(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < self.r or self.x > ANCHO-self.r: self.vx *= -1
        if self.y < self.r or self.y > ALTO-self.r: self.vy *= -1
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, ROJO, (int(self.x), int(self.y)), self.r)

enemigos = []

# --- Funciones ---
def colision(a, b, r1, r2):
    return math.hypot(a[0]-b[0], a[1]-b[1]) < (r1 + r2)

def mostrar_menu():
    ventana.fill(LILA)
    titulo = FUENTE.render("UNA AVENTURA GEOMETRICA", True, NEGRO)
    opciones = [
        "1 - Triángulo",
        "2 - Cuadrado",
        "3 - Círculo",
        "ESPACIO - Dibujo Libre",
        "ESC - Salir"
    ]
    ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 60))
    y = 160
    for op in opciones:
        txt = FUENTE.render(op, True, NEGRO)
        ventana.blit(txt, (ANCHO//2 - txt.get_width()//2, y))
        y += 44
    nota = FUENTE.render("Presiona ENTER para pausar la figura automatica", True, NEGRO)
    ventana.blit(nota, (ANCHO//2 - nota.get_width()//2, ALTO-80))
    pygame.display.flip()

def crear_ruta_figura(nombre):
    cx, cy = ANCHO//2, ALTO//2
    if nombre == "TRIANGULO":
        return [(cx, cy-100), (cx-100, cy+80), (cx+100, cy+80), (cx, cy-100)]
    if nombre == "CUADRADO":
        return [(cx-100, cy-100), (cx+100, cy-100), (cx+100, cy+100), (cx-100, cy+100), (cx-100, cy-100)]
    if nombre == "CIRCULO":
        pasos = 60
        pts = []
        for i in range(pasos):
            a = 2*math.pi*i/pasos
            pts.append((cx + int(100*math.cos(a)), cy + int(100*math.sin(a))))
        pts.append((cx+100, cy))
        return pts
    return []

# Loop principal
clock = pygame.time.Clock()
ruta = []
idx = 0
last_enemy_spawn = 0 

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        #  MENU: iniciar 
        if estado == MENU and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if e.key == pygame.K_SPACE:
                # dibujo libre
                canvas.fill(LILA)
                enemigos = [Enemigo() for _ in range(3)]
                modo_libre = True
                estado = JUGANDO
                jugador_pos = [ANCHO//2, ALTO//2]
                dibujando = True
                paused = False
                idx = 0; ruta = []
                last_enemy_spawn = pygame.time.get_ticks()
            if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                opciones = {pygame.K_1: "TRIANGULO", pygame.K_2: "CUADRADO", pygame.K_3: "CIRCULO"}
                forma = opciones[e.key]
                ruta = crear_ruta_figura(forma)
                idx = 0
                canvas.fill(LILA)
                enemigos = [Enemigo() for _ in range(3)]
                modo_libre = False
                estado = JUGANDO
                jugador_pos = list(ruta[0]) if ruta else [ANCHO//2, ALTO//2]
                dibujando = True
                paused = False

        #  JUGANDO: ENTER 
        if estado == JUGANDO and e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                dibujando = not dibujando
                if not modo_libre:
                    paused = not paused

        #  GAME OVER / GANASTE 
        if estado in (GANASTE, GAME_OVER) and e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                estado = MENU
                canvas.fill(LILA)
                ruta = []; idx = 0
                enemigos = []

    # MENÚ 
    if estado == MENU:
        mostrar_menu()
        clock.tick(30)
        continue

    # JUGANDO 
    if estado == JUGANDO:
        if modo_libre:
            teclas = pygame.key.get_pressed()
            antes = jugador_pos.copy()
            if teclas[pygame.K_LEFT]:  jugador_pos[0] -= velocidad
            if teclas[pygame.K_RIGHT]: jugador_pos[0] += velocidad
            if teclas[pygame.K_UP]:    jugador_pos[1] -= velocidad
            if teclas[pygame.K_DOWN]:  jugador_pos[1] += velocidad
            jugador_pos[0] = max(0, min(ANCHO-1, jugador_pos[0]))
            jugador_pos[1] = max(0, min(ALTO-1, jugador_pos[1]))
            if dibujando and antes != jugador_pos:
                pygame.draw.line(canvas, MORADO, (int(antes[0]), int(antes[1])), (int(jugador_pos[0]), int(jugador_pos[1])), 3)

            # spawn de enemigos cada 10 segundos
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - last_enemy_spawn >= 10000:  
                enemigos.append(Enemigo())
                last_enemy_spawn = tiempo_actual

        else:
            # seguir ruta automática
            if not paused:
                if idx < len(ruta) - 1:
                    antes = jugador_pos.copy()
                    siguiente = ruta[idx+1]
                    dx = siguiente[0] - jugador_pos[0]
                    dy = siguiente[1] - jugador_pos[1]
                    dist = math.hypot(dx, dy)
                    paso = 4
                    if dist <= paso:
                        jugador_pos = [siguiente[0], siguiente[1]]
                        idx += 1
                    else:
                        jugador_pos[0] += dx/dist * paso
                        jugador_pos[1] += dy/dist * paso
                    if dibujando:
                        pygame.draw.line(canvas, MORADO, (int(antes[0]), int(antes[1])), (int(jugador_pos[0]), int(jugador_pos[1])), 3)
                else:
                    estado = GANASTE

        # enemigos
        if estado == JUGANDO:
            for enemigo in enemigos:
                enemigo.mover()
                if colision(jugador_pos, (enemigo.x, enemigo.y), radio, enemigo.r):
                    estado = GAME_OVER

        # dibujar
        ventana.blit(canvas, (0,0))
        pygame.draw.rect(ventana, GRIS, (0,0,ANCHO,36))
        estado_txt = "LIBRE" if modo_libre else "FIGURA"
        dib_txt = "ON" if dibujando else "OFF"
        pausa_txt = "PAUSADO" if (not modo_libre and paused) else ""
        info = f"Modo: {estado_txt}   Dibujando: {dib_txt}   {pausa_txt}   Enemigos: {len(enemigos)}"
        ventana.blit(FUENTE.render(info, True, BLANCO), (8, 6))
        pygame.draw.circle(ventana, BLANCO, (int(jugador_pos[0]), int(jugador_pos[1])), radio)
        for enemigo in enemigos: enemigo.dibujar(ventana)
        pygame.display.flip()

    elif estado == GAME_OVER:
        ventana.fill(LILA)
        txt = FUENTE.render("¡PERDISTE:(! Presiona ENTER para volver al menú", True, NEGRO)
        ventana.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - txt.get_height()//2))
        pygame.display.flip()

    elif estado == GANASTE:
        ventana.blit(canvas, (0,0))
        txt = FUENTE.render("¡ERES EL MEJOR! Presiona ENTER para volver al menú", True, NEGRO)
        ventana.blit(txt, (ANCHO//2 - txt.get_width()//2, 30))
        pygame.display.flip()

    clock.tick(60)
