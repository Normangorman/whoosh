import pymunk
import pyglet.window.key as key
from whoosh.defaultsetup import default_core, default_window
from whoosh.components.base import BaseComponent
from whoosh.components.input import InputComponent
from whoosh.components.physics import PhysicsComponent
from whoosh.components.animatedsprite import AnimatedSpriteComponent
from whoosh.graphics.animatedsprite import AnimationData
from whoosh.blob import Blob
from whoosh.maths import Vec2f


class FireballScript(BaseComponent):

    def on_tick(self):
        #print("FireballScript on_tick")
        inp = self.get_blob().get_component(InputComponent)
        phys = self.get_blob().get_component(PhysicsComponent)

        f = 1500 * phys.body.mass
        right = Vec2f(1, 0)
        left = Vec2f(-1, 0)
        up = Vec2f(0, 1)
        down = Vec2f(0, -1)
        if inp.is_key_pressed(key.UP):
            phys.body.apply_force_at_world_point(up*f, up*10)
        if inp.is_key_pressed(key.RIGHT):
            phys.body.apply_force_at_world_point(right*f, right*10)
        if inp.is_key_pressed(key.LEFT):
            phys.body.apply_force_at_world_point(left*f, left*10)
        if inp.is_key_pressed(key.DOWN):
            phys.body.apply_force_at_world_point(down*f, down*10)

def make_wall(a, b):
    wall = Blob("wall")

    phys = PhysicsComponent(body_type=pymunk.Body.STATIC)
    shape = phys.add_segment(a, b, 5.0)
    shape.elasticity = 0.95
    shape.friction = 0.9
    wall.add_component(phys)

    return wall

def make_fireball(mass=500, radius=30):
    fireball = Blob("fireball")

    # Input
    fireball.add_component(InputComponent(update_from_local_player=True))

    # Physics
    #phys = PhysicsComponent(mass=mass, moment=pymunk.moment_for_circle(mass, 0, radius))
    phys = PhysicsComponent(mass=mass, moment=pymunk.moment_for_circle(mass*100, 0, radius))
    shape = phys.add_equilateral(radius, 5)
    shape.friction = 0.9
    shape.elasticity = 0.7
    phys.set_position(Vec2f(200.0, 200.0))
    fireball.add_component(phys)

    # Script
    fireball.add_component(FireballScript())

    # Animation
    anim = AnimatedSpriteComponent("fireball_sprite.png", 4, 4)
    anim.animated_sprite.add_animation(AnimationData("default", range(0, 16)))
    anim.animated_sprite.set_current_animation("default")
    anim.animated_sprite.set_scale(0.1)
    fireball.add_component(anim)

    return fireball


core = default_core(resource_directory="examples/")
window = default_window(core)
window.enable_fps_display = True
window.enable_physics_debug = True

world = core.game_world
world.add_blob(make_fireball())

# Add 4 surrounding walls
margin = 55.0
w = window.width
h = window.height
world.add_blob(make_wall((margin, margin), (w-margin, margin)))
world.add_blob(make_wall((w-margin, margin), (w-margin, h-margin)))
world.add_blob(make_wall((w-margin, h-margin), (margin, h-margin)))
world.add_blob(make_wall((margin, h-margin), (margin, margin)))
world.add_blob(make_wall((margin*4, h/2), (w - margin*4, h/2)))

window.start()
