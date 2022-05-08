import argparse
import csv
import json
import random
import re
from argparse import RawTextHelpFormatter

description = """
Generates a password out of Simpsons character names and random characters.

Takes a password length argument.

Example:
$ python pw.py 12
"""


class Password:

    # Opens JSON file of character names and returns it in a list.
    def openJSON(self):
        with open(
            "/Users/releach/Desktop/misc-scripts/password_generator/character_data.json"
        ) as f:
            data = json.load(f)
            return data

    # Returns a list of cleaned character names.
    def cleanData(self):
        data = self.openJSON()
        # charList = self.openCSV()
        charList = []
        for item in data:
            name = item["name"]
            cleanName = name.replace(" ", "-")
            cleanerName = re.sub("[#.,/\"'é&%]", "", cleanName)
            charList.append(cleanerName)
        return charList

    # Returns a string of random characters.
    def randomChars(self):
        randomChars = "!@#$%&*?123457689"
        return randomChars

    # Creates a password of n length that combines a character name and random characters.
    def createPW(self, length):
        chars = self.randomChars()
        charsSimp = self.cleanData()
        chosenOne = random.choice(charsSimp)
        someChars = "".join(random.choices(chars, k=4))
        pw = f"{chosenOne}{someChars}"
        while len(pw) <= length:
            anotherChosen = random.choice(charsSimp)
            pw = f"{pw}{anotherChosen}"
        print("")
        print(f"{pw}")
        print("")


if __name__ == "__main__":
    password = Password()

    argparser = argparse.ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter
    )
    argparser.add_argument("length", help="Provide a minimum password length.")
    cliargs = argparser.parse_args()
    length = int(cliargs.length)
    password.createPW(length)
