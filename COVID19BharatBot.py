#!/usr/bin/env python3

"""
COVID19Bharat Bot to provide live statistics and Corona virus information from India.
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
                [InlineKeyboardButton('Statistics State-wise', callback_data='statewise')],
                [InlineKeyboardButton('Refresh', callback_data='helplines')]]
    return InlineKeyboardMarkup(keyboard)


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

# Opening helpline JSON file
helpline_json = requests.get(helpline).json()
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
    state_data = "*State-Wise Cases:*\n\nState / UT | Confirmed | Recovered | Deaths | Active\n"
    for single_state in latest_stats_json['data']['statewise']:
        state_data += "*" + str(single_state['state']) + "* | " + str(single_state['confirmed']) + " | " + str(
            single_state['recovered']) + " | " + \
                      str(single_state['deaths']) + " | " + str(single_state['active']) + "\n"
    return state_data


# helpline data
def get_helpline_data():
    helpline_data = ""
    # print(helpline_json["data"]["contacts"])
    for state in helpline_json["data"]["contacts"]["regional"]:
        # print(str(state["loc"]))
        helpline_data += str(state["loc"]) + ": " + str(state["number"]) + "\n"
    return helpline_data


############################# Messages #################################

def main_menu_message():
    return 'Hello, I\'m COVID19 Bharat Bot, I\'ll provide you COVID19 Bharat updates based on state press bulletins ' \
           'and reliable news channels. Let me ' \
           'know what do you want to know\n/about - Description\n/stats -  Statistics India\n/statewise - Statistics ' \
           'state-wise India\n/helpline - COVID helpline numbers\n/faq - Frequently Asked Questions\n/guidelines - to ' \
           'win war against COVID-19'


def faq_message():
    return "Q.Why does I have more postive count than MoH?\nA.MoH updates the data at a scheduled time and I provide " \
           "you update from COVID19India.org which takes data from state press bulletin and reliable news " \
           "channels.\n\nQ. Why people putting in time and resources to create me while not gaining a single penny " \
           "from " \
           "me?\nA. Because it affects all of us. Today it's someone else who is getting infected. Tomorrow it will " \
           "be us. We need to prevent the spread. We need to document the data so that people with knowledge are able " \
           "to map the data.\n\nQ. How is the data gathered for this project?\nA. I collect the data from " \
           "COVID19India.org which takes it from each state press release, official government links and reputable " \
           "news channels as source. Data is validated by group of volunteers and pushed into Google sheets at the " \
           "moment. Google sheet is also available for public."


def guidelines_message():
    return "*Help the nation,\nHelp stop coronavirus.*\n\n*DO THE FIVE*\n1. *HANDS* Wash them often\n2. *ELBOW* Cough " \
           "into it\n3. *FACE* Don't touch it\n4. *SPACE* Keep safe distance\n5. *HOME* Stay if you can\n\n*DO NOT DO " \
           "THE FIVE*\n1. *EYES* Do " \
           "not touch it\n2. *NOSE* Do not touch it\n3. *MOUTH* Do not touch it\n4. *HOME* Do not leave it\n5. " \
           "*RUMORS* Do not spread it"


def help_message():
    return "This is what all you can ask me to share\n/about - Description\n/stats -  Statistics India\n/statewise - " \
           "Statistics state-wise India\n/helpline - COVID helpline numbers\n/faq - Frequently Asked " \
           "Questions\n/guidelines - to win war against COVID-19'"


############################# Responders ###############################

# Send description
def helpline(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(get_helpline_data(), parse_mode=telegram.ParseMode.MARKDOWN)


# Send description
def description(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(main_menu_message(), parse_mode=telegram.ParseMode.MARKDOWN)


def guidelines(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(guidelines_message(), parse_mode=telegram.ParseMode.MARKDOWN)


def statewise(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(get_stats_statewise(), parse_mode=telegram.ParseMode.MARKDOWN)


def faq(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(faq_message(), parse_mode=telegram.ParseMode.MARKDOWN)


# Help details
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_message(), parse_mode=telegram.ParseMode.MARKDOWN)


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
    dp.add_handler(CommandHandler("guidelines", guidelines))
    dp.add_handler(CommandHandler("helpline", helpline))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("statewise", statewise))
    dp.add_handler(CommandHandler("about", description))
    dp.add_handler(CommandHandler("faq", faq))
    # Buttons
    dp.add_handler(CallbackQueryHandler(helplines_menu, pattern='^helplines$'))
    dp.add_handler(CallbackQueryHandler(statistics_menu, pattern='^statistics$'))
    dp.add_handler(CallbackQueryHandler(statewise_menu, pattern='^statewise$'))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

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
