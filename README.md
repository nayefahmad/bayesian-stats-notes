# bayesian-stats-notes
Notes on Bayesian statistics


## Repo structure 

- `src` directory: code files 
- `renv` directory: files created by `renv` R package to replicate environment. Helpful 
  reference: 
  - [Introduction to renv](https://rstudio.github.io/renv/articles/renv.html)
- `.pre-commit-config.yaml`: config for use with `pre-commit`. It specifies what hooks to use. 
  Once this file is created, if you run `pre-commit install`, the pre-commit tool will populate the 
  `pre-commit` file in the `./.git/hooks` directory. Helpful references: 
    - [Automate Python workflow using pre-commits: black and flake8](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/)
    - [Keep your code clean using Black & Pylint & Git Hooks & Pre-commit](https://towardsdatascience.com/keep-your-code-clean-using-black-pylint-git-hooks-pre-commit-baf6991f7376)
    - [pre-commit docs](https://pre-commit.com/#)
- `.flake8`: config for Flake8. Mainly used to specify max-line-length=88, to match [Black's default](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
- `.isort.cfg`: config for isort 


### Notes on R workflow  
- my current workflow is to include a `library(<package>)` call in the
script I'm working on, then in the console, call `renv::hydrate`. This seems 
to correctly install the package in the local env. 

## Contents 
1. [Visualizing the Bayesian workflow](https://github.com/nayefahmad/bayesian-stats-notes/blob/main/src/2022-02-21_visualizing-the-bayesian-workflow.md)
