__author__ = 'ryshackleton'

import sys
from pprint import pprint
from MVE_importer import build_FracTraces, print_FracTraces
import FracTrace

def main(inputFileName,outputfilename,concatentationTolerance):
    """Creates FracTraces from lines in a file
     :param inputFileName : ascii text file of MVE exported lines to parse as fracture traces
     :param outputfilename: name of the output file to write the data to
     :param concatentationTolerance: distance tolerance to check for traces with similar endpoints
            and concatenate the traces if their endpoints are too close
     """
    try:
        tolerance = float(concatentationTolerance)
    except TypeError as e:
        print("Invalid tolerance: Tolerance must be a floating point number")
        return

    traces = build_FracTraces(inputFileName)

    # concatenate traces whose endpoints lie within the concatenationTolerance
    doubleCheck = True
    i = 0
    while doubleCheck == True:
        doubleCheck = False
        while i < len(traces)-1:
            j=i+1
            while j < len(traces):
                if traces[i].append_if_same_endpoints(traces[j],tolerance):
                    traces.pop(i+1)
                    doubleCheck == True
                    break
                j += 1
            i += 1

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

    with open(outputfilename,'w') as f:
        f.write('Name  Id   TraceLength\n')
        for t in traces:
            f.write('{} {}  {}\n'.format(t._traceName,t._traceId,t.get_trace_length2()))

        f.write('\n{} Trace Intersections:\n'.format(len(allIntersects)))
        for p in allIntersects:
            f.write('{} {} 0.0 Point2\n'.format(p._x, p._y))

#    print_FracTraces(traces)


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError as e:
        print("Incorrect command line arguments.")
        print("usage: TraceLengths InputFileName OutputFileName DistanceToleranceToConcatenateTraces")
