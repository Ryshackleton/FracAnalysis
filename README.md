# FracAnalysis
## Summary
Some basic python tools for representing and analyzing fracture traces on 2D planes.  Includes functionality for finding lengths of fractures, intersections of fracture traces with other objects like straight and circular scan lines, and computing fracture intensity.  Very much a work in progress.

These python scripts were written to analyze the difference between fractures mapped in the field by a geologist, vs those mapped using only lower resolution imagery taken from a drone.  The work was a collaboration with Clare Bond from the University of Aberdeen and is outlined in [this abstract](http://www.searchanddiscovery.com/abstracts/html/2015/90216ace/abstracts/2099690.html) from the American Association of Petroleum Geologists 2015 Meeting and summarized below.

## General workflow
3D models of [the overall area](https://sketchfab.com/models/e3d1b9adf4f74492a265cdc9f95b27b6) and [detailed models of an area of interest](https://sketchfab.com/models/fecfd9ab629d4824ae95d8b9bbf68345) were created using photogrammetry from imagery taken using a small, consumer grade UAV.  The outcrops were located near Canajoharie, NY, USA and are located in the Flat Creek Shale.  From these models, we can generate orthorectified imagery such as the image below, with validated length scales based measured markers placed within the image.
#### Outline of fracture digitization for field mapping case, including optional creation of a simple 3D extrusion model of the fracture set.
![alt text](https://github.com/Ryshackleton/FracAnalysis/blob/master/FractureMapDigitization.png "Fracture Map Digitization Workflow")

The python scripts here were used to compute circular scanline analyses, which involves counting line-circle (fracture trace-circular scanline) intersections for circles of a given size.  We do this on a grid to compute fracture intensity, and then compare the results of fracture intensity mapped by a geologist in the field, vs those mapped by a geologist on a lower resolution image in the lab.

#### Detailed fracture map from field mapping by Thomas Wild (student):
![alt text](https://github.com/Ryshackleton/FracAnalysis/blob/master/FieldChecked_Thomas_Traces_Digitized.JPG "Fracture traces")

#### Fracture intensity from field mapped fracture traces, with a scale showing fracture length (meters) / fracture area (meters^2).  The point grid for computing circular scanlines is also shown, with an example of the circle size used for the computation).
![alt text](https://github.com/Ryshackleton/FracAnalysis/blob/master/FieldChecked_Thomas_intensity_1meter_circular_scans_grid.JPG "Fracture Intensity")
![alt text](https://github.com/Ryshackleton/FracAnalysis/blob/master/FractureLengthPerAreaScaleBar.JPG "Scale Bar for Fracture Intensity")

Feel free to use or modify these scripts, and please [email me](mailto:ryan@shackletoncomputing.com) with questions, comments, or suggestions.


