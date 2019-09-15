CREATE DATABASE IF NOT EXISTS dev;
USE dev;
CREATE TABLE IF NOT EXISTS 'chats'(
    'chat_id' int,
    'data_begin' date,
    'month_budget' int,
    'balance' int,
    'daily_income_tome' time,
    'month_update' datetime,
    PRIMARY KEY ('chat_id')
);