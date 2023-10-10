def end_timing(iteration_start):
    """
    Description: calculates mean annual climate properties from a set of month-year climate rasters
    Inputs: 'iteration_start' -- an integer value of the number of years, which is the denominator in the mean calculation
    Returned Value: Returns a raster dataset on disk containing the mean annual climate property
    Preconditions: requires input month-year climate rasters that can be downloaded from SNAP at UAF
    """

    # Import packages
    import datetime
    import time

    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()
    # Report success
    print(
        f'Completed at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('----------')
