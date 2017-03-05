"""
This module offers you a Camera, capable of viewing the world from different positions, angles and zooms.
"""
import pyglet
import pyglet.window.key as key
import whoosh.maths
from pyglet.gl import *
from whoosh.maths import Vec2f

def opengl_init():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class Camera:
    """
    A Camera is constructed by the Window and allows customizable viewing of the game world.
    Credit: http://stackoverflow.com/questions/16969094/best-way-to-scroll-a-window-using-pyglet
    """
    ORTHOGRAPHIC = 1
    ISOMETRIC = 2
    PERSPECTIVE = 3
    MIN_ZOOM = 0.1
    MAX_ZOOM = 1.0

    def __init__(self, width=640, height=480):
        self.mode = Camera.ORTHOGRAPHIC
        self.x, self.y, self.z = 0, 0, 512
        self.rx, self.ry, self.rz = 0, -45, 0
        self.width, self.height = width, height
        self.viewport_width, self.viewport_height = width, height
        self.far = 8192
        self.minfov = 1
        self.maxfov = 50
        self.fov = self.maxfov
        self.default_zoom = 0.25
        self.current_zoom = self.default_zoom

        self.activate_orthographic()
        self._update_after_zoom()

    def activate_orthographic(self):
        """
        Sets the camera to an orthographic projection
        """
        self.mode = Camera.ORTHOGRAPHIC
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.viewport_width, 0, self.viewport_height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def activate_isometric(self):
        """
        Sets the camera to an isometric projection
        """
        self.mode = Camera.ISOMETRIC
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w = self.viewport_width
        h = self.viewport_height
        glOrtho(-w/2.0, w/2.0, -h/2.0, h/2.0, 0, self.far)
        glMatrixMode(GL_MODELVIEW)

    def activate_perspective(self):
        """
        Sets the camera to an perspective projection
        """
        self.mode = Camera.PERSPECTIVE
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.viewport_width/float(self.viewport_height), 0.1, self.far)
        glMatrixMode(GL_MODELVIEW)

    def convert_screen_to_world(self, pos):
        """
        Converts an x,y position on screen to the relevant world position
        """
        if self.mode != Camera.ORTHOGRAPHIC:
            raise NotImplemented("convert_screen_to_world only implemented for Orthographic camera")
        elif self.rx != 0 or self.rz != 0:
            raise NotImplemented("convert_screen_to_world doesn't account for rotation yet")
        sx = pos.x / float(self.width)
        sy = pos.y / float(self.height)
        worldx = self.x + sx * self.viewport_width
        worldy = self.y + sy * self.viewport_height
        return Vec2f(worldx, worldy)

    def convert_world_to_screen(self, pos):
        """
        Converts an x,y position in the world to the relevant screen position
        """
        if self.mode != Camera.ORTHOGRAPHIC:
            raise NotImplemented("convert_world_to_screen only implemented for Orthographic camera")
        elif self.rx != 0 or self.rz != 0:
            raise NotImplemented("convert_world_to_screen doesn't account for rotation yet")
        dx = pos.x - self.x
        dy = pos.y - self.y
        return Vec2f(dx / self.current_zoom, dy / self.current_zoom)

    def center_on(self, pos):
        """
        Center the camera on a world position
        """
        self.x = pos.x - self.viewport_width/2.0
        self.y = pos.y - self.viewport_height/2.0

    def pan(self, vec):
        """
        Pans the camera in the x-y plane by the given vector.
        """
        self.x += -vec.x
        self.y += -vec.y

    def rotate(self, vec):
        """
        Rotates the camera in the x-y plane by the given vector.
        """
        self.rx += vec.x
        self.ry += vec.y

    def zoom(self, amount):
        """
        Takes a number between -1 and 1. Positive number causes a zoom in, and negative a zoom out.
        """
        if not (amount >= -1 and amount <= 1):
            raise ValueError("Invalid zoom parameter {0}".format(amount))
        self.current_zoom -= amount
        self.current_zoom = whoosh.maths.keep_within_range(Camera.MIN_ZOOM, Camera.MAX_ZOOM, self.current_zoom)
        #print("current_zoom: {0}".format(self.current_zoom))
        self._update_after_zoom()

    def set_zoom(self, zoom):
        """
        Takes a number between Camera.MIN_ZOOM and Camera.MAX_ZOOM.
        Sets the current zoom to the number given.
        """
        if not (zoom >= Camera.MIN_ZOOM and zoom <= Camera.MAX_ZOOM):
            raise ValueError("Invalid zoom parameter {0}".format(zoom))
        self.current_zoom = zoom
        self._update_after_zoom()

    def apply(self):
        """
        Apply camera transformation.
        """
        glLoadIdentity()
        glTranslatef(-self.x, -self.y, 0)
        if self.mode == Camera.ORTHOGRAPHIC:
            return
        glTranslatef(0, 0, -self.z)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.ry, 0, 1, 0)
        glRotatef(self.rz, 0, 0, 1)

    def change_size(self, width, height):
        """
        Probably only called if the window changes size.
        """
        print "Viewport " + str(width) + "x" + str(height)
        self.width, self.height = width, height
        glViewport(0, 0, width, height)

    def refresh(self):
        """
        Refreshes the camera state. It seems that OpenGL calls don't have effect if the camera is created before
        the window starts.
        """
        self._update_after_zoom()

    def debug_draw(self):
        """
        Can be used to print debug information about the camera to screen.
        """
        mode_name = ["", "Orthographic", "Isometric", "Perspective"][self.mode]
        lines = ["Camera debug:"
                ,"mode = {0}".format(mode_name)
                ,"(width, height) = ({0}, {1})".format(self.width, self.height)
                ,"(x,y,z) = ({0}, {1}, {2})".format(self.x, self.y, self.z)
                ,"(viewport_width, viewport_height) = ({0}, {1})".format(self.viewport_width, self.viewport_height)
                ,"current_zoom = {0}".format(self.current_zoom)
                ]   
        label_start = Vec2f(self.x + 20, self.y + 150)
        line_height = 16
        for i, line in enumerate(lines):
            label = pyglet.text.Label(line, x=label_start.x, y=label_start.y - i * line_height)
            label.draw()

    def _update_after_zoom(self):
        """
        Updates self.fov based on self.current_zoom
        """
        self.fov = self.minfov + (self.maxfov - self.minfov) * self.current_zoom
        old_width = self.viewport_width
        old_height = self.viewport_height
        self.viewport_width = self.width * self.current_zoom
        self.viewport_height = self.height * self.current_zoom
        width_change = old_width - self.viewport_width
        height_change = old_height - self.viewport_height
        #print("width_change", width_change, "height_change", height_change)
        self.x += width_change / 2.0
        self.y += height_change / 2.0
        if self.mode == Camera.ORTHOGRAPHIC:
            self.activate_orthographic()
        elif self.mode == Camera.ISOMETRIC:
            self.activate_isometric()
        elif self.mode == Camera.PERSPECTIVE:
            self.activate_perspective()

