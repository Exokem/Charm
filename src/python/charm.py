import src.python.accessor as acc
import src.python.listener as ltr


def init():
    acc.recover_data()
    greet_user()


def greet_user() -> None:
    print(acc.greeting)
    ltr.wait()


if __name__ == '__main__':
    init()
