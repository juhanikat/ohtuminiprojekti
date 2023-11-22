from entities.reference import Reference

class ReferenceManager:
    def __init__(self):
        self.references = list()
    
    def New(self, name: str, fields: dict = dict()):
        """
        Create a new reference and add it to this manager.

        Parameters:
            name (str): Name of the new reference.
            fields (dict, optional): Attribures of the new reference.
        
        Returns:
            None
        """
        self.Add(Reference(name, fields))

    def Add(self, reference: Reference):
        """
        Add an existing reference to this manager. Reference name must be new.

        Parameters:
            reference (Reference): The reference to add.
        
        Returns:
            None
        """
        name = reference.name
        if self.FindByName(name) == None:
            self.references.append(reference)
        else:
            raise BaseException(f"Reference with name '{name}' already exists")
    
    def Edit(self, name: str, field: str, value = None):
        """
        Edit an attribute in a reference.

        Parameters
            name (str): The name of the reference.
            field (str): The field to edit.
            value (any, optional): The value to put on the field.

        Returns:
            bool: Was specified reference found.
        
        """
        ref = self.FindByName(name)
        if ref == None:
            return False
        ref.fields[field] = value
        return True
    
    def FindByName(self, name: str):
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

    def FindByAttribute(self, field: str, value):
        """
        Get all references with a specified value in a specified field.

        Parameters:
            field (str): The field to check in.
            value (Any): The value to check for.

        Returns:
            list: All matching references (empty if no matches).
        """
        matches = []

        for ref in self.references:
            if field in ref.fields.keys():
                if ref.fields[field] == value:
                    matches.append(ref)
        
        return matches

    def Remove(self, name: str):
        """
        Removes the reference with this name.

        Parameters:
            name (str): Name of the Reference.
        
        Returns:
            bool: Was specified reference found and removed.
        """
        for i in range(len(self.references)):
            if self.reference.name == name:
                self.references.remove(i)
                return True
        return False

    def GetAllReferences(self):
        """
        Get a list with all references in this manager.

        Returns:
            list: References in this manager.
        """
        return self.references