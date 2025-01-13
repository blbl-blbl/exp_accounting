import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from unicodedata import numeric

from config_reader import config
from aiogram.types import Message
from aiogram.fsm.state import default_state

from datetime import datetime, timedelta

import keyboards
from database import Operation, database_connect, show_last_records, del_record
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


operation_unit = Operation()

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

    # Обновление парметра user_id и cost_category для базы данных
    operation_unit.user_id = user_id
    operation_unit.cost_category = category


    # отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text="Выбери дату траты или введи вручную в формате ДД.ММ.ГГ",
        reply_markup=keyboards.date_enter_keyboard()
    )

    # Устанавливаем состояние ожидания выбора / ввода даты траты
    await state.set_state(FSMFillForm.date_cost_state)


# Этот хэндлер будет срабатывать, если была выбрана корректная категория трат
@dp.message(StateFilter(FSMFillForm.date_cost_state))
async def process_amount_sent(message: Message, state: FSMContext):
    # Дата, введенная пользователем
    check_date = message.text
    try:
        # Если была нажата кнопка "сегодня" или "вчера"
        if check_date.lower() == "сегодня":
            check_date = datetime.now().date().strftime('%d.%m.%y')

        elif check_date.lower() == "вчера":
            check_date = (datetime.now().date() - timedelta(days=1)).strftime('%d.%m.%y')

        date = datetime.strptime(check_date, '%d.%m.%y')

        # Проверяем корректность введенной даты и чтобы она не превышала
        # дату сегодняшнего дня
        if date > datetime.now():
            await message.answer(text="Введенная дата больше текущей")
            await state.set_state(FSMFillForm.date_cost_state)
        # Проверка что введенная дата не меньше текущей на 30 дней
        elif date < (datetime.now() - timedelta(days=30)):
            await message.answer(text="Введенная дата не должна быть меньше текущей более "
                                      "чем на 30 дней")
            await state.set_state(FSMFillForm.date_cost_state)

        else:
            await message.answer(text="Введи сумму трат в рублях",
                                 reply_markup=keyboards.return_to_menu_keyboard())
            await state.set_state(FSMFillForm.cost_amount_state)

        # Обновление парметра date для базы данных
        operation_unit.date = datetime.date(date)

    except ValueError:
        await message.answer(text="Неверный формат даты.\n"
                                  "Введите дату в формате ДД.ММ.ГГ (только последние цифры года)")




# Этот хэндлер будет срабатывать, если была введена корректная дата
@dp.message(StateFilter(FSMFillForm.cost_amount_state))
async def process_finish(message: Message, state: FSMContext):
    try:
        amount_input = int(message.text)

        # Обновление парметра cost_amount для базы данных
        operation_unit.cost_amount = amount_input

        # Добавление записи в базу данных
        database_connect(operation_unit=operation_unit)

        await message.answer(text="Запись успешно добавлена",
                             reply_markup=keyboards.start_keyboard())
        await state.set_state(FSMFillForm.menu_state)

    except:
        await message.answer(text="Траты должны быть целым числом")


@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'последние записи')
async def proc_show_last_records(message: Message, state: FSMContext):
    user_id = message.from_user.id
    op_counter = 1
    for op in show_last_records(user_id=user_id, limit=5):
        await message.answer(text=f"{op_counter}. {op.date.strftime('%d.%m.%y')} : {op.cost_category} : {op.cost_amount} руб.")
        op_counter += 1


# Этот хэндлер будет срабатывать, если введена команда'удалить статью трат' на этапе старта
# и переводить в следующее состояние
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'удалить статью трат')
async def proc_del_command(message: Message, state: FSMContext):
    await message.answer(
        text="Введи номер траты которую хочешь удалить",
        reply_markup=keyboards.record_number_for_del()
    )

    user_id = message.from_user.id
    op_counter = 1
    for op in show_last_records(user_id=user_id, limit=4):
        await message.answer(
            text=f"{op_counter}. {op.date.strftime('%d.%m.%y')} : {op.cost_category} : {op.cost_amount} руб.")
        op_counter += 1

    # Устанавливаем состояние ожидания выбора траты которую хотят удалить
    await state.set_state(FSMFillForm.del_cost_state)


# Этот хендлер будет срабатывать при выборе статьи трат, которую хотят удалить
@dp.message(StateFilter(FSMFillForm.del_cost_state))
async def proc_rec_for_del_chose(message: Message, state: FSMContext):
    user_id = message.from_user.id
    number = message.text
    try:
        number = int(number)
        if number not in range(1, 5):
            raise ValueError
        else:
            operation = show_last_records(user_id=user_id, limit=4)[number - 1]
            del_record(operation=operation)
            await message.answer(text="Запись удалена")
            await state.set_state(FSMFillForm.menu_state)
    except ValueError:
        await message.answer(text="Формат ответа в виде числа от 1 до 4")
        await state.set_state(FSMFillForm.del_cost_state)


# Этот хэндлер выдают информацию о боте при запросе 'info'
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'info')
async def proc_info_command(message: Message):
    await message.answer('INFO\nДанный бот создан с целью помочь отслеживать собственные траты. Можешь добавлять сюда'
                             ' свои расходы, разделенные по категориям, а затем в любое время запросить'
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
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except:
        print("Бот остановлен")

asyncio.run(main())


