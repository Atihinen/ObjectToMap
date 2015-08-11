*** Settings ***
Library  Collections
Library  RequestsLibrary
Library  String
Resource  resources/common.robot
Suite Setup  Create Session  ${LOCATION}  http://${SERVER}

*** Test Cases ***

Getting Fire Hydrants Should Return 200
  ${resp}=  Get  ${LOCATION}  /fire-hydrant/
  Verify that '${resp}' status code is '200'

Creating New Fire Hydrant With Valid Values Should Return 200
  ${data}=  Create Fire Hydrant Data With Valid Values  ${LOCATION}
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '200'

*** Keywords ***
Create Fire Hydrant Data
    [Arguments]  ${cat_id}  ${lat}  ${long}  ${desc}  ${trunk_line}
    ${data}=  Create Dictionary  category_id  ${cat_id}  latitude  ${lat}  longitude  ${long}  description  ${desc}  trunk_line_diameter  ${trunk_line}
    [Return]  ${data}

Create Fire Hydrant Data With Valid Values
    [Arguments]  ${session}
    ${cat_id}=  Get Latest Category Id  ${session}
    ${desc}=  Generate Random String  12
    ${trunk_line}=  Set Variable  14
    ${data}=  Create Fire Hydrant Data  ${cat_id}  60.2251  24.7782  ${desc}  ${trunk_line}
    [Return]  ${data}


Get Latest Category Id
    [Arguments]  ${session}
    ${categories}=  Get Categories  ${session}
    ${category}=  Get Latest Item  ${categories}
    ${id}=  Get Category Id  ${category}
    [Return]  ${id}

Create New Fire Hydrant
  [Arguments]  ${session}  ${data}
  ${headers}=  Create Post Headers
  ${resp}=  Post  ${session}  /fire-hydrant/new/  data=${data}  headers=${headers}
  [Return]  ${resp}