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


from random import random
import pygame
import gi
from ball import Ball
from bat import Bat
from brick import Brick
from enum import Enum

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

State = Enum('State', ['STILL', 'PLAY', 'WON', 'LOST'])

class BallAndBrick:
    def __init__(self):
        self.green = (34, 139, 34)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 153)

        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.black = (0, 0, 0)
        self.back_col = (255, 255, 255)
        self.brick_col = (0, 0, 0)
        self.scroll_col = (0, 0, 0)
        self.clock = pygame.time.Clock()
        self.pause = False
        self.shake = 0
        self.ball_vel = pygame.Vector2(7, -7)
        self.theme_keys = (
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
        )
        self.back_cols = (
            (255, 255, 255),
            (228, 47, 12),
            (47, 79, 79),
            (140, 89, 51),
            (0, 255, 255),
            (115, 69, 35),
            (6, 43, 22),
            (25, 25, 112),
            (9, 84, 190),
        )
        self.brick_cols = (
            (0, 0, 0),
            (245, 226, 226),
            (255, 255, 255),
            (237, 201, 175),
            (34, 139, 34),
            (0, 255, 0),
            (173, 255, 47),
            (255, 255, 49),
            (212, 219, 178),
        )
        self.scroll_cols = (
            (0, 0, 0),
            (0, 255, 0),
            (255, 255, 255),
            (237, 201, 175),
            (34, 139, 34),
            (0, 255, 0),
            (173, 255, 47),
            (255, 255, 49),
            (212, 219, 178),
        )

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    def run(self):
        def vw(x):
            return (x / 100) * pygame.display.get_surface().get_width()

        def vh(y):
            return (y / 100) * pygame.display.get_surface().get_height()

        def restart_game():
            pygame.mixer.music.load("assets/jazz.ogg")
            pygame.mixer.music.play(-1)

            self.bat = Bat((vw(50), vh(88)), (vw(11.7), vw(2)))
            
            self.balls = []
            new_ball()

            self.lives = 3
            self.score = 0
            self.state = State.STILL

            brick_make()

        def new_ball():
            r = vw(1.4)
            self.balls.append(Ball((vw(50), vh(88) - r - 3), r))

        def sx(x):
            screen = pygame.display.get_surface()
            scale = screen.get_width() / 1200
            x *= scale
            return x

        def brick_make():
            screen = pygame.display.get_surface()
            brick_w = round((screen.get_width()) / 10.7)
            brick_h = round((screen.get_height()) / 32)

            brick_start_pos_y = 70
            self.bricks_arr = []
            for _ in range(7):
                brick_start_pos_x = (screen.get_width() - (brick_w + sx(10)) * 8) / 2
                for _ in range(8):
                    self.bricks_arr.append(
                        Brick((brick_start_pos_x, brick_start_pos_y), (brick_w, brick_h))
                    )
                    brick_start_pos_x += brick_w + sx(10)
                brick_start_pos_y += brick_h + 5

        def draw_bricks():
            if self.shake > pygame.time.get_ticks():
                rand = (random() - 0.5) * 6, (random() - 0.5) * 6
            else:
                rand = 0, 0

            for brick in self.bricks_arr:
                brick.draw(offset = rand)

        def check_input():
            while Gtk.events_pending():
                Gtk.main_iteration()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.bat.move(-1)

            if keys[pygame.K_RIGHT]:
                self.bat.move(1)

            if keys[pygame.K_c] and self.state == State.STILL:
                if self.score > 150:
                    vel = (10, -10)
                elif self.score > 100:
                    vel = (8, -8)
                else:
                    vel = (7, -7)

                for ball in self.balls:
                    ball.set_velocity(vel)

                self.state = State.PLAY
            elif keys[pygame.K_n] and (
                self.state == State.LOST or self.state == State.WON
            ):
                restart_game()
            elif keys[pygame.K_s]:
                settings()
            elif keys[pygame.K_q]:
                pygame.quit()
                quit()

        def handle_collisions():
            # Bricks collision
            for brick in self.bricks_arr:
                for ball in self.balls:
                    if ball.check_collision(brick.rect):
                        self.score += 3
                        self.bricks_arr.remove(brick)
                        ball.bounce_against(brick.rect)
                        self.shake = pygame.time.get_ticks() + 200
                        break

            # Bat collision
            for ball in self.balls:
                if ball.check_collision(self.bat.rect) and self.bat.rect.y > ball.position[1]:
                    ball.bounce_against(self.bat.rect)

            if len(self.bricks_arr) == 0:
                self.state = State.WON
            if len(self.balls) == 0:
                self.lives -= 1
                new_ball()
                self.state = State.STILL
            if self.lives == 0:
                self.state = State.LOST


        def score_lives():
            screen = pygame.display.get_surface()
            
            medfont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(30)))
            font_surface = medfont.render(
                "Score: " + str(self.score), True, self.brick_col
            )
            live_surface = medfont.render(
                "Lives left: " + str(self.lives), True, self.brick_col
            )
            screen.blit(font_surface, (sx(100), 5))
            screen.blit(
                live_surface,
                (round(screen.get_width() / 2 - live_surface.get_width() / 2), 5),
            )
            pause_mess = medfont.render("Press P to pause", True, self.brick_col)
            screen.blit(
                pause_mess,
                (round(screen.get_width() - pause_mess.get_width() - sx(100)), 5),
            )

        def text_size(text, color, size):
            smallfont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(30)))
            medfont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(40)))
            largefont = pygame.font.Font("fonts/comicsansms.ttf", int(sx(70)))
            if size == "small":
                textSurf = smallfont.render(text, True, color)
            if size == "medium":
                textSurf = medfont.render(text, True, color)
            if size == "large":
                textSurf = largefont.render(text, True, color)

            return textSurf, textSurf.get_rect()

        def message_to_screen(msg, color, y_displace=100, size="small"):
            screen = pygame.display.get_surface()
            scale = screen.get_height() / 900

            textSur, textRect = text_size(msg, color, size)
            textRect.center = ((screen.get_width()) / 2), (
                (screen.get_height() - 50) / 2
            ) + y_displace * scale
            screen.blit(textSur, textRect)

        def unpause():
            global pause
            pygame.mixer.music.unpause()
            self.pause = False

        def paused():
            screen = pygame.display.get_surface()
            screen.fill(self.back_col)
            message_to_screen("Paused", self.brick_col, 0, size="large")
            message_to_screen("Press P to continue", self.brick_col, 100, size="medium")
            message_to_screen(
                "Press N for a new game", self.brick_col, 170, size="medium"
            )
            message_to_screen("Press Q to quit", self.brick_col, 240, size="medium")
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
                            gameLoop()

        def settings():
            screen = pygame.display.get_surface()
            screen.fill(self.yellow)
            message_to_screen("Settings", self.black, -400, size="large")
            message_to_screen("Press N to start a new game", self.black, -300, size="medium")
            message_to_screen("Press Q to quit", self.black, -230, size="medium")
            message_to_screen("Themes: ", self.black, -150, size="medium")
            message_to_screen("1. Classic ", self.black, -80, size="small")
            message_to_screen("2. Fresh and Bright ", self.black, -30, size="small")
            message_to_screen("3. Professional ", self.black, 20, size="small")
            message_to_screen("4. Earthy ", self.black, 70, size="small")
            message_to_screen("5. Watery ", self.black, 120, size="small")
            message_to_screen("6. Natural ", self.black, 170, size="small")
            message_to_screen("7. Energetic ", self.black, 220, size="small")
            message_to_screen("8. Day and Night ", self.black, 270, size="small")
            message_to_screen("9. Aqua Blues ", self.black, 320, size="small")
            message_to_screen(
                "Press the theme number to select the theme ",
                self.black,
                370,
                size="medium",
            )
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
                        if event.key == pygame.K_n:
                            gameLoop()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            quit()
                        else:
                            for i, key in enumerate(self.theme_keys):
                                if event.key == key:
                                    self.back_col = self.back_cols[i]
                                    self.brick_col = self.brick_cols[i]
                                    self.scroll_col = self.scroll_cols[i]
                                    gameLoop()
                                    break

        def gameLoop():
            screen = pygame.display.get_surface()

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
                            paused()

                self.clock.tick(50)
                screen.fill(self.back_col)

                check_input()
                draw_bricks()
                score_lives()
                self.bat.update()
                if self.state == State.PLAY:
                    for ball in self.balls:
                        ball.update()
                        if ball.is_lost():
                            self.balls.remove(ball)
                    
                    handle_collisions()
                
                elif self.state == State.STILL:
                    for ball in self.balls:
                        n_x  = self.bat.rect.left + self.bat.rect.width / 2
                        n_y = self.bat.rect.top - ball.radius * 2
                        ball.set_position((n_x, n_y))
                        ball.draw()
                    message_to_screen(
                        "Press C to play", self.brick_col, 0, size="large"
                    )
                
                elif self.state == State.LOST:
                    message_to_screen("Game Over", self.brick_col, 50, size="large")
                    message_to_screen(
                        "Press N for New Game", self.brick_col, 150, size="medium"
                    )
                    message_to_screen(
                        "Press S for setting the theme",
                        self.brick_col,
                        220,
                        size="medium",
                    )
                    message_to_screen(
                        "Press Q to quit", self.brick_col, 290, size="medium"
                    )
                    pygame.mixer.music.stop()
                
                elif self.state == State.WON:
                    message_to_screen("You Won", self.brick_col, 50, size="large")
                    message_to_screen(
                        "Press N for New Game", self.brick_col, 150, size="medium"
                    )
                    message_to_screen(
                        "Press S for setting the theme",
                        self.brick_col,
                        220,
                        size="medium",
                    )
                    message_to_screen(
                        "Press Q to quit", self.brick_col, 290, size="medium"
                    )
                    pygame.mixer.music.stop()

                pygame.display.update()

        #####################################################################
        pygame.init()
        pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        screen = pygame.display.get_surface()

        def draw_welcome():
            screen.fill(self.yellow)
            message_to_screen(
                "Welcome to Ball and Brick", [0, 0, 0], -100, size="large"
            )
            message_to_screen("Press C to start the game", self.green, 0, size="medium")
            message_to_screen(
                "Press S for setting the theme", self.green, 70, size="medium"
            )
            message_to_screen("Press Q to quit the game", self.red, 140, size="medium")
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
    game = BallAndBrick()
    game.run()


if __name__ == "__main__":
    main()
