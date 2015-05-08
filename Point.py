__author__ = 'ryshackleton'

import math

class Point2:
    """Models a point in 2D"""

    def __init__(self, x=0.0, y=0.0):
        """
        Initializes a 2d point
        :param x: x value as a float
        :param y: y value as a float
        :return: None
        """
        self._x = float(x)
        self._y = float(y)

    # This establishes the format of the output string if you print a vector (an object instance).
    def __str__(self):
        return 'Point2(%s, %s)' % (self._x, self._y)


    #============================================================================

    # This section defines methods for vector arithmetic and comparison.
    # Operator overloading is established here.

    # Addition
    def add_point(self, other):
        """Vector addition
        :param: other: another Point2 object to add to this one
        :return: a point representing the sum of this point and the other
         """
        if isinstance(other, Point2):
            return Point2(self._x + other._x, self._y + other._y)


    def __add__(self, other):
        """Vector addition
        :param: other: another Point2 object to add to this one
        :return: a point representing the sum of this point and the other
         """
        if isinstance(other, Point2):
            return Point2(self._x + other._x, self._y + other._y)


    # Subtraction
    def sub_point(self, other):
        """Vector subtraction
        :param: other: another Point2 object to subtract from this one
        :return: a point representing the difference between this point and the other
         """
        if isinstance(other, Point2):
            return Point2(self._x - other._x, self._y - other._y)


    def __sub__(self, other):
        """Vector subtraction
        :param: other: another Point2 object to subtract from this one
        :return: a point representing the difference between this point and the other
         """
        if isinstance(other, Point2):
            return Point2(self._x - other._x, self._y - other._y)


    # Scaling operations.
    def scale_vector(self, scale_factor):
        """Scaling operations
        Note that the operator overloading cases
        must have the vector preceding the scaling factor!
        e.g.  vector * 1.2   or   vector / 3.2,  but not    1.2 * vector
        :param: scale_factor: the value to scale this vector by
        :return: a point representing the scaled version of this vector by scale_factor
         """
        return Point2( self._x * scale_factor, self._y * scale_factor)


    def __mul__(self, scale_factor):
        """Scaling operations
        Note that the operator overloading cases
        must have the vector preceding the scaling factor!
        e.g.  vector * 1.2   or   vector / 3.2,  but not    1.2 * vector
        :param: scale_factor: the value to scale this vector by
        :return: a point representing the scaled version of this vector by scale_factor
         """
        return Point2( self._x * scale_factor, self._y * scale_factor)


    def __div__(self, scale_factor):
        """Scaling: division operation
        :param: scale_factor: the value to divide this vector by
        :return: a point representing the scaled version of this vector by scale_factor
         """
        return Point2( self._x / scale_factor, self._y / scale_factor)


    # Comparisons.
    def same_point(self, other, tolerance=1e-03):
        """
        Returns true if the other point is within the specified tolerance
        :param other: another Point2 to compare to
        :param tolerance: the minimum distance to be considered the same point
        :return: True if the points are closer than the tolerance
                False if the points are further than the tolerance
        """
        return self.distance_to(other) < tolerance


    def equal(self, other):
        if isinstance(other, Point2):
            return (self._x == other._x) and (self._y == other._y)

    def not_equal(self, other):
        if isinstance(other, Point2):
            return (self._x != other._x) or (self._y != other._y)

    def __lt__(self, other):
        if isinstance(other, Point2):
            return self._x < other._x and self._y < other._y

    def __le__(self, other):
        if isinstance(other, Point2):
            return self._x <= other._x and self._y <= other._y

    def __eq__(self, other):
        if isinstance(other, Point2):
            return self.equal(other)

    def __ne__(self, other):
        if isinstance(other, Point2):
            return self.not_equal(other)

    def __gt__(self, other):
        if isinstance(other, Point2):
            return self._x > other._x and self._y > other._y

    def __ge__(self, other):
        if isinstance(other, Point2):
            return self._x >= other._x and self._y >= other._y

    #============================================================================

    def distance_to(self,o):
        """Determine the distance from this point to another point
        :param: o: other point to determine the distance to
        :return: a scalar representing the distance to from this point to the other
        """
        if( self.equal(o) ):
            return 0.0
        dx = self._x - o._x
        dy = self._y - o._y
        return ( dx*dx + dy*dy)**0.5


    def length(self):
        """Determine the scaler length of the vector. This uses the
        squareroot operation.
        :return: a scalar representing the length of this vector
        """
        return ( self._x*self._x + self._y*self._y)**0.5

    def distance_squared(self,o):
        """
        Length squared can sometimes be used in substitution for the scaler length
        of a vector. Length squared is much faster to calculate since there is
        no squareroot operation.
        :param: o: other point to determine the distance to
        :return: a scalar representing the square of the distance to from this point to o
        """
        dx = self._x - o._x
        dy = self._y - o._y
        return dx*dx + dy*dy

    def normal(self):
        """
        Returns a vector in the same direction as the
        original but with a length of 1 (unit length).
        :return: a vector in the same direction with a length of 1 (unit length).
        """
        return self / self.length()

    def set_magnitude(self, magnitude_target):
        """
        Returns a vector in the same direction as the
        original but with a length equal to the target magnitude.
        :return: a vector in the same direction with a length equal to the target magnitude.
        """
        return self.normal() * magnitude_target

    def dot(self, other):
        """
        Dot product with another vector.
        :param: other: another vector to take the dot product with respect to
        :return: a scalar representing  the dot product with another vector.
        """
        return (self._x * other._x) + (self._y * other._y)

    # The vector component of the self vector along the direction of the B vector.
    # (Refer to the drawings in the PDF.)
    def projection_onto(self, other):
        vB_dot_vB = other.dot(other)
        if (vB_dot_vB > 0):
            return other * ( self.dot(other) / vB_dot_vB )
        else:
            # If vec_B has zero magnitude, return a zero magnitude vector. In this
            # case, the dot product of the two vectors will be zero. This leaves the
            # projection undetermined; vec_B * (0/0). It would be appropriate to
            # return a None value here! But the zero magnitude vector is handy for
            # dealing with the spring-anchored pucks (because the separation distance
            # between the puck and the pinning point eventually goes to zero as the
            # disturbed puck loses energy). So again, it would be better to return a
            # None here and catch this in the code following the projection.
            return self * 0

    # Rotate 90 degrees counterclockwise.
    def rotate90(self):
        return Point2(-self._y, self._x)

    # Flip it around (reverse the direction of the vector).
    def rotate180(self):
        return Point2(-self._x, -self._y)

    # Rotate (change the direction of) the original vector by a specified number of degrees.
    # (Original vector rotated by angle_degrees.)
    def rotated(self, angle_degrees, sameVector=False):
        angle_radians = math.radians(angle_degrees)
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        # The rotation transformation.
        x = self._x * cos - self._y * sin
        y = self._x * sin + self._y * cos
        if sameVector:
            self._x = x
            self._y = y
        else:
            return Point2(x, y)

    # Set the direction of the vector to a specific angle.
    def set_angle(self, angle_degrees):
        self._x = self.length()
        self._y = 0
        return self.rotated(angle_degrees)

    # Determine the angle that this vector makes with the x axis. Measure
    # counterclockwise from the x axis.
    def get_angle(self):
        if (self.length_squared() == 0):
            return 0
        return math.degrees(math.atan2(self._y, self._x))

    # Determine the angle between two vectors.
    def get_angle_between(self, other):
        cross = self._x*other._y - self._y*other._x    #= ABsin(theta)
        dot   = self._x*other._x + self._y*other._y    #= ABcos(theta)
        # Use the two parameter input (y,x) form of the arctan. This is safer than
        # taking the arctan of the cross/dot which can be zero in the denominator.
        return math.degrees(math.atan2(cross, dot))

        # Return a tuple containing the two components of the vector.
    def tuple(self):
        return (self._x, self._y)

