library(mongolite)

m <- mongo(db = "test1", collection = "collection1")

m$find()
m$find()$data[[2]]
