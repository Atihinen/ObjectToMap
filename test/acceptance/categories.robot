*** Settings ***
Library  Collections
Library  RequestsLibrary
Suite Setup  Create Session  ${LOCATION}  http://${SERVER}


*** Test Cases ***

Create new category with default values
  ${resp}=  Create New Category With Default Values  ${LOCATION}
  Verify that '${resp}' Status Code Is '200'

*** Keywords ***
Create New Category With Default Values
  [Arguments]  ${session}
  ${data}=  Create Dictionary  name  My cat
  ${resp}=  Create New Category  ${session}  ${data}
  [Return]  ${resp}

Create New Category
  [Arguments]  ${session}  ${data}
  ${headers}=  Create Post Headers
  ${resp}=  Post  ${session}  /category/new  data=${data}  headers=${headers}
  [Return]  ${resp}

Create Post Headers
  ${headers}=  Create Dictionary  Content-Type  application/x-www-form-urlencoded
  [Return]  ${headers}

Verify that '${resp}' status code is '${error_code}'
  ${error_code}=  Convert To Integer  ${error_code}
  Should Be Equal As Strings  ${resp.status_code}  ${error_code}