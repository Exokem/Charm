"""
Contains classes and parsing functions relevant to data storage.

Classes:

    Part
    Word
    Phrase

Functions:

    parse_line(line)
    parts()
    names()
    get_part(index)

Authors:

    Samuel Henderson
"""

import enum
from dataclasses import dataclass


class Part(enum.Enum):
    """
    A class representing a part of speech.
    All parts of speech are predefined.

    Attributes:

        NOUN : tuple
            1 Noun            a word that represents a person, place, thing, or concept.
        PNOU : tuple
            2 Pronoun         a word used in the place of a noun (he/she/they/it/etc.).
        VERB : tuple
            3 Verb            a word that represents an action.
        ADVB : tuple
            4 Adverb          a word that describes a verb.
        ADJC : tuple
            5 Adjective       a word that describes a noun.
        PREP : tuple
            6 Preposition     a word that is used before a noun/pronoun to form a phrase (in/on/at/onto/etc.).
        CONJ : tuple
            7 Conjunction     a word that connects clauses or sentences (and/but/if/etc.).
        INTJ : tuple
            8 Interjection    a word that represents a short exclamation or interruption.
        DETE : tuple
            9 Determiner      a word that determines the reference a noun has (a/the/every/etc.).

    Functions:

        indx() -> int:
            Provides the index attached to the enumerated part of speech on which it is called.
            The returned value is always inclusively between 1 and 9.
        name() -> str:
            Provides the name attached to the enumerated part of speech on which it is called.

    """

    NOUN = ("noun", 1)
    PNOU = ("pronoun", 2)

    VERB = ("verb", 3)
    ADVB = ("adverb", 4)

    ADJC = ("adjective", 5)
    PREP = ("preposition", 6)
    CONJ = ("conjunction", 7)
    INTJ = ("interjection", 8)
    DETE = ("determiner", 9)

    def __hash__(self):
        return hash(self.name())

    def __eq__(self, other):
        return self.name() == other.name() and self.indx() == other.indx()

    def __str__(self):
        return self.value[0]

    def indx(self) -> int:
        return self.value[1]

    def name(self) -> str:
        return self.value[0]


@dataclass
class Word:
    """
    A class representing a word.

    Attributes:

        keys : dict
            The unique keys associated with their word.
            All key-value pairs inserted into this field should follow the model: (K: str, V: int), where
            the value attached to a key represents the number of times it has been added.
        word : str
            The word string of a Word.
        parts : list
            A list of the parts of speech (see the Part class) that a Word has been assigned to.
        defn : str
            The definition of a Word.

    Functions:

        top_part() -> int:
            Provides the enumerated index of the first Part a Word was assigned to.
        parts() -> str:
            Produces a string containing all Part indices separated by a space.
        add_part(part):
            Assigns a Word to a new part of speech.
        add_key(key):
            Adds a new key to the dictionary of stored keys, or increments the value attached to it.
        define(defn):
            Updates the definition (see defn attribute) of a Word.
        format() -> str:
            Provides a formatted string to be inserted as the entry of a Word into the words data file.

    """

    keys: dict
    word: str
    parts: list
    defn: str = ''

    def __init__(self, word: str, indices: list):
        """
        Constructs a new Word.

        :param word: The word or line to
        :param indices: The parts of speech that this Word is
        """

        self.word = word
        self.parts = []

        for index in indices:
            # Parse the list of indices into parts of speech to attach to this Word
            part = get_part(int(index))
            if part is not None and not self.parts.__contains__(part):
                self.parts.append(part)

    def __hash__(self):
        # Hash words only by string so the same word strings will not be split over different Word instances
        return hash(self.word)

    def __eq__(self, other):
        # Words are equal if they have the same word string
        # This should not be meaningfully usable as there should never be two Word instances comparable by their word
        return self.word == other.word

    def __str__(self):
        return self.word

    def top_part(self) -> int:
        """
        Access the first Part this Word was assigned to
        :return: -1 indicates no parts; 1-9 indicates the index of the Part as defined in its enum entry
        """

        if len(self.parts) < 1:
            # No Parts
            return -1
        return self.parts[0].indx()

    def parts(self) -> str:
        """
        Formats the functional parts of speech of this Word into a string, separated with spaces.
        """

        # Start with first Part
        out: str = self.parts[0].value[1]
        for index in range(1, len(self.parts)):
            # Append a space and the next Part index
            out = out + " " + str(self.parts[index].value[1])
        return out

    def add_part(self, part: Part) -> None:
        """
        Assign this Word to a new part of speech.
        Duplicates are ignored.
        """

        if not self.parts.__contains__(part):
            self.parts.append(part)

    def add_key(self, key: str) -> None:
        """
        Add a key string to the dictionary of keys associated with this Word.
        Adding an existing key will increment its value.

        :param key: The key to add or increment
        """

        if self.keys is None:
            # Initialize keys if undefined
            self.keys = {}

        if self.keys.get(key) is None:
            # Add first occurrence of the provided key
            self.keys[key] = 1
        else:
            # Increment occurrences of existing keys
            self.keys[key] = self.keys[key] + 1

    def define(self, defn: str) -> None:
        """
        Define this Word.
        """

        self.defn = defn

    def format(self) -> str:
        """
        Formats necessary elements of this Word for saving.

        WORD,P P P P P P P P P,DEFINITION,KEY0:V0 ... KEYN:VN
        """

        # Start with the word and top Part
        out: str = self.word + "," + str(self.top_part())

        for index in range(1, len(self.parts)):
            # Add all other Parts followed by a space
            out = out + " " + str(self.parts[index].indx())

        if self.defn is not None:
            out = out + "," + self.defn + ","

        # TODO: append keys

        return out + "\n"


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


def parse_line(line: str):
    """
    Parses a Word from a string.

    :param line: The line to be parsed into a Word
    :return: A new Word, or None when no Word can be parsed
    """

    # Split line by spaces to read more detailed word information
    line = line.split(',')

    # Word should be the first value
    word = line[0]
    indices = line[1].replace('\n', '').split(' ')

    obj = Word(word, indices)
    return obj


def parts():
    """
    Provides a list of all enumerated parts of speech.
    """

    return [Part.NOUN, Part.VERB, Part.ADJC, Part.PNOU, Part.ADVB, Part.PREP, Part.CONJ, Part.INTJ, Part.DETE]


def names() -> dict:
    """
    Provides a dictionary of the names of each enumerated Part.
    """

    out = {}
    for part in parts():
        out[part.name()] = part
    return out


def get_part(index: int):
    """
    Returns a Part if the provided index matches that of any enumerated Part.
    Nothing is returned if no enumerated Part has the provided index.
    """

    for part in parts():
        if index == part.value[1]:
            return part
