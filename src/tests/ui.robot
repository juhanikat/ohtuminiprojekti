*** Settings ***
Resource  resource.robot

*** Test Cases ***
Input Invalid Command
    Ask For Input
    Input  abc
    Output Should Contain  Invalid input

Input Listing Command When No References
    Input  l
    Ask For Input
    Output Should Not Contain  Invalid input

Input Listing Command When References
    Create Test Reference
    Input  l
    Ask For Input
    Output Should Contain  | test | article | hello | 1991 |

Input Remove When Reference Exists
    Create Test Reference
    Input  r
    Ask For Input
    ${reference_removed}=  Remove Reference  test
    Run Keyword If  '${reference_removed}' == 'PASS'
    ...  Output Should Contain  Removed reference with name: test
    ...  Output Should Not Contain  Reference with name 'test' not found

Input Remove When Reference Does Not Exist
    Input  r
    Ask For Input
    ${reference_removed}=  Remove Reference  test
    Run Keyword If  '${reference_removed}' == 'FAIL'
    ...  Output Should Contain  Reference with name 'test' not found
    ...  Output Should Not Contain  Removed reference with name: test
