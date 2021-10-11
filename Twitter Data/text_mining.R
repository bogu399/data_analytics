# Data Wrangling and Visualization
library(glue)
library(cowplot)
library(dplyr)
library(ggplot2)
library(tibble)
library(stringr)
library(magrittr)
library(plotly)
library(tidyverse)
library(widyr)
# Date & Time Manipulation.
library(hms)
library(lubridate) 
# Text Mining
library(tidytext)
library(tm)
library(wordcloud)
# Network Analysis
library(igraph)
# Network Visualization (D3.js)
library(networkD3)

################# tts ORIGINAL TABLE / ttr HANDLING TABLE / copyttr HANDLING TABLE'S COPY #################

tts <- read.csv('election.csv',header=T,stringsAsFactors=F,encoding='UTF-8')
head(tts$created)
as_tibble(tts)

#WITHOUT ACCOUNTS SHOWN
ttr <- tts 
#CHR TO DTTM
ttr <- ttr %>% mutate(created = created %>% str_replace('T',' ') %>% parse_date_time(orders = '%Y-%m-%d %%H%M%S')) %>% as_tibble() 
#CONVERTER UTC TO UTC-3 AND GET JUST MINUTES
ttr <- ttr %>% mutate(created = created - (3*60*60))
ttr <- ttr %>% mutate(created_round = created %>% round(units = 'min') %>% as.POSIXct())

#NORMALIZATION
ttr <- ttr %>% mutate(text = text %>% str_remove_all(pattern = '\\n')) %>%
		   mutate(text = text %>% str_remove_all(pattern = '&amp')) %>%
		   mutate(text = text %>% str_remove_all(pattern = 'https://t.co/[a-z,A-Z,0-9]*')) %>%
		   mutate(text = text %>% str_remove_all(pattern = 'http://t.co/[a-z,A-Z,0-9]*')) %>%
		   mutate(text = text %>% str_remove_all(pattern = 'https')) %>%
		   mutate(text = text %>% str_remove_all(pattern = 'http')) %>%
		   mutate(text = text %>% str_remove_all(pattern = '#[a-z,A-Z]*')) %>%
		   mutate(text = text %>% str_remove_all(pattern = '@[a-z,A-Z,0-9]*')) %>%
		   mutate(text = text %>% str_remove_all(pattern = 'rt [a-z,A-Z,0-9]*:')) %>%
		   mutate(text = text %>% str_remove_all(pattern = '^RT')) %>%
		   mutate(text = text %>% str_remove_all(pattern = ' : ')) %>%
		   mutate(text = text %>% str_remove_all(pattern = '\\_')) %>%
		   mutate(text = text %>% str_trim())

#TM CORPUS
corpus <- Corpus(x = VectorSource(x = ttr$text))
ttr.txt <- corpus %>% tm_map(removePunctuation) %>%
	     tm_map(removeNumbers) %>%
	     tm_map(removeWords, stopwords('english')) %>%
	     tm_map(PlainTextDocument)
ttr <- ttr %>% mutate(text = ttr.txt[[1]]$content)

#EXTRACTING HASHTAGS
getHashs <- function(tweet) {
	hashtag.string <- str_extract_all(string = tweet, pattern = "#\\S+", simplify = F) %>% as.character()
	hashtag_word <- unlist(hashtag.string)
	hashtag_word <- gsub("[[:punct:]]", "", hashtag_word)
	hashtag_word <- gsub('character0','NA',hashtag_word)
	hashtag_word <- gsub('c','',hashtag_word)
	########################################### hashtag_word <- gsub('…','NA',hashtag_word) #### SE NECESSÁRIO, USAR
	hashtag.join <- data.frame(Hashtags = hashtag_word)

	return(hashtag.join)
}

#TUTORIAL FUNCTION
GetHashtags <- function(tweet) {

  hashtag.vector <- str_extract_all(string = tweet, pattern = '#\\S+', simplify = TRUE) %>% 
    as.character()
  
  hashtag.string <- NA
  
  if (length(hashtag.vector) > 0) {
    
    hashtag.string <- hashtag.vector %>% str_c(collapse = ', ')
    
  } 

  return(hashtag.string)
}

