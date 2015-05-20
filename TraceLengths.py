__author__ = 'ryshackleton'

import sys
from pprint import pprint
from MVE_importer import build_FracTraces, print_FracTraces

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

    with open(outputfilename,'w') as f:
        f.write('Name  Id   TraceLength\n')
        for t in traces:
            f.write('{} {}  {}\n'.format(t._traceName,t._traceId,t.get_trace_length2()))

#    print_FracTraces(traces)


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError as e:
        print("Incorrect command line arguments.")
        print("usage: TraceLengths InputFileName OutputFileName DistanceToleranceToConcatenateTraces")
