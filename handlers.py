import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from config_reader import config
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.fsm.state import default_state, State, StatesGroup


import keyboards
from datebase import User, database_connect
from states import FSMFillForm


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

categories = ["авто",
              "коммуналка",
              "кафе",
              "продукты",
              "дом",
              "здоровье",
              "личные расходы",
              "подарки",
              "одежда",
              "техника",
              "услуги",
              "прочее"]

# Подключение к датабазе
database_connect()


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к одному из следующих состояний через выбор кнопки
@dp.message(Command('start'), StateFilter(default_state))
@dp.message(lambda x: x.text.lower() == 'главное меню', ~StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):

    await message.answer(
        "Выбери нужную кнопку снизу:",
        reply_markup=keyboards.start_keyboard()
    )
    # Устанавливаем состояние ожидания ввода команды после /start
    await state.set_state(FSMFillForm.menu_state)


# Этот хэндлер будет срабатывать, если введена команда'добавить статью трат' на этапе старта
# и переводить в следующее состояние
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'добавить статью трат')
async def proc_start_command(message: Message, state: FSMContext):

    # отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text="Выбери категорию затрат",
        reply_markup=keyboards.select_category_keyboard()
    )

    # Устанавливаем состояние ожидания выбора категории затрат
    await state.set_state(FSMFillForm.add_cost_state)


# Этот хэндлер будет срабатывать, если была выбрана сущестующая категория трат
@dp.message(StateFilter(FSMFillForm.add_cost_state),
            lambda x: x.text.lower() in categories)
async def process_date_sent(message: Message, state: FSMContext):

    # Получение данных от пользователя для записи в SQL
    category = message.text.lower()
    user_id = message.from_user.id

    # отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text="Выбери дату траты или введи вручную в формате dd/mm/yyyy",
        reply_markup=keyboards.date_enter_keyboard()
    )

    # Устанавливаем состояние ожидания выбора / ввода даты траты
    await state.set_state(FSMFillForm.add_cost_state)


# Этот хэндлер будет срабатывать, если была введена корректная дата трат
# @dp.message(StateFilter(FSMFillForm.date_cost_state))



# Этот хэндлер будет срабатывать, если введена команда'удалить статью трат' на этапе старта
# и переводить в следующее состояние
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'удалить статью трат')
async def proc_del_command(message: Message, state: FSMContext):
    await message.answer(
        text="Выбери какую статью трат необходимо удалить"
    )

    # Устанавливаем состояние ожидания выбора траты которую хотят удалить
    await state.set_state(FSMFillForm.del_cost_state)


# Этот хэндлер выдают информацию о боте при запросе 'info'
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'info')
async def proc_info_command(message: Message):
    await message.answer('INFO\nДанный бот создан с целью помочь отслеживать собственные траты. Можешь добавлять сюда'
                             'все свои расходы, разделенные по категориям, а затем в любое время запросить'
                             'сформированный Excel файл для их анализа')


# Этот хендлер срабатывает на любые сообщения, кроме тех
# для которых есть отдельные хэндеры
@dp.message(~StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(
        text="Нераспознанная команда"
    )



# ЭТО В MAIN
# Запускаем бота и пропускаем все накопленные входящие
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())


