__author__ = 'ryshackleton'

from Point import Point2

class Point2_MVE(Point2):
    '''
    Models a point with some extra crap from the MVE file
    '''
    def __init__(self, x=0.0, y=0.0 ):
        super().__init__(x,y)
        self._z = float(0.0)
        self._traceId = 0
        self._Name = ''
        self._ptype = 0
        self._colorindex = 0
        self._colornum = 0
        self._rvalue = 255
        self._gvalue = 255
        self._bvalue = 255
        self._otherint  = 0
        self._otherfloat = 0.0

    def to_string(self):
        # 'x	y	z	Name	Id	PType	Colour Num	Colour Id	Colour (red)	Colour (green)	Colour (blue)')
        str = '{}   {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}'.format(self._x,self._y,self._z,
                                                                       self._Name,self._traceId,self._ptype,
                                                                       self._colornum,self._colorindex,
                                                                       self._rvalue,self._gvalue,self._bvalue,
                                                                       self._otherint,
                                                                       self._otherfloat)
        return str


