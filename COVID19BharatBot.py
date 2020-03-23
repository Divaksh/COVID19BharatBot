#!/usr/bin/env python

"""
Simple COVID19Bharat Bot to provide live statistics and Corona virus information from India.
"""
import logging

# importing modules
import json
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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


# Welcome message
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, I\'m COVID19 Bharat Bot.\nPlease send\n1. /stats - for statistics')


# Help details
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


###############################################################################
#                                                                             #
#                            Feeds for the data                               #
#                                                                             #
# Official data Stats https://api.rootnet.in/covid19-in/stats/latest
# Stats as a daily series: https://api.rootnet.in/covid19-in/stats/daily
# Hospitals & bed stats: https://api.rootnet.in/covid19-in/stats/hospitals
# Contact & helpline: https://api.rootnet.in/covid19-in/contacts
# Notifications & advisories: https://api.rootnet.in/covid19-in/notifications

latest_stats = "https://api.rootnet.in/covid19-in/stats/latest"
daily_stats = "https://api.rootnet.in/covid19-in/stats/daily"
hospitals_stats = "https://api.rootnet.in/covid19-in/stats/hospitals"
helpline = "https://api.rootnet.in/covid19-in/contacts"
notifications = "https://api.rootnet.in/covid19-in/notifications"

# Opening latest_stats JSON file
latest_stats_json = requests.get(latest_stats).json()
# print(json_file.json())
total = latest_stats_json['data']['summary']['total']
confirmed_cases_indian = latest_stats_json['data']['summary']['confirmedCasesIndian']
confirmed_cases_foreign = latest_stats_json['data']['summary']['confirmedCasesForeign']
confirmed_cases_unknown = latest_stats_json['data']['summary']['confirmedButLocationUnidentified']
discharged = latest_stats_json['data']['summary']['discharged']
deaths = latest_stats_json['data']['summary']['deaths']

# latest_data
stats_data = "Total - " + str(total) + "\nIndians - " + str(confirmed_cases_indian) + "\nForeign - " + str(
    confirmed_cases_foreign) + "\nUnidentified - " + str(confirmed_cases_unknown) + "\nCured - " + str(
    discharged) + "\nDeaths - " + str(deaths)

# Send statistics
def stats(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(stats_data)


# Send description
def description(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(total)


# Send news
def news(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(total)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


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
    dp.add_handler(CommandHandler("NEWS", news))

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
