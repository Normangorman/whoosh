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

    def add_rect(self, width, height):
        """
        Utility method which creates a rectangular pymunk Poly shape and adds it to the body
        """
        hw, hh = width/2.0, height/2.0
        vertices = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        print("vertices={0}".format(vertices))
        return self.add_poly(vertices)

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