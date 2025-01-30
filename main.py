def printTitle():
    print("______ _   _______   _____        _____            _ _ _                 _    ")
    print("|  _  \\ \\ | |  _  \\ |  ___|      /  ___|          | | | |               | |   ")
    print("| | | |  \\| | | | | |___ \\  ___  \\ `--. _ __   ___| | | |__   ___   ___ | | __")
    print("| | | | . ` | | | |     \\ \\/ _ \\  `--. \\ '_ \\ / _ \\ | | '_ \\ / _ \\ / _ \\| |/ /")
    print("| |/ /| |\\  | |/ /  /\\__/ /  __/ /\\__/ / |_) |  __/ | | |_) | (_) | (_) |   < ")
    print("|___/ \\_| \\_/___/   \\____/ \\___| \\____/| .__/ \\___|_|_|_.__/ \\___/ \\___/|_|\\_\\")
    print("                                       | |                                    ")
    print("                                       |_|                                    ")
    print("\nEasily search and kep track of spells for all your DND campaign needs!")

def printMenuOptions():
    print("\nAPPLICATION FUNCTIONS")
    print("1: Search for a spell by the spell's name.") # (ex. Search for 'shocking grasp', 'fireball', etc.)
    print("2: Search for a spell by a keyword within the spell's description.") # (ex. Searching 'acid' returns all entries with 'acid' associated with it.)
    print("3: View bookmarks.")
    print("4: Help Manual.")
    print("0: Quit.\n")

def getUserInput():
    userInput = -1
    invalidInput = True
    while (invalidInput):
        try:
            userInput = int(input("Choose an option [0, 1, 2, 3, 4]: "))
            if (userInput < 0 or userInput > 4):
                print("Invalid Input. Please enter a valid option!")
            else:
                invalidInput = False
        except ValueError:
            print("Invalid Input. Please enter an integer!")
    return userInput

def searchSpellName():
    print("Option 1 chosen.")

def searchKeyWord():
    print("Option 2 chosen.")

def showHelpMenu():
    print("Option 3 chosen.")

def showBookmarks():
    print("Option 4 chosen.")

def main():
    # variables
    userInput = -1

    # Display Title
    printTitle()

    # User input loop
    while (userInput != 0):
        printMenuOptions()
        userInput = getUserInput()
        if (userInput == 1):
            searchSpellName()
        elif (userInput == 2):
            searchKeyWord()
        elif (userInput == 3):
            showHelpMenu()
        elif (userInput == 4):
            showBookmarks()
        else:
            print("\nProgram closed.")

    


if __name__ == "__main__":
    main()