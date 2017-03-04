"""
Watch me as I animate haha haha ha
"""
import pymunk
import pyglet
import os
from whoosh.components.base import BaseComponent
from whoosh.graphics.animatedsprite import AnimatedSprite, AnimationData


class AnimatedSpriteComponent(BaseComponent):
    """
    Spritesheet based animation for your blobs!
    """
    def __init__(self, spritesheet_path, rows, cols):
        BaseComponent.__init__(self)
        self.animated_sprite = AnimatedSprite(spritesheet_path, rows, cols)

    def draw(self, pos):
        """
        Draws the animation at the given position (a Vec2f)
        """
        self.animated_sprite.draw(pos)
