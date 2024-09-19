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
    normalized_rescaled = (normalized_metric * 10000) + 0.5
    normalized_int = normalized_rescaled.astype('int32')

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


# Define a function to process covariate data for the AKVEG foliar cover maps
def foliar_cover_predictors(covariate_data, predictors):
    """
    Description: processes the covariates in a dataframe for prediction
    Inputs: covariate_data -- the dataframe containing all covariates for model training and prediction
            predictors -- a set of all predictor variables used in model training and prediction
    Returned Value: returns a dataframe of full predictors
    Preconditions: requires a dataframe containing initial predictors
    """

    # Import packages
    import numpy as np

    # Impute missing S1 data
    covariate_data['s1_1_vva'] = impute_band_data('s1_1_vva', 's1_1_vva', covariate_data)
    covariate_data['s1_1_vvd'] = impute_band_data('s1_1_vvd', 's1_1_vva', covariate_data)
    covariate_data['s1_1_vha'] = impute_band_data('s1_1_vha', 's1_1_vhd', covariate_data)
    covariate_data['s1_1_vhd'] = impute_band_data('s1_1_vhd', 's1_1_vha', covariate_data)

    covariate_data['s1_2_vva'] = impute_band_data('s1_2_vva', 's1_2_vva', covariate_data)
    covariate_data['s1_2_vvd'] = impute_band_data('s1_2_vvd', 's1_2_vva', covariate_data)
    covariate_data['s1_2_vha'] = impute_band_data('s1_2_vha', 's1_2_vhd', covariate_data)
    covariate_data['s1_2_vhd'] = impute_band_data('s1_2_vhd', 's1_2_vha', covariate_data)

    covariate_data['s1_3_vva'] = impute_band_data('s1_3_vva', 's1_3_vva', covariate_data)
    covariate_data['s1_3_vvd'] = impute_band_data('s1_3_vvd', 's1_3_vva', covariate_data)
    covariate_data['s1_3_vha'] = impute_band_data('s1_3_vha', 's1_3_vhd', covariate_data)
    covariate_data['s1_3_vhd'] = impute_band_data('s1_3_vhd', 's1_3_vha', covariate_data)

    #covariate_data['s2_1_blue'] = impute_band_data('s2_1_blue', 'B2', covariate_data)
    #covariate_data['s2_1_green'] = impute_band_data('s2_1_green', 'B3', covariate_data)
    #covariate_data['s2_1_red'] = impute_band_data('s2_1_red', 'B4', covariate_data)
    #covariate_data['s2_1_redge1'] = impute_band_data('s2_1_redge1', 'B5', covariate_data)
    #covariate_data['s2_1_redge2'] = impute_band_data('s2_1_redge2', 'B6', covariate_data)
    #covariate_data['s2_1_redge3'] = impute_band_data('s2_1_redge3', 'B7', covariate_data)
    #covariate_data['s2_1_nir'] = impute_band_data('s2_1_nir', 'B8', covariate_data)
    #covariate_data['s2_1_redge4'] = impute_band_data('s2_1_redge4', 'B8A', covariate_data)
    #covariate_data['s2_1_swir1'] = impute_band_data('s2_1_swir1', 'B11', covariate_data)
    #covariate_data['s2_1_swir2'] = impute_band_data('s2_1_swir2', 'B12', covariate_data)

    #covariate_data['s2_2_blue'] = impute_band_data('s2_2_blue', 'B2', covariate_data)
    #covariate_data['s2_2_green'] = impute_band_data('s2_2_green', 'B3', covariate_data)
    #covariate_data['s2_2_red'] = impute_band_data('s2_2_red', 'B4', covariate_data)
    #covariate_data['s2_2_redge1'] = impute_band_data('s2_2_redge1', 'B5', covariate_data)
    #covariate_data['s2_2_redge2'] = impute_band_data('s2_2_redge2', 'B6', covariate_data)
    #covariate_data['s2_2_redge3'] = impute_band_data('s2_2_redge3', 'B7', covariate_data)
    #covariate_data['s2_2_nir'] = impute_band_data('s2_2_nir', 'B8', covariate_data)
    #covariate_data['s2_2_redge4'] = impute_band_data('s2_2_redge4', 'B8A', covariate_data)
    #covariate_data['s2_2_swir1'] = impute_band_data('s2_2_swir1', 'B11', covariate_data)
    #covariate_data['s2_2_swir2'] = impute_band_data('s2_2_swir2', 'B12', covariate_data)

    #covariate_data['s2_3_blue'] = impute_band_data('s2_3_blue', 'B2', covariate_data)
    #covariate_data['s2_3_green'] = impute_band_data('s2_3_green', 'B3', covariate_data)
    #covariate_data['s2_3_red'] = impute_band_data('s2_3_red', 'B4', covariate_data)
    #covariate_data['s2_3_redge1'] = impute_band_data('s2_3_redge1', 'B5', covariate_data)
    #covariate_data['s2_3_redge2'] = impute_band_data('s2_3_redge2', 'B6', covariate_data)
    #covariate_data['s2_3_redge3'] = impute_band_data('s2_3_redge3', 'B7', covariate_data)
    #covariate_data['s2_3_nir'] = impute_band_data('s2_3_nir', 'B8', covariate_data)
    #covariate_data['s2_3_redge4'] = impute_band_data('s2_3_redge4', 'B8A', covariate_data)
    #covariate_data['s2_3_swir1'] = impute_band_data('s2_3_swir1', 'B11', covariate_data)
    #covariate_data['s2_3_swir2'] = impute_band_data('s2_3_swir2', 'B12', covariate_data)

    #covariate_data['s2_4_blue'] = impute_band_data('s2_4_blue', 'B2', covariate_data)
    #covariate_data['s2_4_green'] = impute_band_data('s2_4_green', 'B3', covariate_data)
    #covariate_data['s2_4_red'] = impute_band_data('s2_4_red', 'B4', covariate_data)
    #covariate_data['s2_4_redge1'] = impute_band_data('s2_4_redge1', 'B5', covariate_data)
    #covariate_data['s2_4_redge2'] = impute_band_data('s2_4_redge2', 'B6', covariate_data)
    #covariate_data['s2_4_redge3'] = impute_band_data('s2_4_redge3', 'B7', covariate_data)
    #covariate_data['s2_4_nir'] = impute_band_data('s2_4_nir', 'B8', covariate_data)
    #covariate_data['s2_4_redge4'] = impute_band_data('s2_4_redge4', 'B8A', covariate_data)
    #covariate_data['s2_4_swir1'] = impute_band_data('s2_4_swir1', 'B11', covariate_data)
    #covariate_data['s2_4_swir2'] = impute_band_data('s2_4_swir2', 'B12', covariate_data)

    #covariate_data['s2_5_blue'] = impute_band_data('s2_5_blue', 'B2', covariate_data)
    #covariate_data['s2_5_green'] = impute_band_data('s2_5_green', 'B3', covariate_data)
    #covariate_data['s2_5_red'] = impute_band_data('s2_5_red', 'B4', covariate_data)
    #covariate_data['s2_5_redge1'] = impute_band_data('s2_5_redge1', 'B5', covariate_data)
    #covariate_data['s2_5_redge2'] = impute_band_data('s2_5_redge2', 'B6', covariate_data)
    #covariate_data['s2_5_redge3'] = impute_band_data('s2_5_redge3', 'B7', covariate_data)
    #covariate_data['s2_5_nir'] = impute_band_data('s2_5_nir', 'B8', covariate_data)
    #covariate_data['s2_5_redge4'] = impute_band_data('s2_5_redge4', 'B8A', covariate_data)
    #covariate_data['s2_5_swir1'] = impute_band_data('s2_5_swir1', 'B11', covariate_data)
    #covariate_data['s2_5_swir2'] = impute_band_data('s2_5_swir2', 'B12', covariate_data)

    # Calculate derived metrics for season 1
    covariate_data['s2_1_nbr'] = normalized_index('s2_1_nir', 's2_1_swir2', covariate_data)
    covariate_data['s2_1_ngrdi'] = normalized_index('s2_1_green', 's2_1_red', covariate_data)
    covariate_data['s2_1_ndmi'] = normalized_index('s2_1_nir', 's2_1_swir1', covariate_data)
    covariate_data['s2_1_ndsi'] = normalized_index('s2_1_green', 's2_1_swir1', covariate_data)
    covariate_data['s2_1_ndvi'] = normalized_index('s2_1_nir', 's2_1_red', covariate_data)
    covariate_data['s2_1_ndwi'] = normalized_index('s2_1_green', 's2_1_nir', covariate_data)

    # Calculate derived metrics for season 2
    covariate_data['s2_2_nbr'] = normalized_index('s2_2_nir', 's2_2_swir2', covariate_data)
    covariate_data['s2_2_ngrdi'] = normalized_index('s2_2_green', 's2_2_red', covariate_data)
    covariate_data['s2_2_ndmi'] = normalized_index('s2_2_nir', 's2_2_swir1', covariate_data)
    covariate_data['s2_2_ndsi'] = normalized_index('s2_2_green', 's2_2_swir1', covariate_data)
    covariate_data['s2_2_ndvi'] = normalized_index('s2_2_nir', 's2_2_red', covariate_data)
    covariate_data['s2_2_ndwi'] = normalized_index('s2_2_green', 's2_2_nir', covariate_data)

    # Calculate derived metrics for season 3
    covariate_data['s2_3_nbr'] = normalized_index('s2_3_nir', 's2_3_swir2', covariate_data)
    covariate_data['s2_3_ngrdi'] = normalized_index('s2_3_green', 's2_3_red', covariate_data)
    covariate_data['s2_3_ndmi'] = normalized_index('s2_3_nir', 's2_3_swir1', covariate_data)
    covariate_data['s2_3_ndsi'] = normalized_index('s2_3_green', 's2_3_swir1', covariate_data)
    covariate_data['s2_3_ndvi'] = normalized_index('s2_3_nir', 's2_3_red', covariate_data)
    covariate_data['s2_3_ndwi'] = normalized_index('s2_3_green', 's2_3_nir', covariate_data)

    # Calculate derived metrics for season 4
    covariate_data['s2_4_nbr'] = normalized_index('s2_4_nir', 's2_4_swir2', covariate_data)
    covariate_data['s2_4_ngrdi'] = normalized_index('s2_4_green', 's2_4_red', covariate_data)
    covariate_data['s2_4_ndmi'] = normalized_index('s2_4_nir', 's2_4_swir1', covariate_data)
    covariate_data['s2_4_ndsi'] = normalized_index('s2_4_green', 's2_4_swir1', covariate_data)
    covariate_data['s2_4_ndvi'] = normalized_index('s2_4_nir', 's2_4_red', covariate_data)
    covariate_data['s2_4_ndwi'] = normalized_index('s2_4_green', 's2_4_nir', covariate_data)

    # Calculate derived metrics for season 5
    covariate_data['s2_5_nbr'] = normalized_index('s2_5_nir', 's2_5_swir2', covariate_data)
    covariate_data['s2_5_ngrdi'] = normalized_index('s2_5_green', 's2_5_red', covariate_data)
    covariate_data['s2_5_ndmi'] = normalized_index('s2_5_nir', 's2_5_swir1', covariate_data)
    covariate_data['s2_5_ndsi'] = normalized_index('s2_5_green', 's2_5_swir1', covariate_data)
    covariate_data['s2_5_ndvi'] = normalized_index('s2_5_nir', 's2_5_red', covariate_data)
    covariate_data['s2_5_ndwi'] = normalized_index('s2_5_green', 's2_5_nir', covariate_data)

    # Re-order covariates
    covariate_data[predictors] = covariate_data[predictors].interpolate()
    for name, values in covariate_data[predictors].items():
        covariate_data[name] = covariate_data[name].fillna(np.mean(values))

    return covariate_data
