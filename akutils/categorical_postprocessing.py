def apply_smoothing_filter(input_array, window_size=3, iterations=1, threshold=None, nodata_value=-128):
    """
    Smooths rasters by replacing pixels with the majority value of their neighborhood.
    Works for both binary and multi-categorical data using vectorized array shifting.

    Parameters:
    - input_array: 2D numpy array to be smoothed.
    - window_size: Odd integer (3, 5, 7) defining the grid size. 3 means 3x3 (9 pixels).
    - iterations: Number of times to run the filter. More passes = more organic rounding.
    - threshold: Minimum number of matching neighbors required to change a pixel.
                 If None, it defaults to a simple absolute majority.
    - nodata_value: Value used to pad the edges of the array.
    """
    # Import packages
    import numpy as np
    from scipy import stats

    # Raise an error for even window sizes
    if window_size % 2 == 0:
        raise ValueError("Window size must be an odd number (e.g., 3, 5, 7).")

    # Prepare the input data
    filtered_array = input_array.copy()
    pad_width = window_size // 2

    # Calculate simple majority threshold if none is provided
    if threshold is None:
        threshold = (window_size ** 2) // 2 + 1

    for _ in range(iterations):
        # Pad the array to prevent edge shrinking
        padded = np.pad(filtered_array, pad_width=pad_width, mode='constant', constant_values=nodata_value)

        # Dynamically build the shifted neighborhood arrays
        neighbors = []
        for i in range(window_size):
            for j in range(window_size):
                # Slice the shifted window to perfectly match original array dimensions
                neighbor = padded[i: i + filtered_array.shape[0], j: j + filtered_array.shape[1]]
                neighbors.append(neighbor)

        # Stack the arrays and calculate the mode across the Z-axis
        neighbors_stack = np.stack(neighbors, axis=0)
        mode_result = stats.mode(neighbors_stack, axis=0, keepdims=False)

        # Apply the replacement mask based on your threshold parameter
        replace_mask = (mode_result.count >= threshold)
        filtered_array = np.where(replace_mask, mode_result.mode, filtered_array)

    return filtered_array
