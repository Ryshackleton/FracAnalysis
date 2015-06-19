__author__ = 'ryshackleton'

import sys
from pprint import pprint
import MVE_importer
import Point2_MVE
import FracTrace

def main(fractureTraceFileName,gridFileName,fractureIntersectionsPerAreaRadius,outputFileName):
    '''
    Computes fractures/area on a specified grid from a 2D map view of fracture traces
    :param fractureTraceFileName: filename of a Midland Valley-Move software export
                                    representing lines representing fracture traces
    :param gridFileName: file containing a Midland Valley-Move software export of points representing the grid
                            over which to compute the intersections per area
    :param fractureIntersectionsPerAreaRadius: radius of a circle to search within
    :param outputFileName: name of the output file to write the grid points with number of intersections within the
                            specified radius
    :return: nothing
    '''
    tolerance = 1e-03
    try:
        radius = float(fractureIntersectionsPerAreaRadius)
    except TypeError as e:
        print("Invalid fractureIntersectionsPerAreaRadius: The radius must be a floating point number")
        return

    traces = MVE_importer.build_FracTraces(fractureTraceFileName)
    gridPoints = MVE_importer.build_point_list(gridFileName)

#    doubleCheck = True
#    i = 0
#    while doubleCheck == True:
#        doubleCheck = False
#        while i < len(traces)-1:
#            j=i+1
#            while j < len(traces):
#                if traces[i].append_if_same_endpoints(traces[j],tolerance):
#                    traces.pop(i+1)
#                    doubleCheck == True
#                    break
#                j += 1
#            i += 1

    # find all intersection points
    allIntersects = []
    i = 0
    while i < len(traces):
        j = i+1
        while j < len(traces):
            pts = traces[i].intersection_points_with_trace(traces[j])
            for p in pts:
                if p not in allIntersects:
                    allIntersects.append(p)
            j += 1
        i += 1

    # count intersections within the specified radius for each grid point
    for pt in gridPoints:
        for ipt in allIntersects:
            if pt.distance_to(ipt) < radius:
                pt._otherint += 1

    with open(outputFileName,'w') as f:
        f.write('x	y	z	Name	Id	PType	Colour_Num	Colour_Id	Colour_(red)	Colour_(green)	Colour_(blue)')
        f.write('   IntersectionsWithin{}\n'.format(radius))
        for pt in gridPoints:
            f.write(pt.to_string() + '\n')


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4])
    except IndexError as e:
        print("Incorrect command line arguments.")
        print("usage: FractureIntersectionsPerRadius fractureTraceFileName gridFileName radius_in_meters outputFileName")
