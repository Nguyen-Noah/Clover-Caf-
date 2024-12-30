import math

class vec4:
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return f"vec4({self.x}, {self.y}, {self.z}, {self.w})"

    def __add__(self, other):
        if isinstance(other, vec4):
            return vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        raise TypeError("Can only add vec4 to vec4")

    def __sub__(self, other):
        if isinstance(other, vec4):
            return vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
        raise TypeError("Can only subtract vec4 from vec4")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return vec4(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)
        raise TypeError("Can only multiply vec4 by a scalar")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)) and scalar != 0:
            return vec4(self.x / scalar, self.y / scalar, self.z / scalar, self.w / scalar)
        raise TypeError("Can only divide vec4 by a non-zero scalar")

    def __neg__(self):
        return vec4(-self.x, -self.y, -self.z, -self.w)

    def __eq__(self, other):
        return (
            math.isclose(self.x, other.x) and 
            math.isclose(self.y, other.y) and 
            math.isclose(self.z, other.z) and 
            math.isclose(self.w, other.w)
        )

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        elif index == 3:
            return self.w
        else:
            raise IndexError("Vector4 index out of range")
        
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        elif index == 3:
            self.w = value
        else:
            raise IndexError("Vector4 index out of range")

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return vec4(0, 0, 0, 0)
        return self / mag

    def lerp(self, other, t):
        if isinstance(other, vec4) and isinstance(t, (int, float)):
            return self + (other - self) * t
        raise TypeError("Invalid arguments for lerp")

    def distance_to(self, other):
        if isinstance(other, vec4):
            return (self - other).magnitude()
        raise TypeError("Can only calculate distance to another vec4")

    def copy(self):
        return vec4(self.x, self.y, self.z, self.w)
    
    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "w": self.w
        }
    
    @classmethod
    def deserialize(cls, data):
        x = data.get('x', 0)
        y = data.get('y', 0)
        z = data.get('z', 0)
        w = data.get('w', 0)
        return cls(x, y, z, w)
