from _ast import Set

___author__ = 'ryshackleton'

import math
from Point import Point2

class StraightLine2:
    """Models a line segment in 2D"""

    def __init__(self, v0x=0.0, v0y=0.0, v1x=0.0, v1y=0.0):
        """
        Initializes a 2d point
        :param v0: Point2 representing the first point
        :param v1: Point2 representing the second point
        :return: None
        """
        self._v0 = Point2(v0x,v0y)
        self._v1 = Point2(v1x,v1y)

    def isEndPoint(self,o,tol):
        if self._v0.same_point(o,tol):
            return True
        if self._v1.same_point(o,tol):
            return True
        return False


    def minimumDistance(self,p, tolerance=1e-03):
        '''
        Returns the minimum distance of the specified point to this line segment
        :param p: Point2 to return the distance to
        :param tolerance: necessary tolerance for determining whether point's perpendicular distance is 0. or not
        :return: the minimum distance to this point
        '''
        d = (self._v1._x-self._v0._x)*(self._v1._x-self._v0._x) + \
            (self._v1._y-self._v0._y)*(self._v1._y-self._v0._y)
        n = (self._v1._x-self._v0._x)*(p._x-self._v0._x) + \
            (self._v1._y-self._v0._y)*(p._y-self._v0._y)

        t = n / d
        min_dist = None
        if t > 0.0 and (t-1.0) < tolerance:
            p0v = Point2(self._v1,self._v0)
            pv = Point2(p._x,p._y)
            pt = ((self._v1 - self._v0) * t ).add_point(p0v)
            min_dist = (pt - pv).length()
        else:
            min_dist = min(self._v0.distance_to(p),self._v1.distance_to(p))
        return min_dist;


    def intersectionPoints(self,line,tolerance=1e-03):
        '''
        Checks for intersections of this segment with another segment
        :param line: the other line to be checked against
        :param tolerance: distance tolerance for sameness of points
        :return: a list of Point2 objects representing line intersections with this segment
        '''

        intersectionPoints = []

        # coor values
        xlk = self._v1._x - self._v0._x
        xnm = line._v1._x - line._v0._x
        xmk = line._v0._x - self._v0._x
        ylk = self._v1._y - self._v0._y
        ynm = line._v1._y - line._v0._y
        ymk = line._v0._y - self._v0._y

        s = 0.0
        t = 0.0
        denom = xnm*ylk - xlk*ynm
        if math.fabs (denom) > tolerance:
            s = (xnm*ymk - xmk*ynm) / denom
            t = (xlk*ymk - ylk*xmk) / denom
        else: # parallel lines
            # test if line end-points lies on this line
            if self.isEndPoint(line._v0,tolerance):
                intersectionPoints.append(Point2(line._v0))
            # test if line end-points lies on this line
            if self.isEndPoint(line._v1,tolerance):
                intersectionPoints.append(Point2(line._v1))
            return intersectionPoints

        # no intersection
        if (s<0.0 or t<0.0 or s>1.0 or t>1.0):
            return intersectionPoints

        # intersection (pt. of intersection, use s)
        int_pt = Point2(self._v0._x+(self._v1._x-self._v0._x)*s,
                       self._v0._y+(self._v1._y-self._v0._y)*s)
        intersectionPoints.append(int_pt)

        return intersectionPoints


    # This establishes the format of the output string if you print a vector (an object instance).
    def __str__(self):
        return 'StraightLine2(%s, %s : %s, %s)' % (self._v0._x, self._v0._y,self._v1._x, self._v1._y,)

