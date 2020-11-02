import random
from src.python.printer import *
from src.python.data import *


def wait() -> None:
    process_input(input())


def process_input(line: str) -> None:
    """"""

    # Do not lines if empty or commands
    # Built in commands take precedence to other processing
    if line_valid(line) and not check_commands(line):

        # Split the line into its constituent words
        words = line.split(' ')

        # As long as any words in the last line are unknown, attempt to learn them
        while unknown_words(words) is not None:
            learn_new_word(unknown_words(words))

    wait()


def line_valid(line: str) -> bool:
    return line != ' ' and line != ''


def check_commands(line: str) -> bool:
    """
    Processes some built in commands.
    True is returned if further input processing should be skipped.

    COMMANDS:
    ===================== =================================================================
    <save_phrase>         Saves all stored content. The command itself is user-defined.
    'x'                   Causes the program to exit.
    ===================== =================================================================
    """
    if line == acc.save_phrase:
        acc.save()
        post_query("I " + line + "!")
        return True
    elif line == 'x':
        exit(0)

    return False


def unknown_words(words: list):
    """
    Scans a list of words. If the list contains words that are not stored, the first unknown word is returned.
    """

    for word in words:
        if acc.book.get(hash(word.lower())) is None:
            return word
    return None


def learn_new_word(word: str) -> None:
    """
    Facilitates the learning of a provided word.
    The user is repeatedly prompted for the part of speech until their input contains a valid one.
    """

    unlearned: bool = True

    while unlearned:
        line = input("What is " + word + "?")
        valid_names = names()

        line = line.split(' ')

        for arg in line:
            if valid_names.__contains__(arg):
                acc.add_word(word, valid_names[arg])
                try_ask_save()
                return


def try_ask_save() -> None:
    """
    Attempts to derive a save phrase from the user.
    By default, there is no save phrase - it must be defined by the user when prompted.
    There is a 95% chance that the user will be asked to provide a save phrase if it has not already been defined.
    """

    if acc.save_phrase == '':
        val = random.random()
        if val < 0.95:
            val = input("What should I do with that?")
            if line_valid(val):
                acc.save_phrase = val
                post_query("I will \'" + acc.save_phrase + "\' to keep new information")
            else:
                post_query("That does not make sense")


def post_query(subject: str, value="", mode='e'):
    """
    Posts a generic query to the console with a subject and optional value.
    The mode determines the format of the printed query.
    Modifiers can be attached to modes, but only one mode should be used.

    MODE:
    ========= ===============================================================
    'c'       query a comparison: 'subject' is 'query'
    'd'       query a direct definition: 'subject' 'query'
    'e'       query a statement: 'subject'
    ========= ===============================================================

    MODIFIERS:
    ========= ===============================================================
    'x'       add an exclamation to the query
    ========= ===============================================================
    """

    message: str = ""

    # Apply mode
    if mode.__contains__('c'):
        message = subject + " is " + str(value) + "?"
    elif mode.__contains__('d'):
        message = subject + " " + str(value) + "?"
    elif mode.__contains__('e'):
        message = subject

    # Apply stackable modifiers
    if mode.__contains__('x'):
        message = message + "!"

    print(message)
