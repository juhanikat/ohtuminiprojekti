def get_reference_type(print_message=True):
    while True:
        reference_type = input("Enter reference type (article, book, inproceedings)"
                               " or  exit: ").lower()
        if reference_type == "exit":
            return None
        if reference_type in ['article', 'book', 'inproceedings']:
            return reference_type
        if print_message:
            print("Invalid type")


def ask_fields(reference_type):
    reference_key = input("Enter key for reference: ")
    while not reference_key.strip():
        print("Cannot be empty")
        reference_key = input("Enter key for reference: ")

    fields = {}

    required_fields = {
        'article': ['author', 'title', 'journal', 'year', 'volume'],
        'book': ['author', 'title', 'publisher', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year']
    }

    for field in required_fields.get(reference_type, []):
        valid_input = False
        while not valid_input:
            user_input = input(f"Enter {field}: ")
            if user_input.strip():
                if field == 'year' and not user_input.isdigit():
                    print("Invalid input")
                else:
                    fields[field] = user_input
                    valid_input = True
            else:
                print("Field cannot be empty")

    return reference_key, fields