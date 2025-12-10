"""
Simple example of approx Bayesian computation (ABC).

References:
    - Martin et al, "Bayesian modeling and computation in python", p237
"""
import numpy as np
import pymc as pm

data = np.random.normal(1, .9, 1000)


def normal_simulator(mu: float, sigma: float) -> np.ndarray:
    return np.random.normal(loc=mu, scale=sigma, size=1000)


with pm.Model() as model:
    mu = pm.Normal("mu", mu=0.0, sigma=1.0)
    sigma = pm.HalfNormal("sigma", sigma=1.0)
    s = pm.Simulator(
        "s", normal_simulator,
        params=[mu, sigma],
        distance="gaussian",
        sum_stat="sort",
        epsilon=1,
        observed=data
    )
    trace = pm.sample_smc(kernel="ABC")



