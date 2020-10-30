import enum
from dataclasses import dataclass


class Part(enum.Enum):
    # Person/Place/Thing/Concept
    NOUN = ("noun", 1)
    # Used in the place of a noun
    PNOU = ("pronoun", 2)

    # Action
    VERB = ("verb", 3)
    # Descriptor to verb
    ADVB = ("adverb", 4)

    # Descriptor
    ADJC = ("adjective", 5)
    # Used before noun/pronoun to form a phrase - time, place, direction, agent, instrument (in, on, at, into, etc.)
    PREP = ("preposition", 6)
    # Unitive - transitions and elemental relation discriptors
    CONJ = ("conjunction", 7)
    # Expressive
    INTJ = ("interjection", 8)


@dataclass
class Word:
    # The string representation of this Word
    word: str
    # The part of speech that this Word is
    part: Part

    def __init__(self, word: str, part: Part):
        """
        Constructs a new Word.

        :param word: The word or line to
        :param part: The part of speech that this Word is
        """
        self.word = word
        self.part = part

    def __hash__(self):
        return hash(self.word)


def parse(line: str, part: Part):
    """
    Parses a Word from a string.

    :param line: The line to be parsed into a Word
    :return: A new Word, or None when no Word can be parsed
    """

    # Split line by spaces to read more detailed word information
    line = line.split(' ')

    # Word should be the first value
    word = line[0]
    return Word(word, part)


def parts():
    return [Part.NOUN, Part.VERB, Part.ADJC, Part.PNOU, Part.ADVB, Part.PREP, Part.CONJ, Part.INTJ]


def get_part(index: int):
    for part in parts():
        if index == part.value[1]:
            return part



