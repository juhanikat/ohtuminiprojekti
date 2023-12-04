*** Settings ***
Library           OperatingSystem

*** Test Cases ***
Test Program Output on Quit
    ${output}=    Run    python ./src/interact_with_index.py
    Should Contain    ${output}    Input a to add a new reference
    Should Contain    ${output}    Input l to list all references
    Should Contain    ${output}    Input e to export references as a .bib file
    Should Contain    ${output}    Input q to exit

Test Program Output on Add Reference
    ${output}=    Run    python ./src/interact_with_index.py a
    Should Contain    ${output}    Choose the entry type (Enter empty to abort):