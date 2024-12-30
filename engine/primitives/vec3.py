import math

class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError("Can only add vec3 to vec3")

    def __sub__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError("Can only subtract vec3 from vec3")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return vec3(self.x * scalar, self.y * scalar, self.z * scalar)
        raise TypeError("Can only multiply vec3 by a scalar")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)) and scalar != 0:
            return vec3(self.x / scalar, self.y / scalar, self.z / scalar)
        raise TypeError("Can only divide vec3 by a non-zero scalar")

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        return (
            math.isclose(self.x, other.x) and 
            math.isclose(self.y, other.y) and 
            math.isclose(self.z, other.z)
        )

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector3 index out of range")
        
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Vector3 index out of range")

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return vec3(0, 0, 0)
        return self / mag

    def dot(self, other):
        if isinstance(other, vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        raise TypeError("Can only calculate dot product with another vec3")

    def cross(self, other):
        if isinstance(other, vec3):
            return vec3(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        raise TypeError("Can only calculate cross product with another vec3")

    def lerp(self, other, t):
        if isinstance(other, vec3) and isinstance(t, (int, float)):
            return self + (other - self) * t
        raise TypeError("Invalid arguments for lerp")

    def distance_to(self, other):
        if isinstance(other, vec3):
            return (self - other).magnitude()
        raise TypeError("Can only calculate distance to another vec3")

    def copy(self):
        return vec3(self.x, self.y, self.z)
    
    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
    
    @classmethod
    def deserialize(cls, data):
        x = data.get('x', 0)
        y = data.get('y', 0)
        z = data.get('z', 0)
        return cls(x, y, z)
