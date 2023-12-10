def get_reference_type():
    while True:
        reference_type = input("Enter reference type (article, book,"
                               " inproceedings)or  exit: ").lower()
        if reference_type == "exit":
            return None
        if reference_type in ['article', 'book', 'inproceedings']:
            return reference_type
        print("Invalid type")


def ask_fields(reference_type):
    reference_key = input("Enter key for reference: ").strip()
    while not reference_key:
        print("Cannot be empty")
        reference_key = input("Enter key for reference: ").strip()

    fields = {}
    required_fields = {
        'article': ['author', 'title', 'journal', 'year', 'volume'],
        'book': ['author', 'title', 'publisher', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year']
    }

    for field in required_fields.get(reference_type, []):
        user_input = input(f"Enter {field}: ").strip()
        while not user_input:
            print("Field cannot be empty")
            user_input = input(f"Enter {field}: ").strip()

        if field == 'year' and not user_input.isdigit():
            print("Invalid input")
        else:
            fields[field] = user_input

    return reference_key, fields
