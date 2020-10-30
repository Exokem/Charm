import src.python.accessor as acc

nouns:  dict = {}
pronou: dict = {}

verbs:  dict = {}
adverb: dict = {}

adject: dict = {}
prepos: dict = {}
conjuc: dict = {}
intjec: dict = {}


def init() -> None:
    """"""

    acc.recover_user_data()
    acc.recover_words()
    print(intjec)


if __name__ == '__main__':
    init()
