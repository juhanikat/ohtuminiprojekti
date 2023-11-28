class Reference:
    def __init__(self, name: str, fields: dict = None):
        if fields is None:
            fields = {}
        self.name = name
        self.fields = fields

    def __str__(self):
        key_value_pairs = [key.capitalize() + ': ' + self.fields[key]
                           for key in self.fields]
        fields_str = ', '.join(key_value_pairs)
        return f"{self.name} ({fields_str})"