hashtags.join <- getHashs(tweet = tts$text)



#COPY ttr TABLE

copyttr <- ttr #COPY ttr TABLE
ttr <- copyttr #COPY ttr TABLE

#COPY ttr TABLE


ttr %<>% bind_cols(hashtags.join) #MERGE TABLES?????
ttr <- ttr %>% mutate(Hashtags = Hashtags %>% na_if('NA')) #CONVERTER "NA" EM NA VALUES


#WORD COUNTS
extra.stop.words <- c('q')

stopwords.df <- tibble(
  word = c(stopwords(kind = 'en'),  
           extra.stop.words)
  )
words.ttr <- ttr %>% unnest_tokens(input=text,output=word) %>% anti_join(y = stopwords.df, by = 'word')
words.count.ttr <- words.ttr %>% count(word,sort=T)
words.count.ttr <- words.count.ttr %>% drop_na()
#GET OUT KEYWORDS
words.count.ttr <- words.count.ttr %>% 
	filter(!str_detect(word,"trump")) %>%
	filter(!str_detect(word, "clinton")) %>%
	filter(!str_detect(word, "sanders")) %>%
	filter(!str_detect(word,"hillary")) %>%
	filter(!str_detect(word, "bernie")) %>%
	filter(!str_detect(word, "donald"))


#HASHTAGS COUNTS
hashtag.ttr <- ttr %>% 
  select(created_round, Hashtags) %>% 
  unnest_tokens(input = Hashtags, output = hashtag)


hashtags.count.ttr <- hashtag.ttr %>% 
  count(hashtag,sort = T) %>% 
  drop_na()

#GET OUT KEYWORDS
hashtag.ttr <- hashtag.ttr %>% 
	filter(!str_detect(hashtag,"trump")) %>%
	filter(!str_detect(hashtag, "clinton")) %>%
	filter(!str_detect(hashtag, "sanders")) %>%
	filter(!str_detect(hashtag,"hillary")) %>%
	filter(!str_detect(hashtag, "bernie")) %>%
	filter(!str_detect(hashtag, "donald"))

hashtags.count.ttr <- hashtags.count.ttr %>% 
	filter(!str_detect(hashtag,"trump")) %>%
	filter(!str_detect(hashtag, "clinton")) %>%
	filter(!str_detect(hashtag, "sanders")) %>%
	filter(!str_detect(hashtag,"hillary")) %>%
	filter(!str_detect(hashtag, "bernie")) %>%
	filter(!str_detect(hashtag, "donald"))

#BIGRAM
bigram <- ttr %>% 
		unnest_tokens(input = text,output = bigram, token = 'ngrams', n = 2) %>%
		filter(! is.na(bigram))
bigram %>% select(bigram) %>% head(10)
bigram %<>% 
  separate(col = bigram, into = c('word1', 'word2'), sep = ' ') %>% 
  filter(! word1 %in% stopwords.df$word) %>% 
  filter(! word2 %in% stopwords.df$word) %>% 
  filter(! is.na(word1)) %>% 
  filter(! is.na(word2))
bigram.count <- bigram %>% 
  count(word1, word2, sort = TRUE) %>% 
  # We rename the weight column so that the 
  # associated network gets the weights (see below).
  rename(weight = n)

## NETWORK BIGRAM
threshold <- 100

ScaleWeight <- function(x, lambda) {
  x / lambda
}

network <-  bigram.count %>%
  filter(weight > threshold) %>%
  mutate(weight = ScaleWeight(x = weight, lambda = 2E3)) %>% 
  graph_from_data_frame(directed = T)

clusters(graph = network) #TO SEE THE NETWORK'S ORGANIZATION

## NETWORK SKIPGRAM
skip.window <- 2

skipgram <- ttr %>%
	unnest_tokens(input = text, output = skipgram, token = 'skip_ngrams', n = skip.window) %>%
	filter(!is.na(skipgram))

skipgram <- skipgram %>% mutate(num_words = sapply(strsplit(skipgram, " "), length))

