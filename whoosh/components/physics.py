"""
With a physics component, you can fly.
Well, not for long.
You'll shortly fall to your death.
"""
import pymunk
import whoosh.maths
from whoosh.components.base import BaseComponent


class PhysicsComponent(BaseComponent):
    """
    Useful for recreating Angry Birds.
    GameWorld.add_blob will automatically add the physics body to the physics world as long as the component was added
    to the blob before add_blob was called.
    Boy that was a long sentence.
    """
    def __init__(self, **kwargs):
        BaseComponent.__init__(self)
        self.body = pymunk.Body(**kwargs)
        self.shapes = []

        """
        mass = 10.0
        moment = pymunk.moment_for_circle(mass, inner_radius=0, outer_radius=10)
        self.body = pymunk.Body(mass=mass, moment=moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pymunk.vec2d.Vec2d(300 + 50, 105 + 20.0)
        self.shapes = [pymunk.Circle(self.body, 20)]
        #self.space.add(body, shape)
        """

        self._new_position = None
        self._new_velocity = None
        #self.body.position_func = self._set_position_func
        #self.body.velocity_func = self._set_velocity_func

    def get_position(self):
        """
        Returns the position of the body as a Vec2f.
        """
        #print("PhysicsComponent.get_position returning {0}".format(self.body.position))
        return whoosh.maths.Vec2f.from_pyvec(self.body.position)

    def get_velocity(self):
        """
        Returns the velocity of the body as a Vec2f.
        """
        return whoosh.maths.Vec2f.from_pyvec(self.body.velocity)

    def get_rotation(self):
        """
        Returns the clockwise rotation of the body in degrees.
        """
        return whoosh.maths.radians_to_degrees(self.body.angle)

    def set_position(self, pos):
        """
        Sets the position of the body.
        The position won't actually be changed until the next physics world step, when
        chipmunk calls our _set_velocity_func.
        """
        #self._new_position = pos
        #self.body.position = pymunk.vec2d.Vec2d(200.0, 200.0)
        self.body.position = pos

    def add_circle(self, radius, **kwargs):
        """
        Utility method which creates a pymunk Circle shape and adds it to the body.
        """
        shape = pymunk.Circle(self.body, radius, **kwargs)
        self.shapes.append(shape)
        return shape

    def add_poly(self, vertices, **kwargs):
        """
        Utility method which creates a pymunk Poly shape and adds it to the body.
        """
        shape = pymunk.Poly(self.body, vertices, **kwargs)
        self.shapes.append(shape)
        return shape

    def add_segment(self, a, b, radius):
        """
        Utility method which creates a pymunk Segment shape and adds it to the body.
        """
        shape = pymunk.Segment(self.body, a, b, radius)
        self.shapes.append(shape)
        return shape

    def add_equilateral(self, radius, sides):
        """
        Utility method which creates a pymunk Poly shape and adds it to the body.
        The vertices are calculated automatically using the given number of sides and radius.
        """
        verts = whoosh.maths.get_ngon_vertices(radius, sides)
        print("Verts are {0}".format(verts))
        return self.add_poly(verts)

    def _set_position_func(self, body, dt):
        """
        Called by chipmunk every time step. If something has called set_position recently then the position will be
        actually updated here.
        """
        if self._new_position:
            self.body.position = self._new_position
        self._new_position = None

    def _set_velocity_func(self, gx, gy, damping, dt):
        """
        Called by chipmunk every time step. If something has called set_velocity recently then the velocity will be
        actually updated here.
        """
        if self._new_velocity:
            self.body.position = self._new_velocity
        self._new_velocity = None
