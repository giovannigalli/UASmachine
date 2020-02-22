
#### Function ######################################################################################
simulator = function(design = design, n.treat.reg = n.treat.reg, n.treat.check = n.treat.check,
                     n.row.treat = n.row.treat, n.block = n.block, n.plant = n.plant, r = r,
                     r.unif = NULL, H2 = H2, sigma.t = sigma.t, sigma.b = sigma.b, x.hat = x.hat,
                     layout = layout, seed = seed, write.files = T){
  
  require(agricolae)
  
  set.seed(seed)
  
  #randomizing the experiment
  if(design == "dau"){
    n.treat.total = n.treat.reg + n.treat.check
    n.treat.reg.byblock = n.treat.reg/n.block
    n.treat.total.byblock = n.treat.reg.byblock + n.treat.check
    n.row = n.treat.total.byblock * n.row.treat
    trt1 = 1:n.treat.check
    trt2 = (n.treat.check + 1):(n.treat.check+n.treat.reg)
    r = 1
    book = design.dau(trt1 = trt1, trt2 = trt2, r = n.block, serie = 2, randomization = T, seed = seed)$book
    
    if(length(unique(table(book$block))) != 1){
      stop("Blocks are uneven")
    }
  }
  
  if(design == "lattice"){
    book = design.lattice(trt = 1:n.treat.reg, r = r, serie = 2, randomization = T, seed = seed)$book
    n.block = max(as.integer(book$block))
    n.treat.reg.byblock = n.treat.reg/(n.block/r)
    n.treat.total.byblock = n.treat.reg.byblock
    n.row = n.treat.reg.byblock * n.row.treat
    n.treat.total = n.treat.reg
    n.treat.check = NULL
  }
  
  #indexer
  border.inc = function(book, n.block, n.treat){
    x = NULL
    for(i in 1:n.block){
      x[(length(x) + 1):(length(x) + n.treat * n.row.treat)] = rep(book[(n.treat * i - n.treat + 1):(n.treat * i)], each = n.row.treat)}
    return(book = x)}
  
  book.inc.trt = border.inc(book = book$trt, n.block = n.block, n.treat = n.treat.total.byblock)
  book.inc.block = border.inc(book = as.numeric(book$block)-1, n.block = n.block, n.treat = n.treat.total.byblock)
  book.inc.row.gis = border.inc(book = 1:(n.treat.total.byblock), n.block = 1, n.treat = n.treat.total.byblock)
  
  #qgis meta:row determination
  ranges = c(0,n.treat.total.byblock*(1:layout[2]))
  row.gis = list()
  for(i in 1:(length(ranges)-1)){
    pos = ranges[i]
    row.gis[[i]] = rep(book.inc.row.gis+pos,layout[1])
  }
  row.gis = unlist(row.gis); row.gis = rep(row.gis, each = n.plant)
  
  #estimating residual variance
  sigma.e = (sigma.t*(1-H2))/H2
  
  #estimating error values
  error = rnorm(n.row * n.plant * n.block, 0, sqrt(sigma.e))
  
  #estimating treatment effects
  xt = rnorm(n.treat.total, x.hat, sqrt(sigma.t))
  names(xt) <- 1:n.treat.total
  xt[length(xt)+1] <- x.hat
  names(xt)[length(xt)] <- 0
  xt = xt[as.character(book.inc.trt)]
  
  #estimating block effects
  xb = rnorm(n.block, 0, sqrt(sigma.b))
  names(xb) <- (1:n.block)-1
  xb = xb[as.character(book.inc.block)]
  
  #estimating replication effect
  if(design == "dau"){xr <- 0}
    else{xr <- runif(r, -r.unif, r.unif)}
  
  #full dataframe for blender
  book.blender.full = data.frame(block.name = rep(book.inc.block, each = n.plant),
                                 block.eff = rep(xb, each = n.plant),
                                 row.bpy = rep(rep(1:n.row-1, each = n.plant), n.block),
                                 trat.name = rep(book.inc.trt, each = n.plant),
                                 trat.eff = rep(xt, each = n.plant),
                                 error = error,
                                 phenotype = rep(xr, each = (n.plant * n.row * n.block/r)) + rep(xb, each = n.plant) + rep(xt, each = n.plant) + error,   #ADICIONAR EFEITO DE REP
                                 plant = rep(1:n.plant, n.row * n.block) - 1,
                                 rep = rep(1:r, each = (n.plant * n.row * n.block/r)),
                                 row.gis = row.gis,
                                 col.gis = rep(book.inc.block, each = n.plant)  %% layout[1] + 1,
                                 id = 1:length(error),
                                 rep.eff = rep(xr, each = (n.plant * n.row * n.block/r)))
  
  #adapting full frame to quantum gis
  book.qgis.full = book.blender.full
  
  #determining rows to eliminate for reduced frame
  phenotype.mean =  tapply(X = book.blender.full$phenotype, INDEX = paste0(book.blender.full$rep, '_', book.blender.full$block.name,'_',book.blender.full$trat.name), FUN = mean)
  phenotype.mean = phenotype.mean[match(unique(paste0(book.blender.full$rep, '_', book.blender.full$block.name,'_',book.blender.full$trat.name)),names(phenotype.mean))]
  
  #qgis meta:row determination
  ranges = c(0,n.treat.total.byblock*(1:layout[2]))
  row.gis = list()
  for(i in 1:(length(ranges)-1)){
    pos = ranges[i]
    row.gis[[i]] = rep(unique(book.inc.row.gis)+pos,layout[1])
  }
  row.gis.mean = unlist(row.gis)
  
  #reduced dataframe for qgis
  book.qgis.mean = data.frame(block.name = book$block,
                              block.eff = xb[as.character(as.numeric(book$block) - 1)],
                              trat.name = book$trt,
                              trat.eff = xt[as.character(book$trt)],
                              phenotype = phenotype.mean,
                              plot = 1:(n.treat.total.byblock * n.block),
                              rep = rep(1:r, each = (n.treat.total.byblock * n.block/r)),
                              rep.eff = rep(xr, each = (n.treat.total.byblock * n.block/r)),
                              row.gis = row.gis.mean,
                              col.gis = rep(1:n.block - 1 , each = n.treat.total.byblock) %% layout[1] + 1)
  
  parameters = c(n_block = n.block, reps = r, n_plant = n.plant, row = n.row,
                 n_row_treat = n.row.treat, treat_reg_byblock = n.treat.reg.byblock,
                 treat_reg_byblock = n.treat.total.byblock, x.hat = x.hat, sigma.e = sigma.e)
  
  cat("#Block:", n.block, "\n",
      "#Reps:", r, "\n",
      "#Plant:", n.plant, "\n",
      "#Row:", n.row, "\n",
      "#Row each treat:", n.row.treat, "\n",
      "#Checks:", n.treat.check, "\n",
      "#Regular treat each block:", n.treat.reg.byblock, "\n",
      "#Total treat each block:", n.treat.total.byblock)
  
  if(write.files==T){
    write.table(book.blender.full, paste0("bpy.", design, ".", H2, ".", sigma.t, ".", as.character(seed), ".txt"), row.names = F, col.names = F)
    write.table(book.qgis.full, paste0("qgis.ind.", design, ".", H2, ".", sigma.t, ".", as.character(seed), ".txt"), row.names = F, col.names = T)
    write.table(book.qgis.mean, paste0("qgis.plot.", design, ".", H2, ".", sigma.t, ".", as.character(seed), ".txt"), row.names = F, col.names = T)
    write.table(parameters, paste0("par.", design, ".", H2,".", sigma.t, ".", as.character(seed), ".txt"), row.names = F, col.names = F)
  }
  
  return(list(book.blender.full = book.blender.full,
              book.qgis.full = book.qgis.full,
              book.qgis.mean = book.qgis.mean,
              parameters = parameters))
}
