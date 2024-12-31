import math

class JMath:
    @staticmethod
    def rotate(vec, angle_deg, origin):
        """
        Rotates a vec2 around an origin by angle_deg degrees.
        :param vec: vec2 - the vector to rotate
        :param angle_deg: float - the angle in degrees
        :param origin: vec2 - the origin point of rotation
        """
        # Translate to origin
        x = vec.x - origin.x
        y = vec.y - origin.y

        # Perform rotation
        cos = math.cos(math.radians(angle_deg))
        sin = math.sin(math.radians(angle_deg))
        x_prime = (x * cos) - (y * sin)
        y_prime = (x * sin) + (y * cos)

        # Translate back
        x_prime += origin.x
        y_prime += origin.y

        # Update vector
        vec.x = x_prime
        vec.y = y_prime

    @staticmethod
    def compare(x, y, epsilon=None):
        """
        Compares two floats with a given epsilon for tolerance.
        :param x: float - first number
        :param y: float - second number
        :param epsilon: float - tolerance for comparison (optional)
        :return: bool - whether x and y are considered equal
        """
        if epsilon is None:  # Default to machine epsilon
            epsilon = math.ulp(1.0)
        return abs(x - y) <= epsilon * max(1.0, max(abs(x), abs(y)))

    @staticmethod
    def compare_vec2(vec1, vec2, epsilon=None):
        """
        Compares two vec2 objects with a given epsilon for tolerance.
        :param vec1: vec2 - first vector
        :param vec2: vec2 - second vector
        :param epsilon: float - tolerance for comparison (optional)
        :return: bool - whether vec1 and vec2 are considered equal
        """
        return JMath.compare(vec1.x, vec2.x, epsilon) and JMath.compare(vec1.y, vec2.y, epsilon)
