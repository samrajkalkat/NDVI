import gdal
from gdal import Open
from ndvi import ndvi

# Open NIR image and get its only band.
nir_tiff = Open(r'NIR_IMAGE.tif')
nir_band = nir_tiff.GetRasterBand(1)

# Open red image and get its only band.
red_tiff = Open(r'RED_IMAGE.tif')
red_band = red_tiff.GetRasterBand(1)

# Get the rows and cols from one of the images (both should always be the same)
rows, cols, geotransform = nir_tiff.RasterYSize, nir_tiff.RasterXSize, nir_tiff.GetGeoTransform()
print(geotransform)

# Set the output for a 32-bit floating point (-1 to 1)
out_tiff_float32 = r'NDVI_FLOAT32.tif'


# Run the function for 32-bit floating point
ndvi(nir_band, red_band, rows, cols, geotransform, out_tiff_float32, gdal.GDT_Float32)

print('done')