def raster_block_progress(detail, windows, count, progress):
    """
    Description: tracks progress of rasterio block processing
    Inputs: 'detail' -- an integer representing the number of reports to provide
            'windows' -- an integer representing the total number of windows to be processed
            'count' -- an iteration integer, which should be initialized at 1
            'progress' -- a progress integer, which should be initialized at 0
    Returned Value: returns a count
    Preconditions: requires a 
    """
    
    # Assign missing count
    try:
        count
    except:
        count = 1
    
    # Assign missing progress
    try:
        progress
    except:
        progress = 0
    
    # Assign previous progress
    previous_progress = progress
    
    # Report progress
    progress = int((int((count / windows) * detail) / detail) * 100)
    if (progress > previous_progress):
        print(f'\tProgress completed {progress}%...')
    
    # Increase count
    count += 1
    
    # Return count
    return count, progress
