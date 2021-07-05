from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from sql import SQL

bot = Bot('1898335775:AAGrZ6w2Mhk1oMZVZHqg7P4hicEXms8e76Y')
dp = Dispatcher(bot)

db = SQL('db.db')


@dp.message_handler(commands=['admin_panel'])
async def admin_panel(message: types.Message):
    status = db.get_status(message.from_user.id)
    if status != 1:
        await message.answer('You have no rights')
    else:
        button_change_status = KeyboardButton('/change_status')
        button_choose_period = KeyboardButton('/choose_period')
        button_analyse_video = KeyboardButton('/analyse_video')
        admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        admin_kb.add(button_change_status, button_choose_period, button_analyse_video)
        await message.reply('Choose action', reply_markup=admin_kb)


@dp.message_handler(commands=['moderator_panel'])
async def moderator_panel(message: types.Message):
    status = db.get_status(message.from_user.id)
    if status == 3:
        await message.answer('You have no rights')
    else:
        button_choose_period = KeyboardButton('/choose_period')
        button_analyse_video = KeyboardButton('/analyse_video')
        moderator_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        moderator_kb.add(button_choose_period, button_analyse_video)
        await message.reply('Choose action', reply_markup=moderator_kb)


@dp.message_handler(commands=['user_panel'])
async def user_panel(message: types.Message):
    button_analyse_video = KeyboardButton('/analyse_video')
    admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    admin_kb.add(button_analyse_video)
    await message.reply('Choose action', reply_markup=admin_kb)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button_admin = KeyboardButton('/admin_panel')
    button_moderator = KeyboardButton('/moderator_panel')
    button_user = KeyboardButton('/user_panel')

    start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_kb.add(button_admin, button_moderator, button_user)
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    await message.reply('Choose mode', reply_markup=start_kb)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
