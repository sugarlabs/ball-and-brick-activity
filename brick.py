# Copyright (C) 2023 Riya Jain
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

import pygame

class Brick:

    def __init__(self, position, dimensions):
        self.gameDisplay = pygame.display.get_surface()

        self.rect = pygame.Rect(
                position[0], position[1], dimensions[0], dimensions[1]
            )
        
        self.color = (0, 0, 0)

    def update(self):
        self.draw()

    def draw(self, offset = (0, 0)):
        x, y = self.rect.x, self.rect.y
        self.rect.x += offset [0]
        self.rect.y += offset [1]
        pygame.draw.rect(self.gameDisplay, self.color, self.rect)
        self.rect.x = x
        self.rect.y = y
