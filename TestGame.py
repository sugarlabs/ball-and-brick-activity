#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BallAndBrick
# Copyright (C) 2017  Hitesh Agarwal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import pygame
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TestGame:

    def __init__(self):
        self.green = (34,139,34)
        self.red = (255,0,0)
        self.yellow = (255,255,153)

        self.white = (255,255,255)
        self.blue  = (0,0,255)
        self.black = (0,0,0)
        self.back_col = [(255, 255, 255)] 
        self.brick_colour =[(0,0,0)]
        self.scroll_col = [(0,0,0)]
        self.ball_still = 0
        self.ball_play = 1
        self.ball_won = 2
        self.ball_game_over = 3
        self.clock = pygame.time.Clock()
        self.pause = False
        self.ball_vel = [7,-7]
    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass
    
    def run(self):
        def restart_game():
            pygame.mixer.music.load('assets/jazz.ogg')
            pygame.mixer.music.play(-1)
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter

            self.lives = 3
            self.score = 0
            self.state = self.ball_still

            self.paddle   = pygame.Rect(int(screen.get_width()/2),y_scrol,scroller_w,scroller_h)
            self.ball     = pygame.Rect(int(screen.get_width()/2),y_scrol - b_diameter,b_diameter,b_diameter)

            

            brick_make()

        def sx(x):
            screen = pygame.display.get_surface()
            scale = screen.get_width() / 1200
            x *= scale 
            return x
            
        def brick_make():
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter

            brick_start_pos_y = 70
            self.bricks_arr = [ ]
            for i in range(7):
                brick_start_pos_x = (screen.get_width() - (brick_w + sx(10)) * 8) / 2
                for j in range(8):
                    self.bricks_arr.append(pygame.Rect(brick_start_pos_x,brick_start_pos_y,brick_w,brick_h))
                    brick_start_pos_x += brick_w + sx(10)
                brick_start_pos_y += brick_h + 5

        def draw_bricks():
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter

            for brick in self.bricks_arr:
                pygame.draw.rect(screen, self.brick_colour[0], brick)
            
        def check_input():
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter
            while Gtk.events_pending():
                        Gtk.main_iteration()
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                self.paddle.left -= 10
                if self.paddle.left < 0:
                    self.paddle.left = 0

            if keys[pygame.K_RIGHT]:
                self.paddle.left += 10
                if self.paddle.left > x_max_scrol:
                    self.paddle.left = x_max_scrol

            if keys[pygame.K_c] and self.state == self.ball_still:
                if self.score > 150:
                    self.ball_vel = [10,-10]
                elif self.score > 100:
                    self.ball_vel = [8, -8]
                else:
                    self.ball_vel = [7, -7]
                self.state = self.ball_play
            elif keys[pygame.K_n] and (self.state == self.ball_game_over or self.state == self.ball_won):
                restart_game()
            elif keys[pygame.K_s]:
                settings()
            elif keys[pygame.K_q]:
                pygame.quit()
                quit()
        def move_ball():
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter

            self.ball.left += self.ball_vel[0]
            self.ball.top  += self.ball_vel[1]

            if self.ball.left <= 0:
                self.ball.left = 0
                self.ball_vel[0] = -self.ball_vel[0]
            elif self.ball.left >= x_max_ball:
                self.ball.left = x_max_ball
                self.ball_vel[0] = -self.ball_vel[0]
            
            if self.ball.top < 0:
                self.ball.top = 0
                self.ball_vel[1] = -self.ball_vel[1]
            elif self.ball.top >= y_max_ball:            
                self.ball.top = y_max_ball
                self.ball_vel[1] = -self.ball_vel[1]

        def handle_collisions():
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter

            for brick in self.bricks_arr:
                if self.ball.colliderect(brick):
                    self.score += 3
                    self.ball_vel[1] = -self.ball_vel[1]
                    self.bricks_arr.remove(brick)
                    break

            if len(self.bricks_arr) == 0:
                self.state = self.ball_won
                
            if self.ball.colliderect(self.paddle):
                self.ball.top = y_scrol - b_diameter
                self.ball_vel[1] = -self.ball_vel[1]
            elif self.ball.top > self.paddle.top:
                self.lives -= 1
                if self.lives > 0:
                    self.state = self.ball_still
                else:
                    self.state = self.ball_game_over

        def score_lives():
                screen = pygame.display.get_surface()
                brick_w   = round((screen.get_width())/10.7)
                brick_h   = round((screen.get_height())/32)
                scroller_w  = round((screen.get_width())/10.7)
                scroller_h  = round((screen.get_height())/40)
                b_diameter = round((scroller_w)/3.75)
                x_max_scrol = screen.get_width() - scroller_w
                y_scrol = (screen.get_height() -10) - scroller_h-70
                x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
                y_max_ball   = (screen.get_height() -10) - b_diameter


                medfont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(30)))
                font_surface = medfont.render("Score: " + str(self.score), True, self.brick_col)
                live_surface = medfont.render("Lives left: " + str(self.lives),  True, self.brick_col)
                screen.blit(font_surface, (sx(100),5))
                screen.blit(live_surface, (round(screen.get_width()/2 - live_surface.get_width()/2) ,5))
                pause_mess = medfont.render("Press P to pause", True, self.brick_col)
                screen.blit(pause_mess, (round(screen.get_width() - pause_mess.get_width() - sx(100)), 5))
        def text_size(text, color, size):
                            screen = pygame.display.get_surface()
                            brick_w   = round((screen.get_width())/10.7)
                            brick_h   = round((screen.get_height())/32)
                            scroller_w  = round((screen.get_width())/10.7)
                            scroller_h  = round((screen.get_height())/40)
                            b_diameter = round((scroller_w)/3.75)
                            x_max_scrol = screen.get_width() - scroller_w
                            y_scrol = (screen.get_height() -10) - scroller_h-70
                            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
                            y_max_ball   = (screen.get_height() -10) - b_diameter

                            smallfont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(30)))
                            medfont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(40)))
                            largefont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(70)))
                            if size == "small":
                                  textSurf = smallfont.render(text, True,color)
                            if size == "medium":
                                  textSurf = medfont.render(text, True,color)
                            if size == "large":
                                  textSurf = largefont.render(text, True,color)

                            return textSurf ,textSurf.get_rect()

        def message_to_screen(msg, color, y_displace=100, size = "small"):
                            screen = pygame.display.get_surface()
                            scale = screen.get_height() / 900
                            brick_w   = round((screen.get_width())/10.7)
                            brick_h   = round((screen.get_height())/32)
                            scroller_w  = round((screen.get_width())/10.7)
                            scroller_h  = round((screen.get_height())/40)
                            b_diameter = round((scroller_w)/3.75)
                            x_max_scrol = screen.get_width() - scroller_w
                            y_scrol = (screen.get_height() - 10) - scroller_h-70
                            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
                            y_max_ball   = (screen.get_height() - 10) - b_diameter

                            textSur, textRect = text_size( msg, color, size)
                            textRect.center = ((screen.get_width())/2), ((screen.get_height() - 50)/2) + y_displace * scale
                            screen.blit(textSur, textRect)
        def unpause():
                global pause
                pygame.mixer.music.unpause()
                self.pause = False
        def paused():
                screen = pygame.display.get_surface()
                screen.fill(self.back_col[0])
                message_to_screen( "Paused", self.brick_colour[0], 0, size = "large")
                message_to_screen ( "Press P to continue", self.brick_colour[0], 100, size = "medium")
                message_to_screen( "Press N for a new game", self.brick_colour[0], 170, size = "medium")
                message_to_screen( "Press Q to quit", self.brick_colour[0], 240, size = "medium")
                pygame.mixer.music.pause()
                pygame.display.update()
                
                self.pause = True
                while self.pause:
                              while Gtk.events_pending():
                                      Gtk.main_iteration()
                              for event in pygame.event.get():
                                    if event.type == pygame.VIDEORESIZE:
                                          pygame.display.set_mode(event.size, pygame.RESIZABLE)

                                    if event.type == pygame.QUIT:
                                          pygame.quit()
                                          quit()
                                    if event.type == pygame.KEYDOWN:
                                          if event.key == pygame.K_p:
                                                unpause()
                                          elif event.key == pygame.K_q:
                                                pygame.quit()
                                                quit()
    
                                          elif event.key == pygame.K_n:
                                                TestGame().run()

                
        def settings():
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter
            screen.fill(self.yellow)
            message_to_screen( "Settings", self.black, -400, size = "large")
            message_to_screen ( "Press P to continue", self.black, -300, size = "medium")
            message_to_screen( "Press Q to quit", self.black, -230, size = "medium")
            message_to_screen( "Themes: ", self.black, -150, size = "medium")
            message_to_screen( "1. Classic ", self.black, -80, size = "small")
            message_to_screen( "2. Fresh and Bright ", self.black, -30, size = "small")
            message_to_screen( "3. Professional ", self.black, 20, size = "small")
            message_to_screen( "4. Earthy ", self.black, 70, size = "small")
            message_to_screen( "5. Watery ", self.black, 120, size = "small")
            message_to_screen( "6. Natural ", self.black, 170, size = "small")
            message_to_screen( "7. Energetic ", self.black, 220, size = "small")
            message_to_screen( "8. Day and Night ", self.black, 270, size = "small")
            message_to_screen( "9. Aqua Blues ", self.black, 320, size = "small")
            message_to_screen( "Press the theme number to select the theme ", self.black, 370, size = "medium")
            pygame.display.update()
            while True:
                              while Gtk.events_pending():
                                      Gtk.main_iteration()
                              for event in pygame.event.get():
                                    if event.type == pygame.VIDEORESIZE:
                                          pygame.display.set_mode(event.size, pygame.RESIZABLE)

                                    if event.type == pygame.QUIT:
                                          pygame.quit()
                                          quit()
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_p:
                                            TestGame().run()
                                        elif event.key == pygame.K_q:
                                            pygame.quit()
                                            quit()
                                        elif event.key == pygame.K_1:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.back_col.append((255, 255, 255)) 
                                            self.brick_colour.append((0,0,0))
                                            self.scroll_col.append((0,0,0))
                                            gameLoop()
                                        elif event.key == pygame.K_2:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.back_col.append((228,47,12)) 
                                            self.brick_colour.append((245, 226, 226))
                                            self.scroll_col.append((0,255,0))
                                            gameLoop()
                                        elif event.key == pygame.K_3:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (255,255,255) )
                                            self.back_col.append( (47,79,79) )
                                            self.scroll_col.append((255,255,255) )
                                            gameLoop()
                                        elif event.key == pygame.K_4:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (237, 201, 175) )
                                            self.back_col.append( (140, 89, 51) )
                                            self.scroll_col.append((237, 201, 175) )
                                            gameLoop()

                                        elif event.key == pygame.K_5:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (34,139,34) )
                                            self.back_col.append( (0,255,255) )
                                            self.scroll_col.append((34,139,34) )
                                            gameLoop()

                                        elif event.key == pygame.K_6:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (0,255,0) )
                                            self.back_col.append((115,69,35) )
                                            self.scroll_col.append((0,255,0) )
                                            gameLoop()


                                        elif event.key == pygame.K_7:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (173,255,47) )
                                            self.back_col.append(( 6, 43, 22) )
                                            self.scroll_col.append((173,255,47) )
                                            gameLoop()

                                        elif event.key == pygame.K_8:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (255, 255, 49) )
                                            self.back_col.append(( 25, 25, 112) )
                                            self.scroll_col.append((255, 255, 49) )
                                            gameLoop()

                                        elif event.key == pygame.K_9:
                                            if self.back_col:
                                                self.back_col.remove(self.back_col[0])
                                            if self.brick_colour:
                                                self.brick_colour.remove(self.brick_colour[0])
                                            if self.scroll_col:
                                                self.scroll_col.remove(self.scroll_col[0])
                                            self.brick_colour.append( (212, 219, 178) )
                                            self.back_col.append(( 9, 84, 190) )
                                            self.scroll_col.append((212, 219, 178) )
                                            gameLoop()

                                            
                                            
                                              
        
        def gameLoop():
            
            screen = pygame.display.get_surface()
            brick_w   = round((screen.get_width())/10.7)
            brick_h   = round((screen.get_height())/32)
            scroller_w  = round((screen.get_width())/10.7)
            scroller_h  = round((screen.get_height())/40)
            b_diameter = round((scroller_w)/3.75)
            x_max_scrol = screen.get_width() - scroller_w
            y_scrol = (screen.get_height() -10) - scroller_h-70
            x_max_ball   = (screen.get_width() - sx(10)) - b_diameter
            y_max_ball   = (screen.get_height() -10) - b_diameter
            
            pygame.display.update()
            restart_game()
            while 1:            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.pause = True
                            pause = True
                            paused()

                self.clock.tick(50)
                screen.fill(self.back_col[0])
                check_input()
                draw_bricks()
                pygame.draw.rect(screen, self.scroll_col[0], self.paddle)
                pygame.draw.circle(screen, self.scroll_col[0], (self.ball.left + int(b_diameter/2), self.ball.top + int(b_diameter/2)), int(b_diameter/2))
                score_lives()
                if self.state == self.ball_play:
                    move_ball()
                    handle_collisions()
                elif self.state == self.ball_still:
                    self.ball.left = self.paddle.left + self.paddle.width / 2
                    self.ball.top  = self.paddle.top - self.ball.height
                    message_to_screen( "Press C to play", self.brick_colour[0], 0, size = "large")
                elif self.state == self.ball_game_over:
                    message_to_screen( "Game Over", self.brick_colour[0], 50, size = "large")
                    message_to_screen( "Press N for New Game", self.brick_colour[0], 150, size = "medium")
                    message_to_screen( "Press S for setting the theme", self.brick_colour[0], 220, size = "medium")
                    message_to_screen( "Press Q to quit", self.brick_colour[0], 290, size = "medium")
                    pygame.mixer.music.stop()
                elif self.state == self.ball_won:
                    message_to_screen( "You Won", self.brick_colour[0], 50, size = "large")
                    message_to_screen( "Press N for New Game", self.brick_colour[0], 150, size = "medium")
                    message_to_screen( "Press S for setting the theme", self.brick_colour[0], 220, size = "medium")
                    message_to_screen( "Press Q to quit", self.brick_colour[0], 290, size = "medium")
                    pygame.mixer.music.stop()

                

                pygame.display.update()



        #####################################################################  
        pygame.init()
        pygame.display.set_mode((0, 0), pygame.RESIZABLE)  
        screen = pygame.display.get_surface()

        def draw_welcome():
            screen.fill(self.yellow)
            message_to_screen("Welcome to Ball and Brick",
                              [0,0,0], -100, size = "large")
            message_to_screen("Press C to start the game",
                              self.green, 0, size = "medium")
            message_to_screen("Press S for setting the theme",
                              self.green, 70, size = "medium")
            message_to_screen("Press Q to quit the game",
                              self.red, 140, size = "medium") 
            pygame.display.flip()    
            self.clock.tick(10)
        draw_welcome()
        while True:
                              while Gtk.events_pending():
                                      Gtk.main_iteration()
                              for event in pygame.event.get():
                                    if event.type == pygame.VIDEORESIZE:
                                          pygame.display.set_mode(event.size, pygame.RESIZABLE)

                                    if event.type == pygame.QUIT:
                                          pygame.quit()
                                          quit()
                                    if event.type == pygame.KEYDOWN:
                                          if event.key == pygame.K_c:
                                                gameLoop()
                                          elif event.key == pygame.K_s:
                                                settings()  
                                          elif event.key == pygame.K_q:
                                                pygame.quit()
                                                quit()
                              self.clock.tick(10)


def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = TestGame()
    game.run()
    

if __name__ == '__main__':
    main()
