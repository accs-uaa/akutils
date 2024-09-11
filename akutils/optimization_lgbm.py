# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Optimization for LightGBM
# Author: Timm Nawrocki
# Last Updated: 2024-09-10
# Usage: Must be executed in an Anaconda Python 3.12+ distribution.
# Description: "Optimization for LightGBM" is a set of functions that perform Bayesian optimization on either a LightGBM classifier or regressor.
# ---------------------------------------------------------------------------

# Define a function to conduct a cross validation iteration for a LightGBM classifier
def lgbmclassifier_cv(num_leaves, max_depth, learning_rate, n_estimators,
                      min_split_gain, min_child_weight, min_child_samples,
                      subsample, colsample_bytree, reg_alpha, reg_lambda,
                      data, targets, groups):
    """
    Description: conducts cross validation of a LightGBM regressor with a particular set of hyperparameter values
    Inputs: 'data' -- the covariate data to conduct the model training and validation
            'targets' -- the response data to conduct the model training and validation
            'groups' -- the group data for the cross validation method
            All other inputs are set by other functions
    Returned Value: Returns the cross validation score
    Preconditions: requires pre-processed X and y data
    """

    # Import packages
    from lightgbm import LGBMClassifier
    from sklearn.model_selection import StratifiedGroupKFold
    from sklearn.model_selection import cross_val_score

    # Define cross validation
    cv_splits = StratifiedGroupKFold(n_splits=5)

    # Define estimator
    estimator = LGBMClassifier(
        boosting_type='gbdt',
        num_leaves=int(num_leaves),
        max_depth=int(max_depth),
        learning_rate=learning_rate,
        n_estimators=int(n_estimators),
        objective='binary',
        class_weight='balanced',
        min_split_gain=min_split_gain,
        min_child_weight=min_child_weight,
        min_child_samples=int(min_child_samples),
        subsample=subsample,
        subsample_freq=1,
        colsample_bytree=colsample_bytree,
        reg_alpha=reg_alpha,
        reg_lambda=reg_lambda,
        n_jobs=4,
        importance_type='gain',
        verbosity=-1
    )

    # Define cross validation
    scores = cross_val_score(
        estimator,
        data,
        targets,
        scoring='balanced_accuracy',
        cv=cv_splits,
        groups=groups
    )

    return scores.mean()


# Define a function to conduct a cross validation iteration for a LightGBM regressor
def lgbmregressor_cv(num_leaves, max_depth, learning_rate, n_estimators,
                     min_split_gain, min_child_weight, min_child_samples,
                     subsample, colsample_bytree, reg_alpha, reg_lambda,
                     data, targets, groups):
    """
    Description: conducts cross validation of a LightGBM regressor with a particular set of hyperparameter values
    Inputs: 'data' -- the covariate data to conduct the model training and validation
            'targets' -- the response data to conduct the model training and validation
            'groups' -- the group data for the cross validation method
            All other inputs are set by other functions
    Returned Value: Returns the cross validation score
    Preconditions: requires pre-processed X and y data
    """

    # Import packages
    from lightgbm import LGBMRegressor
    from sklearn.model_selection import StratifiedGroupKFold
    from sklearn.model_selection import cross_val_score

    # Define cross validation
    cv_splits = StratifiedGroupKFold(n_splits=5)

    # Define estimator
    estimator = LGBMRegressor(
        boosting_type='gbdt',
        num_leaves=int(num_leaves),
        max_depth=int(max_depth),
        learning_rate=learning_rate,
        n_estimators=int(n_estimators),
        objective='regression',
        min_split_gain=min_split_gain,
        min_child_weight=min_child_weight,
        min_child_samples=int(min_child_samples),
        subsample=subsample,
        subsample_freq=1,
        colsample_bytree=colsample_bytree,
        reg_alpha=reg_alpha,
        reg_lambda=reg_lambda,
        n_jobs=4,
        importance_type='gain',
        verbosity=-1
    )

    # Define cross validation
    scores = cross_val_score(
        estimator,
        data,
        targets,
        scoring='neg_mean_squared_error',
        cv=cv_splits,
        groups=groups
    )

    # Return mean score across all cross validation partitions
    return scores.mean()


