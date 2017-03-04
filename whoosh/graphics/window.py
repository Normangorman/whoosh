"""
Draw stuff in the game!
"""
import pyglet
import pyglet.window.key
import pyglet.gl as gl
import pymunk.pyglet_util
import whoosh.graphics.camera
from whoosh.engine.core import WhooshCore
from whoosh.components.animatedsprite import AnimatedSpriteComponent
from whoosh.components.physics import PhysicsComponent
from whoosh.components.input import InputComponent
from whoosh.graphics.camera import Camera


class WhooshWindow(pyglet.window.Window):
    """
    Open a magical window into your game world.
    Who knows what you might see?
    """
    def __init__(self, core, fps, **kwargs):
        pyglet.window.Window.__init__(self, **kwargs)
        self.core = core
        self.camera = Camera(width=kwargs.get('width'), height=kwargs.get('height'))
        self.fps = fps
        self.enable_fps_display = False
        self.enable_physics_debug = False
        self.enable_camera_debug = False
        self.enable_pixelart_mode = False
        self._fps_display = pyglet.clock.ClockDisplay()
        self._batch = pyglet.graphics.Batch() # TODO: this isn't used yet
        self._physics_draw_options = pymunk.pyglet_util.DrawOptions()
        self._physics_draw_options.flags = self._physics_draw_options.DRAW_SHAPES # enable shape drawing by default

        self.core.set_window(self)
        pyglet.clock.schedule_interval(self.update, 1/float(fps))
        whoosh.graphics.camera.opengl_init()

    def start(self):
        """
        Hopefully it won't blow up
        """
        pyglet.app.run()

    def on_show(self):
        if self.enable_pixelart_mode:
            self.activate_pixelart_mode()
        self.camera.refresh()

    def update(self, dt):
        """
        Updates the core
        """
        self.core.update(dt)
        self.render(dt)
        self.core.on_render()

    def get_camera(self):
        """
        Returns the Camera object the window is using.
        """
        return self.camera

    def draw_physics_debug(self):
        """
        Draws every object in the physics world to screen.
        Pretty damn useful.
        """
        self.core.game_world.physics_world.debug_draw(self._physics_draw_options)

    def activate_pixelart_mode(self):
        """
        Does some OpenGL stuff to prevent pixel art being blurred when zooming.
        """
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        self.enable_pixelart_mode = True

    def render(self, dt):
        """
        Renders everything in the core's game world
        """
        self.clear()
        self.camera.apply()

        for blob in self.core.game_world.blobs:
            anim = blob.get_component(AnimatedSpriteComponent)
            phys = blob.get_component(PhysicsComponent)
            if anim and phys:
                anim.animated_sprite.update(dt)
                anim.animated_sprite.set_rotation(phys.get_rotation())
                anim.draw(phys.get_position())

        if self.enable_physics_debug:
            self.draw_physics_debug()

        if self.enable_fps_display:
            self._fps_display.draw()
        
        if self.enable_camera_debug:
            self.camera.debug_draw()
