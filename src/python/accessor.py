import os.path as path
from src.python.data import *
from src.python.printer import *


version: str = ""

save_phrase: str = ""
greeting: str = ""

alpha: list = []

book: dict = {}


def recover_data() -> None:
    """"""
    recover_words()
    recover_user_data()
    print_value_message("Connected to Charm Communication Console", version)


def recover_user_data() -> None:
    """
    Recovers user data from the user_data file.
    """
    global alpha, version, save_phrase, greeting

    if path.exists("data/user_data"):
        userdata = open("data/user_data").read()

        userdata = userdata.split('\n')

        for line in range(len(userdata)):
            sections = userdata[line].split(",")
            if 1 < len(sections):
                if line == 0:
                    # Alphabet is stored in the first line
                    alpha = sections
                elif line == 1:
                    version = sections[1][:-2] + str(stored_words()) + "-"
                    for i in range(len(alpha) - 3, len(alpha)):
                        if 0 <= i:
                            version += alpha[i]
                elif line == 2:
                    save_phrase = sections[1]
                elif line == 3:
                    greeting = sections[1]


def stored_words() -> int:
    return len(book)


def recover_words() -> None:
    """
    Recovers any words stored in their respective files.
    """
    global alpha

    count = 0

    dest = "data/words"
    if path.exists(dest):
        # If the file exists, parse its contents into Word objects
        word_file = open(dest)
        for line in word_file:
            word = parse(line)
            if word is not None:
                # Store Word if it has been parsed successfully
                count += 1
                book[hash(word)] = word
                print_status("Recovering words from " + dest, count)
    else:
        file = open(dest, "w+")
        file.close()


def save():
    global save_phrase, greeting

    open("data/words", "w").close()
    words = open("data/words", "r+")
    words.truncate(0)
    for word in book.values():
        words.write(word.format())
    words.close()

    data = store_contents("data/user_data")
    if 4 <= len(data):
        if save_phrase != "":
            data[2] = "save," + save_phrase + "\n"
        if greeting != "":
            data[3] = "greeting," + greeting + "\n"

    userdata = open("data/user_data", "r+")
    for entry in data:
        userdata.write(entry)


def store_contents(file: str) -> list:
    """
    Reads the contents of a file into a list.
    Each entry in the list represents a line in the provided file, if it exists.

    :param file: The path of the file to read.
    :return: A list containing the contents of the file.
    """

    if not path.exists(file):
        return []
    else:
        lines = []
        for line in open(file):
            lines.append(line)
        return lines
