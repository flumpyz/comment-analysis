from pathlib import Path
from wordcloud import WordCloud
from sentiment_determinant import SentimentDeterminant
import commentParser as cp


class Word_Cloud:
    @staticmethod
    def make_picture(video_url):
        # Читать текстовое содержимое
        cp.getCommentsFromVideo(video_url, 0)
        list = SentimentDeterminant.get_comments_from_file("parent_video_comment.csv")
        file = open('comments.txt', 'w', encoding='utf-8')
        for item in list:
            file.write("%s\n" % item)
        file.close()
        current_directory = Path.cwd()
        text = Path.open(current_directory/"comments.txt", encoding='utf-8').read()

        # Создать объект экземпляра облака слов
        wordcloud = WordCloud()

        # Загрузить текстовое содержимое в объект облака слов.
        wordcloud.generate(text)

        # Вывести изображение с заданным именем файла изображения.
        wordcloud.to_file('WordCloud_pic.png')
