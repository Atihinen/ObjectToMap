*** Settings ***
Library  Collections
Library  RequestsLibrary
Library  String
Suite Setup  Create Session  ${LOCATION}  http://${SERVER}


*** Test Cases ***

Create new category with default values should return 200
  ${resp}=  Create New Category With Default Values  ${LOCATION}
  Verify that '${resp}' Status Code Is '200'
  [Teardown]  Run Keyword If Test Passed  Delete If Needed

Creating new category with invalid values should return 406
  ${too_long}=  Generate Random String  51
  ${data}=  Create Category Data  ${too_long}
  ${resp}=  Create New Category  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'
  ${data}=  Create Category Data  ${EMPTY}
  ${resp}=  Create New Category  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'

Deleting existing category should return 200
  ${data}=  Create Dictionary  name  Delete Me
  ${resp}=  Create New Category  ${LOCATION}  ${data}
  Verify that '${resp}' Status Code Is '200'
  ${categories}=  Get Categories  ${LOCATION}
  ${category}=  Get Latest Item  ${categories}
  Verify That Category Contains Correct Values  ${category}  Delete Me
  ${id}=  Get Category Id  ${category}
  ${resp}=  Delete Category  ${id}  ${LOCATION}
  Verify that '${resp}' Status Code Is '200'

Deleting not existing category should return 404
  ${resp}=  Delete Category  0  ${LOCATION}
  Verify that '${resp}' status code is '404'

Deleting category with faulty id should return 406
  ${resp}=  Delete Category  asdsa  ${LOCATION}
  Verify that '${resp}' status code is '406'

Get Existing Category Should Return Correct Data
  ${data}=  Create Category Data  category 1
  ${resp}=  Create New Category  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '200'
  ${categories}=  Get Categories  ${LOCATION}
  ${category}=  Get Latest Item  ${categories}
  ${id}=  Get Category Id  ${category}
  ${resp}  ${category}=  Get Category  ${LOCATION}  ${id}
  Verify That Category Contains Correct Values  ${category}  category 1
  [Teardown]  Run Keyword If Test Passed  Delete If Needed  category 1

Fetching Not Existing Category Should Return 404
  ${resp}  ${category}=  Get Category  ${LOCATION}  0
  Verify that '${resp}' status code is '404'

Fetching Category With Invalid Id Should Return 406
  ${resp}  ${category}=  Get Category  ${LOCATION}  asdsas
  Verify that '${resp}' status code is '406'

Updating Category With Valid Values Should Return 200
  ${data}=  Create Category Data  update_category
  ${resp}=  Create New Category  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '200'
  ${categories}=  Get Categories  ${LOCATION}
  ${category}=  Get Latest Item  ${categories}
  ${id}=  Get Category Id  ${category}
  ${resp}  ${category}=  Get Category  ${LOCATION}  ${id}
  Verify That Category Contains Correct Values  ${category}  update_category
  ${data}=  Create Category Data  updated_category
  ${resp}=  Update Category  ${id}  ${data}  ${LOCATION}
  Verify that '${resp}' status code is '200'
  ${resp}  ${category}=  Get Category  ${LOCATION}  ${id}
  Verify That Category Contains Correct Values  ${category}  updated_category
  [Teardown]  Run Keyword If Test Passed  Delete If Needed  updated_category


*** Keywords ***
Get Categories
  [Arguments]  ${session}
  ${data}=  Get  ${session}  /category/
  [Return]  ${data.json()}

Get Latest Item
  [Arguments]  ${data}
  [Return]  ${data[-1]}

Get Category
  [Arguments]  ${session}  ${id}
  ${data}=  Get  ${session}  /category/${id}/
  [Return]  ${data}  ${data.json()}

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

Create Category Data
  [Arguments]  ${name}
  ${data}=  Create Dictionary  name  ${name}
  [Return]  ${data}

Create Post Headers
  ${headers}=  Create Dictionary  Content-Type  application/x-www-form-urlencoded
  [Return]  ${headers}

Verify that '${resp}' status code is '${error_code}'
  ${error_code}=  Convert To Integer  ${error_code}
  Should Be Equal As Strings  ${resp.status_code}  ${error_code}

Delete Category
  [Arguments]  ${id}  ${session}
  ${resp}=  Delete  ${session}  /category/${id}/
  [Return]  ${resp}

Category '${category}' '${key}' should be '${value}'
  ${real_value}=  Get From Dictionary  ${category}  ${key}
  Should Be Equal  ${value}  ${real_value}

Verify That Category Contains Correct Values
  [Arguments]  ${category}  ${name}
  Category '${category}' 'name' should be '${name}'

Get Category Id
  [Arguments]  ${category}
  ${id}=  Get From Dictionary  ${category}  id
  [Return]  ${id}

Delete If Needed
  [Arguments]  ${name}=My cat
  ${categories}=  Get Categories  ${LOCATION}
  ${category}=  Get Latest Item  ${categories}
  Verify That Category Contains Correct Values  ${category}  ${name}
  ${id}=  Get Category Id  ${category}
  Delete Category  ${id}  ${LOCATION}
  Verify that '${resp}' Status Code Is '200'

Update Category
  [Arguments]  ${id}  ${data}  ${session}
  ${headers}=  Create Post Headers
  ${resp}=  Put  ${session}  /category/${id}/  data=${data}  headers=${headers}
  [Return]  ${resp}
