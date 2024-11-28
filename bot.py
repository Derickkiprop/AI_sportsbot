# bot.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import json
from config import TELEGRAM_TOKEN, DIALOGFLOW_WEBHOOK_URL

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I can help you with upcoming sporting events. Type 'upcoming' to see the events.")

def upcoming(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Get user's message
    
    # Send the user's message to Dialogflow for processing
    response = requests.post(DIALOGFLOW_WEBHOOK_URL, json={
        "queryInput": {
            "text": {
                "text": user_message,
                "languageCode": "en"
            }
        }
    })

    # Get the response from Dialogflow and send it to the user
    dialogflow_response = response.json()
    fulfillment_text = dialogflow_response['fulfillmentText']
    update.message.reply_text(fulfillment_text)

def main():
    # Set up the Updater with your Telegram Bot token
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("upcoming", upcoming))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
