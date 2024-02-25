import argparse
import json
import random
import re
import os
from argparse import RawTextHelpFormatter

description = """
Generates a password out of Simpsons character names and random characters.

Takes a password length argument.

Example:
$ python pw.py 12
"""

class Password:

    def __init__(self):
        # Construct a path relative to this script's location
        self.char_data_path = os.path.join(os.path.dirname(__file__), 'character_data.json')

    # Opens JSON file of character names and returns it in a list.
    def openJSON(self):
        with open(self.char_data_path) as f:
            data = json.load(f)
            return data

    # Returns a list of cleaned character names.
    def cleanData(self):
        data = self.openJSON()
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
        pw = ""
        while len(pw) < length:
            chosenOne = random.choice(charsSimp)
            someChars = "".join(random.choices(chars, k=4))
            pw_chunk = f"{chosenOne}{someChars}"
            if len(pw) + len(pw_chunk) > length:
                pw_chunk = pw_chunk[:length - len(pw)]  
            pw += pw_chunk
        print("\n{}\n".format(pw))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument("length", type=int, help="Provide a minimum password length.")
    args = parser.parse_args()

    password = Password()
    password.createPW(args.length)
