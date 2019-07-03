from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from datetime import datetime, date, time
import os
import db
from db import Chat
import calendar


data = {}
updater = None

SETTING, SET_TIMER, LIVE, SPEND, EARN = range(5)

def start(update, context):
    # update.message.reply_text('Send me the sum on month: /set <sum>')
    # Создаём новую запись в бд, или игнорит, есл страрая была
    update.message.reply_text('Привет! Давай начнём работу.\nОтправь мне сколько ты готов тратить в этот месяц ')
    return SETTING

def set(update, context):
    chat_id = update.message.chat_id
    month_sum = int(update.message.text)

    day_sum = month_sum / 30
    data[chat_id] = {"sum": month_sum, "day_sum": month_sum / 30, "balance": month_sum / 30}
    update.message.reply_text('В месяц вы готовы тратить {}p. \nПолучается в день можете портатить {}p.'.format(month_sum, month_sum / 30))

    #Записываем в бд
    chat = db.get_chat(chat_id)
    chat.data_begin = datetime.now().date()
    chat.month_budget = month_sum
    chat.balance = round(day_sum)
    db.session.commit()

    #ЧАСТЬ С ЗАДАНИЕМ ВРЕМЕНИ ОПОВЕЩЕНИЯ
    d = date(2019, 3, 14)

    #-3 for heroku app
    t = time(6, 00)
    dt = datetime.combine(d, t)

    job = context.job_queue.run_daily(dialy_update_balance, dt.time(), context=chat_id)
    job_m = context.job_queue.run_once(month_end, db.data_begin +  + datetime.timedelta(days=30) , context=chat_id)

    chat.daily_income_time = t ##добавляем в бд время
    db.session.commit()

    #add job to the context
    name = 'job'+ str(chat_id)

    context.chat_data[name] = job
    #КОНЕЦ ЧАСТИ

    update.message.reply_text('Теперь, если будешь тратить или внезапно получишь деньги отправляй: /spend или /earn')

    return LIVE

def spend(update, context):
    update.message.reply_text('Напишите мне сколько вы потратили')
    return SPEND

def do_spend(update, context):
    amount = int(update.message.text)
    chat_id = update.message.chat_id
    chat = db.get_chat(chat_id)
    data[chat_id]["balance"] -= amount
    chat.balance -=amount
    db.session.commit()

    text = 'Вы потратили '
    update.message.reply_text(text + '{} p.\nСегодня вы можете потратить ещё {}.p'.format(amount, data[chat_id]["balance"]))

    return LIVE

def earn(update, context):
    update.message.reply_text('Напишите мне сколько вы заработали')
    return EARN

def do_earn(update, context):
    amount = int(update.message.text)
    chat_id = update.message.chat_id
    chat = db.get_chat(chat_id)
    data[chat_id]["balance"] += amount
    chat.balance += amount
    db.session.commit()

    text = 'Вы заработали '
    update.message.reply_text(text + '{} p.\nСегодня вы можете потратить ещё {}.p'.format(amount, data[chat_id]["balance"]))
    return LIVE

def status(update, context):
    update.message.reply_text(data[update.message.chat_id])

def dialy_update_balance(context):
    job = context.job
    chat_id = job.context
    chat = db.get_chat(chat_id)
    day_sum = round(chat.month_budget / 30)
    chat.balance += day_sum
    db.session.commit()
    # data[chat_id]["balance"] += data[chat_id]["day_sum"]
    updater.bot.send_message(chat_id, text='Доброе утро!\n+{}\nСегодня вы можете потратить {}p.\n'.format(day_sum, chat.balance))

def month_end(update, context):
    job = context.job
    chat_id = job.context
    chat = db.get_chat(chat_id)
    context.bot.send_message(chat_id, text='Поздравляю, прошёл месяц.\nВаш баланс: {} \n\n Чтобы начать снова нажмите \stop и потом \start'.format(chat.balance))

def stop(update, context):

    chat_id = update.message.chat_id
    chat = db.get_chat(chat_id)
    name = 'job' + str(chat_id)

    #Изменить на БДшные
    if name not in context.chat_data or chat == None or chat.daily_income_time == None :
        update.message.reply_text('У вас нет активных аккаунтов. Отправь мне /start чтобы начать заново.')
        return ConversationHandler.END

    job = context.chat_data[name]
    job.schedule_removal()
    del context.chat_data[name]

    del data[update.message.chat_id]
    chat.daily_income_time = None
    db.session.commit()

    update.message.reply_text('Ваш аккаунт диактивирован. Отправь мне /start чтобы начать заново.')

    return ConversationHandler.END

def do_echo(update):
    update.message.reply_text(update.message.text)

def job_queue_after_reboot(updater):
    j = updater.job_queue
    chats = db.session.query(Chat).all()
    for chat in chats:
        if (chat.daily_income_time != None):
            j.run_daily(dialy_update_balance, chat.daily_income_time, context=chat.chat_id)
        ## И еще добавить херню по оканчанию месяца

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = os.getenv("TOKEN", "796647708:AAH4AM9ZOaBaUQCUAwRe3YhN1pA4nC8rzLM")
    global updater
    updater = Updater(token=TOKEN, use_context=True, base_url="https://telegg.ru/orig/bot")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SETTING: [MessageHandler((Filters.text | Filters.group), set)],
            LIVE: [CommandHandler("spend", spend),
                   CommandHandler("earn", earn) ],
            SPEND: [MessageHandler((Filters.text | Filters.group), do_spend)],
            EARN: [MessageHandler((Filters.text | Filters.group), do_earn)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("status", status))

    message_handler = MessageHandler(Filters.text, do_echo)
    dp.add_handler(message_handler)

    job_queue_after_reboot(updater)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()