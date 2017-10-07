# paleogeography
code for processing gplates-format paleogeographies

The notebooks contain examples of:
- extracting paleoshorelines from a set of polygons that describe environments either above (land, 
mountain) or below (shallow marine, deep marine) sea-level

- interpolating paleoshorelines at different times by 'tweening' between the polygon geometries at two 
times bracketing a time range

- make a cross-section visualisation through a paleogeography/tectonic reconstruction, showing the locations
of land masses, oceans, plate boundaries that the cross-section lines transects

Most of the low level code is contained in the .py files. These functions must be available to be imported 
into the notebooks. 

dependencies:
pygplates, numpy, matplotlib, basemap, xarray, scikit-image
gmt v5.x (tested with v5.4.1)

The examples are generally designed to run on the paleogeography polygons from Cao et al (in review),
the files are available in the zip supplement linked to on this page:
https://www.biogeosciences-discuss.net/bg-2017-94/
