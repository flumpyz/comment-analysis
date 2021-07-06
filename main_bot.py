import telebot
import sql
import datetime as dt
import keyboards
import commentParser as cp
import videoParser as vp
from sentiment_determinant import SentimentDeterminant
from sql import SQL
from visualizer import Visualizer

bot = telebot.TeleBot('1898335775:AAGrZ6w2Mhk1oMZVZHqg7P4hicEXms8e76Y')

DataBase = sql.SQL('VideoDatabase')
interaction = sql.Interaction(DataBase)
interaction.create_user_table()
interaction.create_statistic_table()
interaction.create_table_for_admins()
interaction.create_favourites_table()
interaction.create_table_for_moderators()


def GetState(message):
    if message.from_user.username is not None:
        data = interaction.get_user_state(str(message.from_user.username))
        state = int(data[0][1])
    else:
        data = interaction.get_user_state(str(message.from_user.id))
        state = int(data[0][1])
    return state


def SetState(message, number_state):
    if message.from_user.username is not None:
        interaction.update_state_in_user_table(str(message.from_user.username), str(number_state))
    else:
        interaction.update_state_in_user_table(str(message.from_user.id), str(number_state))


@bot.message_handler(commands=['start'])
def start_work(message):
    try:
        if message.from_user.username is not None:
            interaction.insert_into_user_table(message.from_user.username, 0)
        else:
            interaction.insert_into_user_table(str(message.from_user.id), 0)
    except:
        pass
    bot.send_message(message.chat.id,
                     "Ссылки принимаются только такого формата"
                     "\nВидео: https://www.youtube.com/watch?v***"
                     "\nКанал: https://www.youtube.com/channel/***, необходимо указать только ID канала на месте звездочек",
                     reply_markup=keyboards.main_keyboard(message))


