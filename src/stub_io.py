class StubIO:
    def __init__(self, inputs=None):
        self.inputs = inputs or []
        self.outputs = []

    def write(self, value):
        self.outputs.append(value)

    def read(self, message=None):
        if len(self.inputs) > 0:
            return self.inputs.pop(0)
        return message

    def add_input(self, value):
        self.inputs.append(value)
