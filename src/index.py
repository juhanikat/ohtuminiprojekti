from ui.ui import UI
from default_io import DefaultIO
from services.file_manager import save_data, load_data


def main():
    manager = load_data()
    ui = UI(manager)

    ui.ui_loop()
    # after the user has quit the program
    save_data(manager)


if __name__ == "__main__":
    main()
