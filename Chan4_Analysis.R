chan4_df <- read.csv(file = "posts_4chan_pol_delim.csv",
             header = TRUE,
             sep = ",",
             stringsAsFactors = FALSE)

library(tibble)
chan4_df <- as.tibble(chan4_df)

library(tidyr)
library(dplyr)

chan4_df <- chan4_df %>% gather(key = "word_no",
                                value = "word",
                                comment_1:comment_206)

chan4_df %>% group_by(word) %>% count(X) %>% arrange(desc(.))

sort(table(chan4_df$word),decreasing=TRUE)

chan4_full <- read.csv(file = "posts_4chan_pol_2.csv",
                              header = TRUE,
                              sep = ",",
                              stringsAsFactors = FALSE)

chan4_corpus <- corpus(chan4_full$Comment)