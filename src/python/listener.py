import src.python.charm as charm
import src.python.accessor as acc
import src.python.printer as prt
from src.python.data import *

bypass_checks: bool = False
active_question: bool = False
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

    words = line.split(' ')

    if 0 < len(words):
        if not bypass_checks:
            if check_new_word(words):
                return

        if not wait_confirm and 0 < len(last_input):
            # If the last input contained an unknown word
            for part in parts():
                if words[0] == part.value[0]:
                    # Scan for part of speech matching current input and query
                    prt.print_query(last_input[0], part.value[0])
                    queried_part = part
                    wait_confirm = True
                    return
            print("Oh")
            reset()
        else:
            if words[0].lower() == "yes":
                word = parse(last_input[0] + " " + str(queried_part.value[1]))
                if word is not None:
                    acc.book[word.__hash__()] = word
                    if acc.save_phrase == "":
                        print("What should I do with that?")
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


def check_new_word(words: list) -> bool:
    global last_input
    for word in words:
        if acc.book.get(word.lower().__hash__()) is None:
            # Make sure all input words are known, ask about them if not
            ask_word(word)
            last_input = words
            return True
    return False


def ask_word(word: str) -> None:
    print("What is \'" + word + "\'?")


def reset():
    global last_input, wait_confirm, queried_part, bypass_checks
    last_input = []
    wait_confirm = False
    queried_part = None
    bypass_checks = False