#FILTER TWO WORDS SKIPGRAM - TUTORIAL FOLLOWING
skipgram %<>% filter(num_words == 2) %>% select(- num_words)
skipgram %<>%
	separate(col = skipgram, into = c('word1','word2'), sep = ' ') %>%
	filter(!word1 %in% stopwords.df$word) %>%
	filter(!word2 %in% stopwords.df$word) %>%
	filter(!is.na(word1)) %>%
	filter(!is.na(word2))

skipgram.count <- skipgram %>% 
  count(word1, word2, sort = TRUE) %>% 
  rename(weight = n)

#SKIPGRAM NODE IMPORTANCE
cc.network <- induced_subgraph(
  graph = network,
  vids = which(V(network)$cluster == which.max(clusters(graph = network)$csize))
)

node.impo.df <- tibble(
  word = V(cc.network)$name,  
  degree = strength(graph = cc.network),
  closeness = closeness(graph = cc.network), 
  betweenness = betweenness(graph = cc.network))

#COMMUNITY DETECTION
comm.det <- cluster_louvain(
  graph = cc.network, 
  weights = E(cc.network)$weight
)

#PHI CORRELATION BETWEEN TWO WORDS
cor.words <- words.ttr %>% 
  group_by(word) %>% 
  filter(n() > 10) %>% 
  pairwise_cor(item = word, feature = id_str)






#############################
########    PLOTS   #########
#############################





#TWEETS PER MINUTE
p1 <- ttr %>% count(created_round) %>% ggplot(mapping = aes(created_round,n)) + theme_light() + geom_line(size=1) + xlab(label = 'Date') + ylab(label = NULL) + ggtitle(label = 'Números de Tweets por Minuto')
p1 %>% ggplotly()

#WORDS COUNTS
p2 <- words.count.ttr %>% filter(n > 487) %>% mutate(word = reorder(word,n)) %>% ggplot(aes(x = word,y = n)) + theme_light() + geom_col(fill = 'black', alpha = 0.8) + xlab(NULL) + coord_flip() + ggtitle(label = 'Top 10 Palavras')
p2 %>% ggplotly()

#WORDCLOUD
#WORDS
wordcloud(words = words.count.ttr$word, freq = words.count.ttr$n, min.freq = 100, colors = brewer.pal(8, 'Dark2'))

#HASHTAGS
wordcloud(
  words = str_c('#',hashtags.count.ttr$hashtag), 
  freq = hashtags.count.ttr$n, 
  min.freq = 5, 
  colors=brewer.pal(8, 'Dark2'))

#HASHTAGS TIMELINE
p3 <- hashtag.ttr %>% 
		#filter(hashtag %in% c('prisongaetz','qanon')) %>%
		count(created_round,hashtag) %>%
		drop_na() %>%
		ggplot(mapping = aes(x = created_round,y = n,color=hashtag)) +
			theme_light() +
			xlab(label = 'Date') +
			ggtitle(label = 'Top Hashtags Counts') +
			geom_line() +
			scale_color_manual(values = c('prisongaetz' = 'green3','qanon' = 'red'))
p3 %>% ggplotly()

#HASHTAG TOP10
tophash <- hashtags.count.ttr$hashtag[1:10]
p4 <- hashtag.ttr %>% 
		filter(hashtag %in% tophash) %>%
		count(created_round,hashtag) %>%
		ggplot(mapping = aes(x = created_round,y = n,color=hashtag)) +
			theme_light() +
			xlab(label = 'Date') +
			ggtitle(label = 'Top 10 Hashtags') +
			geom_line(size=1)
p4 %>% ggplotly()

#BIGRAM
threshold <- 100

ScaleWeight <- function(x, lambda) {
  x / lambda
}

network <-  bigram.count %>%
  filter(weight > threshold) %>%
  mutate(weight = ScaleWeight(x = weight, lambda = 2E3)) %>% 
  graph_from_data_frame(directed = T)

p5 <- bigram.count %>% 
  ggplot(mapping = aes(x = log(weight + 1))) +
    theme_light() +
    geom_histogram() +
    labs(title = "Distribuição Ponderada do Bigrama")

#NETWORK BIGRAM
V(network)$degree <- strength(graph = network) 
E(network)$width <- E(network)$weight/max(E(network)$weight)

