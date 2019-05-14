import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)

data = {}

def start(update, context):
    update.message.reply_text('Send me the sum on month: /set <sum>')

def set(update, context):
    print(context.args)
    chat_id = update.message.chat_id
    month_sum = int(context.args[0])
    data[chat_id] = {"sum": month_sum, "day_sum": month_sum / 30, "balance": month_sum / 30}
    update.message.reply_text('You set {}p. \n You can spend {}p. per day'.format(month_sum, month_sum / 30))

    #should replace with run_dialy
    #this is only for test
    job = context.job_queue.run_repeating(update_balance, 60, 60, context=chat_id)

    #add this for
    context.chat_data['job'] = job

    update.message.reply_text('If you spend some money, send me /spend <amount>')

def spend(update, context):
    print("spended: %s", context.args)
    chat_id = update.message.chat_id
    amount = int(context.args[0])
    data[chat_id]["balance"] -= amount
    update.message.reply_text('You spend {} p.\n Now you balance for today {}.p'.format(amount, data[chat_id]["balance"]))

def status(update, context):
    update.message.reply_text(data[update.message.chat_id])

def update_balance(context):
    job = context.job
    chat_id = job.context
    data[chat_id]["balance"] += data[chat_id]["day_sum"]
    context.bot.send_message(chat_id, text='Good morning!\n +{} \n Today you can spend {}p.\n'.format(data[chat_id]["day_sum"], data[chat_id]["balance"]))

def stop(update, context):

    if 'job' not in context.chat_data:
        update.message.reply_text('You haven`t any active accounts. Send /start to begin new')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('App is disabled successfully')

def do_echo(update):
    update.message.reply_text(update.message.text)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token="773654970:AAEK1AsyL9yuDT-Mt6tuyGPXaMBLyNBd7FA", use_context = True, base_url="https://telegg.ru/orig/bot")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set", set))
    dp.add_handler(CommandHandler("spend", spend))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("stop", stop))

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