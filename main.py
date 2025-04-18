# first stage of data cleaning pipeline

# set up os and folders etc

# regex = regex

# for i in range(len(df)):
    # news_article = df['content'][i]
    # matches = regex.finditer(news_article)
    
    # sentence_list = []

    # for match in matches:
        # match_text = match.group(1).strip()  
        # match_text_split = match_text.split()
        # right_context = ' '.join(match_text_split)
        # sentence_list.append(right_context)

    # for sentence in sentence_list:
        # if sentence in news_article:
            # news_article = news_article.replace(sentence, '')
        # else:
            # pass

# second stage of the data cleaning pipeline

# for sentence in sentence_list:
    # if len(sentence) > 0 and len(sentence) <= 25:
        # news_article = news_article.replace(sentence, '')
    # elif "!" in sentence:
        # if sentence.count("!") <= 3:
            # parts = sentence.split("!")
            # news_article = news_article.replace(sentence, '')
    # elif len(sentence) > 25:
        # if sentence.endswith(".") or sentence.endswith("!"):
            # news_article = news_article.replace(sentence, '')
         # else:
            # words = sentence.split()
            # for i in range(len(words) - 1):
                # if words[i].istitle() and words[i + 1].istitle():
                    # sentence = ' '.join(words[-2:])
                    # news_article = news_article.replace(' '.join(words), sentence)

# third stage of the data cleaning pipeline

# create new column of to put cleaned data and another column to see the words that are changed
# create yes/no

# fourth stage of the data cleaning pipeline

# save as csv

# def to check if news article is certainly full or probably full

# def to check words not in cleaned text
