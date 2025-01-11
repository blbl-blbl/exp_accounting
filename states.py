from aiogram.fsm.state import State, StatesGroup

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем

    menu_state = State() # Состояние ожидания ввода команды после /start

    # Добавление трат
    add_cost_state = State() # Состояние ожидания выбора категории затрат после выбора add_cost
    date_cost_state = State() # Состояние ожидания выбора / ввода даты траты
    cost_amount_state = State() # Состояние ожидания ввода значения трат

    # Удаление трат
    del_cost_state = State()     # Состояние ожидания выбора траты которую хотят удалить

