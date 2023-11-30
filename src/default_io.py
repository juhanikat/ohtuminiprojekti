class DefaultIO:
    def write(self, value):
        print(value)

    def read(self, message):
        return input(message)
