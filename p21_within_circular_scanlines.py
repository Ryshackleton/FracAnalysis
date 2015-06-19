__author__ = 'ryshackleton'

import sys
import math
from pprint import pprint
import MVE_importer
import Point2_MVE
from FracTrace import FracTrace

def main(fractureTraceFileName,gridFileName,fractureIntersectionsPerAreaRadius,outputFileName):
    '''
    Computes fracture length/area (p21) for any number of circular scanlines
        -fractures are specified as 1D traces on a planar 2D surface (currently limited to map view)
        -circular scanlines are usually specified as a grid of points with a specified radius, but can be any points
    :param fractureTraceFileName: filename of a Midland Valley-Move software export
                                    representing lines representing fracture traces
    :param gridFileName: file containing a Midland Valley-Move software export of points representing the grid
                            over which to compute the intersections per area
    :param fractureIntersectionsPerAreaRadius: radius of a circle to search within
    :param outputFileName: name of the output file to write the grid points with fracture length/area within the
                            specified radius
    :return: nothing
    '''

    # ---------------------------------
    # argument checking
    try:
        radius = float(fractureIntersectionsPerAreaRadius)
    except TypeError as e:
        print("Invalid fractureIntersectionsPerAreaRadius: The radius must be a floating point number")
        return
    circleArea = math.pi * radius * radius
    if circleArea < 0.0:
        raise ZeroDivisionError('Circle radius must be non-zero')

    # ---------------------------------
    # file import
    traces = MVE_importer.build_FracTraces(fractureTraceFileName)
    gridPoints = MVE_importer.build_point_list(gridFileName)

    # ---------------------------------
    # do intersection calculations and find P21
    # sum up fracture length inside a circular scanline whose center is at each grid point and whose radius is specified
    for pt in gridPoints:
        circularScanline = FracTrace(0,"CircularScanline")
        circularScanline.build_circular_trace(pt._x,pt._y,radius,20)
        circularScanline.build_segments()

        pt._otherfloat = 0.0
        for trace in traces:
            trace.build_segments()
            pt._otherfloat += trace.trace_length_inside_circular_scanline(circularScanline._segmentList,pt,radius)

        # calculate fracture length/area (p21)
        pt._otherfloat /= circleArea


    # ---------------------------------
    # write the output file
    with open(outputFileName,'w') as f:
        f.write('x	y	z	Name	Id	PType	Colour_Num	Colour_Id	Colour_(red)	Colour_(green)	Colour_(blue)')
        f.write('   NothingAttribute    FractureLengthPerArea{}\n'.format(radius))
        for pt in gridPoints:
            f.write(pt.to_string() + '\n')


if __name__ == '__main__':
    try:
        main( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )
    except IndexError:
        print("Incorrect command line arguments.")
        print("usage: p21_within_circular_scanlines.py fractureTraceFileName gridFileName radius_in_meters outputFileName")
