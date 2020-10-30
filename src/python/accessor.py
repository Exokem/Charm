import os.path as path
from src.python.data import *
from src.python.printer import *


version: str

alpha: list = []

noun: dict = {}
pnou: dict = {}

verb: dict = {}
advb: dict = {}

adjc: dict = {}
prep: dict = {}
conj: dict = {}
intj: dict = {}


def recover_data() -> None:
    """"""
    recover_user_data()
    if 0 < len(alpha):
        recover_words()
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
            if line == 0:
                # Alphabet is stored in the first line
                alpha = sections
            elif line == 1:
                version = sections[1]
                for i in range(len(alpha) - 3, len(alpha)):
                    if 0 <= i:
                        version += alpha[i]


def recover_words() -> None:
    """
    Recovers any words stored in their respective files.
    """
    global alpha

    count = 0

    # Words are divided into letters * parts files, organized alphabetically and by part of speech
    for letter in alpha:
        for part in parts():
            # File path is derived from letter and the part of speech
            dest = "data/" + letter + "_" + part.value[0]
            if path.exists(dest):
                # If the file exists, parse its contents into Word objects
                word_file = open(dest)
                for line in word_file:
                    word = parse(line, part)
                    if word is not None:
                        # Store Word if it has been parsed successfully
                        count += store_word(word)
                        print_status("Recovering words from " + dest, count)


def store_word(word: Word) -> int:
    """
    Stores a word in the active word maps based on its part of speech.

    :param word: The Word to be stored
    """

    if word.part == Part.NOUN:
        noun[word.word] = word
    elif word.part == Part.PNOU:
        pnou[word.word] = word
    elif word.part == Part.VERB:
        verb[word.word] = word
    elif word.part == Part.ADVB:
        advb[word.word] = word
    elif word.part == Part.ADJC:
        adjc[word.word] = word
    elif word.part == Part.PREP:
        prep[word.word] = word
    elif word.part == Part.CONJ:
        conj[word.word] = word
    elif word.part == Part.INTJ:
        intj[word.word] = word
    else:
        return 0

    return 1
