library(RJSONIO)

#Input a URL
url       <- "https://www.reddit.com/r/The_Donald/comments/7c8k0r/just_a_reminder_that_a_little_girl_was_ripped_in/.json"
rawdat    <- fromJSON(readLines(url, warn = FALSE))
main.node <- rawdat[[2]]$data$children

#Getting Comments 
get.comments <- function(node) {
  comment     <- node$data$body
  replies     <- node$data$replies
  reply.nodes <- if (is.list(replies)) replies$data$children else NULL
  return(list(comment, lapply(reply.nodes, get.comments)))
}

txt <- unlist(lapply(main.node, get.comments))
length(txt)

#Writing the output into "data.csv" file which will be created in the current working directory
write.csv(txt, "data.csv")
