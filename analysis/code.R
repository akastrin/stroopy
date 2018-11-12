library(mongolite)

m <- mongo(db = "test1", collection = "results")

m$find()
m$find()$data[[2]]
