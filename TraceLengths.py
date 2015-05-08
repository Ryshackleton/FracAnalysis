__author__ = 'ryshackleton'

import sys
from pprint import pprint
from MVE_importer import build_FracTraces, print_FracTraces

def main(filename,outputfilename):
    """Creates FracTraces from lines in a file
     :param filename : ascii text file of MVE exported lines to parse as fracture traces
     """

    traces = build_FracTraces(filename)

    with open(outputfilename,'w') as f:
        f.write('Name  Id   TraceLength\n')
        for t in traces:
            f.write('{} {}  {}\n'.format(t._traceName,t._traceId,t.get_trace_length2()))

#    print_FracTraces(traces)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
