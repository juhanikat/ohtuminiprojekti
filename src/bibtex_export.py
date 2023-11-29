import os
from pybtex.database import BibliographyData, Entry
# Docs: https://pybtex.org/
from services.reference_manager import ReferenceManager
from services.path import get_full_path
from entities.reference import Reference


def export_to_bibtex(reference_manager: ReferenceManager,
                     file_path: str = None, file_name: str = None,
                     overwrite: bool = False):
    """
    Create a new BibTeX file from a ReferenceManager.
    By defualt, new files are created in './exports/'
    and the file name is 'bibtex_export.bib'.

    Parameters:
        reference_manager (ReferenceManager): The refrence manager to
        export from.
        file_path (str, optional): The path where the file is created.
        Default is './exports/'.
        file_name (str, optional): The name of the exports file.
        Default is 'bibtex_export.bib'.
        overwrite (bool, optional): Overwrite the file if it already exists.
        If set to false, duplicate files will be named 'file_name (i).bib'.
        Default is False.

    Returns:
        None
    """
    if file_name is None:
        file_name = "bibtex_export"

    if file_path is None:
        file_path = "./exports/"

    data = create_bib_data(reference_manager).to_string("bibtex")

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


def create_bib_data(rm: ReferenceManager):
    bib_data = BibliographyData()
    for ref in rm.get_all_references():
        bib_data.add_entry(ref.name, reference_to_entry(ref))
    return bib_data


def reference_to_entry(ref: Reference):
    return Entry(ref.get_type(), ref.get_fields_as_tuples())
