from services.file_manager import load_data, save_data
from ui.ui import UI


def main():
    manager = load_data()
    ui = UI(manager)

    ui.ui_loop()
    # after the user has quit the program
    save_data(manager)


if __name__ == "__main__":
    main()
