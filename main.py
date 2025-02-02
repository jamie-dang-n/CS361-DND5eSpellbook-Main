# import necessary packages
import requests
import textwrap
import json
from alive_progress import alive_bar

#C ONSTANTS for parameter searching
FIRST_LEVEL_PARAMS = ['index', 'name', 'level', 'url']
SECOND_LEVEL_PARAMS = ['index', 'name', 'url', 'desc', 'higher_level', 'range', 'components', 'material', 'area_of_effect', 'ritua', 'duration', 'concentration', 'casting_time', 'level', 'attack_type', 'damage', 'school', 'classes', 'subclasses', 'url']

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

def printMenuOptions():
    print("\nAPPLICATION FUNCTIONS")
    print("3: Search for a spell with exact spell name.") # (ex. Search for 'shocking grasp', 'fireball', etc.)
    print("2: Search for a spell by a keyword within the spell's name.") # (ex. Searching 'acid' returns all entries with 'acid' associated in the name.)
    print("1: Help Manual.")
    print("0: Quit.\n")

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
            print("Error: Spell not found with response code", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        # handle network-related errors/exceptions
        print("Error: ", e)
        return None


def searchKeyWord():
    matchedIndices = [] # initialize empty array of matched indices
    matchedNames = [] # initialize empty array of matched names
    numMatches = 0

    # API endpoint URL
    url = "https://www.dnd5eapi.co/api/spells/"

    # get user input for key word
    keyWord = input("Enter a key word to search for: ")

    # find all matching keywords
    # format user input into lowercase, dashed form
    keyWord = keyWord.lower()
    keyWord = keyWord.replace(" ", "+")

    # Find a spell that matches the key word in name field
    try:
        allSpellsURL = url + "?"
        currURL = allSpellsURL + "name=" + keyWord
        currResponse = requests.get(currURL)
        if currResponse.status_code == 200:
            matchingSpells = currResponse.json()
            for spell in matchingSpells['results']:
                if spell['index'] not in matchedIndices:
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
        i = 1
        for match in matchedNames:
            print(i, ": ", match)
            i += 1
        # give user decision to read more about a spell or return to main menu

    
def inspectSpellOrReturn():
    print("yes")

def printLine():
    print("-----------------------------------------------------------------------------")

def showHelpMenu():
    printLine()
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
    print("that has a match to the keyword in the name. For example, searching 'acid'")
    print("should display any spell whose name has 'acid' in it.")
    printLine()

def printSpell(spell):
    printLine()

    print("Name: ", spell['name'])
    spellDesc = textwrap.wrap(spell['desc'][0], width=60)

    print("\nDescription: ")
    for line in spellDesc:
        print(line)

    if (spell['level'] != 0):
        print("\nHigher level: ")
        levelDesc = textwrap.wrap(spell['higher_level'][0], width=60)
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
    print("Damage type: ", spell['damage']['damage_type']['name'])
    print("School of Magic: ", spell['school']['name'])
    print("Class: ", spell['classes'][0]['name'])

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
    printLine()

def main():
    # variables
    userInput = -1

    # Display Title
    printTitle()

    # User input loop
    while (userInput != 0):
        printMenuOptions()
        userInput = getUserInput()
        if (userInput == 3):
            spell = searchSpellName()
            if (spell):
                # if a spell was returned, print it
                print("\nSpell found!\n")
                printSpell(spell)

        elif (userInput == 2):
            searchKeyWord()
        elif (userInput == 1):
            showHelpMenu()
        else:
            print("\nProgram closed.")

    


if __name__ == "__main__":
    main()