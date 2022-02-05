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

# sim to get mean of Y
hist(replicate(100000, mean(exp(rnorm(100)))))
replicate(100000, mean(exp(rnorm(100)))) %>% mean()

# sim to get var of Y
hist(replicate(100000, var(exp(rnorm(100)))))
replicate(100000, var(exp(rnorm(100)))) %>% mean()



