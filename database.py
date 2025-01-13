import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from aiogram.types import Message

# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase): pass

class Operation(Base):
    __tablename__ = 'operations'
    operation = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Date)
    cost_category = sqlalchemy.Column(sqlalchemy.String)
    cost_amount = sqlalchemy.Column(sqlalchemy.Integer)


def database_connect(operation_unit:Operation):
    # Создание базы данных и таблицы (если их нет)
    # создание движка
    engine = sqlalchemy.create_engine('sqlite:///database.db')

    # запуск движка и подключение
    conn = engine.connect()

    # Метаданные - вся инфорация об устройстве таблиц
    metadata = sqlalchemy.MetaData()

    # Создание таблицы
    costs = sqlalchemy.Table('operations', metadata,
                     sqlalchemy.Column('operation', sqlalchemy.Integer, primary_key=True),
                     sqlalchemy.Column("user_id", sqlalchemy.Integer),
                     sqlalchemy.Column('date', sqlalchemy.Date),
                     sqlalchemy.Column('cost_category', sqlalchemy.Integer),
                     sqlalchemy.Column('cost_amount', sqlalchemy.Integer)
                     )

    # Создание объекта таблицы
    metadata.create_all(engine)

    # Подключение к базе данных
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    with session(bind=engine) as db:
        db.add(operation_unit)
        db.commit()
        db.close()


        # # получение всех объектов (Просмотр всей базы данных)
        # operations = db.query(Operation).all()
        # for op in operations:
        #     print(f"{op.operation}: {op.user_id}; {op.date}; {op.cost_category}; {op.cost_amount}")


# Отображение последних limit записей пользователя
def show_last_records(user_id:int, limit:int):
    # создание движка
    engine = sqlalchemy.create_engine('sqlite:///database.db')

    # Подключение к базе данных
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    with session(bind=engine) as db:
        operations = db.query(Operation).order_by(Operation.date.desc()).filter(Operation.user_id == user_id).limit(limit)
        db.close()
        return operations



# Удаление одной из последних 4 записей пользователя
def del_record(operation):
    # создание движка
    engine = sqlalchemy.create_engine('sqlite:///database.db')

    # Подключение к базе данных
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    with session(bind=engine) as db:
        db.delete(operation)
        db.commit()
        db.close()



