__author__ = 'ryshackleton'

import sys
from Point import Point2
import math
from StraightLine2 import StraightLine2

class FracTrace():
    """Models a fracture trace in 2D or 3D."""

    def __init__(self, traceId=-1, traceName="", coordinatePlane=(0.0,0.0,0.0), vlist3=[ () ]):
        """
        Initializes a FracTrace

        :param traceId: Integer Id of the trace
        :param traceName: Name string of the trace
        :param coordinatePlane: tuple representing the normal of the coordinate plane in which the FracTrace exists
        :param vlist3: list of tuples representing the 3d vertices of the fracture trace

        :type _vlist3 = list of tuples representing the original 3D coordinates of the FracTrace
        :type _vlist2 = list of tuples representing the 2D coordinates of the FracTrace projected to the coordinatePlane
        """
        try:
            self._traceId = int(traceId)
            self._traceName = traceName
            self._coordinatePlane = coordinatePlane
            self._vlist3 = vlist3
            self._vlist2 = []
            self._ptype = []
            self._colorindex = []
            self._colornum = []
            self._rvalue = []
            self._gvalue = []
            self._bvalue = []
            self._segmentList = []
        except (ValueError,TypeError) as e:
            print("Conversion error: {}" \
                  .format(str(e)),file=sys.stderr)


    def build_circular_trace(self,centerx,centery,radius,numpoints):
        '''
        Builds a circular fracture trace
        :param centerx: X coordinate of the center of the circle
        :param centery: Y coordinate of the center of the circle
        :param radius: Radius of the circle
        :param numpoints: number of vertices in the circle
        :return:
        '''

        if numpoints < 4:
            raise ValueError("FracTrace.build_circular_trace(...,numpoints) cannot build a circle with less than 4 pts")

        inc = 2.0 * math.pi / (numpoints - 1)
        rad = 0.0
        i=0
        while i <= numpoints:
            xcoord = centerx + radius * math.cos(rad)
            ycoord = centery + radius * math.sin(rad)
            self._vlist2.append(Point2(xcoord,ycoord))
            self.append_vertex3((xcoord,ycoord,0.0))
            rad += inc
            i += 1

    def append_vertex3(self, vertex):
        """ appends a 3d vertex to the frac trace object
        :param vertex: a tuple representing the cartesian coordinates of the vertex to be appended
        :param color: a color ID or tuples indicating RGB values
        :return:
        :except: raises an invalid index exception of the length of the tuple is not 3
        """
        if( len(vertex) != 3 ):
            raise IndexError
        self._vlist3.append(vertex)

    def append_ptype(self, ptype):
        self._ptype.append(ptype)

    def append_color_index(self, color):
        self._colorindex.append(color)

    def append_color_num(self, color):
        self._colornum.append(color)

    def append_color_R(self, r):
        self._rvalue.append(r)

    def append_color_G(self, g):
        self._gvalue.append(g)

    def append_color_B(self, b):
        self._bvalue.append(b)

    def pop_all(self):
        '''
        Pops one 'entry off of all of the lists'
        :return:
        '''
        self._vlist3.pop()
        self._vlist2.pop()
        self._ptype.pop()
        self._colorindex.pop()
        self._colornum.pop()
        self._rvalue.pop()
        self._gvalue.pop()
        self._bvalue.pop()

    def reverse_all(self):
        '''
        reverses all the lists in this entry
        :return:
        '''
        self._vlist3.reverse()
        self._vlist2.reverse()
        self._ptype.reverse()
        self._colorindex.reverse()
        self._colornum.reverse()
        self._rvalue.reverse()
        self._gvalue.reverse()
        self._bvalue.reverse()

    def extend_other_lists(self,o):
        '''
        Appends all lists in the specified fracture trace to the end of all lists in THIS fracture trace
        :param o: other FracTrace to append items from
        :return:
        '''
        if not isinstance(o,FracTrace):
            raise TypeError

        self._vlist3.extend(o._vlist3)
        self._vlist2.extend(o._vlist2)
        self._ptype.extend(o._ptype)
        self._colorindex.extend(o._colorindex)
        self._colornum.extend(o._colornum)
        self._rvalue.extend(o._rvalue)
        self._gvalue.extend(o._gvalue)
        self._bvalue.extend(o._bvalue)

    def is_endpoint(self, o, tol):
        '''
        Checks if the specified point is an endpoint
        :param o: another Point2 to check for endpointness
        :param tol: distance tolerance to check the specified point for
        :return: None if point o is not an endpoint,
                the index of the matching endpoint in this FracTrace if o lies within the distance tolerance of an endpoint
        '''
        if len(self._vlist2) < 1:
            return None
        if len(self._vlist2) < 1:
            return None
        if self._vlist2[0].same_point(o,tol):
            return 0
        if self._vlist2[len(self._vlist2)-1].same_point(o,tol):
            return len(self._vlist2)-1
        return None

    def build_segments(self):
        '''
        builds the _segmentList variable for later use
        :return:
        '''
        self._segmentList = self.to_segments()

    def to_segments(self):
        '''
        returns a list of StraightLine2 objects representing this line as a list of straight line segments
        :return: A list of segments representing this line
        '''
        segs = []
        i = 1
        while i < len(self._vlist2):
            segs.append(StraightLine2(self._vlist2[i-1]._x, self._vlist2[i-1]._y, \
                                       self._vlist2[i]._x, self._vlist2[i]._y ))
            i += 1
        return segs


    def trace_length_inside_circular_scanline(self,circularSegs,circleCenter,radius,tol=1e-03):
        if not isinstance(circleCenter,Point2):
            raise TypeError("FracTrace.trace_length_inside_circular_frac_trace() can only operate on a Point2")

        # get segment list, don't modify self
        mySegs = []
        if len(self._segmentList) == 0:
            mySegs = self.to_segments()
        else:
            mySegs = self._segmentList

        # check for segments inside the circle
        segList = [] # list of disconnected segments inside the circle to measure the length of
        for m in mySegs:
            # intersection test:
            # the segment must lie within or intersect the circle if the closest point of this segment
            # to the circle's center lies within the circle's radius
            closePt = m.closestPoint(circleCenter)
            if m._v0.distance_to(closePt) <= radius:
                isV0in = m._v0.distance_to(circleCenter) <= radius
                isV1in = m._v1.distance_to(circleCenter) <= radius
                if isV0in and isV1in: # both inside, just add the segment
                    segList.append(m)
                else: # otherwise, find some intersections
                    spanPt = None
                    for o in circularSegs: # find the intersection point with the circle
                        traceIntersects = m.intersectionPoints(o,tol)
                        if len(traceIntersects) == 1:
                            iPt = traceIntersects[0]
                            if isV0in: # v0 in, v1 out - add segment from intersection & v0
                                segList.append(StraightLine2(iPt._x,iPt._y, m._v0._x,m._v0._y))
                            elif isV1in:# v1 in, v0 out - add segment from intersection & v1
                                segList.append(StraightLine2(iPt._x,iPt._y, m._v1._x,m._v1._y))
                            elif spanPt == None: # handle the odd case of a line with endpoints outside,
                                                 # but an intersection inside
                                                 # (assume that we'll hit the other intersection later in the loop)
                                spanPt = iPt
                            else:
                                segList.append(StraightLine2(iPt._x,iPt._y, spanPt._x,spanPt._y))
                                spanPt = None
                        elif len(traceIntersects) > 1:
                            raise ValueError("WTF IS HAPPENING????")

        # sum up lengths
        sumLen = 0.0
        for s in segList:
            sumLen += s._v0.distance_to(s._v1)

        return sumLen


    def intersection_points_with_trace(self, ot, tol=1e-03):
        '''
        Returns a list of Point2's representing the intersection points of this FracTrace with another FracTrace
        :param ot: Other FracTrace to intersect with
        :param tol: Tolerance used for determining distance tolerances
        :return: list(Point2()) representing the 2d intersections of this FracTrace with another FracTrace
        '''
        if not isinstance(ot,FracTrace):
            raise TypeError("FracTrace.intersectionPoints() can only operate on another FracTrace")
        mySegs = self.to_segments()
        otSegs = ot.to_segments()

        traceIntersects = []
        for m in mySegs:
            for o in otSegs:
                traceIntersects.extend(m.intersectionPoints(o,tol))

        return traceIntersects


    def append_if_same_endpoints(self, ot, tol):
        """appends another trace to this trace if one or more of the endpoints
            lie within the specified distance tolerance of one another
            NOTE: this will delete the duplicate endpoint from this trace if the endpoints lie within the tolerance
        :param: o: the other trace to append to this trace
        :param: tol: distance tolerance for endpoint checking
        :return: True if an appendage was made, False if no match and no appendage was made
        """
        if not isinstance(ot,FracTrace):
            raise TypeError
        if len(ot._vlist2) == 0:
            return

        # beginning of other trace matches
        oi = self.is_endpoint(ot._vlist2[0], tol)
        if oi == None:
            # no match, check if tail of other trace matches
            oi = self.is_endpoint(ot._vlist2[len(ot._vlist2)-1], tol)
            if oi == None:
                return False
            elif oi == 0:
                self.reverse_all()
                self.pop_all()
                ot.reverse_all()
                self.extend_other_lists(ot)
                self._traceName += '_JOIN_' + ot._traceName
                return True
            elif oi > 0:
                self.pop_all()
                ot.reverse_all()
                self.extend_other_lists(ot)
                self._traceName += '_JOIN_' + ot._traceName
                return True
        elif oi == 0:
            self.reverse_all()
            self.pop_all()
            self.extend_other_lists(ot)
            self._traceName += '_JOIN_' + ot._traceName
            return True
        elif oi > 0:
            self.pop_all()
            self.extend_other_lists(ot)
            self._traceName += '_JOIN_' + ot._traceName
            return True
        return False

    def get_trace_length2(self):
        """returns the 2D length of the trace by summing up each segment length
        :return: length of this line segment
        """
        flen = 0.0
        last = None
        for v in self._vlist2:
            if( last == None ):
                last = v
                continue
            flen += v.distance_to(last)
            last = v
        return flen


    def build_vlist2(self):
        """Does the 3D to 2D conversion by projecting the vlist3 to the coordinate plane
        and building the _vlist2 vector
        """
        try:
            # simple case of map view where, coordinatePlane == 1 or -1 and z coordinates all == 0.0
            if (0.0,0.0,1.0) == self._coordinatePlane or (0.0,0.0,-1.0) == self._coordinatePlane:
                for vertex in self._vlist3:
                    self._vlist2.append(Point2( vertex[0] , vertex[1] ) )
            else:
                pass
                #TODO: implement generalized projection onto 3d planes

        except TypeError as e:
            print("Conversion error in _build_vlists (non-numeric type in the vertex list??) {}" \
                  .format(str(e)),file=sys.stderr)

    #============================================================================

    # This section defines methods for
    # operator overloading so we can use .index() functions and others
    def __lt__(self, other):
        return self._traceId < other._traceId

    def __le__(self, other):
        return self._traceId <= other._traceId

    def __eq__(self, other):
        return self._traceId == other._traceId

    def __cmp__(self, other):
        if self._traceId < other._traceId:
            return -1
        elif self._traceId == other._traceId:
            return 0
        else:
            return 1

    def __ne__(self, other):
        return self._traceId != other._traceId

    def __gt__(self, other):
        return self._traceId  > other._traceId

    def __ge__(self, other):
        return self._traceId  >= other._traceId

