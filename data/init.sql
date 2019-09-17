CREATE DATABASE IF NOT EXISTS dev;
USE dev;
CREATE TABLE IF NOT EXISTS chats(
    chat_id INTEGER,
    data_begin DATE,
    month_budget INTEGER,
    balance INTEGER,
    daily_income_time TIME,
    month_update DATETIME,
    PRIMARY KEY (chat_id)
);