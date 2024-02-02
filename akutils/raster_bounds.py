def raster_bounds(area_file):
    """
    Description: calculates bounds of a raster using rasterio
    Inputs: 'area_file' -- file path to the raster from which to calculate bounds
    Returned Value: returns raster bounds
    Preconditions: requires rasterio
    """
    # Import packages
    import rasterio

    # Get the bounds for the area of interest
    with rasterio.open(area_file) as area_raster:
        area_bounds = area_raster.bounds
        area_raster.close()

    # Return bounds
    return area_bounds
