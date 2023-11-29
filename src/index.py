from ui.ui import ui_loop, UserInputError
from services.file_manager import save_data, load_data


def main():
    manager = load_data()

    while True:
        try:
            user_input = ui_loop(manager)
        except UserInputError as error:
            print(error)
        if user_input == -1:  # user wants to quit the program
            save_data(manager)
            break


if __name__ == "__main__":
    main()
