from pygame import *
from random import random

mixer.init()
font.init()
size = (700, 500)
game_window = display.set_mode(size)
display.set_caption('Ping-Pong')
events = event.get()
FPS = (60)
kicks = 0
speed_counter = 0
speed_counter2 = 0
p1_lose_counter = 0
p2_lose_counter = 0
#Классы
finish = False
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, image_x, image_y, speed):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image),
            (image_x, image_y)
            )
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
    def reset(self):
        game_window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update_player1(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_s] and self.rect.y <= size[1] - 185:
            self.rect.y += self.speed
        if keys_pressed[K_w] and self.rect.y >= 10:
            self.rect.y -= self.speed
    def update_player2(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_DOWN] and self.rect.y <= size[1] - 185:
            self.rect.y += self.speed
        if keys_pressed[K_UP] and self.rect.y >= 10:
            self.rect.y -= self.speed
class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, image_x, image_y, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, image_x, image_y, 0)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.old_speed_x = speed_x
        self.old_speed_y = speed_y
    def update(self):
        global kicks
        global finish
        global speed_counter
        if kicks == 5:
            kicks = 6
            if speed_counter < 2:
                self.speed_x -= 1
                self.speed_y -= 1
                speed_counter += 1
            if speed_counter >= 4:
                speed_counter = 0
                kicks = 0
                self.speed_x = self.old_speed_x
                self.speed_y = self.old_speed_y
        if kicks == 11:
            kicks = 0
            if speed_counter < 2:
                self.speed_x += 1
                self.speed_y += 1
                speed_counter += 1
            if speed_counter >= 4:
                speed_counter = 0
                self.speed_x = self.old_speed_x
                self.speed_y = self.old_speed_y
        if sprite.collide_rect(self, player1) or sprite.collide_rect(self, player2):
            kick.play()
            kicks += 1
            if abs(self.rect.right - player1.rect.left) < 10 or abs(self.rect.left - player2.rect.right) < 10:
                self.speed_x *= -1
            if abs(self.rect.bottom - player1.rect.top) < 10 or abs(self.rect.bottom - player2.rect.top) < 10:
                self.speed_y *= -1
            if abs(self.rect.top - player1.rect.bottom) < 10 or abs(self.rect.top - player2.rect.bottom) < 10:
                self.speed_y *= -1
            self.speed_x *= -1
            self.speed_y += random()
        if self.rect.y >= 425 or self.rect.y <= 0:
            self.speed_y *= -1
        ping_pong_ball.rect.x += self.speed_x
        ping_pong_ball.rect.y += self.speed_y
#Фоновая музыка и звуки
mixer.music.load('OST.ogg')
mixer.music.set_volume(0.25)
mixer.music.play()
kick = mixer.Sound('kick.ogg')
#Фон и спрайты
background = transform.scale(
        image.load('ping_pong.jpg'),
        (700, 500)
)
font = font.SysFont('Comic Sans MS', 35)
player1 = Player('Рокетка.png', 10, 20, 75, 175, 4)
player2 = Player('Рокетка.png', size[0] - 85, size[1] - 185, 75, 175, 4)
ping_pong_ball = Ball('tennis_ball.jpg', 310, 215, 70, 70, 3, 3)
p_1 = font.render('PLAYER 1', True, (255, 255, 255))
p_2 = font.render('PLAYER 2', True, (255, 255, 255))
#Цикл и флаги
clock = time.Clock()
game = True
time_flag = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    game_window.blit(background, (0, 0))
    game_window.blit(p_1, (10, -5))
    game_window.blit(p_2, (530, -5))
    if not finish:
        player1.reset()
        player1.update_player1()
        player2.reset()
        player2.update_player2()
        ping_pong_ball.reset()
        ping_pong_ball.update()
        p_counters = font.render('P1  P2', True, (255, 0, 0))
        p_numbers = font.render(str(p1_lose_counter) + '    ' + str(p2_lose_counter), True, (255, 0, 0))
        game_window.blit(p_numbers, (315, 455))
        game_window.blit(p_counters, (305, 420))
        if ping_pong_ball.rect.x >= 700 or ping_pong_ball.rect.x <= 0:
            if ping_pong_ball.rect.x >= 700:
                if p1_lose_counter == 2:
                    number = 2
                    game_over = font.render('PLAYER' + ' ' + str(number) + ' ' + 'LOSE!', True, (255, 0, 0))
                    finish = True
                else:
                    p1_lose_counter += 1
                    ping_pong_ball.rect.x = 31
                    ping_pong_ball.rect.y = 21
                    ping_pong_ball.speed_x = 3
                    ping_pong_ball.speed_y = 3
            if ping_pong_ball.rect.x <= 0:
                if p2_lose_counter == 2:
                    number = 1
                    game_over = font.render('PLAYER' + ' ' + str(number) + ' ' + 'LOSE!', True, (255, 0, 0))
                    finish = True
                else:
                    p2_lose_counter += 1
                    ping_pong_ball.rect.x = 310
                    ping_pong_ball.rect.y = 215
                    ping_pong_ball.speed_x = 3
                    ping_pong_ball.speed_y = 3
        if (ping_pong_ball.rect.x >= 525 and ping_pong_ball.rect.x <= 699 and not time_flag) or (ping_pong_ball.rect.x >= 10 and ping_pong_ball.rect.x <= 100 and not time_flag):
            time_flag = True
            start_time = time.get_ticks()
        if ping_pong_ball.rect.x < 530 and ping_pong_ball.rect.x > 105:
            time_flag = False
        if time_flag:
            if start_time - time.get_ticks() < -1000:
                ping_pong_ball.rect.x = 310
                ping_pong_ball.rect.y = 215
                ping_pong_ball.speed_x = 3
                ping_pong_ball.speed_y = 3
        if speed_counter > speed_counter2:
            speed_time = time.get_ticks()
            speed_counter2 = speed_counter
            if speed_time - time.get_ticks() < -500:
                ping_pong_ball.rect.x = 310
                ping_pong_ball.rect.y = 215
                speed_counter = 0
                speed_counter2 = 0
                kicks = 0
    if finish:
        player1.reset()
        player2.reset()
        game_window.blit(game_over, (190, 220))

    display.update()
    clock.tick(FPS)