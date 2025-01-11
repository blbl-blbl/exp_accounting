import sqlalchemy
from sqlalchemy.orm import sessionmaker

def database_connect():
    # Подключение к базе данных
    engine = sqlalchemy.create_engine('sqlite:///database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

# класс базы данных
class User(object):
    __tablename__ = 'costs'
    operation = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Date)
    cost_category = sqlalchemy.Column(sqlalchemy.Integer)
    cost_amount = sqlalchemy.Column(sqlalchemy.Integer)


