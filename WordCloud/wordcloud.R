# Installing the Packages
#---------------------------------------
install.packages("tm")  # for text mining
install.packages("SnowballC") # for text stemming
install.packages("wordcloud") # word-cloud generator 
install.packages("RColorBrewer") # color palettes

# Load the packages
#---------------------------------------
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")

#Import the required file
#---------------------------------------
text <- readLines(file.choose())

# Load the data as a corpus
#---------------------------------------
docs <- Corpus(VectorSource(text))

inspect(docs)

#To Remove special Characters
#---------------------------------------
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "/")
docs <- tm_map(docs, toSpace, "@")
docs <- tm_map(docs, toSpace, "\\|")
docs <- tm_map(docs, toSpace, ";")

#Cleaning the data
#---------------------------------------
# Convert the text to lower case
docs <- tm_map(docs, content_transformer(tolower))
# Remove numbers
docs <- tm_map(docs, removeNumbers)
# Remove punctuations
docs <- tm_map(docs, removePunctuation)
# Eliminate extra white spaces
docs <- tm_map(docs, stripWhitespace)
# Remove english common stopwords
docs <- tm_map(docs, removeWords, stopwords("english"))
# Remove your own stop word
docs <- tm_map(docs, removeWords, c("http", "https", "blogdetails")) 

# Text stemming(Optional)
docs <- tm_map(docs, stemDocument)

#To build a Term Document Matrix
dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)

#Word Cloud
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))

#Top 10 Frequent words plot
head(d, 10)
barplot(d[1:10,]$freq, las = 2, names.arg = d[1:10,]$word,
        col ="lightblue", main ="Most frequent words",
        ylab = "Word frequencies")


