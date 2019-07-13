from sqlalchemy import Column, Integer, String, Date, Time, DateTime, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DATEBASE_URL= os.getenv("CLEARDB_DATABASE_URL", "mysql://root:secret@database/dev").replace("mysql", "mysql+pymysql").split('?')[0]
print(DATEBASE_URL)
engine = create_engine(DATEBASE_URL, echo=True,  pool_recycle=300)
Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(BigInteger, primary_key=True)
    data_begin = Column(Date)
    month_budget = Column(Integer)
    balance = Column(Integer)
    daily_income_time = Column(Time)
    month_update = Column(DateTime)
    
    def __init__(self, chat_id, data_begin, month_budget, balance, daily_income_time, month_update):
       self.chat_id = chat_id
       self.data_begin = data_begin
       self.month_budget = month_budget
       self.balance = balance
       self.daily_income_time = daily_income_time
       self.month_update = month_update

    def __repr__(self):
        return "<"+str(self.chat_id)+", "+str(self.month_budget)+">"

def get_chat(chat_id):
    chat = session.query(Chat).get(chat_id)
    if chat == None:
        chat = Chat(chat_id, None, None, None, None, None)
        session.add(chat)
    return chat


Session = sessionmaker(bind=engine)
session = Session()