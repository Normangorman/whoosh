"""
This module provides the AnimatedSprite class, which provides a more powerful interface to sprite animations
than the default pyglet classes do.
"""
import pyglet
from whoosh.engine.modules.resourceloading import ResourceLoadingModule
import whoosh.engine.api


class AnimatedSprite:
    """
    Give me a spritesheet.
    I give you animations and methods to control them.
    """
    def __init__(self, spritesheet_path, rows, cols):
        """
        The given spritesheet_path should be a file within the asset_directory as set in assetloading.setup
        """
        loader = whoosh.engine.api.get_engine_module(ResourceLoadingModule).get_loader()
        image = loader.image(spritesheet_path)
        self.spritesheet = pyglet.image.ImageGrid(image, rows, cols)
        self.animations = {} # maps string animation names to AnimationData objects
        self._current_animation = None # an AnimationData
        self._current_animation_frame = 0
        self._scale = 1.0
        self._rotation = 0.0

        # Center anchor by default since the physics engine center anchors everything
        for texture in self.spritesheet:
            texture.anchor_x = texture.width // 2
            texture.anchor_y = texture.height // 2

    def add_animation(self, animation_data):
        """
        Adds an animation to the available set.
        Takes an AnimationData object as an argument.
        """
        for frame in animation_data.frames:
            if frame < 0 or frame >= len(self.spritesheet):
                raise ValueError("Given AnimationData has frames which are not in the spritesheet")
        self.animations[animation_data.name] = animation_data

    def set_current_animation(self, animation_name):
        """
        Sets the currently playing animation. Takes the name of the animation (a string)
        """
        if animation_name not in self.animations:
            raise ValueError("No such animation {0}".format(animation_name))
        self._current_animation = self.animations[animation_name]

    def draw(self, pos):
        """
        Draws the animation at the given position (a Vec2f)
        """
        x, y = int(pos.x), int(pos.y)
        sprite = pyglet.sprite.Sprite(self._get_current_frame())
        sprite.set_position(x, y)
        sprite.scale = self._scale
        sprite.rotation = self._rotation
        sprite.draw()

    def update(self, dt):
        """
        Updates the progress of the animation
        """
        # TODO: improve this
        self._current_animation_frame = (self._current_animation_frame + 1) % len(self._current_animation)

    def set_scale(self, scale):
        """
        Scales up or down the sprite. Takes one argument scale (a float)
        """
        self._scale = scale

    def set_rotation(self, rotation):
        """
        Sets the clockwise rotation of the sprite in degrees.
        """
        self._rotation = rotation

    def _get_current_frame(self):
        """
        Returns a pyglet.image.Image which is the current animation frame.
        """
        if not self._current_animation:
            return None
        else:
            spritesheet_frame = self._current_animation.frames[self._current_animation_frame]
            return self.spritesheet[spritesheet_frame]


class AnimationData:
    """
    A simple data bag which represents all the needed information about an animation on a spritesheet.
    """
    def __init__(self, name, frames, frame_duration=0.1, loop=True):
        self.name = name
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop

    def __len__(self):
        return len(self.frames)
