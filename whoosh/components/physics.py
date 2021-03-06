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
        self._touching_ground = False # cache these at the start of every tick
        self._touching_wall = False
        self._touching_ceiling = False

    def on_pre_tick(self):
        self._update_touching_info()

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

    def is_touching_ceiling(self):
        """
        Returns True/False whether the body is touching a ceiling
        """
        return self._touching_ceiling

    def is_touching_ground(self):
        """
        Returns True/False whether the body is touching the ground
        """
        return self._touching_ground

    def is_touching_wall(self):
        """
        Returns True/False whether the body is touching a wall
        """
        return self._touching_wall

    def is_in_air(self):
        """
        Returns True/False whether the body is not touching the ground.
        """
        return not self.is_touching_ground()

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

    def _update_touching_info(self):
        """
        Sets _touching_ground, _touching_wall and _touching_ceiling by checking all of the current collisions the body is in
        with other static or kinematic bodies.
        """
        def f(arbiter):
            my_shape = None
            other_shape = None
            for shape in arbiter.shapes:
                if shape.body is self.body:
                    my_shape = shape
                else:
                    other_shape = shape
            bt = other_shape.body.body_type 
            if bt == pymunk.Body.STATIC or bt == pymunk.Body.KINEMATIC:
                nang = arbiter.contact_point_set.normal.angle_degrees

                if 135 > nang and nang > 45: # Pointing upwards
                    f.touching_ceiling = True
                elif -135 < nang and nang < -45: # Pointing downwards
                    f.touching_ground = True
                else: # Must be pointing sideways
                    f.touching_wall = True
        f.touching_ceiling = False
        f.touching_wall = False
        f.touching_ground = False
        self.body.each_arbiter(f)
        self._touching_ceiling = f.touching_ceiling
        self._touching_wall = f.touching_wall
        self._touching_ground = f.touching_ground