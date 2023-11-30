*** Settings ***
Resource  resource.robot

*** Test Cases ***

Input Invalid Command
    Ask For Input
    Input  abc
    Output Should Contain  Invalid input

Input Listing Command
    Input  l
    Ask For Input
    Output Should Not Contain  Invalid input