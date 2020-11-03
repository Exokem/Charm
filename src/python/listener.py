import random
from src.python.accessor import *
from src.python.data import *


def wait() -> None:
    """
    Wait to process the user input.
    """

    process_input(input())


def process_input(line: str) -> None:
    """
    Processes the user input.

    Input lines are first validated, then compared to built in commands. If they match any such commands, they are not
    processed further and the commands they match are executed.

    After validation, each word in a line is compared to the existing word database to verify that it is known.
    Charm will attempt to learn what part of speech an unknown word belongs to before anything else.
    """

    # Do not lines if empty or commands
    # Built in commands take precedence to other processing
    if line_valid(line) and not check_commands(line):

        # Split the line into its constituent words
        words = line.split(' ')

        while unknown_words(words) is not None:
            # As long as any words in the last line are unknown, attempt to learn them
            learn_new_word(unknown_words(words))

        if len(words) == 1:
            # Attempt to learn the definition of single-word input
            learn_new_defn(words.pop())

    wait()


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

    if line == save_phrase:
        # Save and notify
        save()
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
        if book.get(hash(word.lower())) is None:
            # If any word is unknown, return it to be identified
            return word

    return None


def learn_new_word(word: str) -> None:
    """
    Facilitates the learning of a provided word.

    The user is repeatedly prompted for the part of speech until their input contains a valid one.
    After learning a new word, Charm will try to ask the user what to do with new information.
    """

    if word is None:
        # Cannot learn known words
        return

    unlearned: bool = True

    while unlearned:
        # Ask about the word until it has been learned - its part of speech must be identified
        line = input("What is " + word + "?")
        # Collect a dictionary of the valid Part names for comparison to input
        valid_names = names()

        # Split line by spaces to create a list of words
        line = line.split(' ')

        for arg in line:
            # Check all words in the input line for valid parts of speech
            if valid_names.__contains__(arg):
                add_word(word, valid_names[arg])
                try_ask_save()
                return


def learn_new_defn(word: str) -> None:
    """
    Attempts to learn the definition of a provided word.

    The user is prompted for a definition, but if their input is a negative response, no definition is recorded.
    """

    # Retrieve the Word object from Charm's book
    word = book[hash(word)]

    # Do not inherently ask to redefine
    if word.defn != '':
        return

    # Prompt for definition
    res = input("Define \'" + str(word) + "\'?")

    if negative(res):
        # Do not define if response is negative
        return

    # Notify and define
    post_query("Defined \'" + str(word) + "\' as \'" + res + "\'")
    word.define(res)


def try_ask_save() -> None:
    """
    Attempts to derive a save phrase from the user.
    By default, there is no save phrase - it must be defined by the user when prompted.
    There is a 95% chance that the user will be asked to provide a save phrase if it has not already been defined.
    """
    global save_phrase

    if save_phrase == '':
        # Do not inherently redefine save phrase
        val = random.random()
        if val < 0.95:
            # 95% chance to ask for save phrase
            val = input("What should I do with that?")

            if line_valid(val):
                # Do not use empty or single space lines as a save phrase
                save_phrase = val
                post_query("I will \'" + save_phrase + "\' to keep new information")
            else:
                # Notify the user of their error
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
    'v'       post a statement and parenthesized value: 'subject' ('value')
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
    elif mode.__contains__('v'):
        message = subject + " (" + str(value) + ")"

    # Apply stackable modifiers
    if mode.__contains__('x'):
        message = message + "!"

    print(message)


def line_valid(line: str) -> bool:
    """
    Valid lines are not empty and not a single space.
    """

    return line != ' ' and line != ''


def negative(word: str) -> bool:
    """
    Checks a word against a set of words representing a response of 'no'.
    """

    negatives = ['no', 'negative', 'nah']
    return negatives.__contains__(word)