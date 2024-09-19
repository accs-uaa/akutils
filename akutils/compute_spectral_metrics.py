# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Compute spectral metrics
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2024-09-19
# Usage: Python 3.12+
# Description: "Compute spectral metrics" contains a function to compute standard spectral metrics from user-specified bands of remotely sensed imagery.
# ---------------------------------------------------------------------------

# Define a function to compute normalized index
def normalized_index(band_1, band_2, spectral_data):
    """
    Description: computes a normalized index
    Inputs: band_1 -- the name of the band that will be positive in both numerator and denominator
            band_2 -- the name of the band that will be subtracted in the numerator
            spectral_data -- the dataframe containing the spectral band values
    Returned Value: returns a series of signed integers
    Preconditions: requires a dataframe containing labeled bands with values
    """

    # Calculate metric
    normalized_metric = ((spectral_data[band_1] - spectral_data[band_2])
                         / (spectral_data[band_1] + spectral_data[band_2] + 0.001))
    normalized_int = int((normalized_metric * 10000) + 0.5)

    # Return output series
    return normalized_int

# Define a function to impute missing spectral or SAR data
def impute_band_data(band_1, band_2, band_data):
    """
    Description: imputes missing data using the values of another band
    Inputs: band_1 -- the name of the band that contains the missing values
            band_2 -- the name of the band that will fill the missing values
            s1_data -- the dataframe containing the band values
    Returned Value: returns a series of signed integers
    Preconditions: requires a dataframe containing labeled bands with values
    """

    # Import packages
    import numpy as np

    # Calculate metric
    imputed_band = np.where(band_data[band_1] == np.nan,
                            band_data[band_2],
                            band_data[band_1])

    # Return output series
    return imputed_band
