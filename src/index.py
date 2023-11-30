from ui.ui import UI, UserInputError
from default_io import DefaultIO
from services.file_manager import save_data, load_data


def main():
    manager = load_data()
    ui = UI(manager, DefaultIO())

    ui.ui_loop()
    # after the user has quit the program
    save_data(manager)


if __name__ == "__main__":
    main()
