import src.python.charm as charm
from src.python.printer import *
from src.python.data import *

bypass_checks: bool = False
active_question: bool = False
# Is Charm waiting to confirm a query
wait_confirm: bool = False
queried_part: Part
last_input: list = []


def cycle_input() -> None:
    """"""
    while charm.active:
        handle_input(input())


def handle_input(line: str) -> None:
    """"""
    global last_input, wait_confirm, queried_part, bypass_checks

    if line == acc.save_phrase:
        acc.save()
        print("I " + acc.save_phrase + "!")
        return
    elif line == 'x':
        exit(0)

    words = line.split(' ')

    if 0 < len(words):
        # Nothing to process if the input is empty

        if not bypass_checks:
            if check_new_word(words):
                return

        if not wait_confirm and 0 < len(last_input):
            # If the last input contained an unknown word (and it actually exists)
            for part in parts():
                if words[0] == part.value[0]:
                    # Scan for part of speech matching current input and query
                    post_query(last_input[0], "a " + str(part), mode='c')
                    queried_part = part
                    wait_confirm = True
                    return
            print("Oh")
            reset()
        else:
            if words[0].lower() == "yes":
                # Confirm that the unknown word is what the user specified
                word = parse(last_input[0] + "," + str(queried_part.value[1]))
                if word is not None:
                    acc.book[hash(word)] = word
                    if acc.save_phrase == "":
                        post_query("What should I do with that?")
                        bypass_checks = True
                    else:
                        print("Thanks!")
                        reset()
                else:
                    print("That does not make sense")
                    reset()
                return
            elif bypass_checks:
                acc.save_phrase = line
                print("I will " + line + " after new words")
                reset()
            else:
                wait_confirm = False
                check_new_word(last_input)


def post_query(subject: str, value="", mode='e'):
    """
    MODE:
    ========= ===============================================================
    'e'       query a statement
    'c'       query a comparison: 'x' is 'y'
    ========= ===============================================================
    """

    if mode == 'e':
        print(subject)
    elif mode == 'c':
        print(subject + " is " + str(value) + "?")


def check_new_word(words: list) -> bool:
    global last_input
    for word in words:
        if acc.book.get(hash(word.lower())) is None:
            # Make sure all input words are known, ask about them if not
            ask_word(word)
            last_input = words
            return True
    return False


def reset():
    global last_input, wait_confirm, queried_part, bypass_checks
    last_input = []
    wait_confirm = False
    queried_part = None
    bypass_checks = False
