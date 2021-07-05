import telebot

from youtube import commentParser as cp
from youtube import videoParser as vp
from sentiment_determinant import SentimentDeterminant
from sql import SQL
from visualizer import Visualizer

db = SQL('db.db')
bot = telebot.TeleBot('1898335775:AAGrZ6w2Mhk1oMZVZHqg7P4hicEXms8e76Y')


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/admin_panel', '/moderator_panel', '/user_panel')
    bot.send_message(message.chat.id, 'Hi', reply_markup=keyboard)


@bot.message_handler(commands=['admin_panel'])
def admin_panel(message):
    status = db.get_status(message.from_user.id)
    if status != 1:
        bot.send_message(message.chat.id, 'You have no rights')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('/change_status', '/choose_channel', '/get_analyse')
        bot.send_message(message.chat.id, 'Choose action', reply_markup=keyboard)


@bot.message_handler(commands=['moderator_panel'])
def admin_panel(message):
    status = db.get_status(message.from_user.id)
    if status == 3:
        bot.send_message(message.chat.id, 'You have no rights')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('/choose_channel', '/get_analyse')
        bot.send_message(message.chat.id, 'Choose action', reply_markup=keyboard)


@bot.message_handler(commands=['user_panel'])
def admin_panel(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/get_analyse')
    bot.send_message(message.chat.id, 'Choose action', reply_markup=keyboard)


@bot.message_handler(commands=['change_status'])
def change_status(message):
    msg = bot.send_message(message.from_user.id, 'Enter ID and status ID')
    bot.register_next_step_handler(msg, change_status_2)


def change_status_2(message):
    array = message.text.split(' ')
    db.change_subscription(array[0], array[1])
    bot.send_message(message.from_user.id, 'Done!')


@bot.message_handler(commands=['choose_channel'])
def choose_channel(message):
    msg = bot.send_message(message.from_user.id, 'Enter channel ID')
    bot.register_next_step_handler(msg, choose_channel_2)


def choose_channel_2(message):
    vp.getVideoFromChannel(message)
    file = open('parent_video_comment.csv', 'rb')
    bot.send_document(message.from_user.id, file)
    file.close()


@bot.message_handler(commands=['get_analyse'])
def get_analyse(message):
    msg = bot.send_message(message.from_user.id, 'Enter URL')
    bot.register_next_step_handler(msg, get_analyse_2)


def get_analyse_2(message):
    #cp.getCommentsFromVideo(message, 0)
    comments = SentimentDeterminant.get_sentiment_array_from_file()
    Visualizer.build_a_schedule(comments)
    file = open('schedule.svg')
    bot.send_document(message.from_user.id, file)
    file.close()


bot.polling()
