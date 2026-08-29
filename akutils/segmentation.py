def merge_spectral(clusters, segmentation_image, threshold=0.005):
    """
    Merges adjacent segments based on spectral similarity.

    Parameters:
    - clusters: A GEE asset of clusters calculated through the GEE implementation of SNIC.
    - segmentation_image: The raw image used for segmentation, expecting blue, green, red, nir, and ndvi.
    - threshold: A decimal threshold of spectral similarity.
    """

    # Calculate spectral means of clusters over segmentation image
    raw_means = segmentation_image.addBands(clusters).reduceConnectedComponents(
        reducer=ee.Reducer.mean(),
        labelBand='clusters',
        maxSize=256
    )

    # Detect edges on raw spectral means
    min_val = raw_means.focal_min(radius=1.5, units='pixels')
    max_val = raw_means.focal_max(radius=1.5, units='pixels')
    diff = max_val.subtract(min_val)

    # Identify weak boundaries (spectral diff <= threshold)
    similar = diff.reduce(ee.Reducer.max()).lte(ee.Number(threshold))

    # Adopt neighbor's ID where spectral difference is low
    clusters_max = clusters.focal_max(radius=1.5, units='pixels')
    clusters_merged = clusters.where(similar, clusters_max)
    return clusters_merged.rename('clusters')


def merge_size(clusters, threshold=5):
    """
    Merges adjacent segments based on pixel count.

    - clusters: A GEE asset of clusters calculated through the GEE implementation of SNIC.
    - threshold: An integer threshold of the maximum pixel count to be removed.
    """

    # Count pixels in each segment
    size = clusters.connectedPixelCount(maxSize=100, eightConnected=True)

    # Mask small segments
    large_segments = clusters.updateMask(size.gte(threshold))

    # Fill holes with majority neighbor
    filled = large_segments.unmask(
        large_segments.focal_mode(radius=1.5, iterations=1)
    )
    return filled.rename('clusters')
