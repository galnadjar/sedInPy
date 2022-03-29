#MADE BY GAL NADJAR
#DATE CREATED : 29-03-2022

import shutil
import sys
import re
import constants


def lastSubStrInd(userInput):
    """
    find the starting index of the last occurrence of a substring
    :param userInput: the input from the user
    :return:the starting index as mentioned above
    """

    i = len(userInput) - 1
    wordStarted = False
    while i >= 0:

        if userInput[i].isspace(): #if the current word is space
            if wordStarted: #if atleast 1 letter was already called it means previously we had a start of a last substr
                return i+1

        else: #a word which is a space was read
            wordStarted = True

        i-= 1

    return 0 #if the entire string is smooshed together


def getDelim(userInput):
    """
    looks for the delimiter in the user input
    :param userInput: the input came from the user
    :return: the delimiter adjacent to the second s in (" sed 's ") if "sed","'","s" were found beforehand in that order
    otherwise, returns ERROR = -1 meaning this pattern wasn't found or the pattern found wasn't valid
    """

    desired = "'s"
    delimStr = ""

    i = userInput.find("sed ")

    if i != -1: #meaning the "sed " exists in the string
        desiredInd = 0
        i += constants.SEDWORD
        while i < len(userInput) and delimStr != desired:
            if userInput[i] == desired[desiredInd]:
                delimStr += userInput[i]
                desiredInd += 1

            i += 1

        # it is exactly 1 character after the pattern sed 's meaning its the delimiter if in bounds
        if i < len(userInput) and delimStr == desired:
            return userInput[i] #the actual delimiter

    #the delimiter wasn't found
    return constants.ERROR


def sedCmd(inputStreamName,dest,src):
    """
    handles a valid line of command and prints to the stdio the output after the change
    if a file was given as an argument , rewrite it accordingly
    otherwise edits the text in the proper location and prints it
    :param inputStreamName: the name of the stream
    :param dest: the string to be changed
    :param src: the string dest will be changed to
    """


    if inputStreamName != "" and inputStreamName.endswith(".txt"): #the input stream type is a text file

        try: #check if its possible to open it
            inputFile = open(inputStreamName, "r")

            newFile = open("tempname.txt", "w")    #creates a new file with a temp name to posses the new input
            print("The new file input is: ")
            for line in inputFile:                 #printing the new text to the new file and also prints it to the stdo
                newLine = line.replace(dest, src)
                print(newLine)
                newFile.write(newLine)

            newFile.close()
            inputFile.close()

            shutil.move("tempname.txt", inputStreamName) #overwrites the original file with the edited one

        except IOError: #file couldn't open because doesn't exist
            print("file requested does not exist in the directory")


    # a string is given as arg to sed if it was misspelled text file its still treated as a string
    else:
        print(inputStreamName.replace(dest, src))


def checkProperPattern(userInput,delim):
    """
    check the user input for a proper input which matches sed pattern
    :param userInput: the input from the user
    :param delim: the delimiter found in the text
    :return: since its return goes into wasError var,
            false if Input is valid .
            true if input is invalid. """


    if delim != constants.ERROR and delim != '\n' and delim != '\\':
        allExceptDelim = f"[^{delim}]"  # all characters besides the delimiter

        # the sed pattern requested
        pattern = delim.join(["sed\s*'\s*s", allExceptDelim + "+", allExceptDelim + "*", "\s*[n|g|p|w]?\s*'\s*.+"])

        if re.search(pattern, userInput):  # if input is valid because matching the sed pattern
            return False

    return True


def main():

    wasError = False  #flag symbolyzing there wasn't error in the syntax of the input
    dest = ""
    src = ""
    inputStreamName = ""

    #handling receiving arguments through terminal when format is: oldstring newstring filename
    if len(sys.argv) > 1:
        #check if cmd line arguments were given
        if len(sys.argv) == constants.VALIDARGSAMOUNT:
            dest = sys.argv[constants.DESTPOS]
            src = sys.argv[constants.SRCPOS]
            inputStreamName = sys.argv[-1]

        else: #argument were received through the console yet the syntax was invalid
            wasError = True

    #handling receiving a sed sentence
    else:
        userInput = input("enter input: ")
        delim = getDelim(userInput)

        wasError = checkProperPattern(userInput,delim)
        if not wasError:
            start = userInput.find("'")
            end = userInput.rfind("'")

            lst = re.split(delim, userInput[start:end + 1])  # splits the content between the ' ' based on the delimiter

            dest = lst[constants.DESTPOS]
            src = lst[constants.SRCPOS]

            inputStreamName = userInput[lastSubStrInd(userInput)::].rstrip()


    #a file was given as arg and it was properly named
    if not wasError:
       sedCmd(inputStreamName,dest,src)

    #a syntax error was found thorughout the scanning of the input
    else:
        print("Invalid syntax")


if __name__ == '__main__':
    main()