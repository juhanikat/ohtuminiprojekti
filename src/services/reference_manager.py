from entities.reference import Reference
from services.path import get_full_path


class ReferenceManager:
    def __init__(self):
        self.references = []
        # file path where data is saved/loaded from
        self.file_path = get_full_path()

    def new(self, name: str, fields: dict = None):
        """
        Create a new reference and add it to this manager.

        Parameters:
            name (str): Name of the new reference.
            fields (dict, optional): Attribures of the new reference.

        Returns:
            None
        """
        if fields is None:
            fields = {}
        self.add(Reference(name, fields))

    def add(self, reference: Reference):
        """
        Add an existing reference to this manager. Reference name must be new.

        Parameters:
            reference (Reference): The reference to add.

        Returns:
            None
        """
        name = reference.name
        if self.find_by_name(name) is None:
            self.references.append(reference)
        else:
            raise ValueError(f"Reference with name '{name}' already exists")

    def edit(self, name: str, field: str, value: str = None):
        """
        Edit an attribute in a reference.

        Parameters
            name (str): The name of the reference.
            field (str): The field to edit.
            value (str, optional): The value to put on the field.

        Returns:
            bool: Was specified reference found.

        """
        ref = self.find_by_name(name)
        if ref is None:
            return False
        ref.fields[field] = value
        return True

    def find_by_name(self, name: str):
        """
        Get a reference by name.

        Parameters:
            name (str): Name of the reference.

        Returns:
            Reference: If found.
            None: If not found.
        """
        for ref in self.references:
            if ref.name == name:
                return ref
        return None

    def find_by_attribute(self, field: str, value: str,
                          exact_match: bool = False):
        """
        Get all references with a specified value in a specified field.

        Parameters:
            field (str): The field to check in.
            value (str): The value to check for.
            exact_match (bool, optional): Values must be exactly equal.

        Returns:
            list: All matching references (empty if no matches).
        """
        matches = []

        for ref in filter(
                lambda ref: field in ref.fields.keys(), self.references):
            if ref.fields[field] == value:
                matches.append(ref)
            elif ref.fields[field].lower().find(value.lower()) != -1 \
                and not exact_match:
                matches.append(ref)

        return matches

    def search(self, fields: dict, exact_match: bool = False):
        """
        Search references using multiple fields.

        Parameters:
            fields (dict): Key, value pairs to search for.
            exact_match (bool, optional): Match values exactly
        Returns:
            list: All matching references (empty if no matches).
        """
        result = None

        for key, value in fields.items():
            if result is None:
                result = set(self.find_by_attribute(key, value, exact_match))
                continue
            result = result.intersection(
                set(self.find_by_attribute(key, value, exact_match)))

        return list(result) if result is not None else []

    def remove(self, name: str):
        """
        Removes the reference with this name.

        Parameters:
            name (str): Name of the Reference.

        Returns:
            bool: Was specified reference found and removed.
        """
        for i, ref in enumerate(self.references):
            if ref.name == name:
                self.references.pop(i)
                return True
        return False

    def get_all_references(self):
        """
        Get a list with all references in this manager.

        Returns:
            list: References in this manager.
        """
        return self.references

    def get_all_fields(self):
        """
        Get a list containing all fields found in the references
        of this manager.
        Fields are returned sorted.

        Returns:
            list: Fields in the references of this manager.
        """
        fields = set()

        for ref in self.references:
            for field in ref.fields.keys():
                fields.add(field)

        return sorted(fields)
