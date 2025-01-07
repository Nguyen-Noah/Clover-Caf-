import math
from copy import deepcopy

class vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"vec2({self.x}, {self.y})"

    def __add__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return vec2(self.x + other, self.y + other)
        raise TypeError("Can only add vec2 to vec2 or a scalar (int/float)")

    def __sub__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        raise TypeError("Can only subtract vec2 from vec2")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return vec2(self.x * scalar, self.y * scalar)
        raise TypeError("Can only multiply vec2 by a scalar")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)) and scalar != 0:
            return vec2(self.x / scalar, self.y / scalar)
        raise TypeError("Can only divide vec2 by a non-zero scalar")

    def __neg__(self):
        return vec2(-self.x, -self.y)

    def __eq__(self, other):
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2 index out of range")
        
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Vector2 index out of range")

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return vec2(0, 0)
        return self / mag

    def dot(self, other):
        if isinstance(other, vec2):
            return self.x * other.x + self.y * other.y
        raise TypeError("Can only calculate dot product with another vec2")

    def cross(self, other):
        if isinstance(other, vec2):
            return self.x * other.y - self.y * other.x
        raise TypeError("Can only calculate cross product with another vec2")

    def lerp(self, other, t):
        if isinstance(other, vec2) and isinstance(t, (int, float)):
            return self + (other - self) * t
        raise TypeError("Invalid arguments for lerp")

    def distance_to(self, other):
        if isinstance(other, vec2):
            return (self - other).magnitude()
        raise TypeError("Can only calculate distance to another vec2")

    def angle_to(self, other):
        if isinstance(other, vec2):
            dot_product = self.dot(other)
            mag_product = self.magnitude() * other.magnitude()
            if mag_product == 0:
                return 0.0
            return math.degrees(math.acos(max(min(dot_product / mag_product, 1), -1)))
        raise TypeError("Can only calculate angle to another vec2")

    def rotate(self, angle):
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return vec2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

    def copy(self):
        return vec2(self.x, self.y)
    
    def serialize(self):
        return {
            "x": self.x,
            "y": self.y
        }
    
    @classmethod
    def deserialize(cls, data):
        x = data.get('x', 0)
        y = data.get('y', 0)
        return cls(x, y)