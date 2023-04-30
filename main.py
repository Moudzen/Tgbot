import logging
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from pyowm import OWM

BOT_TOKEN = "6075969747:AAG2CWxlfiJTXwjbVGcuhmfe-mOHtpmaaiM"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
base_keyboard = [['/add_product', '/look_list'],
                 ['/stop', '/help']]
base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Я бот, который поможет тебе в разных ситуациях.\n"
        "Узнай, что я могу с помощью /help.", reply_markup=base_markup)


async def add_product(update, context):
    await update.message.reply_text(
        "Введи продукт, который хочешь добавить.")
    return 1


async def add(update, context):
    await update.message.reply_text(
        "Продукт добавлен успешно!")


async def adding(update, context):
    locality = update.message.text
    f = open("products.txt", 'a')
    f.write(f'{locality}\n')
    f.close()
    await update.message.reply_text(
        "Продукт добавлен успешно!")
    return ConversationHandler.END


async def look_list(update, context):
    f = open("products.txt", encoding='utf8')
    lines = f.readlines()
    for i in lines:
        await update.message.reply_text(i)
    f.close()


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def help(update, context):
    await update.message.reply_text(
        "/add_product - добавление продукта, который хочется купить в корзину\n"
        "/look_list - посмотреть весь список")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('add_product', add_product)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, adding)],

        },

        # Точка прерывания диалога. В данном случае — команда /add.
        fallbacks=[CommandHandler('add', add)]
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("look_list", look_list))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
