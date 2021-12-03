from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from utils import *
import telegram
from scmt import getGradesFromWebsite


def start(update, context):
    chatID = update.effective_chat.id
    firstName = update.effective_chat.first_name
    checkUserExist(chatID)

    logging.info(str(chatID) + " triggered start command.")
    
    msg = "Hallo " + firstName + "😊\n"
    msg += "Schreibe /help um zu erfahren was ich alles kann."
    context.bot.send_message(chat_id=chatID, 
                             text=msg,
                             parse_mode=telegram.ParseMode.HTML)

def unknown(update, context):
    chatID = update.effective_chat.id
    checkUserExist(chatID)
    incomingMessage = update.message.text
    logging.info(str(chatID) + " triggered unknown command.")

    lastCommand = checkLastCommand(chatID)

    

    if lastCommand == "username":
        msg = "Username gespeichert 🙂"
        setCredentials(chatID,"usr",incomingMessage)
        setLastCommand("",chatID)
    elif lastCommand == "password":
        msg = "Passwort gespeichert 🙂"
        setCredentials(chatID,"pwd",incomingMessage)
        setLastCommand("",chatID)
    else:
        msg = "Tut mir leid. Das habe ich nicht verstanden 😔"


    
    context.bot.send_message(chat_id=chatID, 
                             text=msg,
                             parse_mode=telegram.ParseMode.HTML)

def help(update,context):
    chatID = update.effective_chat.id
    checkUserExist(chatID)
    logging.info(str(chatID) + " triggered help command.")

    msg = "<b>Hilfe</b>\n"
    msg += "Ich bin ein Bot, der einmal in der Stunde für dich überprüft ob eine neue Note im EIS hochgeladen wurde.\n"
    msg += "Ich benötige dafür deine EIS-Credentials.\n"
    msg += "⚠️<b>ACHTUNG</b>⚠️\nIch speicher deine Zugangsdaten und Noten um vergleichen zu können, ob eine neue Note hochgeladen wurde.\n"
    msg = "Momentan unterstütze ich folgende Funktionen:\n"
    msg += "Schreibe /setUsername um mir deinen EIS Benutzernamen mitzuteilen.\n"
    msg += "Schreibe /setPassword um mir dein EIS Passwort mitzuteilen.\n"
    msg += "Ich kann dir auch eine Notenübersicht zukommen lassen.\nSchreibe dafür /getGrades\n"
    msg += "Um deine Daten zu löschen, schreibe /deleteMyData\n"

    context.bot.send_message(chat_id=chatID, 
                             text=msg,
                             parse_mode=telegram.ParseMode.HTML)

def setUsername(update,context):
    chatID = update.effective_chat.id
    checkUserExist(chatID)
    logging.info(str(chatID) + " triggered setUsername command.")

    #Set users last command to username:
    setLastCommand("username",chatID)

    msg = "Wie lautet dein EIS Benutzername?"
    context.bot.send_message(chat_id=chatID, 
                             text=msg,
                             parse_mode=telegram.ParseMode.HTML)

def setPassword(update,context):
    chatID = update.effective_chat.id
    checkUserExist(chatID)
    logging.info(str(chatID) + " triggered setPassword command.")

    #Set users last command to username:
    setLastCommand("password",chatID)

    msg = "Wie lautet dein EIS Passwort?"
    context.bot.send_message(chat_id=chatID, 
                             text=msg,
                             parse_mode=telegram.ParseMode.HTML)

def getGrades(update,context):
    chatID = update.effective_chat.id
    checkUserExist(chatID)
    logging.info(str(chatID) + " triggered getGrades command.")
    
    eisUsername, eisPassword = getCredentials(chatID)
    
    #Stop if Credentials are missing, else continue
    if credentialsMissing(chatID) == True: return
    
    context.bot.send_message(chat_id=chatID, 
                             text="Ermittle Noten. Das könnte einige Sekunden dauern.",
                             parse_mode=telegram.ParseMode.HTML)

    #Get Grades of User:
    msg = "<b>Hier sind deine Noten:</b>\n\n"
    for grade in getGradesFromWebsite(eisUsername,eisPassword):
        msg += grade["name"] + "\n"
        msg += grade["grade"]+ "\n\n"

    context.bot.send_message(chat_id=chatID, 
                             text=msg,
                             parse_mode=telegram.ParseMode.HTML)

def deleteUserData(update,context):
    chatID = update.effective_chat.id
    checkUserExist(chatID)
    logging.info(str(chatID) + " triggered deleteUserData command.")

    data = loadJSON()

    index = 0
    for user in data["users"]:
        if user["telegramID"] == 1173115367:
            data["users"].pop(index)
            break
        index += 1

    safeJSON(data)

    context.bot.send_message(chat_id=chatID, 
                             text="Daten gelöscht",
                             parse_mode=telegram.ParseMode.HTML)

def main():
    
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        filename='telegram.log', 
                        encoding='utf-8', 
                        level=logging.INFO)

    credentials = loadYAML()

    updater = Updater(token=credentials["telegram"]["token"], use_context=True)
    
    dispatcher = updater.dispatcher
    
    #Start:
    dispatcher.add_handler(CommandHandler('start', start))

    #Help
    dispatcher.add_handler(CommandHandler('help', help))

    #set Username
    dispatcher.add_handler(CommandHandler('setUsername', setUsername))

    #set Password
    dispatcher.add_handler(CommandHandler('setPassword', setPassword))

    #get all Grades
    dispatcher.add_handler(CommandHandler('getGrades', getGrades))

    #Delete Userdata:
    dispatcher.add_handler(CommandHandler('deleteMyData', deleteUserData))

    #Unknows Text
    dispatcher.add_handler(MessageHandler(Filters.text, unknown))

    updater.start_polling()

if __name__ == "__main__":
    main()
