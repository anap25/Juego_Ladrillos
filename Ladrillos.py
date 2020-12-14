import sys, pygame
import time #usamos para pausar, sleep()

pygame.init()

width = 800
height = 600
size = (width,height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ladrillos")

#Monitoreamos el tiempo del juego
clock = pygame.time.Clock()

#Ajustamos la repeticion del evento de la tecla presionada
#genera el movimiento continuo con una presion de la tecla
pygame.key.set_repeat(30) #milisegundos en cada repeticion

#colores
black = (0,0,0)
white = (255,255,255)


#La bolita es un obj y los objs en pygame se los reconoce como sprite
class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bolita.png")
        #obtener rectangulo de la imagen
        self.rect = self.image.get_rect() #para calcular donde poner el objeto
        #Propiedades rect.centerx
        self.rect.centerx = width/2
        #self.rect.centery = height/2
        #Velocidad inicial
        self.speed = [3,3] #indica la cantidad de pixeles que se moveran en x e y

    def movimiento(self): #mueve la pelota a su nueva posicion
        #mueve al elemento a una posicion, esta posicion es el resultado de su posicion actual + lo que le pasamos por parametro(speed), 
        self.rect.move_ip(self.speed)
        #Evitar que salga por debajo (self.rect.bottom >= height or )
        """ if self.rect.top <= 0:
            self.speed[1] = -self.speed[1] """
        if self.rect.right >= width or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargamos imagen
        self.image = pygame.image.load('paleta.png')
        #obtener rectangulo de la imagen
        self.rect = self.image.get_rect() #para calc donde poner el objeto
        #Posicion inicial centrada en x(se movera horizontalmente)
        self.rect.midbottom = (width/2, height - 20)
        #self.rect.centerx = width/2 #lo posiciona al medio
        #Velocidad inicial
        self.speed = [0,0]
        
    def update(self,evento):
        #Buscar si se presiono flecha izquierda o derecha
        if evento.key == pygame.K_LEFT and self.rect.left > 7:
            self.speed = [-7,0]
        elif evento.key == pygame.K_RIGHT and self.rect.right < size[0]-7:
            self.speed = [7,0]
        else:
            self.speed = [0,0]

        self.rect.move_ip(self.speed)


class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ladrillo.png').convert()
        #obtener rectangulo de la imagen
        self.rect = self.image.get_rect() #para calc donde poner el objeto
        #posicion inicial provista externamente
        self.rect.topleft = posicion


class Muro(pygame.sprite.Group):
    def __init__(self,cantLadrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20

        for i in range(cantLadrillos):
            ladrillo = Ladrillo((pos_x,pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width

            #Para colocar los ladrillos en distintas lineas, controlamos que el ladrillo llegue al ancho
            if pos_x >= width:
                pos_x = 0
                pos_y += ladrillo.rect.height


def GameOver():
    #Definimos la fuente
    fuente = pygame.font.SysFont("kristen itc",72)
    #Creamos el texto que vamos a mostrar a partir de la fuente
    text = fuente.render('Game Over', True, white) #Al tener false se mostrara un poco pixelado
    #ubicacion del texto para poder posicionarlo
    text_rect = text.get_rect()
    text_rect.center = [width/2, height/2]
    #dibujamos el texto en la pantalla
    screen.blit(text,text_rect)
    #actualizamos pantalla
    pygame.display.flip()
    #cargamos el sonido
    pygame.mixer.music.load("game_over.mp3")
    #reproducimos el sonido
    pygame.mixer.music.play()
    #antes de salir pausamos por tres segundo
    time.sleep(3)
    #Salimos
    sys.exit()

def mostrarScore():
    fuente = pygame.font.SysFont("serif",20)
    #puntuacion un ancho fijo con 4 ceros(zfill)
    text = fuente.render('Score '+str(score).zfill(4), True,white)
    text_rect = text.get_rect()
    text_rect.topleft = [0,0] 
    screen.blit(text,text_rect)


def mostrarVidas():
    fuente = pygame.font.SysFont("serif",20)
    #puntuacion un ancho fijo con 2 ceros
    text = fuente.render('Vidas '+str(vidas).zfill(2), True,white)
    text_rect = text.get_rect()
    text_rect.topright = [width,0]
    screen.blit(text,text_rect)



ball = Bolita()
player = Player()
muro = Muro(150)
score = 0
vidas = 3
comenzar = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        #Buscamos eventos del teclado
        if event.type == pygame.KEYDOWN:
            player.update(event)
            if comenzar == True and event.key == pygame.K_SPACE: #Si la pelota está en la paleta y además el jugador presiona la tecla de espacio
                comenzar = False
                if ball.rect.centerx < (width/2): #Si está del lado izq
                    ball.speed = [3, -3] #sale hacia la derecha
                else:
                    ball.speed = [-3,-3] #Sale hacia el lado izq


    screen.fill((0,0,0)) #actualizacion de la pantalla, para que no quede rastro de la imagen
    #Si comenzar es falso, es decir, la pelota no está esperando para ser lanzada, actualizamos su moviemiento.
    if comenzar == False:
        ball.movimiento()
    else:
        #para que la pelota empiece en la paleta
        ball.rect.midbottom = player.rect.midtop  

    #Colision entre pelota y jugador
    if pygame.sprite.collide_rect(ball,player):
        ball.speed[1] = -ball.speed[1] #Se invierte en y, ya que solo viene hacia abajo y la debemos mandar para arriba
    
    #Colision entre muro y pelota
    #pygame.sprite.spritecollide(ball,muro,True) El booleano del ultimo indica si deben ser destruidos o no  
    list_impactados = pygame.sprite.spritecollide(ball,muro,False) #Lo dejamos en false, controlamos que elimine de a uno y la pelota cambie de direccion
    if list_impactados:
        ladrillo = list_impactados[0] #Sólo eliminará el primero con el que colisiona

        #Analizamos en q sector tocó la pelota al ladrillo
        cx = ball.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            #Si el centro esta fuera de los lados, invertimos la pelota en x
            ball.speed[0] *= -1
        else:
            ball.speed[1] *= -1

        muro.remove(ladrillo)
        score += 10

    #Revisamos si la pelota sale de la pantalla(por debajo)
    if ball.rect.top > height:
        vidas -= 1
        comenzar = True
   
    
    #Dibujamos los objetos en pantalla
    screen.blit(ball.image,ball.rect) #Dibuja sobre la pantalla la imagen de la bolita en las coordenadas que traera ese objeto
    screen.blit(player.image,player.rect)
    muro.draw(screen)
    mostrarScore()
    mostrarVidas()
    
    pygame.display.flip()
    clock.tick(80) #FPS, nuestro juego correrá a 80 veces por seg como max

    #Antes de que termine el ciclo, controlamos si tiene vidas para poder seguir jugando
    if vidas <= 0:  
        GameOver()