import src.python.accessor as acc


def print_status(message: str, progress: int, end="N"):
    """"""
    if end == "N":
        print(message + ": " + str(progress), end="\r")
    else:
        print(message + ": " + str(progress) + "/" + str(end), end="\r")


def print_value_message(message: str, value) -> None:
    print(message + " (" + str(value) + ")")


def print_query(subject: str, query: str) -> None:
    print("\'" + subject + "\' is a " + query + "?")


def ask_word(word: str) -> None:
    print("What is \'" + word + "\'?")


def print_all_words() -> None:
    for word in acc.book.values():
        print(word.word + " " + str(word.top_part()))