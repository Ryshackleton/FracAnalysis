# Filename: vec2d_jdm.py
# Author: James D. Miller; Gustavus Adolphus College.

# This Vec2D class is based on the vec2d class obtained here:
# http://karpathy.ca/phyces/tutorial1.php

import math

class Vec2D:
    # Components of the vector can be input as individual arguments or as
    # a tuple pair in one argument.
    def __init__(self, x_or_pair, y = None, int_flag = "not_int"):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

        if int_flag == "int":
            self.x = int(round(self.x))
            self.y = int(round(self.y))
        else:
            self.x = float(self.x)
            self.y = float(self.y)
        
    # This establishes the format of the output string if you print a vector (an object instance).
    def __str__(self):
        return 'Vec2D(%s, %s)' % (self.x, self.y)

    #============================================================================
    
    # This section defines methods for vector arithmetic and comparison. 
    # Operator overloading is established here.
    
    # Addition
    def add_vector(self, vec_B):
        return Vec2D(self.x + vec_B.x, self.y + vec_B.y)
    def __add__(self, vec_B):
        return Vec2D(self.x + vec_B.x, self.y + vec_B.y)
    
    # Subtraction
    def sub_vector(self, vec_B):
        return Vec2D(self.x - vec_B.x, self.y - vec_B.y)
    def __sub__(self, vec_B):
        return Vec2D(self.x - vec_B.x, self.y - vec_B.y)
    
    # Scaling operations. Note that the operator overloading cases
    # must have the vector preceeding the scaling factor!
    # e.g.  vector * 1.2   or   vector / 3.2,  but not    1.2 * vector
    def scale_vector(self, scale_factor):
        return Vec2D( self.x * scale_factor, self.y * scale_factor)
    def __mul__(self, scale_factor):
        return Vec2D( self.x * scale_factor, self.y * scale_factor)
    def __div__(self, scale_factor):
        return Vec2D( self.x / scale_factor, self.y / scale_factor)
    
    # Comparisons.
    def equal(self, vec_B):
        return (self.x == vec_B.x) and (self.y == vec_B.y)
    def not_equal(self, vec_B):
        return (self.x != vec_B.x) or (self.y != vec_B.y)
        
    #============================================================================
  
    # Determine the scaler length of the vector. This uses the
    # squareroot operation.
    def length(self):
        return (self.x*self.x + self.y*self.y)**0.5
    
    # Length squared can sometimes be used in substitution for the scaler length
    # of a vector. Length squared is much faster to calculate since there is
    # no squareroot operation.
    def length_squared(self):
        return (self.x*self.x + self.y*self.y)
    
    # Returns a vector in the same direction as the
    # original but with a length of 1 (unit length).
    def normal(self):
        #return self.scale_vector( 1/ self.length())
        return self / self.length()
    
    # Returns a vector in the same direction as the
    # original but with a length equal to the target magnitude.
    def set_magnitude(self, magnitude_target):
        return self.normal() * magnitude_target

    # Dot product with another vector.
    def dot(self, vec_B):
        return (self.x * vec_B.x) + (self.y * vec_B.y)
    
    # The vector component of the self vector along the direction of the B vector.
    # (Refer to the drawings in the PDF.)
    def projection_onto(self, vec_B):
        vB_dot_vB = vec_B.dot(vec_B)
        if (vB_dot_vB > 0):
            return vec_B * ( self.dot(vec_B) / vB_dot_vB )        
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
        return Vec2D(-self.y, self.x)
    
    # Flip it around (reverse the direction of the vector).
    def rotate180(self):
        return Vec2D(-self.x, -self.y)
    
    # Rotate (change the direction of) the original vector by a specified number of degrees.
    # (Original vector rotated by angle_degrees.)
    def rotated(self, angle_degrees, sameVector=False):
        angle_radians = math.radians(angle_degrees)
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        # The rotation transformation.
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        if sameVector:
            self.x = x
            self.y = y
        else:
            return Vec2D(x, y)
        
    # Set the direction of the vector to a specific angle.
    def set_angle(self, angle_degrees):
        self.x = self.length()
        self.y = 0
        return self.rotated(angle_degrees)
    
    # Determine the angle that this vector makes with the x axis. Measure
    # counterclockwise from the x axis.
    def get_angle(self):
        if (self.length_squared() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    
    # Determine the angle between two vectors.
    def get_angle_between(self, vec_B):
        cross = self.x*vec_B.y - self.y*vec_B.x    #= ABsin(theta)
        dot   = self.x*vec_B.x + self.y*vec_B.y    #= ABcos(theta)       
        # Use the two parameter input (y,x) form of the arctan. This is safer than
        # taking the arctan of the cross/dot which can be zero in the denominator.
        return math.degrees(math.atan2(cross, dot))  
        
    # Return a tuple containing the two components of the vector.
    def tuple(self):
        return (self.x, self.y)
    