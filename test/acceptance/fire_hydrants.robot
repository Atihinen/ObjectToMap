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
  [Teardown]  Delete If Needed  ${DESC}

Creating New Fire Hydrant Without Required Fields SHould Return 400
  ${data}=  Create Dictionary  latitude  60.2251  longitude  24.7782
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '400'
  ${data}=  Create Dictionary  category_id  0  latitude  60.2423
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '400'
  ${data}=  Create Dictionary  category_id  0  longitude  60.2423
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '400'

Deleteing Existing Fire Hydrant Should Return 200
  Create Fire Hydrant With Default Values  ${LOCATION}
  ${id}=  Get Latest Fire Hydrant Id  ${LOCATION}
  ${resp}=  Delete Fire Hydrant  ${LOCATION}  ${id}
  Verify that '${resp}' status code is '200'



*** Keywords ***

Delete If Needed
    [Arguments]  ${desc}
    Run Keyword If Test Passed  Delete Latest Fire Hydrant  ${desc}

Delete Latest Fire Hydrant
    [Arguments]  ${desc}
    ${fire_hydrant}=  Get Latest Fire Hydrant  ${LOCATION}
    Fire Hydrant '${fire_hydrant}' 'description' Should Be '${desc}'
    ${id}=  Get Latest Fire Hydrant Id  ${fire_hydrant}
    Delete Fire Hydrant  ${LOCATION}  ${id}

Create Fire Hydrant Data
    [Arguments]  ${cat_id}  ${lat}  ${long}  ${desc}  ${trunk_line}
    ${data}=  Create Dictionary  category_id  ${cat_id}  latitude  ${lat}  longitude  ${long}  description  ${desc}  trunk_line_diameter  ${trunk_line}
    [Return]  ${data}

Create Fire Hydrant Data With Valid Values
    [Arguments]  ${session}
    ${cat_id}=  Get Latest Category Id  ${session}
    ${desc}=  Generate Random String  12
    Set Test Variable  ${DESC}  ${desc}
    ${trunk_line}=  Set Variable  14
    ${data}=  Create Fire Hydrant Data  ${cat_id}  60.2251  24.7782  ${desc}  ${trunk_line}
    [Return]  ${data}

Delete Fire Hydrant
    [Arguments]  ${session}  ${id}
    ${resp}=  Delete  ${session}  /fire-hydrant/${id}/
    [Return]  ${resp}

Get Latest Category Id
    [Arguments]  ${session}
    ${categories}=  Get Categories  ${session}
    ${category}=  Get Latest Item  ${categories}
    ${id}=  Get Category Id  ${category}
    [Return]  ${id}

Get Fire Hydrants
    [Arguments]  ${session}
    ${data}=  Get  ${LOCATION}  /fire-hydrant/
    [Return]  ${data.json()}

Get Latest Fire Hydrant Id
    [Arguments]  ${session}
    ${fire_hydrant}=  Get Latest Fire Hydrant  ${session}
    ${id}=  Get Fire Hydrant Id  ${fire_hydrant}
    [Return]  ${id}

Get Latest Fire Hydrant
    [Arguments]  ${session}
    ${fire_hydrants}=  Get Fire Hydrants  ${session}
    ${fire_hydrant}=  Get Latest Item  ${fire_hydrants}
    [Return]  ${fire_hydrant}

Get Fire Hydrant Id
    [Arguments]  ${fire_hydrant}
    ${id}=  Get From Dictionary  ${fire_hydrant}  id
    [Return]  ${id}


Create New Fire Hydrant
  [Arguments]  ${session}  ${data}
  ${headers}=  Create Post Headers
  ${resp}=  Post  ${session}  /fire-hydrant/new/  data=${data}  headers=${headers}
  [Return]  ${resp}

Create Fire Hydrant With Default Values
  [Arguments]  ${session}
  ${data}=  Create Fire Hydrant Data With Valid Values  ${session}
  ${resp}=  Create New Fire Hydrant  ${session}  ${data}
  Verify that '${resp}' status code is '200'

Fire Hydrant '${fire_hydrant}' '${key}' Should Be '${value}'
  ${real_value}=  Get From Dictionary  ${fire_hydrant}  ${key}
  Should Be Equal  ${real_value}  ${value}