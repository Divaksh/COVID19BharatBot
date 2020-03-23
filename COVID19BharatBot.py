#!/usr/bin/env python

"""
Simple COVID19Bharat Bot to provide live statistics and Corona virus information from India.
"""
import logging

# importing modules
import json
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Read the token from the secret file
def read_token():
    with open('token.json') as f:
        data = json.load(f)
        # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
    return data['token']


############################### Bot Control ####################################

def start(update, context):
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def statistics_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=get_stats(), parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=statistics_keyboard())


def statewise_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=get_stats_statewise(), parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=statewise_keyboard())


def helplines_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=get_helpline_data(), parse_mode=telegram.ParseMode.MARKDOWN,
                            reply_markup=helplines_keyboard())


############################ Keyboards #################################
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Statistics', callback_data='statistics')],
                [InlineKeyboardButton('Statistics State-wise', callback_data='statewise')],
                [InlineKeyboardButton('Helplines', callback_data='helplines')]]
    return InlineKeyboardMarkup(keyboard)


def statistics_keyboard():
    keyboard = [[InlineKeyboardButton('Statistics State-wise', callback_data='statewise')],
                [InlineKeyboardButton('Helplines', callback_data='helplines')],
                [InlineKeyboardButton('Refresh', callback_data='statistics')]]
    return InlineKeyboardMarkup(keyboard)


def statewise_keyboard():
    keyboard = [[InlineKeyboardButton('Statistics', callback_data='statistics')],
                [InlineKeyboardButton('Helplines', callback_data='helplines')],
                [InlineKeyboardButton('Refresh', callback_data='statewise')]]
    return InlineKeyboardMarkup(keyboard)


def helplines_keyboard():
    keyboard = [[InlineKeyboardButton('Statistics', callback_data='statistics')],
                [InlineKeyboardButton('Statistics State-wise', callback_data='statewise')]]
    return InlineKeyboardMarkup(keyboard)


############################# Messages #################################

def main_menu_message():
    return 'Hello, I\'m COVID19 Bharat Bot, I\'ll provide you COVID19 data from trusted sources. Let me ' \
           'know what do you want to know '


# Help details
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


###############################################################################
#                                                                             #
#                            Official feeds for the data                      #
#                                                                             #
# Official data Stats: https://api.rootnet.in/covid19-in/stats/latest          #
# Stats as a daily series: https://api.rootnet.in/covid19-in/stats/daily      #
# Hospitals & bed stats: https://api.rootnet.in/covid19-in/stats/hospitals    #
# Contact & helpline: https://api.rootnet.in/covid19-in/contacts              #
# Notifications & advisories: https://api.rootnet.in/covid19-in/notifications #
#                                                                             #
#                            Unofficial feeds for the data                    #
#                                                                             #
# Patient data: https://api.rootnet.in/covid19-in/unofficial/covid19india.org
# State-wise data: https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise
# State-wise history(from 14th March): https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history

latest_stats = "https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise"
daily_stats = "https://api.rootnet.in/covid19-in/stats/daily"
hospitals_stats = "https://api.rootnet.in/covid19-in/stats/hospitals"
helpline = "https://api.rootnet.in/covid19-in/contacts"
notifications = "https://api.rootnet.in/covid19-in/notifications"

# Opening latest_stats JSON file
latest_stats_json = requests.get(latest_stats).json()
# print(json_file.json())
confirmed = latest_stats_json['data']['total']['confirmed']
deaths = latest_stats_json['data']['total']['deaths']
recovered = latest_stats_json['data']['total']['recovered']
active = latest_stats_json['data']['total']['active']


# latest total data
def get_stats():
    return "*Coronavirus pandemic in India* \n\n" + "Confirmed - " + str(
        confirmed) + "\nDeaths - " + str(deaths) + "\nRecovered - " + str(
        recovered) + "\nActive - " + str(active)


# Send statistics
def stats(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(get_stats(), parse_mode=telegram.ParseMode.MARKDOWN)


# latest statewise total data
def get_stats_statewise():
    return "Under development"


# helpline data
def get_helpline_data():
    return "Under development"


# Send description
def description(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text()


# Send news
def news(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text()


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


############################# Handlers ###############################
def main():
    """Start the bot."""
    updater = Updater(read_token(), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("description", description))
    dp.add_handler(CommandHandler("news", news))
    # Buttons
    dp.add_handler(CallbackQueryHandler(helplines_menu, pattern='^helplines$'))
    dp.add_handler(CallbackQueryHandler(statistics_menu, pattern='^statistics$'))
    dp.add_handler(CallbackQueryHandler(statewise_menu, pattern='^statewise$'))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
