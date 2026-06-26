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

# Define a function to read raster block
def read_raster_block(input_raster, window_bounds):
    """
    Description: reads a raster block using a pre-defined window with rasterio
    Inputs: 'input_raster' -- a raster object opened with rasterio
            'window_bounds' -- a pre-calculated window to read the raster data
    Returned Value: returns raster data for the window
    Preconditions: requires rasterio
    """
    # Import packages
    from rasterio.windows import from_bounds

    # Adapt input window to input raster
    input_window = from_bounds(
        *window_bounds,
        transform=input_raster.transform).round_offsets().round_lengths()

    # Read raster data within window
    output_block = input_raster.read(
        1,
        window=input_window,
        masked=False
    )

    # Return raster data
    return output_block
