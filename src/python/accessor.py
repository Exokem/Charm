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
    global alpha, version

    if path.exists("data/user_data"):
        userdata = open("data/user_data").read()

        userdata = userdata.split('\n')

        for line in range(len(userdata)):
            sections = userdata[line].split(' ')
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
                book[word.__hash__()] = word
                print_status("Recovering words from " + dest, count)
    else:
        file = open(dest, "w+")
        file.close()


def save():
    open("data/words", "w").close()
    words = open("data/words", "r+")
    words.truncate(0)
    for word in book.values():
        words.write(word.word + " " + str(word.top_part()) + "\n")
    words.close()