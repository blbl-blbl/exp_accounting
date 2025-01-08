import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from config_reader import config
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.fsm.state import default_state, State, StatesGroup


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем

    menu_state = State() # Состояние ожидания ввода команды после /start

    # Добавление трат
    add_cost_state = State() # Состояние ожидания выбора категории затрат после выбора add_cost
    cost_amount_state = State() # Состояние ожидания ввода значения трат

    # Удаление трат
    del_cost_state = State()     # Состояние ожидания выбора траты которую хотят удалить



# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к одному из следующих состояний через выбор кнопки
@dp.message(Command('start'), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):

    # Названия кнопок
    add_cost_button = KeyboardButton(text='Добавить статью трат')
    del_cost_button = KeyboardButton(text='Удалить статью трат')
    info_button = KeyboardButton(text='Info')

    # создаю объект клавиатуры
    keyboard = ReplyKeyboardMarkup(
        keyboard= [[add_cost_button, del_cost_button],
                   [info_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Выбери нужную кнопку снизу:",
        reply_markup=keyboard
    )
    # Устанавливаем состояние ожидания ввода команды после /start
    await state.set_state(FSMFillForm.menu_state)


# Этот хэндлер будет срабатывать, если введена команда'добавить статью трат' на этапе старта
# и переводить в следующее состояние
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'добавить статью трат')
async def proc_start1_command(message: Message, state: FSMContext):
    # Названия кнопок - категорий трат
    auto_cost_button = KeyboardButton(text='Авто')
    komm_cost_button = KeyboardButton(text='Коммуналка')
    cafe_cost_button = KeyboardButton(text='Кафе')
    food_cost_button = KeyboardButton(text='Продукты')
    # charity_cost_button = KeyboardButton(text='Благотворительность')
    home_cost_button = KeyboardButton(text='Дом')
    healh_cost_button = KeyboardButton(text='Здоровье')
    personal_cost_button = KeyboardButton(text='Личные расходы')
    gifts_cost_button = KeyboardButton(text="Подарки")
    cloths_cost_button = KeyboardButton(text="Одежда")
    techiq_cost_button = KeyboardButton(text="Техника")
    service_cost_button = KeyboardButton(text="Услуги")
    other_cost_button = KeyboardButton(text='Прочее')
    main_menu_button = KeyboardButton(text="Главное меню")

    # создаю объект клавиатуры
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[auto_cost_button, komm_cost_button, cafe_cost_button, food_cost_button],
                  [home_cost_button, healh_cost_button, personal_cost_button, gifts_cost_button],
                  [cloths_cost_button, techiq_cost_button, service_cost_button, other_cost_button],
                  [main_menu_button]],
        resize_keyboard=True
    )

    # отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text="Выбери категорию затрат",
        reply_markup=keyboard
    )

    # Устанавливаем состояние ожидания выбора категории затрат
    await state.set_state(FSMFillForm.add_cost_state)



# Этот хэндлер будет срабатывать, если введена команда'добавить статью трат' на этапе старта
# и переводить в следующее состояние
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'удалить статью трат')
async def proc_start2_command(message: Message, state: FSMContext):
    await message.answer(
        text="Выбери какую статью трат необходимо удалить"
    )

    # Устанавливаем состояние ожидания выбора траты которую хотят удалить
    await state.set_state(FSMFillForm.del_cost_state)


# Этот хэндлер выдают информацию о боте при запросе 'info'
@dp.message(StateFilter(FSMFillForm.menu_state),
            lambda x: x.text.lower() == 'info')
async def proc_start3_command(message: Message):
    await message.answer('INFO\nДанный бот создан с целью помочь отслеживать собственные траты. Можешь добавлять сюда'
                             'все свои расходы, разделенные по категориям, а затем в любое время запросить'
                             'сформированный Excel файл для их анализа')



# Этот хендлер будет срабатывать на команду "главное меню" в состоянии по умолчанию
# по умолчанию и сообщать, что это команда работает внутри машины состояний
@dp.message(Command('Главное_меню'), StateFilter(default_state))
async def go_menu_command(message: Message):
    await message.answer(
        text="Ты уже в главном меню"
    )


# Этот хэндлер будет срабатывать на команду "назад" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний (перходить в главное меню)
@dp.message(lambda x: x.text.lower() == 'главное меню', ~StateFilter(default_state))
async def go_menu_state(message: Message, state: FSMContext):
    # Названия кнопок
    add_cost_button = KeyboardButton(text='Добавить статью трат')
    del_cost_button = KeyboardButton(text='Удалить статью трат')
    info_button = KeyboardButton(text='Info')

    # создаю объект клавиатуры
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[add_cost_button, del_cost_button],
                  [info_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "Выбери нужную кнопку снизу:",
        reply_markup=keyboard
    )
    # Переход на состояние главного меню
    await state.set_state(FSMFillForm.menu_state)


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


