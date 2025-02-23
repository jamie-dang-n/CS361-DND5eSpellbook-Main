# import necessary packages
import requests
import textwrap
import json
import zmq

#CONSTANTS
FIRST_LEVEL_PARAMS = ['index', 'name', 'level', 'url']
SECOND_LEVEL_PARAMS = ['index', 'name', 'url', 'desc', 'higher_level', 'range', 'components', 'material', 'area_of_effect', 'ritual', 'duration', 'concentration', 'casting_time', 'level', 'attack_type', 'damage', 'school', 'classes', 'subclasses', 'url']
DESC_LENGTH = 70

# Prints out the title of the program with a short sentence describing the application
def printTitle():
    print("______ _   _______   _____        _____            _ _ _                 _    ")
    print("|  _  \\ \\ | |  _  \\ |  ___|      /  ___|          | | | |               | |   ")
    print("| | | |  \\| | | | | |___ \\  ___  \\ `--. _ __   ___| | | |__   ___   ___ | | __")
    print("| | | | . ` | | | |     \\ \\/ _ \\  `--. \\ '_ \\ / _ \\ | | '_ \\ / _ \\ / _ \\| |/ /")
    print("| |/ /| |\\  | |/ /  /\\__/ /  __/ /\\__/ / |_) |  __/ | | |_) | (_) | (_) |   < ")
    print("|___/ \\_| \\_/___/   \\____/ \\___| \\____/| .__/ \\___|_|_|_.__/ \\___/ \\___/|_|\\_\\")
    print("                                       | |                                    ")
    print("                                       |_|                                    ")
    print("\nEasily search for DND5e spells for all your campaign needs!")
    print("\nThis application will only run with an active internet connection.")

# Print out main menu options
def printMenuOptions():
    print("\nAPPLICATION FUNCTIONS")
    print("3: Search for a spell with exact spell name.") # (ex. Search for 'shocking grasp', 'fireball', etc.)
    print("2: Search for a spell by a keyword within the spell's name.") # (ex. Searching 'acid' returns all entries with 'acid' associated in the name.)
    print("1: Help Manual.")
    print("0: Quit.\n")

# Get user input for the main menu
def getUserInput():
    userInput = -1
    invalidInput = True
    while (invalidInput):
        try:
            userInput = int(input("Choose an option [0, 1, 2, 3]: "))
            if (userInput < 0 or userInput > 3):
                print("Invalid Input. Please enter a valid option!")
            else:
                invalidInput = False
        except ValueError:
            print("Invalid Input. Please enter an integer!")
    return userInput

