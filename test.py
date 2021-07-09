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
from DateChecker import Date_Checker as dc


DataBase = sql.SQL('VideoDatabase')
interaction = sql.Interaction(DataBase)
interaction.create_user_table()
interaction.create_statistic_table()
interaction.create_table_for_admins()
interaction.create_favourites_table()
interaction.create_table_for_moderators()
message = 'https://www.youtube.com/channel/UC_WdeoiTXMr-c_jMSP7PLmQ 2021-07-06 2021-07-10'
id = message[32:56]
vp.getVideoFromChannel(id)
dc.check_date(message[57:67], message[68:78])