plot(
  network, 
  vertex.color = 'lightblue',
  vertex.size = 6*V(network)$degree,
  vertex.label.color = 'black', 
  vertex.label.cex = 0.7, 
  vertex.label.dist = 1,
  edge.color = 'gray',
  edge.arrow.size = .35,
  edge.curved = .1,
  edge.width = 4*E(network)$width,
  main = 'Rede dos Brigramas', 
  sub = glue('Peso-Limte: {threshold}'), 
  alpha = 50
)

#FILTER THE BIGGEST BIGRAM
V(network)$cluster <- clusters(graph = network)$membership

cc.network <- induced_subgraph(
  graph = network,
  vids = which(V(network)$cluster == which.max(clusters(graph = network)$csize))
)

V(cc.network)$degree <- strength(graph = cc.network)
E(cc.network)$width <- E(cc.network)$weight/max(E(cc.network)$weight)

 plot(
  cc.network, 
  vertex.color = 'lightblue',
  # Scale node size by degree.
  vertex.size = 20*V(cc.network)$degree,
  vertex.label.color = 'black', 
  vertex.label.cex = 0.6, 
  vertex.label.dist = 1.6,
  edge.color = 'gray', 
  # Set edge width proportional to the weight relative value.
  edge.width = 3*E(cc.network)$width ,
  main = 'Bigram Count Network (Biggest Connected Component)', 
  sub = glue('Weiight Threshold: {threshold}'), 
  alpha = 50
)

#DYNAMIC NETWORK BIGRAM
V(network)$degree <- strength(graph = network) 
E(network)$width <- E(network)$weight/max(E(network)$weight)

network.D3 <- igraph_to_networkD3(g = network)
network.D3$nodes %<>% mutate(Degree = 30*V(network)$degree)
network.D3$nodes %<>% mutate(Group = 1)
network.D3$links$Width <- 30*E(network)$width

forceNetwork(
  Links = network.D3$links, 
  Nodes = network.D3$nodes, 
  Source = 'source', 
  Target = 'target',
  NodeID = 'name',
  Group = 'Group', 
  opacity = 0.9,
  Value = 'Width',
  Nodesize = 'Degree', 
  # We input a JavaScript function.
  linkWidth = JS("function(d) { return Math.sqrt(d.value); }"), 
  fontSize = 12,
  zoom = TRUE, 
  opacityNoHover = 1
)

#SKIPGRAM
threshold <- 100

network <-  skipgram.count %>%
  filter(weight > threshold) %>%
  graph_from_data_frame(directed = FALSE)

V(network)$degree <- strength(graph = network)
E(network)$width <- E(network)$weight/max(E(network)$weight)

plot(
  network, 
  vertex.color = 'lightblue',
  vertex.size = (0.003)*V(network)$degree,
  vertex.label.color = 'black', 
  vertex.label.cex = 0.6, 
  vertex.label.dist = 1.6,
  edge.color = 'gray',
  edge.arrow.size = .35,
  edge.curved = .1,
  #edge.width = E(network)$width,
  main = 'Rede Skigram', 
  sub = glue('Peso-Limte: {threshold}'), 
  alpha = 50
)

#FILTER THE BIGGEST SKIPGRAM - TUTORIAL JUST DID IT
# Select biggest connected component.  
V(network)$cluster <- clusters(graph = network)$membership

cc.network <- induced_subgraph(
  graph = network,
  vids = which(V(network)$cluster == which.max(clusters(graph = network)$csize))
)

# Store the degree.
V(cc.network)$degree <- strength(graph = cc.network)
# Compute the weight shares.
E(cc.network)$width <- E(cc.network)$weight/max(E(cc.network)$weight)

#DYNAMIC SKIPGRAM
# Create networkD3 object.
network.D3 <- igraph_to_networkD3(g = cc.network)
# Define node size.
network.D3$nodes %<>% mutate(Degree = (1E-2)*V(cc.network)$degree)
# Degine color group (I will explore this feature later).
network.D3$nodes %<>% mutate(Group = 1)
# Define edges width. 
network.D3$links$Width <- 10*E(cc.network)$width

