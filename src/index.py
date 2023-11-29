from ui.ui import ui_loop
from services.reference_manager import ReferenceManager


def main():
    manager = ReferenceManager()
    ui_loop(manager)


if __name__ == "__main__":
    main()
