from sqlalchemy import Column, Integer, String, Date, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:secret@172.21.0.2/dev', echo=True)
Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True)
    data_begin = Column(Date)
    month_budget = Column(Integer)
    balance = Column(Integer)
    daily_income_time = Column(Time)
    
    def __init__(self, chat_id, data_begin, month_budget, balance, daily_income_time):
       self.chat_id = chat_id
       self.data_begin = data_begin
       self.month_budget = month_budget
       self.balance = balance
       self.daily_income_time = daily_income_time

    def __repr__(self):
        return "<Chat('%s','%d')>" % (self.chat_id, self.month_budget)

Session = sessionmaker(bind=engine)
session = Session()