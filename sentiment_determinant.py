from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import re


class SentimentDeterminant:

    @staticmethod
    def get_sentiment_array_from_file():
        tokenizer = RegexTokenizer()
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        all_comments_texts = SentimentDeterminant.get_comments_from_file('parent_video_comment.csv')
        dictionary_of_sentiment = []
        keys = []
        results = model.predict(all_comments_texts, k=1)
        for comments, sentiment in zip(all_comments_texts, results):
            dictionary_of_sentiment.append(sentiment)
        for key in dictionary_of_sentiment:
            result_key = str(key)[2:]
            keys.append(re.findall(r'^\w+', str(result_key)).pop(0))
        return keys

    @staticmethod
    def get_comments_from_file(file_name):
        comments_file = open(file_name, 'r')
        comments = comments_file.read().split('Z\n')
        comments.pop(0)
        all_comments_texts = []
        for comment in comments:
            sections_in_comments = comment.split(',')
            all_comments_texts.append(' '.join(sections_in_comments[2:len(sections_in_comments) - 3:]))
        comments_file.close()
        return all_comments_texts
