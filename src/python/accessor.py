import os.path as path
from src.python.data import *
import src.python.charm as charm


alpha: list = []


def recover_data() -> None:
    """"""
    recover_user_data()
    if 0 < len(alpha):
        recover_words()


def recover_user_data() -> None:
    """
    Recovers user data from the user_data file.
    """
    global alpha

    if path.exists("data/user_data"):
        userdata = open("data/user_data").read()

        userdata = userdata.split('\n')

        for line in range(len(userdata)):
            if line == 0:
                # Alphabet is stored in the first line
                alpha = userdata[line].split(' ')


def recover_words() -> None:
    """
    Recovers any words stored in their respective files.
    """
    global alpha

    # Words are divided into letters * parts files, organized alphabetically and by part of speech
    for letter in alpha:
        for part in parts():
            # File path is derived from letter and the part of speech
            dest = "data/" + letter + "_" + part.value[0]
            if path.exists(dest):
                # If the file exists, parse its contents into Word objects
                word_file = open(dest)
                for line in word_file:
                    word = parse(line)
                    if word is not None:
                        # Store Word if it has been parsed successfully
                        store_word(word)


def store_word(word: Word) -> None:
    """
    Stores a word in the active word maps based on its part of speech.

    :param word: The Word to be stored
    """

    if word.part == Part.NOUN:
        charm.nouns[word.word] = word
    if word.part == Part.PNOU:
        charm.pronou[word.word] = word
    if word.part == Part.VERB:
        charm.verbs[word.word] = word
    if word.part == Part.ADVB:
        charm.adverb[word.word] = word
    if word.part == Part.ADJC:
        charm.adject[word.word] = word
    if word.part == Part.PREP:
        charm.prepos[word.word] = word
    if word.part == Part.CONJ:
        charm.conjuc[word.word] = word
    if word.part == Part.INTJ:
        charm.intjec[word.word] = word
