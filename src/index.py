from ui.ui import ask_for_input, UserInputError
from services.reference_manager import ReferenceManager


def main():
    manager = ReferenceManager()

    while True:
        try:
            user_input = ask_for_input(manager)
            if user_input == -1:  # user wants to quit the program
                break
        except UserInputError as error:
            print(error)


if __name__ == "__main__":
    main()
