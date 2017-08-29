# MIT License

# Copyright (c) [2017] [Zachary A. Eckstein]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#Created by Zoro#
#Over-commenting in order to make a map for my future self


import pygame
from pygame.locals import *
import random
import time


pygame.init()

#load sprites
head_sprite = pygame.image.load('snekHead.png')
apple_image = pygame.image.load('apple.png')
body_segment = pygame.image.load('bodysegment.png')
tail_segment = pygame.image.load('tail.png')

#color definitions because this is what people do i guess
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
pink = (255,192,203)
yellow = (255,255,0)
orange = (255,127,80)

#default settings
display_width = 1000
display_height = 800
play_field_width = 800
play_field_height = 800
scale = 40
font_size = 35

#The Game
class Main(object):

    def __init__(self):
        self.done = False
        self.game_over = False
        self.FPS = 10
        self.start = True
        self.color = white
        self.difficulty = 0
        
        #change window dressing
        pygame.display.set_caption('Snek')
        pygame.display.set_icon(apple_image)

        #shorten clock reference
        clock = pygame.time.Clock()

        #make screen
        screen_size = (display_width, display_height)
        game_display = pygame.display.set_mode(screen_size)

        #construct objects
        my_snake = Snake()
        food = Apple()
        play_pen = Gameboard()

        #Rewrite the message to screen functions to make more sense...
        def text_object(text, color, size_of_font = font_size):
        	font = pygame.font.SysFont(None, size_of_font)
        	text_surface = font.render(text, True, color)
        	return text_surface, text_surface.get_rect()

        def message(msg, color, y_diplace = 0, size_of_font = font_size):
            font = pygame.font.SysFont(None, size_of_font)
            text_surface, text_rect = text_object(msg, color, size_of_font)
            text_rect.center = (play_field_width/2), ((play_field_height/2)+y_diplace)
            game_display.blit(text_surface,text_rect)


        #score tracker
        def your_score(score, color, size_of_font = font_size):
            font = pygame.font.SysFont(None, size_of_font)
            screen_number = font.render("Score: " + str(score),True,color)
            game_display.blit(screen_number, [play_field_width, 0])

        #Main game loop
        while not self.done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     self.done = True

            #game over loop to restart game
            while self.game_over == True:
                game_display.fill(white)
                play_pen.draw(game_display)
                your_score(my_snake.score,black)
                message("Game Over", red, -100, 150)
                message("You scored " + str(my_snake.score) + "!", white, -30, 80)
                message("Press C to continue or ESC to Quit.", white, 10, 50)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                        self.game_over = False
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.done = True
                            self.game_over = False
                        if event.key == pygame.K_c:
                            Main()

            #opening menu screen
            while self.start == True:
                game_display.fill(white)
                play_pen.draw(game_display)
                your_score(my_snake.score,black)
                message("Select Your Difficulty:",self.color, -100, 100)
                message("Press 1 for Easy",green, -40, 60)
                message("Press 2 for Medium",yellow, 00, 60)
                message("Press 3 for Hard",orange, 40, 60)
                message("Press 4 for VERY HARD",red, 80, 60)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.done = True
                        self.game_over = False
                        self.start = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.FPS = 3
                            self.start = False
                        if event.key == pygame.K_2:
                            self.FPS = 10
                            self.start = False
                        if event.key == pygame.K_3:
                            self.FPS = 15
                            self.start = False
                        if event.key == pygame.K_4:
                            self.FPS = 5
                            self.start = False
                            self.difficulty = 1
                        if event.key == pygame.K_ESCAPE:
                        	self.done = True
                        	self.game_over = False
                        	self.start = False
   

            #draw stuff to invisible place
            game_display.fill(white)
            play_pen.draw(game_display)
            food.draw(game_display)
            my_snake.update()

            #wall crash detection
            if my_snake.x >= play_field_width or my_snake.x < 0 or my_snake.y < 0 or my_snake.y >= play_field_height:
                self.game_over = True
            else: 
                my_snake.draw(game_display, my_snake.body)

                #self crash
                for bodypart in my_snake.body[:-1]:
                    if bodypart == my_snake.head:
                        self.game_over = True


                #on eat: make new food location and grow snake longer
                if my_snake.x == food.x and my_snake.y == food.y:
                    food.update()

                    for bodypart in my_snake.body:
                        if bodypart[0] == food.x and bodypart[1] == food.y:
                            food.update()
                    else:
                        my_snake.grow()
                        self.FPS += self.difficulty


            #Score tracker updater
            your_score(my_snake.score,black)

            #update screen from invisible place
            pygame.display.flip()

            #FPS
            clock.tick(self.FPS)

            #controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                        self.game_over = False
                        self.start = False
                    if event.key == pygame.K_LEFT:
                        if my_snake.vx > 0 or my_snake.check_collision("Left") is True:
                            pass
                        else:
                            my_snake.vx = -scale
                            my_snake.vy = 0
                            my_snake.rotate = "Left"
                    elif event.key == pygame.K_RIGHT:
                        if my_snake.vx < 0 or my_snake.check_collision("Right") is True:
                            pass
                        else:
                            my_snake.vx = scale
                            my_snake.vy = 0
                            my_snake.rotate = "Right"
                    elif event.key == pygame.K_UP:
                        if my_snake.vy > 0 or my_snake.check_collision("Up") is True:
                            pass
                        else:
                            my_snake.vx = 0
                            my_snake.vy = -scale
                            my_snake.rotate = "Up"
                    elif event.key == pygame.K_DOWN:
                        if my_snake.vy < 0 or my_snake.check_collision("Down") is True:
                            pass
                        else:
                            my_snake.vx = 0
                            my_snake.vy = scale
                            my_snake.rotate = "Down"


        quit()

        

