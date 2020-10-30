import src.python.charm as charm
import src.python.accessor as acc


def cycle_input() -> None:
    """"""
    while charm.active:
        handle_input(input())


def handle_input(line: str) -> None:
    """"""
    line = line.split(' ')

    for word in line:
        known: bool = False
        for part in acc.book:
            known = known or part.get(word) is not None

        if not known:
            print("What is " + word + "?")
            return
