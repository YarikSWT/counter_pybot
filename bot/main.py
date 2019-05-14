from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

data = {}

def do_start(bot: Bot, update: Update):
    print("start")
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Отправь мне сколько бабосов ты готов потратить в рублях",
    )

def set_info(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    month_sum = int(update.message.text)
    data[chat_id] = {"sum": month_sum, "day_sum": month_sum / 30 , "balance":  month_sum / 30 }

    text = "Ваш ID = {}\n Вы готовы потратить {} \n На день: {} \n".format(chat_id, update.message.text,
                                                                           int(update.message.text) / 30)
    bot.send_message(
        chat_id=chat_id,
        text=text,
    )

def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    month_sum = int(update.message.text)
    data[chat_id] = {"sum": month_sum, "day_sum": month_sum/30}

    text = "Ваш ID = {}\n Вы готовы потратить {} \n На день: {} \n".format(chat_id, update.message.text, int(update.message.text)/30 )

    bot.send_message(
        chat_id=chat_id,
        text=text,
    )

def do_spend(update: Update, context):
    print("Spend")

    amount = int(context.args[0])
    chat_id = update.message.chat_id
    data[chat_id]["balance"] -= amount

    # bot.send_message(
    #     chat_id=update.message.chat_id,
    #     text="Вы потратили: {}\n Сегодня еще можете потратить: {}\n".format(amount, data[chat_id]["balance"]),
    # )




def main():
    bot = Bot(
        # token="641651003:AAEmcYj4KYNVJC3YnSlGJac_Gm9G2wubPhM",
        token= "773654970:AAEK1AsyL9yuDT-Mt6tuyGPXaMBLyNBd7FA",
        base_url="https://telegg.ru/orig/bot",
    )
    updater = Updater(
        bot=bot,
    )


    start_handler = CommandHandler("start", do_start)
    spend_handler = CommandHandler("spend", do_spend, pass_args=True, pass_chat_data=True)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(spend_handler)
    updater.dispatcher.add_handler(message_handler)


    # Начать обработку входящих сообщений
    updater.start_polling()

    # Не прерывать скрипт до обработки всех сообщений
    updater.idle()


if __name__ == '__main__':
    main()
