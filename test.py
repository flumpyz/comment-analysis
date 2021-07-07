import telebot
import sql
import datetime as dt
import keyboards
import commentParser as cp
import videoParser as vp
from sentiment_determinant import SentimentDeterminant
from sql import SQL
from visualizer import Visualizer
from word_cloud import Word_Cloud as wc


DataBase = sql.SQL('VideoDatabase')
interaction = sql.Interaction(DataBase)
interaction.create_user_table()
interaction.create_statistic_table()
interaction.create_table_for_admins()
interaction.create_favourites_table()
interaction.create_table_for_moderators()

url = "https://www.youtube.com/watch?v=zyOcvb4-3-E"
info_from_video = cp.get_information_from_youtube_video(url[32:43])
print(info_from_video[1])
