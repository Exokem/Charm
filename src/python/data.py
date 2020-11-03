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
    # The keys associated with this Word
    keys: dict

    # The string representation of this Word
    word: str
    # The part of speech that this Word is
    parts: list
    # The definition of this Word
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
    return [Part.NOUN, Part.VERB, Part.ADJC, Part.PNOU, Part.ADVB, Part.PREP, Part.CONJ, Part.INTJ, Part.DETE]


def names():
    out = {}
    for part in parts():
        out[part.name()] = part
    return out


def get_part(index: int):
    for part in parts():
        if index == part.value[1]:
            return part
