import numpy as np
from numpy import nan_to_num, subtract, add, divide, multiply
from osgeo import gdal, gdalconst
from gdal import GetDriverByName


def ndvi(in_nir_band, in_colour_band, in_rows, in_cols, in_geotransform, out_tiff, data_type=gdal.GDT_Float32):

    # Read the input bands as numpy arrays.
    np_nir = in_nir_band.ReadAsArray(0, 0, in_cols, in_rows)
    np_colour = in_colour_band.ReadAsArray(0, 0, in_cols, in_rows)

    # Convert the np arrays to 32-bit floating point to make sure division will occur properly.
    np_nir_as32 = np_nir.astype(np.float32)
    np_colour_as32 = np_colour.astype(np.float32)

    # Calculate the NDVI formula.
    numerator = subtract(np_nir_as32, np_colour_as32)
    denominator = add(np_nir_as32, np_colour_as32)
    result = divide(numerator, denominator)

    # Remove any out-of-bounds areas
    result[result == -0] = -99

    # Initialize a geotiff driver.
    geotiff = GetDriverByName('GTiff')

    # create a float32 geotiff with one band and
    # write the contents of the float32 NDVI calculation to it.
    if data_type == gdal.GDT_Float32:
        output = geotiff.Create(out_tiff, in_cols, in_rows, 1, gdal.GDT_Float32)
        output_band = output.GetRasterBand(1)
        output_band.SetNoDataValue(-99)
        output_band.WriteArray(result)
    else:
        raise ValueError('Invalid output data type.  Valid types are gdal.UInt16 or gdal.Float32.')

    # Set the geographic transformation as the input.
    output.SetGeoTransform(in_geotransform)

    return None

