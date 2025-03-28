from typing import Dict, Union

import numpy as np
import pandas as pd
import pymc as pm
from pymc_extras.model_builder import ModelBuilder

RANDOM_SEED = 8927
rng = np.random.default_rng(RANDOM_SEED)

# Generate data
x = np.linspace(start=0, stop=1, num=100)
y = 0.3 * x + 0.5 + rng.normal(0, 1, len(x))

with pm.Model() as model:
    # priors
    a = pm.Normal("a", mu=0, sigma=1)
    b = pm.Normal("b", mu=0, sigma=1)
    eps = pm.HalfNormal("eps", 1.0)

    # observed data
    y_model = pm.Normal("y_model", mu=a + b * x, sigma=eps, observed=y)

    # Fitting
    idata = pm.sample()
    idata.extend(pm.sample_prior_predictive())

    # posterior predict
    idata.extend(pm.sample_posterior_predictive(idata))


class LinearModel(ModelBuilder):
    # Give the model a name
    _model_type = "LinearModel"

    # And a version
    version = "0.1"

    def build_model(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        """
        build_model creates the PyMC model

        Parameters:
        model_config: dictionary
            it is a dictionary with all the parameters that we need in our model
            example:  a_loc, a_scale, b_loc
        X : pd.DataFrame
            The input data that is going to be used in the model. This should be a
            DataFrame containing the features (predictors) for the model. For
            efficiency reasons, it should only contain the necessary data columns,
            not the entire available dataset, as this will be encoded into the data
            used to recreate the model.

        y : pd.Series
            The target data for the model. This should be a Series representing the
            output or dependent variable for the model.

        kwargs : dict
            Additional keyword arguments that may be used for model configuration.
        """
        # Check the type of X and y and adjust access accordingly
        X_values = X["input"].values
        y_values = y.values if isinstance(y, pd.Series) else y
        self._generate_and_preprocess_model_data(X_values, y_values)

        with pm.Model(coords=self.model_coords) as self.model:
            # Create mutable data containers
            x_data = pm.MutableData("x_data", X_values)
            y_data = pm.MutableData("y_data", y_values)

            # prior parameters
            a_mu_prior = self.model_config.get("a_mu_prior", 0.0)
            a_sigma_prior = self.model_config.get("a_sigma_prior", 1.0)
            b_mu_prior = self.model_config.get("b_mu_prior", 0.0)
            b_sigma_prior = self.model_config.get("b_sigma_prior", 1.0)
            eps_prior = self.model_config.get("eps_prior", 1.0)

            # priors
            a = pm.Normal("a", mu=a_mu_prior, sigma=a_sigma_prior)
            b = pm.Normal("b", mu=b_mu_prior, sigma=b_sigma_prior)
            eps = pm.HalfNormal("eps", eps_prior)

            obs = pm.Normal(   # noqa:
                "y", mu=a + b * x_data, sigma=eps, shape=x_data.shape, observed=y_data
            )

    def _data_setter(
        self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray] = None
    ):
        if isinstance(X, pd.DataFrame):
            x_values = X["input"].values
        else:
            # Assuming "input" is the first column
            x_values = X[:, 0]

        with self.model:
            pm.set_data({"x_data": x_values})
            if y is not None:
                pm.set_data({"y_data": y.values if isinstance(y, pd.Series) else y})

    @staticmethod
    def get_default_model_config() -> Dict:
        """
        Returns a class default config dict for model builder if no model_config is
        provided on class initialization. The model config dict is generally used to
        specify the prior values we want to build the model with. It supports more
        complex data structures like lists, dictionaries, etc. It will be passed to
        the class instance on initialization, in case the user doesn't provide any
        model_config of their own.
        """
        model_config: Dict = {
            "a_mu_prior": 0.0,
            "a_sigma_prior": 1.0,
            "b_mu_prior": 0.0,
            "b_sigma_prior": 1.0,
            "eps_prior": 1.0,
        }
        return model_config

    @staticmethod
    def get_default_sampler_config() -> Dict:
        """
        Returns a class default sampler dict for model builder if no sampler_config
        is provided on class initialization. The sampler config dict is used to send
        parameters to the sampler . It will be used during fitting in case the user
        doesn't provide any sampler_config of their own.
        """
        sampler_config: Dict = {
            "draws": 1_000,
            "tune": 1_000,
            "chains": 3,
            "target_accept": 0.95,
        }
        return sampler_config

    @property
    def output_var(self):
        return "y"

    @property
    def _serializable_model_config(self) -> Dict[str, Union[int, float, Dict]]:
        """
        _serializable_model_config is a property that returns a dictionary with all
        the model parameters that we want to save. as some of the data structures are
        not json serializable, we need to convert them to json serializable objects.
        Some models will need them, others can just define them to return the
        model_config.
        """
        return self.model_config

    def _save_input_params(self, idata) -> None:
        """
        Saves any additional model parameters (other than the dataset) to the idata
        object.

        These parameters are stored within `idata.attrs` using keys that correspond
        to the parameter names. If you don't need to store any extra parameters,
        you can leave this method unimplemented.

        Example:
            For saving customer IDs provided as an 'customer_ids' input to the model:
            self.customer_ids = customer_ids.values #this line is done outside of the
            function, preferably at the initialization of the model object.
            idata.attrs["customer_ids"] = json.dumps(self.customer_ids.tolist())  #
            Convert numpy array to a JSON-serializable list.
        """
        pass

        pass

    def _generate_and_preprocess_model_data(
        self, X: Union[pd.DataFrame, pd.Series], y: Union[pd.Series, np.ndarray]
    ) -> None:
        """
        Depending on the model, we might need to preprocess the data before fitting
        the model. all required preprocessing and conditional assignments should be
        defined here.
        """

        # in our case we're not using coords, but if we were, we would define them
        # here, or later on in the function, if extracting them from the data. as we
        # don't do any data preprocessing, we just assign the data given by the user.
        # Note that it's a very basic model, and usually we would need to do some
        # preprocessing, or generate the coords from the data.
        self.model_coords = None
        self.X = X
        self.y = y
