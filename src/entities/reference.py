class Reference:
    def __init__(self, name: str, attributes: dict = dict()):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return f"{self.name}: {self.attributes}"