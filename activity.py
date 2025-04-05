import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import pygame

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton

import sugargame.canvas

import game


class BallAndBrickActivity(Activity):
    def __init__(self, handle):
        Activity.__init__(handle)

        self.paused = False

        # Build the activity toolbar.
        self.build_toolbar()

        # Create the game instance.
        self.game = game.BallAndBrick()

        # Build the Pygame canvas.

        self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display,
                                               pygame.mixer,
                                               pygame.font]
        )

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        # Blank space (separator) and Stop button at the end:

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)

    def get_preview(self):
        return self._pygamecanvas.get_preview()
