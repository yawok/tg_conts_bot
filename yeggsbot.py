from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters)
from telegram import ReplyKeyboardMarkup
import json

contacts = {
        "name": "",
        "number": ""
        }

SAVE, UPDATE, NAME, NUMBER, CONF = range(5)

def start(update, context):
    reply_keyboard = [["save", "update"]]
    update.message.reply_text("Hello this is YEggs. Choose your gender",
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = False, input_field_placeholder = "None",)) 
    return NAME


def add_name(update, context):
    user_in = update.message.text
    if user_in == "":
        print(user_in)
    update.message.reply_text(f"Enter name of contact. ")
    return NUMBER
    

def add_number(update, context):
    user_in  = update.message.text
    save("name", user_in)
    print(user_in)
    update.message.reply_text("Enter number of contact. ")
    return SAVE


def conf_message(update, context):
    user_in = update.message.text
    save("number", int(user_in))
    update.message.reply_text(f"Saved {contacts['number']} with the name {contacts['name']} successfully.")
    print(contacts)
    update_database(contacts)
    return -1


def help(update, context):
    update.message.reply_text("""
    These are the commands available:

    /start --> Start conversation with bot.
    /contact --> Show bot creator's contacts
    /help --> Show helpful message

    """)


def save(key, user_in):
    contacts[key] = user_in


def save_number(update, context):
    user_in = update.message.text
    contacts["number"] = user_in


def update_database(c):
    def write_json(data, filename="contacts_info.json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


    with open("contacts_info.json") as json_file:
        data = json.load(json_file)
        temp = data["contacts"]
        print(data["contacts"])
        temp.append(c)

    write_json(data)
    print("saved")

with open("token.txt", "r") as f:
    TOKEN = f.read().replace("\n", "")


updater = Updater(TOKEN, use_context=True)
disp = updater.dispatcher
convHandler = ConversationHandler(entry_points = [CommandHandler("start", start)],
        states = {
            NAME : [MessageHandler(Filters.text, add_name)],
            NUMBER : [MessageHandler(Filters.text, add_number)],
            SAVE : [MessageHandler(Filters.text, conf_message)]
            },
        fallbacks=[CommandHandler("help", help)]
        )

disp.add_handler(convHandler)
updater.start_polling()
updater.idle()

