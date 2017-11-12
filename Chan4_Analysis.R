library(tibble)
library(tidyr)
library(dplyr)
library(quanteda)

# First tried just looking at the most common words in the 4chan data cut
# It was not particularly interesting or meaningful.
chan4_df <- read.csv(file = "posts_4chan_pol_delim.csv",
             header = TRUE,
             sep = ",",
             stringsAsFactors = FALSE)

chan4_df <- as.tibble(chan4_df)

chan4_df <- chan4_df %>% gather(key = "word_no",
                                value = "word",
                                comment_1:comment_206)

chan4_df %>% group_by(word) %>% count(X) %>% arrange(desc(.))

sort(table(chan4_df$word),decreasing=TRUE)

#Here, I utilized quanteda to parse the words into pairs or larger groups
setwd("~/DataDive 2017")
chan4_full <- read.csv(file = "posts_4chan_pol_2.csv",
                              header = TRUE,
                              sep = ",",
                              stringsAsFactors = FALSE)

#Converted timestamp from UNIX to POSIXct
chan4_full$Timestamp <- anytime(chan4_full$Timestamp)

#Removed every symbol other than letters and spaces
chan4_full$Comment <- as.character(gsub("[^a-zA-Z ]+","",chan4_full$Comment))

#Created the corpus object for use in the package
chan4_corpus <- corpus(chan4_full,text_field="Comment")

#Created an object of tokens (individual words parsed out) and removed common filler
#words and some arbitrarily selected common terms in the set
chan4_toks <- tokens(chan4_corpus,remove_punct=TRUE,remove_symbols=TRUE)
chan4_toks <- removeFeatures(chan4_toks,stopwords())
chan4_toks <- removeFeatures(chan4_toks,c("like","go","ive","im"))

#Created top sets of various sizes of ngrams (word pairs/triples/quadruples)
#Word pairs
chan4_ngram2 <- tokens_ngrams(chan4_toks)
tf_ng2 <- topfeatures(dfm(chan4_ngram2),n=50)
#Word triplets
chan4_ngram3 <- tokens_ngrams(chan4_toks,n=3L)
tf_ng3 <- topfeatures(dfm(chan4_ngram3),n=50)
#Word quadruplets
chan4_ngram4 <- tokens_ngrams(chan4_toks,n=4L)
tf_ng4 <- topfeatures(dfm(chan4_ngram4),n=50)

#Started to explore these top features to see the context in which these phrases were
#used. More refinement is needed to select meaningful phrases
kwic(chan4_toks,gsub("_"," ",tf_ng3[[1]]),valuetype="glob")
kwic(chan4_full$Comment,"world trade",window=10,valuetype="glob")


