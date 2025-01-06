import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from unicodedata import category
from config_reader import config
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()
builder = ReplyKeyboardBuilder()


# Хэндлер на команду /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    start_buttons = ['Добавить статью трат', 'Удалить статью трат', 'Info']
    for i in start_buttons:
        builder.add(types.KeyboardButton(text=i))
    builder.adjust(2)
    await message.answer(
        "Выбери нужную кнопку снизу:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_leyboard=True))


# Если в basic_state выбрана кнопка "добавить статью трат"
@dp.message(F.text.lower() == 'добавить статью трат')
async def add_cost(message: types.Message):

    ''' Функция для отображения кнопок с выбором категории трат.
    Существующие категории трат отображены в списке cost_categories. '''


    cost_categories = ['Авто', 'Коммуналка', 'Кафе', 'Еда', 'Благотворительность', 'Прочее']
    for categ in cost_categories:
        builder.add(types.KeyboardButton(text=categ))
    builder.adjust(4)
    await message.answer(
        "Выберете категорию трат:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )
    # Нужно дальше дописать о том что статья расходов добавляется в некоторую базу


# Если в basic_state выбрана кнопка "Удалить статью трат"
# доделать после того как сделаю базу данных
@dp.message(F.text.lower() == 'Удалить статью трат')
async def del_cost(message: types.Message):
    pass


# Если в basic_state выбрана кнопка "Ifno"
# Доделать оформление текста с информацией
@dp.message(F.text.lower() == 'Info')
async def get_info(message: types.Message):
    await message.answer('INFO\nДанный бот создан с целью помочь отслеживать собственные траты. Можешь добавлять сюда'
                         'все свои расходы, разделенные по категориям, а затем в любое время запросить'
                         'сформированный Excel файл для их анализа')


# ЭТО В MAIN
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

asyncio.run(main())