@bot.message_handler(content_types=['text'])
def processing_message(message):
    if message.text == "Функции администратора":
        bot.send_message(message.chat.id, "Функции администратора", reply_markup=keyboards.admin_keyboard())

    elif message.text == "Добавить нового администратора":
        bot.send_message(message.chat.id, "Введите username пользователя, которого вы хотите сделать администратором")
        SetState(message, 71)

    elif message.text == "Удалить администратора":
        bot.send_message(message.chat.id,
                         "Введите username пользователя, которого вы хотите убрать из списка администраторов")
        SetState(message, 72)

    elif message.text == "Добавить модератора":
        bot.send_message(message.chat.id,
                         "Введите username пользователя, которого вы хотите убрать из списка модераторов")
        SetState(message, 81)

    elif message.text == "Удалить модератора":
        bot.send_message(message.chat.id,
                         "Введите username пользователя, которого вы хотите убрать из списка модераторов")
        SetState(message, 82)

    elif message.text == "Посмотреть статистику":  # новые + за неделю
        bot.send_message(message.chat.id, "Статистика", reply_markup=keyboards.statistics_keyboard())

    elif message.text == "Новые пользователи":  # за день за неделю
        bot.send_message(message.chat.id, "Новые пользователи", reply_markup=keyboards.new_users_keyboard())

    elif message.text == "За день":
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())
        today_date = dt.date.today()
        data = interaction.check_new_users(today_date)
        if data == []:
            bot.send_message(message.chat.id, f'Количество новых пользователей за день: 0',
                             reply_markup=keyboards.back_keyboard())
        else:
            bot.send_message(message.chat.id, f'Количество новых пользователей за день: {len(data)}',
                             reply_markup=keyboards.back_keyboard())

    elif message.text == "За неделю":
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())
        today_date = dt.date.today()
        quantity = interaction.check_week_new_users()
        if quantity == []:
            bot.send_message(message.chat.id, f'Количество новых пользователей за неделю: 0',
                             reply_markup=keyboards.back_keyboard())
        else:
            bot.send_message(message.chat.id, f'Количество новых пользователей за неделю: {quantity[0][0]}',
                             reply_markup=keyboards.back_keyboard())

    elif message.text == "Действия пользователей за неделю":  # юзернейм действие по датам (неделя)
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())
        string = ''
        action_ac = interaction.print_actions_from_statistic_table('ac')
        if action_ac == []:
            string += 'Анализ комментариев под видео: 0 раз\n'
        else:
            string += f'Анализ комментариев под видео: {len(action_ac)} раз' + '\n'

        action_cc = interaction.print_actions_from_statistic_table('cc')
        if action_cc == []:
            string += 'Сравнение двух видео: 0 раз\n'
        else:
            string += f'Сравнение двух видео: {len(action_cc)} раз' + '\n'

        action_ach = interaction.print_actions_from_statistic_table('ach')
        if action_ach == []:
            string += 'Анализ комментариев на канале: 0 раз\n'
        else:
            string += f'Анализ комментариев на канале: {len(action_ach)} раз' + '\n'

        bot.send_message(message.chat.id, string, reply_markup=keyboards.back_keyboard())

    elif message.text == "Анализ комментариев":
        bot.send_message(message.chat.id, "Проанализировать комментарии...", reply_markup=keyboards.analysis_keyboard(message))

    elif message.text == "Избранное":
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboards.fav_keyboard())

    elif message.text == "История":
        # выводим список из 10 последний ссылок
        bot.send_message(message.chat.id, "История", reply_markup=keyboards.back_keyboard())
        bot.send_message(message.chat.id, "Список 10 последних ссылок")

    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=keyboards.main_keyboard(message))

    elif message.text == "Под видео":
        bot.send_message(message.chat.id, "Введите ссылку на видео", reply_markup=keyboards.back_keyboard())
        SetState(message, 1)

    elif message.text == "На канале":
        bot.send_message(message.chat.id, "Введите ссылку на канал", reply_markup=keyboards.back_keyboard())
        SetState(message, 2)

    elif message.text == "Посмотреть избранное":
        bot.send_message(message.chat.id, "Выводим список избранных", reply_markup=keyboards.back_keyboard())
        if message.from_user.username is not None:
            favourites = interaction.print_favorites_table(message.from_user.username)
        else:
            favourites = interaction.insert_into_statistic_table(str(message.from_user.id))
        count = 1
        string = ''
        for i in favourites:
            string += f'{count}. i[1]'

        bot.send_message(message.chat.id, string, reply_markup=keyboards.back_keyboard())

    elif message.text == "Добавить в избранное":
        # проверка на количесвто избранных (макс 10)
        bot.send_message(message.chat.id, "Введите ссылку, которую вы хотите добавить в избранное",
                         reply_markup=keyboards.back_keyboard())
        SetState(message, 51)

    elif message.text == "Удалить из избранного":
        bot.send_message(message.chat.id, "Введите ссылку, которую вы хотите удалить из избранного",
                         reply_markup=keyboards.back_keyboard())
        SetState(message, 52)

        # занесение в бд
        # картинка

    elif message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Доброго времени суток! Что вы хотите сделать?",
                         reply_markup=keyboards.main_keyboard(message))

    elif message.text == "/help":
        bot.send_message(message.chat.id,
                         "Если возникла ошибка после ввода ссылки => была введена неверная ссылка. Попробуйте ввести другую "
                         "\nЕсли вы не знаете как начать со мной работать => просто напишите мне 'Привет'"
                         "\nОбращаем ваше внимание на то, что ссылки, который вы подаете боту, должны быть в следующем формате:"
                         "\nВидео: https://www.youtube.com/watch?v***"
                         "\nКанал: https://www.youtube.com/channel/***  или \nhttps://www.youtube.com/user/***")

    elif message.text[0:31] == "https://www.youtube.com/watch?v":
        if GetState(message) == 1:
            try:
                if message.from_user.username is not None:
                    interaction.insert_into_statistic_table(message.from_user.username, "ac")
                else:
                    interaction.insert_into_statistic_table(str(message.from_user.id), "ac")

                bot.link_video1 = message.text
                #cp.getCommentsFromVideo(bot.link_video1)
                comments = SentimentDeterminant.get_sentiment_array_from_file()
                Visualizer.build_a_schedule(comments)
                bot.send_message(message.chat.id,
                                 "Анализ комментариев может занять некоторое время, пожалуйста, дождитесь результата.")
                f = open("schedule.svg", "rb")
                bot.send_document(message.chat.id, f)
            except:
                bot.send_message(message.chat.id, "Произошла непредвиденная ошибка, попробуйте еще раз. Если ошибка "
                                                  "не исправляется - попробуйте удалить чат с ботом и попробовать "
                                                  "сначала")
            SetState(message, 0)

    else:
        bot.send_message(message.chat.id, "Возникла ошибка. Была введена неизвестная команда или неверная ссылка"
                                          "\nНапишите /help")
        SetState(message, 0)


bot.polling(none_stop=True, interval=0)
