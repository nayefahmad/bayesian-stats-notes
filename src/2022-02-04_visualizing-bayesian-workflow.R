#' # Visualizing the bayesian workflow in R 
#' 
#' 2022-02-04 
#' 
#' Reference: https://www.monicaalexander.com/posts/2020-28-02-bayes_viz/
#' 


library(tidyverse)
library(rstan)
library(brms)
library(bayesplot)
library(loo)
library(tidybayes)

ds <- read_rds("births_2017_sample.RDS")
head(ds)
