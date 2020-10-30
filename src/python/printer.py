
def print_status(message: str, progress: int, end="N"):
    """"""
    if end == "N":
        print(message + ": " + str(progress), end="\r")
    else:
        print(message + ": " + str(progress) + "/" + str(end), end="\r")


def print_value_message(message: str, value) -> None:
    print(message + " (" + str(value) + ")")