# Define a function to optimize hyperparameters for a LightGBM classifier
def optimize_lgbmclassifier(data, targets, groups):
    """
    Description: applies Bayesian optimization to the hyperparameters of a LightGBM classifier
    Inputs: 'data' -- the covariate data to conduct the model training and validation
            'targets' -- the response data to conduct the model training and validation
            'groups' -- the group data for the cross validation method
    Returned Value: Returns the hyperparameters from the iteration with the best cross validation performance
    Preconditions: requires pre-processed X and y data
    """

    # Import packages
    from bayes_opt import BayesianOptimization

    # Define a function to return hyperparameters from an optimization iteration
    def lgbmclassifier_params(num_leaves, max_depth, learning_rate, n_estimators,
                              min_split_gain, min_child_weight, min_child_samples,
                              subsample, colsample_bytree, reg_alpha, reg_lambda):
        '''
        Description: returns the hyperparameter values from a cross validation set
        Inputs: All inputs are set by other functions
        Returned Value: Returns a set of hyperparameters
        Preconditions: this function wraps lgbmclassifier_cv
        '''

        return lgbmclassifier_cv(
            num_leaves=num_leaves,
            max_depth=max_depth,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            min_split_gain=min_split_gain,
            min_child_weight=min_child_weight,
            min_child_samples=min_child_samples,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            reg_alpha=reg_alpha,
            reg_lambda=reg_lambda,
            data=data,
            targets=targets,
            groups=groups
        )

    optimizer = BayesianOptimization(
        f=lgbmclassifier_params,
        pbounds={
            'num_leaves': (5, 200),
            'max_depth': (3, 12),
            'learning_rate': (0.001, 0.2),
            'n_estimators': (50, 100),
            'min_split_gain': (0.001, 0.1),
            'min_child_weight': (0.001, 1),
            'min_child_samples': (1, 200),
            'subsample': (0.3, 0.9),
            'colsample_bytree': (0.3, 0.9),
            'reg_alpha': (0, 5),
            'reg_lambda': (0, 5)
        },
        random_state=314,
        verbose=2
    )
    optimizer.maximize(init_points=3, n_iter=7)

    return optimizer.max['params']


# Define a function to optimize hyperparameters for a LightGBM regressor
def optimize_lgbmregressor(data, targets, groups):
    """
    Description: applies Bayesian optimization to the hyperparameters of a LightGBM regressor
    Inputs: 'data' -- the covariate data to conduct the model training and validation
            'targets' -- the response data to conduct the model training and validation
            'groups' -- the group data for the cross validation method
    Returned Value: Returns the hyperparameters from the iteration with the best cross validation performance
    Preconditions: requires pre-processed X and y data
    """

    # Import packages
    from bayes_opt import BayesianOptimization

    # Define a function to return hyperparameters from an optimization iteration
    def lgbmregressor_params(num_leaves, max_depth, learning_rate, n_estimators,
                             min_split_gain, min_child_weight, min_child_samples,
                             subsample, colsample_bytree, reg_alpha, reg_lambda):
        '''
        Description: returns the hyperparameter values from a cross validation set
        Inputs: All inputs are set by other functions
        Returned Value: Returns a set of hyperparameters
        Preconditions: this function wraps lgbmregressor_cv
        '''

        return lgbmregressor_cv(
            num_leaves=num_leaves,
            max_depth=max_depth,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            min_split_gain=min_split_gain,
            min_child_weight=min_child_weight,
            min_child_samples=min_child_samples,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            reg_alpha=reg_alpha,
            reg_lambda=reg_lambda,
            data=data,
            targets=targets,
            groups=groups
        )

    optimizer = BayesianOptimization(
        f=lgbmregressor_params,
        pbounds={
            'num_leaves': (5, 200),
            'max_depth': (3, 12),
            'learning_rate': (0.001, 0.2),
            'n_estimators': (50, 100),
            'min_split_gain': (0.001, 0.1),
            'min_child_weight': (0.001, 1),
            'min_child_samples': (1, 200),
            'subsample': (0.3, 0.9),
            'colsample_bytree': (0.3, 0.9),
            'reg_alpha': (0, 5),
            'reg_lambda': (0, 5)
        },
        random_state=314,
        verbose=2
    )
    optimizer.maximize(init_points=3, n_iter=7)

    return optimizer.max['params']
