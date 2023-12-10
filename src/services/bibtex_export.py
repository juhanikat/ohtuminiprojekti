import os

from pybtex.database import BibliographyData, Entry

from entities.reference import Reference
from services.path import get_full_path
from services.reference_manager import ReferenceManager

# Pybtex Docs: https://pybtex.org/



def export_to_bibtex(reference_manager: ReferenceManager,
                     file_path: str = None, file_name: str = None,
                     overwrite: bool = False):
    """
    Create a new BibTeX file from a ReferenceManager.
    By default, new files are created in './exports/'
    and the file name is 'bibtex_export.bib'.

    Parameters:
        reference_manager (ReferenceManager): The reference manager to
        export from.
        file_path (str, optional): The path where the file is created.
        Default is './exports/'.
        file_name (str, optional): The name of the exports file.
        Default is 'bibtex_export.bib'.
        overwrite (bool, optional): Overwrite the file if it already exists.
        If set to false, duplicate files will be named 'file_name (i).bib'.
        Default is False.

    Returns:
        str: Path to created file
    """
    if file_name is None:
        file_name = "bibtex_export"

    if file_path is None:
        file_path = "./exports/"

    data = create_bibtex_string(reference_manager)

    # create a new file_name to avoid overwriting
    if not overwrite and os.path.exists(
            get_full_path(file_path, file_name) + ".bib"):
        i = 1
        while os.path.exists(
                f"{get_full_path(file_path, file_name)} ({i}).bib"):
            i += 1
        file_name += f" ({i})"

    file_name += ".bib"
    full_path = get_full_path(file_path, file_name)

    with open(full_path, "w", encoding="utf-8") as file:
        file.write(data)

    return full_path


def create_bibtex_string(reference_manager: ReferenceManager):
    """
    Create a BibTex formatted string from a ReferenceManager.

    Parameters:
        reference_manager (RerefenceManager): The reference manager to convert.

    Returns:
        str: References as a BibTex formatted string.
    """
    return create_bib_data(reference_manager).to_string("bibtex")


def create_bib_data(rm: ReferenceManager):
    bib_data = BibliographyData()
    for ref in rm.get_all_references():
        bib_data.add_entry(ref.name, reference_to_entry(ref))
    return bib_data


def reference_to_entry(ref: Reference):
    return Entry(ref.get_type(), ref.get_fields_as_tuples())
