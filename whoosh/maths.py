"""
Ah maths. The real good stuff happens in this module.
"""
import math
import pymunk


class Vec2f(pymunk.vec2d.Vec2d):
    """
    It's likely that one vector implementation is not enough to rule them all.
    So we'll add some extra goodies here.
    """
    def __str__(self):
        return "Vec2f({0}, {1})".format(self.x, self.y)

    def tuple(self):
        """
        Sigh... not everyone likes vectors.
        """
        return (self.x, self.y)

    def rounded(self):
        """
        Returns a new vector which is a version of this one but the components are rounded to the nearest integer.
        """
        return Vec2f(int(self.x), int(self.y))

    @staticmethod
    def from_pyvec(pyvec):
        """
        Converts a pymunk Vec2d into a Vec2f.
        """
        v = Vec2f(pyvec.x, pyvec.y)
        return v

def radians_to_degrees(rads):
    """
    Convert from radians to degrees. I mean who likes radians really.
    """
    return rads * 180 / math.pi

def degrees_to_radians(degs):
    """
    Convert from degrees to radians. Pff, who actually works in degrees?.
    """
    return degs * math.pi / 180.0

def sign(x):
    return -1 if x < 0 else 1

def get_ngon_vertices(radius, sides):
    """
    So you want to make a game with octagons?
    This function returns a list of Vec2fs for an equilateral with the given number of sides and radius.
    The first vertex points directly upwards, and the rest proceed in anti-clockwise order.
    There will be sides + 1 vertices as the first vertex is also the last vertex (this works nicely with pymunk)
    """
    assert(sides > 0)
    v = Vec2f(0, -1) * radius
    verts = []
    rotation = 360.0 / sides
    for s in range(sides):
        verts.append(v.rotated_degrees(s * rotation))
    return verts

def keep_within_range(minimum, maximum, x):
    """
    Returns the value of x limited to the range [min, max]
    This means if x is less than min, min is returned.
    If x is greater than max, max is returned.
    """
    if x <= minimum:
        return minimum
    elif x >= maximum:
        return maximum
    else:
        return x
