from scmt import getGradesFromWebsite
from utils import *

def hourlyUpdate():
    
    safedFile = loadJSON()

    for user in safedFile["users"]:

        userName = user["usr"]
        userPwd = user["pwd"]
        telegramID = user["telegramID"]
        safedGrades = user["grades"]

        if credentialsMissing(telegramID) == True: return

        websiteGrades = getGradesFromWebsite(userName,userPwd)

        compareGrades(websiteGrades, safedGrades,telegramID)

        #Change Grades in data:
        user["grades"] = websiteGrades

    safeJSON(safedFile)

if __name__ == "__main__":

    hourlyUpdate()

        