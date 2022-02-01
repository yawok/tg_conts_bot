from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters)
from telegram import ReplyKeyboardMarkup
import json

##callback functions
contacts = {
        "name": "",
        "number": ""
        }
changing_var = None
INIT, NAME, NUMBER, SAVE, CONT_VAR, EDIT, UPDATE= range(7)


def start(update, context):
    """Password collection to start conversation."""
    update.message.reply_text("Enter password.")
    return INIT

def init(update, context):
    """Starting message for bot conversation."""
    reply_keyboard = [["save", "update"]]
    update.message.reply_text("Hello this is YEggs contacts saver. Would you like to add or update a contact?",
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = False, input_field_placeholder = "None",)) 
    return NAME


def add_name(update, context):
    """Collect name of new contact."""
    user_in = update.message.text
    print(user_in)
    update.message.reply_text(f"Enter name of contact. ")
    return NUMBER
    

def add_number(update, context):
    """Colllect number of new contact."""
    #temporarily storing name of new contact
    user_in  = update.message.text
    save("name", user_in)
    print(user_in)
    update.message.reply_text("Enter number of contact. ")
    return SAVE


#editing contact

def update(update, context):
    """Showing user, contacts available for editing."""
    user_in = update.message.text
    with open("contacts_info.json", "r") as json_file:
        data = json.load(json_file)
        temp = data["contacts"]
        name = [[f"{a['name']} : {a['number']}"]  for a in temp]

    print(name[0])

    update.message.reply_text(f"Which contact do you wish to edit?",
            reply_markup = ReplyKeyboardMarkup(name, one_time_keyboard = False, input_field_placeholder = "None",)) 
    return CONT_VAR


def contVar(update, context):
    """Select contact variable(name, number) to edit."""
    user_in = update.message.text
    global old_data
    old_data = user_in.split(" ")[0]
    contacts["name"], contacts["number"]= user_in.split(" ")[0], user_in.split(" ")[2]
    reply_keyboard = [["name", "number"]]

    update.message.reply_text("Do you wish to edit the name or the number?",
            reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = False, input_field_placeholder = "None",)) 
    return EDIT


def edit(update, context):
    """Edit choosing variable with new user input."""
    global changing_var
    changing_var = update.message.text
    print(changing_var)
    update.message.reply_text(f"Enter a new {changing_var} for {contacts['name']}.")
    return UPDATE


def conf_msg_1(update, context):
    """Update json and tell user"""
    user_in = update.message.text
    save("number", int(user_in))
    update.message.reply_text(f"Saved {contacts['number']} with the name {contacts['name']} successfully.")
    print(contacts)
    save_to_database(contacts)
    return INIT


def conf_msg_2(update, context):
    """Update json and tell user."""
    try:
        user_in = int(update.message.text)
    except:
        user_in = update.message.text
    print(changing_var)
    save(changing_var , user_in)
    update.message.reply_text(f"Saved {contacts['number']} with the name {contacts['name']} successfully.")
    print(contacts)
    update_database(contacts)
    return INIT
 

def help(update, context):
    """Help message for user."""
    update.message.reply_text("""
    These are the commands available:

    /start --> Start conversation with bot.
    /contact --> Show bot creator's contacts
    /help --> Show helpful message

    """)

#background functions
def save(key, user_in):
    """Update contacts dictionary with values."""
    contacts[key] = user_in


def save_to_database(c):
    """Save new contact to json file."""
    def write_json(data, filename="contacts_info.json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


    with open("contacts_info.json") as json_file:
        data = json.load(json_file)
        temp = data["contacts"]
        print(type(x[1] for x in temp))
        temp.append(c)

    write_json(data)
    print("saved")


def update_database(c):
    """Updating contact in json file that matches user input."""
    def write_json(data, filename="contacts_info.json"):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


    with open("contacts_info.json") as json_file:
        data = json.load(json_file)
        temp = data["contacts"]
        print(c)
        for idx, obj in enumerate(temp):
            if old_data == obj["name"]:
                print(temp[idx]["name"])
                data["contacts"][idx] = c
                print(temp[idx][changing_var])
                print(temp)
                break
    print(temp)

    
    write_json(data)
    print("updated")

def main():
    with open("token.txt", "r") as f:
        TOKEN = f.read().replace("\n", "")


    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher
    conv = ConversationHandler(entry_points = [CommandHandler("start", start)],
            states = {
                INIT : [MessageHandler(Filters.regex('^(password)$'), init)],
                NAME : [MessageHandler(Filters.regex('^(save)$'), add_name), MessageHandler(Filters.regex('^(update)$'), update)],
                NUMBER : [MessageHandler(Filters.text, add_number)],
                SAVE : [MessageHandler(Filters.text, conf_msg_1)], 
                CONT_VAR : [MessageHandler(Filters.text, contVar)],
                EDIT : [MessageHandler(Filters.text, edit)],
                UPDATE : [MessageHandler(Filters.text, conf_msg_2)]
              },
            fallbacks=[CommandHandler("help", help)]
            )


    disp.add_handler(conv)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

