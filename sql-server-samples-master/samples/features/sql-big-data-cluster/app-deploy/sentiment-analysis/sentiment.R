library(MicrosoftML)
rds <- readRDS("sentiment.rds")
model <- rxUnserializeModel(rds)

handler <- function(reviewText) {
  dataFrame = data.frame(Text = reviewText, Rating = as.integer(c(0)), stringsAsFactors = FALSE)
  result <- rxPredict(model, data = dataFrame)
  result
}