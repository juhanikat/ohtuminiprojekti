# ohtuminiprojekti
[![CI](https://github.com/juhanikat/ohtuminiprojekti/actions/workflows/main.yml/badge.svg)](https://github.com/juhanikat/ohtuminiprojekti/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/juhanikat/ohtuminiprojekti/graph/badge.svg?token=2MRXDOBOKW)](https://codecov.io/gh/juhanikat/ohtuminiprojekti)

Group: Fast Fishes

# Table of Contents
1. [Definition of Done](#definition-of-done)
2. [Installing and Running the Program](#installing-and-running-the-program)
    - [Download](#download)
    - [Installation](#installation)
    - [Running the Program](#running-the-program)
3. [Backlog](#backlog)
4. [File Storage and Export Details](#file-storage-and-export-details)
    - [Location of Stored References](#location-of-stored-references)
    - [Exporting References](#exporting-references)
5. [Retrospective Results](#retrospective-results)

## Definition of Done:
- Functionality has been implemented
- Functionality has been tested
- Functionality has been integrated into the rest of the program

## Installing and Running the Program

### Download

Run the following command in the terminal:
```bash
git clone git@github.com:juhanikat/ohtuminiprojekti.git
```

### Installation

Install the dependencies by running the following command in the terminal:
```bash
poetry install
```

### Running the Program
Run the program with the command:

```bash
poetry run python3 src/index.py
```
At the start of execution program automatically loads the data from the data.json file.
When the program is running, you can use it via terminal UI.
The use options are the following:
- Input a to add new reference
 - The program asks for inputs for the reference and saves it in reference manager
- Input l to view references
 - The program prints all references in the reference manager
- Input r to remove a reference
 - The program deletes a reference from the reference manager
- Input e to export references
 - The program exports all references in the reference manager to a bibtex file
- Input s to search references
 - User can input various parameters to limit the viewed references
- Input q to quit the program
 - The program saves the reference manager to the data.json file and quits.


## Backlog

[https://docs.google.com/spreadsheets/d/1t6cWLe60YoNf533Mlu33QweL5PVB-RmYKTP6vHFyb5Q/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1t6cWLe60YoNf533Mlu33QweL5PVB-RmYKTP6vHFyb5Q/edit?usp=sharing)


## Codecov

[https://app.codecov.io/gh/juhanikat/ohtuminiprojekti](https://app.codecov.io/gh/juhanikat/ohtuminiprojekti)

## File Storage and Export Details

### Location of Stored References

All inputted references are stored in a JSON file for easy access and management. You can find this file at: src/repositories/data.json

### Exporting References

Exported bibtex files are stored in the following directory: src/exports/bibtex_export.bib

## Liecense

This project is licensed under the MIT License - see the [LICENSE](https://github.com/juhanikat/ohtuminiprojekti/blob/main/LICENSE.md)

## Retrospective Results

Results of retrospectives can be found in the [retro.md](https://github.com/juhanikat/ohtuminiprojekti/blob/main/documentation/retro.md). The results are in Finnish.
