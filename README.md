# bayesian-stats-notes
Notes on Bayesian statistics


## Repo structure 

- `src` directory: code files 
- `renv` directory: files created by `renv` R package to replicate environment. Helpful 
  reference: 
  - [Introduction to renv](https://rstudio.github.io/renv/articles/renv.html)


### Notes 
- my current workflow is to include a `library(<package>)` call in the
script I'm working on, then in the console, call `renv::hydrate`. This seems 
to correctly install the package in the local env. 