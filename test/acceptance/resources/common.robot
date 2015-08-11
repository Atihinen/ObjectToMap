*** Keywords ***
Verify that '${resp}' status code is '${error_code}'
  ${error_code}=  Convert To Integer  ${error_code}
  Should Be Equal As Strings  ${resp.status_code}  ${error_code}

Get Categories
  [Arguments]  ${session}
  ${data}=  Get  ${session}  /category/
  [Return]  ${data.json()}

Get Latest Item
  [Arguments]  ${data}
  [Return]  ${data[-1]}

Get Category Id
  [Arguments]  ${category}
  ${id}=  Get From Dictionary  ${category}  id
  [Return]  ${id}

Create Post Headers
  ${headers}=  Create Dictionary  Content-Type  application/x-www-form-urlencoded
  [Return]  ${headers}