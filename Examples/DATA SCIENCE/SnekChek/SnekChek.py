# SnekChek.py | 2018-09-20
# Author: Raymond Tran
# Scrapes the CSUS mailing list and updates the day-to-day membership spreadsheet.
# This is because the signee must fist accept the activation E-Mail before they're able to receive newsletters.

# RoboBrowser required. (Collection of web-scraping modules.)
# Pandas required. (Data analysis library.)
import getpass
import os
import pandas
import re
import sys

from pandas import DataFrame, Series
from robobrowser import RoboBrowser


# Logs in using the given parameters, and scrapes the mailing list.
# Returns a list with each element being an e-mail in string format.
def pullList():

    # Header message.
    try:
        os.system('cls')
    except:
        os.system('clear')
    print("\n#####################################################")
    print("# SnekChek: CSUS Membership Spreadsheet Updater 1.0 #")
    print("#####################################################")
    print("Author: Raymond Tran | E-Mail: traymondbiz@gmail.com")
	
    # Log-in.
    inputID = input("\n[INPUT] CSUS-L E-Mail: ")
    inputPW = getpass.getpass(prompt="[INPUT] CSUS-L Password: ")
	
    # Set-up the browser.
    print("\n[STATUS] Connecting to server.")
    browser = RoboBrowser(parser="html.parser")
    browser.open("http://mailman.ucalgary.ca/mailman/listinfo/csus-L")

    print("[STATUS] Logging in.")
    # Log-in to Mailing List
    form = browser.get_form(action="http://mailman.ucalgary.ca/mailman/roster/csus-l")
    form["roster-email"].value = inputID
    form["roster-pw"].value = inputPW
    browser.submit_form(form)

    # Pulls the data. (All members of the undigested HTML list.)
    print("[STATUS] Pulling data.")
    try:
        section = browser.find("ul")
        mailList = section.find('li')
        mailList = mailList.text
    except AttributeError:
        print("\n[ERROR] Failed to log in and retrieve section.")
        print("[ERROR] Were the correct credentials entered?")
        sys.exit()

    # Cleans and formats the data.
    print("[STATUS] Formatting data.")
    mailList = mailList.replace(" at ", "@")
    mailList = mailList.replace("(","")
    mailList = mailList.replace(")","")
    mailList = mailList.splitlines()

    return mailList

# Given a spreadsheet of e-mails and their mailing list status, compares it
# against an online mailing list. If an e-mail marked pending on the list is
# in the online list, update its status to "Yes". Performed in O(N^2) time. (Brute-force.)
def updateSpreadsheet(inputMailList):
    mailList = inputMailList

    # Prompt for file input/output names.
    inputFile = input("\n[INPUT] File to read from (ex: file.csv): ")
    outputFile = input("[INPUT] File to write to (ex: file.csv): ")
    print()

    try:
        file = pandas.read_csv(inputFile)
    except FileNotFoundError:
        print("\n[ERROR] Input file " + inputFile + " was invalid.")
        print("[ERROR] Is the file in the same directory, or of .csv format?")
        sys.exit()

    # Flag that leaves a message if data is/isn't modified.
    update = False

    # Updates the spreadsheet according to the online mailing list.
    userIndex = 0
    for userRow in file["Mailing List?"]:
        # Pending -> Yes/Pending
        if userRow == "Pending":
            # Prints the e-mail by indexing the rows that have 'Pending',
            # then taking their E-Mail from its respective column.
            if file.iloc[userIndex].loc["Email"] in mailList:
                file.iloc[userIndex].loc["Mailing List?"] = "Yes"
                print((("[UPDATE] " + file.iloc[userIndex].loc["Email"]).ljust(50,".")) + "(Pending) to \"Yes\"")
                update = True
        # Yes -> No
        elif userRow == "Yes":
            if file.iloc[userIndex].loc["Email"] not in mailList:
                file.iloc[userIndex].loc["Mailing List?"] = "No"
                print((("[UPDATE] " + file.iloc[userIndex].loc["Email"]).ljust(50,".")) + "(Yes) to \"No\"")
                update = True
        # No -> Yes
        elif userRow == "No":
            if file.iloc[userIndex].loc["Email"] in mailList:
                file.iloc[userIndex].loc["Mailing List?"] = "Yes"
                print((("[UPDATE] " + file.iloc[userIndex].loc["Email"]).ljust(50,".")) + "(No) to \"Yes\"")
                update = True
        # Check the next user in the list.
        userIndex += 1

    # Flag that leaves a message if data is/isn't modified.
    if update == False:
        print("[STATUS] Nothing to update.")
    else:
        print("\n[STATUS] Note that some may be on the mailing list under a different E-Mail that's not listed in the file.")
            
    # Save file to system based on user input.
    print("[STATUS] Saving to system as " + outputFile)
    try:
        file.to_csv(outputFile)
    except PermissionError:
        print("\n[ERROR] Permission to write as " + inputFile + " denied.")
        print("[ERROR] Is the file currently open on your system?")
        sys.exit()
    
    return

def main():
    emailList = pullList()
    updateSpreadsheet(emailList)
    print ("[STATUS] End of program.")

main()
