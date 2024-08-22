import pygame
import random
import math
from pygame import mixer  # Para trabajar con sonidos.


# Inicializar Pygame.
pygame.init()


# Crear pantalla.
pantalla = pygame.display.set_mode((800, 600))


# Título e Icono.
pygame.display.set_caption('Space Invaders')
icono = pygame.image.load('imagenes/ovni.png')  # Para los iconos he recurrido a Flaticon (recomendado).
pygame.display.set_icon(icono)
fondo = pygame.image.load('imagenes/fondo.png')


# Agregar música.
mixer.music.load('sonidos/MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)  # -1 para que suene en loop.


# Variables del jugador.
img_jugador = pygame.image.load('imagenes/astronave.png')
jugador_x = 360  # Eje x, es 800/2-40 (la mitad de su dimensión) para que esté centrado.
jugador_y = 550  # Eje y, 600-40 para que esté en el suelo, un poco más para que se eleve ligeramente.
jugador_x_cambio = 0  # El valor de posición modificado por el juego. Se modificará dinámicamente en el loop.


# Variables de BTC.
img_btc = []
btc_x = []
btc_y = []
btc_x_cambio = []
btc_y_cambio = []
cantidad_enemigos = 8
# Cuando se ejecuta el programa se generan las listas vacias, luego con el loop las recorremos tantas veces como
# enemigos tenemos para crearlos, en cada vuelta se crean 8 índices para cada variable.
for e in range(cantidad_enemigos):
    img_btc.append(pygame.image.load('imagenes/bitcoin.png'))
    btc_x.append(random.randint(0, 752))  # Eje x
    btc_y.append(random.randint(50, 150))  # Eje y
    btc_x_cambio.append(0.5)  # Velocidad de movimiento inicial.
    btc_y_cambio.append(50)  # 50 píxeles.


# Variables de la bala.
balas = []  # Lo utilizaremos para lanzar varias balas.
img_bala = pygame.image.load('imagenes/bala.png')
bala_x = 0
bala_y = 550
bala_x_cambio = 0
bala_y_cambio = 0.1
bala_visible = False


# Puntuación.
puntuacion = 0
fuente = pygame.font.Font('fuentes/space_age.ttf', 32)  # Extraida de 1001freefonts, guardarla dentro de la carpeta
# que contiene todos los archivos.
texto_x = 10
texto_y = 10


# Texto final de juego.
fuente_final = pygame.font.Font('fuentes/space_age.ttf', 40)


def texto_final():
    mi_fuente_final = fuente_final.render('JUEGO TERMINADO', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (140, 200))  # Centro de la pantalla.


# Función mostrar puntuación.
def mostrar_puntuacion(x, y):
    texto = fuente.render(f'Puntuación: {puntuacion}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Función jugador.
def jugador(x, y): # Estos parámetros son para que reciba valores que van cambiando.
    pantalla.blit(img_jugador, (x, y)) # blit es arrojar.


# Función BTC.
def btc(x, y, ene):  # Estos parámetros son para que reciba los valores los cuales van cambiando.
    pantalla.blit(img_btc[ene], (x, y))  # blit lo usamos para mostrar (arrojar).


# Función disparar bala.
def disparar_bala(x, y):
    global bala_visible  # Necesitamos que la variable sea global para acceder a bala_visible desde esta función.
    bala_visible = True  # Cuando accedamos a ella se podrá ver.
    pantalla.blit(img_bala, (x + 16, y + 10))  # Para que aparezca en medio de la nave.


# Función detectar colisiones.
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))  # Fórmula de la distancia
    # entre dos objetos.
    if distancia < 27:  # Aquí ha habido colisión.
        return True
    else:
        return False


# Loop del juego.
se_ejecuta = True
while se_ejecuta:
    # Repasamos todos los eventos que suceden dentro del juego y si se ejecuta QUIT entonces se_ejecuta será False.
    # Imagen de fondo.
    # Pantalla, lo primero que mostraremos, lo sacamos del bucle for para que así sea.
    pantalla.blit(fondo, (0, 0))  # Coordenadas 0, 0 porque queremos que ocupe toda la pantalla.

    # Iterar eventos.
    for evento in pygame.event.get():
        # Evento cerrar.
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # Evento presionar teclas.
        if evento.type == pygame.KEYDOWN:  # KEYDOWN es tecla presionada. Si el usuario suelta la tecla es
            # el evento KEYUP.
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('sonidos/Disparo.mp3')
                sonido_bala.set_volume(0.1)
                sonido_bala.play()
                nueva_bala = {
                    'x': jugador_x,
                    'y': jugador_y,
                    'velocidad': -1
                }
                balas.append(nueva_bala)

        # Evento soltar flechas.
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0


    # Modificar ubicación del jugador.
    jugador_x += jugador_x_cambio  # Hacemos que antes de que se muestre a jugador_x se modifiquen sus valores
    # de acuerdo a los parámetros lógicos que hemos establecido.


    # Mantener dentro de bordes al jugador.
    if jugador_x <= 0:  # Cada vez que quiera atravesar la barrera reestablecemos el valor para que no lo haga.
        jugador_x = 0
    elif jugador_x >= 760:  # 800-40 para que no atraviese el borde derecho.
        jugador_x = 760


    # Modificar ubicación del BTC.
    for e in range(cantidad_enemigos):

        # Fin del juego:
        if btc_y[e] > 500:
            for k in range(cantidad_enemigos):
                # Los mandamos debajo de la pantalla generando la ilusión de que desaparecieron.
                btc_y[k] = 1000  # Nuestra pantalla tiene 600.
            texto_final()
            break

        btc_x[e] += btc_x_cambio[e] # En cada una de las variables de BTC agregamos el índice [e], el índice en
        # el que se encuentra en cada una de las iteraciones.


    # Mantener dentro de bordes al BTC.
        if btc_x[e] <= 0:  # Cambiará de dirección al llegar al borde.
            btc_x_cambio[e] = 0.5
            btc_y[e] += btc_y_cambio[e]
        elif btc_x[e] >= 752:
            btc_x_cambio[e] = -0.5
            btc_y[e] += btc_y_cambio[e]

        # Colisión.
        for bala in balas:
            colision_bala_enemigo = hay_colision(btc_x[e], btc_y[e], bala['x'], bala['y'])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('sonidos/Golpe.mp3')
                sonido_colision.set_volume(0.1)
                sonido_colision.play()
                balas.remove(bala)
                puntuacion += 1
                # Cuando le damos a BTC aparece en otro lugar.
                btc_x[e] = random.randint(0, 752)  # Eje x
                btc_y[e] = random.randint(50, 150)  # Eje y

        btc(btc_x[e], btc_y[e], e)

    # Movimiento bala.
    for bala in balas:
        bala['y'] += bala['velocidad']
        pantalla.blit(img_bala, (bala['x'] + 12, bala['y'] + 10))
        if bala['y'] < 0:
            balas.remove(bala)


    jugador(jugador_x, jugador_y)
    mostrar_puntuacion(texto_x, texto_y)


    # Actualizar
    pygame.display.update()
