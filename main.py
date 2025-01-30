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
    print("3: Search for a spell by the spell's name.") # (ex. Search for 'shocking grasp', 'fireball', etc.)
    print("2: Search for a spell by a keyword within the spell's description.") # (ex. Searching 'acid' returns all entries with 'acid' associated with it.)
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

def searchSpellName():
    print("Option 3 chosen.")

def searchKeyWord():
    print("Option 2 chosen.")

def showHelpMenu():
    print("\n-----------------------------------------------------------------------------")
    print("Help Manual")
    print("This program supports searching the DND5e API for particular spells")
    print("based on spell name or a particular keyword. In depth descriptions follow:\n")
    print("Option 3: Search for a spell by the spell's name")
    print("If the user already knows the name of a particular spell they want")
    print("to view the details of, input '3' from the main menu and type in")
    print("the name of a spell, like 'Shocking Grasp'. Information about the")
    print("spell will appear in the console.\n")
    print("Option 2: Search for a spell by a keyword within the spell's description")
    print("If you cannot recall the name of a spell, no worries! This option")
    print("allows you to find a spell based on a 'key word' that you, the user,")
    print("provide. Input '2' from the main menu and type in your desired key word.")
    print("The application will search and display any spell that has a match to the ")
    print("keyword in the spell fields. For example, searching 'acid' should display ")
    print("any spell whose text fields (like 'description', 'damage type', etc.) have")
    print("'acid' in it.")
    print("-----------------------------------------------------------------------------")


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
            searchSpellName()
        elif (userInput == 2):
            searchKeyWord()
        elif (userInput == 1):
            showHelpMenu()
        else:
            print("\nProgram closed.")

    


if __name__ == "__main__":
    main()