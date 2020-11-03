"""
Facilitates storage of Charm data.

Functions:

    add_word(word, part)
    recover_data()
    recover_user_data()
    recover_words()
    save()
    store_contents() -> list

Variables:

    version
    savek
    greeting
    alpha
    book

Authors:

    Samuel Henderson
"""


import os.path as path
from src.python.data import *
from src.python.listener import post_query


# The user-specific version, save key, and greeting
version: str = ""
savek: str = ""
greeting: str = ""

# The user-specific alphabet
alpha: list = []

# The user-specific book of words
book: dict = {}


def add_word(word: str, part: Part) -> None:
    """
    Add a word to the book.
    A new Word is created using a provided string and part of speech and added to the dictionary of all known words.
    """

    word = Word(word, [part.indx()])
    book[hash(word)] = word


def recover_data() -> None:
    """
    Recovers all saved data.
    This function exists because the order of execution for the separate data recovery functions matters.
    The word recovery is a prerequisite of the userdata recovery.
    """

    recover_words()
    recover_user_data()
    post_query("Connected to Charm interactive", version, mode='v')


def recover_user_data() -> None:
    """
    Recovers user data from the user_data file.

    LINES:
    ========= ==============
    0         Alphabet
    1         Version
    2         Save Key
    3         Greeting
    ========= ==============
    """

    global alpha, version, savek, greeting

    if path.exists("data/user_data"):
        userdata = open("data/user_data").read()

        userdata = userdata.split('\n')

        for line in range(len(userdata)):
            sections = userdata[line].split(",")
            if line == 0:
                # Alphabet is stored in the first line
                alpha = sections[0]
            elif 1 < len(sections):
                if line == 1:
                    # Version is stored in the second line
                    version = sections[1][:-2] + str(len(book)) + "-"
                    end = len(alpha) - 1
                    # Append last three characters in alphabet to displayed version
                    version += alpha[end - 4] + alpha[end - 2] + alpha[end]
                elif line == 2:
                    # Save key is stored in the third line
                    savek = sections[1]
                elif line == 3:
                    # Greeting is stored in the fourth line
                    greeting = sections[1]


def recover_words() -> None:
    """
    Parses each line in the 'words' file as a Word.
    """

    dest = "data/words"

    if path.exists(dest):
        # If the file exists, open it and parse
        word_file = open(dest)
        for line in word_file:
            # Attempt to parse a Word from the current line
            word = parse_line(line)
            if word is not None:
                # Store Word if it has been parsed successfully
                book[hash(word)] = word
    else:
        # Create the file if it is missing
        file = open(dest, "w+")
        file.close()


def save():
    """
    Saves all stored word and user data.
    """

    global savek, greeting

    # First clear the words data file
    open("data/words", "w").close()
    words = open("data/words", "r+")
    words.truncate(0)

    # Write each formatted Word into a separate line in the empty file
    for word in book.values():
        words.write(word.format())
    words.close()

    # Collect the contents of the user data file before erasing it
    data = store_contents("data/user_data", create=True)

    if 4 <= len(data):
        # Overwrite the third and fourth lines of the data file with the new save key and greeting values
        # Only updated if not an empty string
        if savek != "":
            data[2] = "save," + savek + "\n"
        if greeting != "":
            data[3] = "greeting," + greeting + "\n"

    # Open the data file and write its new contents
    userdata = open("data/user_data", "r+")
    for entry in data:
        userdata.write(entry)


def store_contents(file: str, create: bool = False) -> list:
    """
    Reads the contents of a file into a list.
    Each entry in the list represents a line in the provided file, if it exists.

    :param file: The path of the file to read
    :param create: Should the file be created if it does not exist
    :return: A list containing the contents of the file
    """

    if not path.exists(file):
        if create:
            open(file, "w+").close()
        return []
    else:
        lines = []
        for line in open(file):
            lines.append(line)
        return lines
