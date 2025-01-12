from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_keyboard():
    # Названия кнопок
    add_cost_button = KeyboardButton(text='Добавить статью трат')
    del_cost_button = KeyboardButton(text='Удалить статью трат')
    show_last_button = KeyboardButton(text="Последние записи")
    info_button = KeyboardButton(text='Info')


    # создаю объект клавиатуры
    keyboard = ReplyKeyboardMarkup(
        keyboard= [[add_cost_button, del_cost_button],
                   [show_last_button, info_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def select_category_keyboard():
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
    return keyboard


def date_enter_keyboard():
    # Названия кнопок
    today_date_button = KeyboardButton(text='Сегодня')
    yestoday_date_button = KeyboardButton(text="Вчера")
    main_menu_button = KeyboardButton(text="Главное меню")

    # создаю объект клавиатуры
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[today_date_button, yestoday_date_button],
                  [main_menu_button]],
        resize_keyboard=True
    )
    return keyboard

def return_to_menu_keyboard():
    # Названия кнопок
    main_menu_button = KeyboardButton(text="Главное меню")

    # создаю объект клавиатуры
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[main_menu_button]],
        resize_keyboard=True
    )
    return keyboard
