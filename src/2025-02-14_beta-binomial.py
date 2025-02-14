from dataclasses import dataclass
import time

import arviz as az
import matplotlib.pyplot as plt
import pymc as pm


@dataclass
class BetaPriorParams:
    alpha: float = 1
    beta: float = 1


p1 = BetaPriorParams()


if __name__ == '__main__':
    with pm.Model() as model:
        y = [1, 1, 0]
        theta = pm.Beta('theta', alpha=p1.alpha, beta=p1.beta)
        y_obs = pm.Binomial('y_obs', n=1, p=theta, observed=y)

        # Sampling without data:
        start = time.time()
        idata = pm.sample(1000, return_inferencedata=True, progressbar=True)
        elapsed_seconds = time.time() - start

        prior_samples = pm.sample_prior_predictive(500, model)

    az.plot_trace(idata)
    plt.show()

    az.summary(idata, kind='stats')

    az.plot_ppc(prior_samples.prior['theta'], kind='kde')
    plt.show()



    print(elapsed_seconds)
    print(idata)



    print('done')

