from ui.ui import UI
from stub_io import StubIO
from services.reference_manager import ReferenceManager


class UILibrary:
    def __init__(self) -> None:
        self.manager = ReferenceManager()
        self.io = StubIO()
        self.ui = UI(self.manager, self.io)

    def input(self, value):
        self.io.add_input(value)

    def output_should_contain(self, value):
        outputs = self.io.outputs
        inputs = self.io.inputs

        if not value in outputs:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(outputs)}, " +
                f"Inputs: {str(inputs)}"
            )

    def output_should_not_contain(self, value):
        outputs = self.io.outputs
        inputs = self.io.inputs

        if value in outputs:
            raise AssertionError(
                f"Output \"{value}\" is in {str(outputs)}, " +
                f"Inputs: {str(inputs)}"
            )

    def output_should_be(self, value):
        outputs = self.io.outputs
        inputs = self.io.inputs

        if len(outputs) > 1 or not value in outputs:
            raise AssertionError(
                f"Output \"{value}\" is not the same as {str(outputs)}, " +
                f"Inputs: {str(inputs)}"
            )

    def ask_for_input(self):
        self.ui.ask_for_input()
