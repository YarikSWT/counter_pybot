import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from datetime import datetime, date, time

data = {}

SETTING, SET_TIMER, LIVE, SPEND, EARN = range(5)

def start(update, context):
    # update.message.reply_text('Send me the sum on month: /set <sum>')
    update.message.reply_text('Привет! Давай начнём работу.\nОтправь мне сколько ты готов тратить в этот месяц ')

    return SETTING

def set(update, context):
    chat_id = update.message.chat_id
    month_sum = int(update.message.text)
    data[chat_id] = {"sum": month_sum, "day_sum": month_sum / 30, "balance": month_sum / 30}
    update.message.reply_text('В месяц вы готовы тратить {}p. \nПолучается в день можете портатить {}p.'.format(month_sum, month_sum / 30))

    d = date(2019, 3, 14)
    t = time(9)
    dt = datetime.combine(d, t)
    print(dt.time())

    #should replace with run_dialy
    #this is only for test
    job = context.job_queue.run_daily(dialy_update_balance, dt.time(), context=chat_id)

    #add this for
    context.chat_data['job'] = job

    update.message.reply_text('Теперь, если будешь тратить или внезапно получишь деньги отправляй: /spend или /earn')

    return LIVE

def spend(update, context):
    update.message.reply_text('Напишите мне сколько вы потратили')
    return SPEND

def do_spend(update, context):
    amount = int(update.message.text)
    chat_id = update.message.chat_id
    data[chat_id]["balance"] -= amount
    text = 'Вы потратили '
    update.message.reply_text(text + '{} p.\nСегодня вы можете потратить ещё {}.p'.format(amount, data[chat_id]["balance"]))

    return LIVE

def earn(update, context):
    update.message.reply_text('Напишите мне сколько вы заработали')
    return EARN

def do_earn(update, context):
    amount = int(update.message.text)
    chat_id = update.message.chat_id
    data[chat_id]["balance"] += amount
    text = 'Вы заработали '
    update.message.reply_text(text + '{} p.\nСегодня вы можете потратить ещё {}.p'.format(amount, data[chat_id]["balance"]))
    return LIVE

def status(update, context):
    update.message.reply_text(data[update.message.chat_id])

def dialy_update_balance(context):
    job = context.job
    chat_id = job.context
    data[chat_id]["balance"] += data[chat_id]["day_sum"]
    context.bot.send_message(chat_id, text='Доброе утро!\n+{}\nСегодня вы можете потратить {}p.\n'.format(data[chat_id]["day_sum"], data[chat_id]["balance"]))

def stop(update, context):

    if 'job' not in context.chat_data:
        update.message.reply_text('У вас нет активных аккаунтов. Отправь мне /start чтобы начать заново.')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Ваш аккаунт диактивирован. Отправь мне /start чтобы начать заново.')

def do_echo(update):
    update.message.reply_text(update.message.text)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token="773654970:AAEK1AsyL9yuDT-Mt6tuyGPXaMBLyNBd7FA", use_context = True, base_url="https://telegg.ru/orig/bot")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SETTING: [MessageHandler(Filters.text, set)],
            LIVE: [CommandHandler("spend", spend),
                   CommandHandler("earn", earn)
                    ],
            SPEND: [MessageHandler(Filters.text, do_spend)],
            EARN: [MessageHandler(Filters.text, do_earn)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    #хз зачем это надо
    # dp.add_error_handler(error)

    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("set", set))
    # dp.add_handler(CommandHandler("spend", spend))
    dp.add_handler(CommandHandler("status", status))
    # dp.add_handler(CommandHandler("stop", stop))

    message_handler = MessageHandler(Filters.text, do_echo)
    dp.add_handler(message_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()