class Reference:
    def __init__(self, name: str, fields: dict = dict()):
        self.name = name
        self.fields = fields

    def __str__(self):
        return f"{self.name} ({', '.join([key.capitalize() + ': ' + self.fields[key] for key in self.fields])})"
