#' # Quick simulation to derive mean/var of a rv 
#' 
#' 2022-02-04 
#' 
#' ## Question
#' - X is a standard normal rv
#' - Y = exp(X)
#' - What are mean/var of Y? 
#' 

library(magrittr)

hist(replicate(100000, mean(exp(rnorm(100)))))
replicate(100000, mean(exp(rnorm(100)))) %>% mean()

hist(replicate(100000, var(exp(rnorm(100)))))
replicate(100000, var(exp(rnorm(100)))) %>% mean()



