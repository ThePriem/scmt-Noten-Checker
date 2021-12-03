import json
import yaml
import telegram
import logging

def sendMessage(id,msg):

    configuration = loadYAML()
    bot = telegram.Bot(token=configuration["telegram"]["token"])
    bot.send_message(text=msg, 
                         chat_id=id,
                         parse_mode=telegram.ParseMode.HTML)

def safeJSON(data):
    with open("data.json", "w") as outfile:
        outfile.write(json.dumps(data,indent=4))

def loadJSON():
    with open("data.json", "r") as read_file:
        data = json.load(read_file)
    return data

def loadYAML():
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data

def compareGrades(websiteGrades, safedGrades,telegramID):
    for entryWebsite in websiteGrades:

        alreadySafed = False

        gradeNameWebsite = entryWebsite["name"]
        for entryFile in safedGrades:
            gradeNameFile = entryFile["name"]
            if gradeNameWebsite == gradeNameFile:
                #print("Grade already in Database.")
                alreadySafed = True
                break
            
        if alreadySafed == True: continue
        #If Code Reaches this Code. Grade is not in safed file.
        #print("Grade not in safed file!")
        msg = "<b>Neue Note</b>\n" + entryWebsite["name"] + "\n" + entryWebsite["grade"]
        sendMessage(telegramID,msg)

def setLastCommand(command,id):
    logging.info("Setting lastCommand of user " + str(id) + " to " + str(command))

    data = loadJSON()
    for user in data["users"]:
        if user["telegramID"] == id:
            user["lastCommand"] = command
            break
    safeJSON(data)

def checkLastCommand(id):

    lastCommand = ""
    logging.info("Checking lastCommand of user " + str(id))

    data = loadJSON()

    for user in data["users"]:
        if user["telegramID"] == id:
            lastCommand = user["lastCommand"]
            break
    
    return lastCommand

def setCredentials(id,credential,value):
    logging.info("Setting " + str(credential) + " for user " + str(id))

    data = loadJSON()
    for user in data["users"]:
        if user["telegramID"] == id:
            user[credential] = value
            break

    safeJSON(data)

def getCredentials(id):
    logging.info("Getting credentials for user " + str(id))

    data = loadJSON()
    for user in data["users"]:
        if user["telegramID"] == id:
            return user["usr"], user["pwd"]

def checkUserExist(id):
    logging.info("Checking if user " + str(id) + " exist.")
    exist = False

    data = loadJSON()

    for user in data["users"]:
        if user["telegramID"] == id:
            exist = True
            break

    if exist == False:
        newUser = {
            "usr": "",
            "pwd": "",
            "telegramID": id,
            "lastCommand": "",
            "grades": []
        }

        data["users"].append(newUser)

        safeJSON(data)

def credentialsMissing(chatID):

    eisUsername, eisPassword = getCredentials(chatID)

    if eisUsername != "" and eisPassword != "": 
        return False

    msg = ""

    #Break if username or Passwort not provided.
    if eisUsername == "": msg += "Benutzername nicht vorhanden. Bitte setze ihn über /setUsername\n"
    if eisPassword == "": msg += "Passwort nicht vorhanden. Bitte setze es über /setPassword"

    sendMessage(chatID,msg)

    return True

