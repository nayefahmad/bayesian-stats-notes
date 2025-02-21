"""
# Creating a prediction interval for quantity of parts ordered

Background: https://stats.stackexchange.com/questions/493716/accounting-for-multiple-layers-of-uncertainty-in-a-model  # noqa

Total parts depends on how many orders, and on how many parts per order.

We can set priors for average qty per order, and for num orders, and use a normal
likelihood that is parametrized such that mu = num_orders * average_qty_per_order.

"""
import arviz as az
import numpy as np
import pymc as pm
import pytensor

pytensor.config.blas__ldflags = (
    "-LC:/Nayef/bayesian-stats-notes/.venv/Lib/" "site-packages/scipy.libs -lopenblas"
)

rng = np.random.RandomState(2020)

# Simulate data
true_avg_qty = 3.0
true_num_orders = 12
true_mu = true_avg_qty * true_num_orders  # expected total parts

# Simulate observed total parts (a single observation)
observed_total_parts = rng.poisson(true_mu)
print("Simulated observed total parts:", observed_total_parts)

if __name__ == "__main__":
    with pm.Model() as simple_model:
        avg_qty_per_order = pm.Exponential("avg_qty_per_order", lam=1.8)
        num_orders = pm.Poisson("num_orders", mu=10)
        mu = pm.Deterministic("mu", num_orders * avg_qty_per_order)
        total_parts = pm.Poisson("total_parts", mu=mu, observed=observed_total_parts)

        # Sample from the posterior
        trace = pm.sample(1000, tune=1000, return_inferencedata=True)
        prior_samples = pm.sample_prior_predictive(500, model=simple_model)

    az.plot_trace(trace)
    print(az.summary(trace))
