class Reference:
    def __init__(self, name: str, fields: dict = None):
        if fields is None:
            fields = {}
        self.name = name
        self.fields = fields

    def get_type(self):
        if "entry_type" in self.fields:
            return self.fields["entry_type"]
        return None

    def get_fields_as_dict(self):
        return self.fields

    def get_fields_as_tuples(self):
        return [(key, value)
                for key, value in self.fields.items() if key != "entry_type"]

    def __str__(self):
        key_value_pairs = [key.capitalize() + ': ' + self.fields[key]
                           for key in self.fields]
        fields_str = ', '.join(key_value_pairs)
        return f"{self.name} ({fields_str})"