class Snake(object):
    
    def __init__(self):
        self.x = 0
        self.y = play_field_height/2-scale
        self.vx = scale
        self.vy = 0
        self.size = (scale,scale)
        self.color = (green)
        self.body = []
        self.length = 3
        self.score = 0
        self.rotate = "Right"
        self.rotate_position = []
         
    def update(self):
        self.x += self.vx
        self.y += self.vy

        #create body list
        self.head = []
        self.head.append(self.x)
        self.head.append(self.y)
        self.body.append(self.head)

        #create rotation list for head and tail sprites
        self.rotate_position.append(self.rotate)

        #keeps snake correct length
        if len(self.body) > self.length:
            del self.body[0]
            del self.rotate_position[0]

            
    def grow(self):
        self.length += 1
        self.score += 1

        
    def draw(self, display, bodylist):

        #rotate snake head to face correct direction
        if self.vx == scale:
            head = pygame.transform.rotate(head_sprite, 270)
        elif self.vx == -scale:
            head = pygame.transform.rotate(head_sprite, 90)
        elif self.vy == scale:
            head = pygame.transform.rotate(head_sprite, 180)
        elif self.vy == -scale:
            head = pygame.transform.rotate(head_sprite, 0)

        #rotate tail
        if self.rotate_position[0] == 'Right':
            tail = pygame.transform.rotate(tail_segment, 270)
        elif self.rotate_position[0] == 'Left':
            tail = pygame.transform.rotate(tail_segment, 90)
        elif self.rotate_position[0] == 'Down':
            tail = pygame.transform.rotate(tail_segment, 180)
        elif self.rotate_position[0] == 'Up':
            tail = pygame.transform.rotate(tail_segment, 0)


        #draw the head
        display.blit(head, self.body[-1])

        #draw the body parts
        for bodypart in bodylist[1:-1]:
            display.blit(body_segment, bodypart)

        #draw the tail
        display.blit(tail, self.body[0])

    #so you cannot get two direction changes before the snake moves and run into yourself when you shouldnt be able to
    def check_collision(self, direction):
        if direction == "Right":
            if self.body[-1][0] + scale == self.body[-2][0]:
                return True
            else:
                return False
        if direction == "Left":
            if self.body[-1][0] - scale == self.body[-2][0]:
                return True
            else:
                return False
        if direction == "Up":
            if self.body[-1][1] - scale == self.body[-2][1]:
                return True
            else:
                return False
        if direction == "Down":
            if self.body[-1][1] + scale == self.body[-2][1]:
                return True
            else:
                return False



class Apple(object):

    def __init__(self):
        self.x = round(random.randrange(0, play_field_width-scale)/scale)*scale
        self.y = round(random.randrange(0, play_field_height-scale)/scale)*scale
        self.size = (scale,scale)

    def update(self):
        self.x = round(random.randrange(0, play_field_width-scale)/scale)*scale
        self.y = round(random.randrange(0, play_field_height-scale)/scale)*scale

    def draw(self, display):
        display.blit(apple_image, (self.x, self.y))
        

class Gameboard(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = black
        self.size = (play_field_width,play_field_height)

    def draw(self, display):
        pygame.draw.rect(display, self.color, [(self.x, self.y), self.size])
        
        
Main ()
