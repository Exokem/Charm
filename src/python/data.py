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

    DETE = ("determiner", 9)


@dataclass
class Word:
    # The string representation of this Word
    word: str
    # The part of speech that this Word is
    parts: list
    # The keys associated with this Word
    keys: dict

    def __init__(self, word: str, part: Part):
        """
        Constructs a new Word.

        :param word: The word or line to
        :param part: The part of speech that this Word is
        """
        self.word = word
        self.parts = [part]
        self.keys = {}

    def __hash__(self):
        return hash(self.word)

    def __eq__(self, other):
        return self.word == other.word

    def top_part(self) -> int:
        top: Part = self.parts[0]
        return top.value[1]

    def add_part(self, part: Part) -> None:
        self.parts.append(part)

    def add_key(self, key: str) -> None:
        """
        Add a key string to the dictionary of keys associated with this Word.
        Adding an existing key will increment its value.

        :param key: The key to add or increment
        """
        if self.keys.get(key) is None:
            self.keys[key] = 1
        else:
            self.keys[key] = self.keys[key] + 1


@dataclass
class Phrase:
    # The ordered list of words that form this Phrase
    words: list

    def __init__(self, words: list):
        """
        Initialize this Phrase.
        The list of words that constitutes this Phrase should only be modified during initialization.

        :param words: The list of words representative of this Phrase.
        """
        self.words = words

    def __hash__(self):
        code = 0
        for index in range(len(self.words)):
            part = self.words[index]
            code += (hash(part) * index)
        return code

    def __eq__(self, other):
        if len(self.words) != len(other.words):
            return False
        for index in range(len(self.words)):
            if self.words[index] != other.words[index]:
                return False
        return True


def parse(line: str):
    """
    Parses a Word from a string.

    :param line: The line to be parsed into a Word
    :return: A new Word, or None when no Word can be parsed
    """

    # Split line by spaces to read more detailed word information
    line = line.split(' ')

    # Word should be the first value
    # try:
    word = line[0]
    part = get_part(int(line[1]))
    return Word(word, part)
    # except :
    #     return None


def parts():
    return [Part.NOUN, Part.VERB, Part.ADJC, Part.PNOU, Part.ADVB, Part.PREP, Part.CONJ, Part.INTJ, Part.DETE]


def get_part(index: int):
    for part in parts():
        if index == part.value[1]:
            return part
