"""
Contains common information on bibtex entries
"""

REQUIRED_FIELDS = {
    "article": ["title", "year", "author", "journal"],
    "book": ["title", "year", "author", "publisher"],
    "booklet": ["title"],
    "conference": ["title", "year", "author", "booktitle"],
    "inbook": ["title", "year", "author", "chapter", "pages", "publisher"],
    "incollection": ["title", "year", "author", "booktitle", "publisher"],
    "inproceedings": ["title", "year", "author", "booktitle"],
    "manual": ["title"],
    "mastersthesis": ["title", "year", "author", "school"],
    "misc": [],
    "phdthesis": ["title", "year", "author", "school"],
    "proceedings": ["title", "year"],
    "techreport": ["title", "year", "author", "institution"],
    "unpublished": ["title", "author", "note"]
}
