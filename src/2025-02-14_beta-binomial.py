from dataclasses import dataclass

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm
import seaborn as sns

seed = 2025
rng = np.random.RandomState(seed)  # instance of np.random.Generator


@dataclass
class BetaPriorParams:
    alpha: float = 1
    beta: float = 1


p1 = BetaPriorParams()
p2 = BetaPriorParams(alpha=5, beta=1)

# Select which parameters to use:
p = p2

if __name__ == '__main__':
    y = rng.binomial(n=1, p=.3, size=20)

    with pm.Model() as model:
        theta = pm.Beta('theta', alpha=p.alpha, beta=p.beta)
        y_obs = pm.Binomial('y_obs', n=1, p=theta, observed=y)

        idata = pm.sample(
            1000, return_inferencedata=True, progressbar=True, cores=8
        )

        prior_samples = pm.sample_prior_predictive(500, model)
        posterior_samples = pm.sample_posterior_predictive(idata, model=model)

    az.summary(idata, kind='stats')

    az.plot_trace(idata)
    plt.show()

    # todo: how to fix these?
    # az.plot_ppc(prior_samples, group='prior', var_names=['y_obs'])
    # plt.show()
    #
    # az.plot_ppc(posterior_samples)
    # plt.show()

    # Extracting values from the idata objects:
    prior_values = prior_samples.prior['theta'].values
    prior_pred_values = prior_samples.prior_predictive['y_obs'].values
    posterior_values = idata.posterior['theta'].values
    posterior_pred_values = posterior_samples.posterior_predictive['y_obs'].values


    # Plot outputs:
    all_values = [
        prior_values, prior_pred_values, posterior_values, posterior_pred_values
    ]
    labels = ['prior', 'prior_predictive', 'posterior', 'posterior_predictive']
    for idx, values in enumerate(all_values):
        sns.distplot(values)
        plt.suptitle(labels[idx])
        plt.show()

    print('done')

