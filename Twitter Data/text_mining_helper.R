##################################################
############# SCRIPT AUXILIAR #################
##################################################

hashtag_pat <- "#\\S+"
hashtag.string <- str_extract_all(string = tts$text, pattern = hashtag_pat, simplify = F) %>% as.character()
hashtag_word <- unlist(hashtag.string)
hashtag_word <- gsub("[[:punct:]]", "", hashtag_word)
hashtag_word <- gsub('character0','NA',hashtag_word)
hashtag_word <- gsub('c','',hashtag_word)
#hashtag_word <- gsub('…','NA',hashtag_word)
hashtag.join <- data.frame(Hashtags = hashtag_word)