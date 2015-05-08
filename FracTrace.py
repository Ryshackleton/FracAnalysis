__author__ = 'ryshackleton'

import sys
import Point

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
        except (ValueError,TypeError) as e:
            print("Conversion error: {}" \
                  .format(str(e)),file=sys.stderr)

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

    def append_trace(self, o):
        """appends another trace to this trace in its entirety to the end of this trace
        :param: o: the other trace to append to this trace
        """
        if not isinstance(o,FracTrace):
            raise TypeError

            self._traceName += o._traceName
            if self._vlist2[ len(self._vlist2)-1 ].same_point(o):
                pass


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
                    self._vlist2.append( Point.Point2( vertex[0] , vertex[1] ) )
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

"""
#define SMALL_NUM   0.00000001 // anything that avoids division overflow
// dot product (3D) which allows vector operations in arguments
#define dot(u,v)   ((u).x * (v).x + (u).y * (v).y + (u).z * (v).z)
#define perp(u,v)  ((u).x * (v).y - (u).y * (v).x)  // perp product  (2D)



// intersect2D_2Segments(): find the 2D intersection of 2 finite segments
//    Input:  two finite segments S1 and S2
//    Output: *I0 = intersect point (when it exists)
//            *I1 =  endpoint of intersect segment [I0,I1] (when it exists)
//    Return: 0=disjoint (no intersect)
//            1=intersect  in unique point I0
//            2=overlap  in segment from I0 to I1
int
intersect2D_2Segments( Segment S1, Segment S2, Point* I0, Point* I1 )
{
    Vector    u = S1.P1 - S1.P0;
    Vector    v = S2.P1 - S2.P0;
    Vector    w = S1.P0 - S2.P0;
    float     D = perp(u,v);

    // test if  they are parallel (includes either being a point)
    if (fabs(D) < SMALL_NUM) {           // S1 and S2 are parallel
        if (perp(u,w) != 0 || perp(v,w) != 0)  {
            return 0;                    // they are NOT collinear
        }
        // they are collinear or degenerate
        // check if they are degenerate  points
        float du = dot(u,u);
        float dv = dot(v,v);
        if (du==0 && dv==0) {            // both segments are points
            if (S1.P0 !=  S2.P0)         // they are distinct  points
                 return 0;
            *I0 = S1.P0;                 // they are the same point
            return 1;
        }
        if (du==0) {                     // S1 is a single point
            if  (inSegment(S1.P0, S2) == 0)  // but is not in S2
                 return 0;
            *I0 = S1.P0;
            return 1;
        }
        if (dv==0) {                     // S2 a single point
            if  (inSegment(S2.P0, S1) == 0)  // but is not in S1
                 return 0;
            *I0 = S2.P0;
            return 1;
        }
        // they are collinear segments - get  overlap (or not)
        float t0, t1;                    // endpoints of S1 in eqn for S2
        Vector w2 = S1.P1 - S2.P0;
        if (v.x != 0) {
                 t0 = w.x / v.x;
                 t1 = w2.x / v.x;
        }
        else {
                 t0 = w.y / v.y;
                 t1 = w2.y / v.y;
        }
        if (t0 > t1) {                   // must have t0 smaller than t1
                 float t=t0; t0=t1; t1=t;    // swap if not
        }
        if (t0 > 1 || t1 < 0) {
            return 0;      // NO overlap
        }
        t0 = t0<0? 0 : t0;               // clip to min 0
        t1 = t1>1? 1 : t1;               // clip to max 1
        if (t0 == t1) {                  // intersect is a point
            *I0 = S2.P0 +  t0 * v;
            return 1;
        }

        // they overlap in a valid subsegment
        *I0 = S2.P0 + t0 * v;
        *I1 = S2.P0 + t1 * v;
        return 2;
    }

    // the segments are skew and may intersect in a point
    // get the intersect parameter for S1
    float     sI = perp(v,w) / D;
    if (sI < 0 || sI > 1)                // no intersect with S1
        return 0;

    // get the intersect parameter for S2
    float     tI = perp(u,w) / D;
    if (tI < 0 || tI > 1)                // no intersect with S2
        return 0;

    *I0 = S1.P0 + sI * u;                // compute S1 intersect point
    return 1;
}
//===================================================================



// inSegment(): determine if a point is inside a segment
//    Input:  a point P, and a collinear segment S
//    Return: 1 = P is inside S
//            0 = P is  not inside S
int
inSegment( Point P, Segment S)
{
    if (S.P0.x != S.P1.x) {    // S is not  vertical
        if (S.P0.x <= P.x && P.x <= S.P1.x)
            return 1;
        if (S.P0.x >= P.x && P.x >= S.P1.x)
            return 1;
    }
    else {    // S is vertical, so test y  coordinate
        if (S.P0.y <= P.y && P.y <= S.P1.y)
            return 1;
        if (S.P0.y >= P.y && P.y >= S.P1.y)
            return 1;
    }
    return 0;
}
//===================================================================
"""
