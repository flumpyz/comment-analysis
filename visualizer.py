import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Visualizer:

    @staticmethod
    def build_a_schedule(array_of_sentiment_of_comments):
        values = Visualizer.get_an_array_of_comments_by_key(array_of_sentiment_of_comments)
        labels = ["Positive", "Negative", "Neutral", "Speech", "Skip"]
        explode = (0.1, 0, 0.15, 0, 0)
        fig, ax = plt.subplots()
        colors = ["#38FF32", "#FF3232", "#32C4FF", "#FF8A32", "#BA32FF"]
        ax.pie(values,
               labels=labels,
               autopct='%1.1f%%',
               shadow=True,
               explode=explode,
               colors=colors,
               wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"},
               rotatelabels=True)
        ax.axis("equal")
        fig.savefig('schedule.svg')

    @staticmethod
    def analyze_the_number_of_comments_by_key(array_of_sentiment_of_comments, key):
        return {
            'positive': array_of_sentiment_of_comments.count('positive'),
            'negative': array_of_sentiment_of_comments.count('negative'),
            'neutral': array_of_sentiment_of_comments.count('neutral'),
            'speech': array_of_sentiment_of_comments.count('speech'),
            'skip': array_of_sentiment_of_comments.count('skip')
        }[key]

    @staticmethod
    def get_an_array_of_comments_by_key(array_of_sentiment_of_comments):
        count_of_positive = Visualizer.analyze_the_number_of_comments_by_key(array_of_sentiment_of_comments,
                                                                             'positive')
        count_of_negative = Visualizer.analyze_the_number_of_comments_by_key(array_of_sentiment_of_comments,
                                                                             'negative')
        count_of_neutral = Visualizer.analyze_the_number_of_comments_by_key(array_of_sentiment_of_comments,
                                                                            'neutral')
        count_of_speech = Visualizer.analyze_the_number_of_comments_by_key(array_of_sentiment_of_comments,
                                                                           'speech')
        count_of_skip = Visualizer.analyze_the_number_of_comments_by_key(array_of_sentiment_of_comments,
                                                                         'skip')
        return [count_of_positive, count_of_negative, count_of_neutral, count_of_speech, count_of_skip]
