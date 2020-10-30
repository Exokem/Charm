import src.python.accessor as acc
from src.python.data import *

noun:  dict = {}
pnou: dict = {}

verb:  dict = {}
advb: dict = {}

adjc: dict = {}
prep: dict = {}
conj: dict = {}
intj: dict = {}


def init() -> None:
    """"""

    global intj, acc

    acc.recover_user_data()
    acc.recover_words()
    print(intj)


def store_word(word: Word) -> None:
    """
    Stores a word in the active word maps based on its part of speech.

    :param word: The Word to be stored
    """

    global noun, pnou, verb, advb, adjc, prep, conj, intj

    if word.part == Part.NOUN:
        noun[word.word] = word
    if word.part == Part.PNOU:
        pnou[word.word] = word
    if word.part == Part.VERB:
        verb[word.word] = word
    if word.part == Part.ADVB:
        advb[word.word] = word
    if word.part == Part.ADJC:
        adjc[word.word] = word
    if word.part == Part.PREP:
        prep[word.word] = word
    if word.part == Part.CONJ:
        conj[word.word] = word
    if word.part == Part.INTJ:
        intj[word.word] = word
    print(intj)


if __name__ == '__main__':
    init()
