import matplotlib.pyplot as plt
import numpy.matlib as matlib
from scipy.stats import multivariate_normal
import numpy as np
import support_code


def likelihood_func(w, X, y_train, likelihood_var):
    '''
    Implement likelihood_func. This function returns the data likelihood
    given f(y_train | X; w) ~ Normal(Xw, likelihood_var).

    Args:
        w: Weights
        X: Training design matrix with first col all ones (np.matrix)
        y_train: Training response vector (np.matrix)
        likelihood_var: likelihood variance

    Returns:
        likelihood: Data likelihood (float)
    '''

    #TO DO
    """
    L_D(w) = P(D|x, w) = p(y0|x0, w) * p(y1|x1, w) *...* p(yn|xn, w)
    """
    num_instances, _ = X.shape
    likelihood = 1
    for i in range(num_instances):
        likelihood *= 1./(2*np.pi * likelihood_var)**0.5 * np.exp(-(y_train[i] - np.dot(X[i], w))**2/(2 * likelihood_var))

    return likelihood


def get_posterior_params(X, y_train, prior, likelihood_var = 0.2**2):
    '''
    Implement get_posterior_params. This function returns the posterior
    mean vector \mu_p and posterior covariance matrix \Sigma_p for
    Bayesian regression (normal likelihood and prior).

    Note support_code.make_plots takes this completed function as an argument.

    Args:
        X: Training design matrix with first col all ones (np.matrix)
        y_train: Training response vector (np.matrix)
        prior: Prior parameters; dict with 'mean' (prior mean np.matrix)
               and 'var' (prior covariance np.matrix)
        likelihood_var: likelihood variance- default (0.2**2) per the lecture slides

    Returns:
        post_mean: Posterior mean (np.matrix)
        post_var: Posterior variance (np.matrix)
    '''

    # TO DO
    """
    P(w|X) ~ L_D(w) * p(w)
    post_mean = (X.T * X + σ^2 * Σ^(−1))^(-1) * X.T * y
    post_var = (σ^(−2) * X.T * X + Σ^(-1))^(-1)
    """
    prior_mean, prior_var = prior['mean'], prior['var']

    post_mean = np.dot(np.dot((np.dot(X.T, X) + likelihood_var * prior_var.getI()).getI(), X.T), y_train)
    post_var = (likelihood_var**-2 * np.dot(X.T, X) + prior_var.getI()).getI()

    return post_mean, post_var


def get_predictive_params(X_new, post_mean, post_var, likelihood_var = 0.2**2):
    '''
    Implement get_predictive_params. This function returns the predictive
    distribution parameters (mean and variance) given the posterior mean
    and covariance matrix (returned from get_posterior_params) and the
    likelihood variance (default value from lecture).

    Args:
        X_new: New observation (np.matrix object)
        post_mean, post_var: Returned from get_posterior_params
        likelihood_var: likelihood variance (0.2**2) per the lecture slides

    Returns:
        - pred_mean: Mean of predictive distribution
        - pred_var: Variance of predictive distribution
    '''

    # TO DO
    """
    pred_mean = post_mean.T * X_new
    pred_var = X_new.T * post_var * X_new + likelihood_var
    """
    pred_mean = np.dot(post_mean.T, X_new)
    pred_var = np.dot(np.dot(X_new.T, post_var), X_new) + likelihood_var

    return pred_mean, pred_var


if __name__ == '__main__':

    '''
    If your implementations are correct, running
        python problem.py
    inside the Bayesian Regression directory will, for each sigma in sigmas_to-test generates plots
    '''

    np.random.seed(46134)
    actual_weights = np.matrix([[0.3], [0.5]])
    data_size = 40
    noise = {"mean":0, "var":0.2 ** 2}
    likelihood_var = noise["var"]
    xtrain, ytrain = support_code.generate_data(data_size, noise, actual_weights)

    #Question (b)
    sigmas_to_test = [1/2, 1/(2**5), 1/(2**10)]
    for sigma_squared in sigmas_to_test:
        prior = {"mean":np.matrix([[0], [0]]),
                 "var":matlib.eye(2) * sigma_squared}

        support_code.make_plots(actual_weights,
                                xtrain,
                                ytrain,
                                likelihood_var,
                                prior,
                                likelihood_func,
                                get_posterior_params,
                                get_predictive_params)
