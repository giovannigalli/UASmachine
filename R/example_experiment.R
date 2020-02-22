
#### Preamble ##############################################################################################

library(tidyr)
source("experiment_gen.R")
options(scipen = 999)

#### Simulating the experiments ############################################################################

#### For a single scenario ####

#### Augmented design

dau <- simulator(design = "dau", n.treat.reg = 8, n.treat.check = 1,
                  n.row.treat = 1, n.block = 4, n.plant = 10, r = 1, r.unif = NULL,
                  H2 = .8, sigma.t = .05, sigma.b = .005, x.hat = 2,
                  layout = c(2,2), seed = 1, write.files = F)


#### Lattice experiments

#number of treatments for lattice experiments
(1:50)^2

#to identify the number of blocks for the layout (for 49 treatments), take a look at the book
length(unique(agricolae::design.lattice(1:49, r = 2, serie = 2, randomization = T, seed = 1)$book$block))

#run
lattice = simulator(design = "lattice", n.treat.reg = 49, n.treat.check = NULL,
          n.row.treat = 1, n.block = NULL, n.plant = 12, r = 2, H2 = .5, r.unif = .05,
          layout = c(2,7), sigma.t = .005, sigma.b = .0005, x.hat = 2, seed = 1, write.files = F)


#### Running function for multiple scenarios using lattice design ####

#parameters
H2 = c(.3, .6, .9)
sigma.t = c(.0005, .05)
seed = 3
scenarios <- crossing(H2,sigma.t, seed)
scenarios$x.hat = 2
scenarios$sigma.b = .0005

#scenarios
scenarios <- as.data.frame(scenarios)
scen_list = list()

#run
for(i in 1:dim(scenarios)[1]){
  x <- scenarios[i,]
  scen_list[[i]] <- simulator(design = "lattice", n.treat.reg = 49, n.treat.check = NULL,
                          n.row.treat = 1, n.block = NULL, n.plant = 12, r = 2, r.unif = .05,
                          H2 = as.numeric(x["H2"]), sigma.t = as.numeric(x["sigma.t"]),
                          sigma.b = as.numeric(x["sigma.b"]), x.hat = 2,
                          layout = c(2,7), seed = as.integer(x["seed"]), write.files = F)}