# Option 3 implementation: Search for a spell in the API by spell name 
# (print 1 spell)
# Code citation: Referenced "GeeksForGeeks"
def searchSpellName():
    # API endpoint URL
    url = "https://www.dnd5eapi.co/api/spells/"

    # get user input
    userSpell = input("Enter a spell name: ")

    # format user input into lowercase, dashed form
    userSpell = userSpell.lower()
    userSpell = userSpell.replace(" ", "-")

    # update URL for API call
    url = url + userSpell

    # do an API call to dnd5eapi, given a spell name
    try:
        response = requests.get(url)

        if (response.status_code) == 200:
            spell = response.json()
            return spell
        else:
            print("\nError: Spell not found with response code", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        # handle network-related errors/exceptions
        print("Error: ", e)
        return None

# Option 2 implementation: search for spells in the API by keyword in spell name 
# (possibly print many spells)
def searchKeyWord():
    matchedIndices = [] # initialize empty array of matched indices
    matchedNames = [] # initialize empty array of matched names
    numMatches = 0

    # API endpoint URL
    url = "https://www.dnd5eapi.co/api/spells/"

    # get user input for key word
    keyWord = input("Enter a key word to search for: ")

    # find all matching keywords
    # format user input into lowercase form
    keyWord = keyWord.lower()
    keyWord = keyWord.replace(" ", "+")

    # Find spells that match the key word in name field
    try:
        allSpellsURL = url + "?"
        currURL = allSpellsURL + "name=" + keyWord
        currResponse = requests.get(currURL)
        if currResponse.status_code == 200:
            matchingSpells = currResponse.json()
            for spell in matchingSpells['results']:
                if spell['index'] not in matchedIndices:
                    # only match spells that have not already been matched
                    matchedIndices.append(spell['index'])
                    matchedNames.append(spell['name'])
                    numMatches += 1
        else:
            print("Error: No response with response code", currResponse.status_code)
    except requests.exceptions.RequestException as e:
        # handle network-related errors/exceptions
        print("Error: ", e)
        return None

    # display the name of every matching spell found
    if numMatches == 0:
        print("\nNo matches were found.")
    else: 
        print("\nMatches were found.")
        printNumberedMatches(matchedNames)

        # give user decision to read more about a spell or return to main menu
        userChoice = subSpellMenu()
        while (userChoice == 1):
            try:
                # Choose a spell to examine further
                spellChoice = getSpellChoice(numMatches, matchedNames)
                try: 
                    # get spell by index
                    spellToPrintURL = url + matchedIndices[spellChoice - 1]
                    spellToPrintResp = requests.get(spellToPrintURL)
                    if spellToPrintResp.status_code == 200:
                        spellToPrint = spellToPrintResp.json()
                        printSpell(spellToPrint)
                        # ask user if they want to add this spell to a bookmarks list
                    else:
                        print("Error: spell could not be displayed.")
                except requests.exceptions.RequestException as e:
                    # handle network-related errors/exceptions
                    print("Error: ", e)
                    return None
                userChoice = subSpellMenu()
            except ValueError:
                print("\nInvalid Input. Please enter an integer!")    

# Get user's spell choice from sub-menu in Option 2
def getSpellChoice(numMatches, matchedNames):
    print("\nSelect a spell from the given indices.")
    printNumberedMatches(matchedNames)
    spellChoiceString = "\nSpell selection [1 to " + str(numMatches) + "]: "
    spellChoice = int(input(spellChoiceString))
    while (spellChoice < 1 or spellChoice > numMatches):
        print("\nInvalid Input. Please enter a valid option!")
        printNumberedMatches(matchedNames)
        spellChoiceString = "\nSpell selection [1 to " + str(numMatches) + "]: "
        spellChoice = int(input(spellChoiceString))
    return spellChoice

# Print out matched spells with indexing for Option 2
def printNumberedMatches(matchedNames):
    i = 1
    for match in matchedNames:
        print(i, ": ", match)
        i += 1
    
# Display spell sub menu options and get user input for sub menu
def subSpellMenu():
    print("\nSPELL OPTIONS")
    print("1: Enter spell index to view more details about that spell")
    print("0: Return to main menu\n")
    userInput = -1
    invalidInput = True
    while (invalidInput):
        try:
            userInput = int(input("Select an option [1 or 0]: "))
            if (userInput < 0 or userInput > 1):
                print("Invalid Input. Please enter a valid option!")
            else:
                invalidInput = False
        except ValueError:
            print("Invalid Input. Please enter an integer!")    
    return userInput

# Print a line for ease of reading
def printLine():
    print("-----------------------------------------------------------------------------")

# Option 1: Display help menu
def showHelpMenu():
    print("Help Manual")
    print("This program supports searching the DND5e API for particular spells")
    print("based on spell name or a particular keyword. In depth descriptions follow:\n")
    print("Option 3: Search for a spell with exact spell name")
    print("If the user already knows the name of a particular spell they want")
    print("to view the details of, input '3' from the main menu and type in")
    print("the name of a spell, like 'Shocking Grasp'. Information about the")
    print("spell will appear in the console.\n")
    print("Option 2: Search for a spell by a keyword within the spell's name")
    print("If you cannot recall the name of a spell, no worries! This option")
    print("allows you to find a spell based on a 'key word' that may appear")
    print("in the spell's name. Input '2' from the main menu and type in your ")
    print("desired key word. The application will search and display any spell ")
    print("that has a match to the keyword in the name. For example, searching")
    print("'acid' should display any spell whose name has 'acid' in it.")
    print("NOTE: This search option will take slightly longer than the first,")
    print("because you will have to select a spell to examine it further, as opposed")
    print("to searching and printing out only 1 spell (as the first option does).\n")
    print("Option 1: Help Manual")
    print("This is the current option you have chosen. Inputting '1' in the main")
    print("menu will always bring you back to this help manual, where you can learn")
    print("more about the commands this application allows.")

# Print select (programmer-specified) data from a single spell
def printSpell(spell):
    printLine()

    print("Name: ", spell['name'])
    spellDesc = textwrap.wrap(spell['desc'][0], width=DESC_LENGTH)

    print("\nDescription: ")
    for line in spellDesc:
        print(line)

    if (spell['higher_level']):
        print("\nHigher level: ")
        levelDesc = textwrap.wrap(spell['higher_level'][0], width=DESC_LENGTH)
        for line in levelDesc:
            print(line)

    print("\nRange: ", spell['range'])
    print("Casting time: ", spell['casting_time'])
    print("Duration: ", spell['duration'])
    print("Level: ", spell['level'])

    if (spell['concentration']):
        print("\nConcentration: Necessary")
    else:
        print("\nConcentration: Not necessary")
    if 'attack_type' in spell:
        print("Attack type: ", spell['attack_type'])
    if ("damage" in spell):
        print("Damage type: ", spell['damage']['damage_type']['name'])
        if 'damage_at_slot_level' in spell['damage']:
            print("\nDamage at slot level:")
            for slot in (spell['damage']['damage_at_slot_level']):
                print("Slot level", 
                        slot, 
                        ":", 
                        spell['damage']['damage_at_slot_level'][slot])
        if 'damage_at_character_level' in spell['damage']:
            print("\nDamage at character level:")
            for level in (spell['damage']['damage_at_character_level']):
                print("Character level ", 
                        level, 
                        ":",
                        spell['damage']['damage_at_character_level'][level])

    print("School of Magic: ", spell['school']['name'])
    print("Class: ", spell['classes'][0]['name'])
    printLine()

def addSpell(spell, bookmarks):
    invalidInput = True
    while (invalidInput):
        try:
            addOption = int(input("Would you like to add this spell to your bookmarks [1 = yes, 0 = no]?: "))
            if (addOption < 0 or addOption > 1):
                print("Invalid Input. Please enter a valid option!")
            else:
                invalidInput = False
        except ValueError:
            print("Invalid Input. Please enter an integer!") 
    if (addOption == 1):
        print("The user wants to add a spell")
        accessBookmarkMods(spell, bookmarks, 1) # set option to 1 to add the spell

def accessBookmarkMods(spell, bookmarks, option):
    # interact with the microservice
    context = zmq.Context()

    # socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # form dictionary request
    input_dict = {
        "json_array": bookmarks,
        "json_object": spell,
        "option": option
    }

    # send request
    socket.send(b"This is a message from main")

    # receive response
    message = socket.recv()
    print(f"Request sent: {message}")




def main():
    # variables
    bookmarks = [] # initialize empty array of spell JSON objects
    userInput = -1
    confirmQuit = -1

    # Display Title
    printTitle()

    # User input loop
    while (confirmQuit != 0):
        printMenuOptions()
        userInput = getUserInput()
        if (userInput == 3):
            spell = searchSpellName()
            if (spell):
                # if a spell was returned, print it
                print("\nSpell found!\n")
                printSpell(spell)
                # ask user if they want to add this spell to a bookmarks list
                addSpell(spell, bookmarks)
                

        elif (userInput == 2):
            searchKeyWord()
        elif (userInput == 1):
            printLine()
            showHelpMenu()
            printLine()
        else:
            confirmQuit = input("Enter 0 to confirm that you want to quit, otherwise enter any value to return to main menu: ")
            try:
                confirmQuit = int(confirmQuit)
            except ValueError:
                confirmQuit = -1
            if (confirmQuit == 0):
                print("\nProgram closed.")

if __name__ == "__main__":
    main()