#!/usr/bin/env python3

__author__ = 'ryshackleton'

import sys
from pprint import pprint
from FracTrace import FracTrace


def read_exported_mve_lines(filename):
    with open(filename, mode='rt', encoding='utf-8') as f:
        return [line.strip().split('\t') for line in f if len(line.strip()) > 0 ]


def build_FracTraces(filename):
    """Builds and returns a list of FracTrace() objects from an MVE file
    :return  [ FracTrace(), FracTrace(), ... ]
    """
    lines = read_exported_mve_lines(filename)
    fracTraceList = []
    # find the indices of x, y, z, etc in each row of the file
    xi = yi = zi = namei = idi = colori = -1
    try:
        if( len(lines) > 0 ):
            header = lines[0]
            xi = header.index('x')
            yi = header.index('y')
            zi = header.index('z')
            namei = header.index('Name')
            idi = header.index("Id")
            ptypei = header.index("PType")
            colori = header.index("Colour Id")
            colorni = header.index("Colour Num")
            colorRi = header.index("Colour (red)")
            colorGi = header.index("Colour (green)")
            colorBi = header.index("Colour (blue)")
    except ValueError as e:
        if xi == -1 \
                or yi == -1 \
                or zi == -1 \
                or idi == -1 \
                or namei == -1:
            errorm ="Invalid header, header should contain AT LEAST the following tab separated items in any order\n" \
                    "x    y   z   Name    Id\n" \
                    "Header can contain ANY of the following tab separated items in any order\n" \
                    "x    y   z   Name    Id    PType   Colour Num  Colour Id   Colour (red)" \
                    "Colour (green)  Colour (blue)"
            print(errorm)

    #TODO: determine the normal vector for the fracture traces
    planeNormal = (0.0,0.0,1.0)

    for l in lines:
        try:
            # skip the header line
            if( not( l[idi].isnumeric() ) ):
                continue

            # find the FracTrace that we're working on if it exists
            thisTrcI = -1
            try:
                # overloaded __eq__ operator finds using id
                thisTrcI = fracTraceList.index(FracTrace(l[idi]))
            except ValueError as e: # if not found, add the trace
                fracTraceList.append( FracTrace( l[idi], l[namei], planeNormal,
                                                 [(l[xi], l[yi], l[zi])] ) )
                thisTrcI = fracTraceList.index(FracTrace(l[idi]))

            thisTrc = fracTraceList[thisTrcI]

            # append all of the xyz and other attributes
            if( xi != -1 and yi != -1 and zi != -1):
                thisTrc.append_vertex3( (l[xi], l[yi], l[zi]) )
            if colorni > 0:
                thisTrc.append_color_num(l[colorni])
            if colori > 0:
                thisTrc.append_color_index(l[colori])
            if colorRi > 0:
                thisTrc.append_color_R(l[colorRi])
            if colorGi > 0:
                thisTrc.append_color_G(l[colorGi])
            if colorBi > 0:
                thisTrc.append_color_B(l[colorBi])
            if ptypei > 0:
                thisTrc.append_ptype(l[ptypei])

        except IndexError as e:
            print("Problem creating fracture traces in build_FracTraces")
        except ValueError as e:
            print("TraceId not found for {}".format(l))

    # do the 3D -> 2D transformation of vertices
    for frac in fracTraceList:
        frac.build_vlist2()

    return fracTraceList

def print_FracTraces(fracTraces=[]):
    """Prints the fracture traces to the stdout
    :param: fracTraces  dict where: key=id : FracTrace()
    """
    for frac in fracTraces:
        #        pprint("{}   {}  vlist3: {}".format(frac._traceId,frac._traceName,frac._vlist3) )
        pprint("Trace Length for trace {} = {}".format(frac._traceName,frac.get_trace_length2()))
        for vertex in frac._vlist2:
            print("Point2({},{})".format(vertex._x,vertex._y))


def main(filename):
    try:
        series = read_exported_mve_lines(filename)
        pprint(series)
    except (FileExistsError, FileNotFoundError):
        print("File '{}' not found or doesn't exist:".format(filename))
        print("usage: python3 MVE_importer filename.")

if __name__ == '__main__':
    main(sys.argv[1])

