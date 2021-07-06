from telebot import types

import sql

user_role = "admin"
try:
    DataBase = sql.SQL('db.db')
    interaction = sql.Interaction(DataBase)
    interaction.create_table_for_admins()
except:
    pass


def main_keyboard(message):
    keyboardmain = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    if message.from_user.username is not None:
        if interaction.get_user_admin(message.from_user.username) is not None:
            keyboardmain.add("Функции администратора")
    else:
        if interaction.get_user_admin(message.from_user.id) is not None:
            keyboardmain.add("Функции администратора")

    keyboardmain.add("Анализ комментариев")
    keyboardmain.row("Избранное", "История")

    return keyboardmain


def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Добавить нового администратора")
    keyboard.add("Удалить администратора")
    keyboard.add("Добавить нового модератора")
    keyboard.add("Удалить модератора")
    keyboard.add("Посмотреть статистику")
    keyboard.add("Назад")

    return keyboard


def statistics_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Новые пользователи")
    keyboard.add("Действия пользователей за неделю")
    keyboard.add("Назад")

    return keyboard


def new_users_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("За день")
    keyboard.add("За неделю")
    keyboard.add("Назад")

    return keyboard


def analysis_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    if message.from_user.username is not None:
        if (interaction.get_user_admin(message.from_user.username) or interaction.get_user_moder(message.from_user.username)) is not None:
            keyboard.add("На канале")
    else:
        if (interaction.get_user_admin(message.from_user.id) or interaction.get_user_moder(message.from_user.id)) is not None:
            keyboard.add("На канале")
    keyboard.add("Под видео")
    keyboard.add("Назад")

    return keyboard


def back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Назад")

    return keyboard


def fav_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Посмотреть избранное")
    keyboard.add("Добавить в избранное")
    keyboard.add("Удалить из избранного")
    keyboard.add("Назад")

    return keyboard