forceNetwork(
  Links = network.D3$links, 
  Nodes = network.D3$nodes, 
  Source = 'source', 
  Target = 'target',
  NodeID = 'name',
  Group = 'Group', 
  opacity = 0.9,
  Value = 'Width',
  Nodesize = 'Degree', 
  # We input a JavaScript function.
  linkWidth = JS("function(d) { return Math.sqrt(d.value); }"), 
  fontSize = 12,
  zoom = TRUE, 
  opacityNoHover = 1
)

#CENTRALITY MEASURES
p6 <- node.impo.df %>% 
  ggplot(mapping = aes(x = degree)) +
    theme_light() +
    geom_histogram(fill = 'blue', alpha = 0.8, bins = 30)
p7 <- node.impo.df %>% 
  ggplot(mapping = aes(x = closeness)) +
    theme_light() +
    geom_histogram(fill = 'red', alpha = 0.8, bins = 30)
p8 <- node.impo.df %>% 
  ggplot(mapping = aes(x = betweenness)) +
    theme_light() +
    geom_histogram(fill = 'green4', alpha = 0.8, bins = 30)
plot_grid(
  ... = p6, 
  p7, 
  p8, 
  ncol = 1, 
  align = 'v'
)

#GROUPING
V(cc.network)$membership <- membership(comm.det)
network.D3$nodes$Group <- V(cc.network)$membership

forceNetwork(
  Links = network.D3$links, 
  Nodes = network.D3$nodes, 
  Source = 'source', 
  Target = 'target',
  NodeID = 'name',
  Group = 'Group', 
  opacity = 0.9,
  Value = 'Width',
  Nodesize = 'Degree', 
  # We input a JavaScript function.
  linkWidth = JS("function(d) { return Math.sqrt(d.value); }"), 
  fontSize = 12,
  zoom = TRUE, 
  opacityNoHover = 1
)

#PHI CORRELATION
topic.words <- c('trump', 'biden', 'gaetz')

threshold <- 0.1

network <- cor.words %>%
  rename(weight = correlation) %>% 
  # filter for relevant nodes.
  filter((item1 %in% topic.words | item2 %in% topic.words)) %>%
  filter(weight > threshold) %>%
  graph_from_data_frame(directed = F)
  
V(network)$degree <- strength(graph = network)

E(network)$width <- E(network)$weight/max(E(network)$weight)

network.D3 <- igraph_to_networkD3(g = network)

network.D3$nodes %<>% mutate(Degree = 5*V(network)$degree)

# Define color groups. 
network.D3$nodes$Group <- network.D3$nodes$name %>% 
  as.character() %>% 
  map_dbl(.f = function(name) {
    index <- which(name == topic.words) 
    ifelse(
      test = length(index) > 0,
      yes = index, 
      no = 0
    )
  }
)

network.D3$links %<>% mutate(Width = 10*E(network)$width)

plot(
  network, 
  vertex.color = 'lightblue',
  vertex.size = (0.01)*V(network)$degree,
  vertex.label.color = 'black', 
  vertex.label.cex = 0.6, 
  vertex.label.dist = 1,
  edge.color = 'gray',
  edge.arrow.size = .35,
  edge.curved = .1,
  #edge.width = E(network)$width,
  main = 'Correlação (Phi) {Trump, Biden, Gaetz}', 
  sub = glue('Correlação-Limte: {threshold}'), 
  alpha = 50
)

forceNetwork(
  Links = network.D3$links, 
  Nodes = network.D3$nodes, 
  Source = 'source', 
  Target = 'target',
  NodeID = 'name',
  Group = 'Group', 
  # We color the nodes using JavaScript code.
  colourScale = JS('d3.scaleOrdinal().domain([0,1,2]).range(["gray", "blue", "red", "black"])'), 
  opacity = 0.8,
  Value = 'Width',
  Nodesize = 'Degree', 
  # We define edge properties using JavaScript code.
  linkWidth = JS("function(d) { return Math.sqrt(d.value); }"), 
  linkDistance = JS("function(d) { return 550/(d.value + 1); }"), 
  fontSize = 18,
  zoom = TRUE, 
  opacityNoHover = 1
)