*** Settings ***
Library  Collections
Library  RequestsLibrary
Library  String
Resource  resources/common.robot
Suite Setup  Create Session  ${LOCATION}  http://${SERVER}

*** Test Cases ***

Getting Fire Hydrants Should Return 200
  ${resp}=  Get  ${LOCATION}  /fire-hydrants
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

Creating New Fire Hydrant With Invalid Category Id Should Return 406
  ${desc}=  Generate Random String  12
  ${data}=  Create Fire Hydrant Data  aasd  60.25  24.7  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'
  ${data}=  Create Fire Hydrant Data  0  60.25  24.7  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'
  ${data}=  Create Fire Hydrant Data  ${EMPTY}  60.25  24.7  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'

Creating New Fire Hydrant With Invalid Latitude Should Return 406
  ${desc}=  Generate Random String  12
  ${cat_id}=  Get Latest Category Id  ${LOCATION}
  ${data}=  Create Fire Hydrant Data  ${cat_id}  asd  24.7  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'
  ${data}=  Create Fire Hydrant Data  ${cat_id}  ${EMPTY}  24.7  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'

Creating New Fire Hydrant With Invalid Longitude Should Return 406
  ${desc}=  Generate Random String  12
  ${cat_id}=  Get Latest Category Id  ${LOCATION}
  ${data}=  Create Fire Hydrant Data  ${cat_id}  60.24  asd  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'
  ${data}=  Create Fire Hydrant Data  ${cat_id}  60.25  ${EMPTY}  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'

Creating New Fire Hydrant With Invalid Description Should Return 406
  ${desc}=  Generate Random String  51
  ${cat_id}=  Get Latest Category Id  ${LOCATION}
  ${data}=  Create Fire Hydrant Data  ${cat_id}  60.24  24.5  ${desc}  14
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'

Creating New Fire Hydrant With Invalid Trunk Line Diameter Should Return 406
  ${desc}=  Generate Random String  12
  ${trunk_line}=  Generate Random String  51
  ${cat_id}=  Get Latest Category Id  ${LOCATION}
  ${data}=  Create Fire Hydrant Data  ${cat_id}  60.24  24.5  ${desc}  ${trunk_line}
  ${resp}=  Create New Fire Hydrant  ${LOCATION}  ${data}
  Verify that '${resp}' status code is '406'

Deleteing Existing Fire Hydrant Should Return 200
  Create Fire Hydrant With Default Values  ${LOCATION}
  ${id}=  Get Latest Fire Hydrant Id  ${LOCATION}
  ${resp}=  Delete Fire Hydrant  ${LOCATION}  ${id}
  Verify that '${resp}' status code is '200'

Deleting Not Existing Fire Hydrant Should Return 404
  ${resp}=  Delete Fire Hydrant  ${LOCATION}  0
  Verify that '${resp}' status code is '404'

Deleting Fire Hydrant With Invalid Id Should Return 406
  ${resp}=  Delete Fire Hydrant  ${LOCATION}  asd
  Verify that '${resp}' status code is '406'

Get Fire Hydrant By Id Should Return 200 And Correct Values
  Create Fire Hydrant With Default Values  ${LOCATION}
  ${id}=  Get Latest Fire Hydrant Id  ${LOCATION}
  ${cat_id}=  Get Latest Category Id  ${LOCATION}
  ${resp}  ${fire_hydrant}=  Get Fire Hydrant  ${LOCATION}  ${id}
  Verify that '${resp}' status code is '200'
  Verify Fire Hydrant Data  ${fire_hydrant}  ${cat_id}  60.2251  24.7782  ${DESC}  14
  [Teardown]  Delete If Needed  ${DESC}

Get Fire Hydrant With Invalid Id Should Return 406
  ${resp}  ${fire_hydrant}=  Get Fire Hydrant  ${LOCATION}  asd
  Verify that '${resp}' status code is '406'

Get Fire Hydrant With Not Existing Id Should Return 404
  ${resp}  ${fire_hydrant}=  Get Fire Hydrant  ${LOCATION}  0
  Verify that '${resp}' status code is '404'

Updating Fire Hydrant With Valid Data Should Return 200
  Create Fire Hydrant With Default Values  ${LOCATION}
  ${id}=  Get Latest Fire Hydrant Id  ${LOCATION}
  ${cat_id}=  Get Latest Category Id  ${LOCATION}
  ${desc}=  Generate Random String  14
  ${data}=  Create Fire Hydrant Data  ${cat_id}  63.2  24.7  ${desc}  15
  ${resp}=  Update Fire Hydrant  ${LOCATION}  ${id}  ${data}
  Verify that '${resp}' status code is '200'
  ${resp}  ${fire_hydrant}=  Get Fire Hydrant  ${LOCATION}  ${id}
  Verify that '${resp}' status code is '200'
  Verify Fire Hydrant Data  ${fire_hydrant}  ${cat_id}  63.2  24.7  ${desc}  15
  [Teardown]  Delete If Needed  ${desc}

Updating Fire Hydrant With Invalid Id Should Return 406
  ${data}=  Create Fire Hydrant Data With Valid Values  ${LOCATION}
  ${resp}=  Update Fire Hydrant  ${LOCATION}  asd  ${data}
  Verify that '${resp}' status code is '406'

Updating Fire Hydrant Without Existing Id Should Return 404
  ${data}=  Create Fire Hydrant Data With Valid Values  ${LOCATION}
  ${resp}=  Update Fire Hydrant  ${LOCATION}  0  ${data}

Updating Fire Hydrant With Invalid Data Should Return 406
  Create Fire Hydrant With Default Values  ${LOCATION}
  ${id}=  Get Latest Fire Hydrant Id  ${LOCATION}
  ${invalid_str}=  Generate Random String  51
  ${data}=  Create Fire Hydrant Data  asd  ${EMPTY}  ${EMPTY}  ${invalid_str}  ${invalid_str}
  ${resp}=  Update Fire Hydrant  ${LOCATION}  ${id}  ${data}
  Verify that '${resp}' status code is '406'
  [Teardown]  Delete If Needed  ${DESC}

Updating Fire Hydrant Without Required Values Should Return 400
  Create Fire Hydrant With Default Values  ${LOCATION}
  ${id}=  Get Latest Fire Hydrant Id  ${LOCATION}
  ${data}=  Create Dictionary  description  asda
  ${resp}=  Update Fire Hydrant  ${LOCATION}  ${id}  ${data}
  Verify that '${resp}' status code is '400'
  [Teardown]  Delete If Needed  ${DESC}

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
    ${data}=  Get  ${LOCATION}  /fire-hydrants
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
  Should Be Equal As Strings  ${real_value}  ${value}

Update Fire Hydrant
  [Arguments]  ${session}  ${id}  ${data}
  ${headers}=  Create Post Headers
  ${resp}=  Put  ${session}  /fire-hydrant/${id}/  data=${data}  headers=${headers}
  [Return]  ${resp}

Verify Fire Hydrant Data
  [Arguments]  ${fire_hydrant}  ${cat_id}  ${lat}  ${long}  ${desc}  ${trunk_line}
  ${category}=  Get From Dictionary  ${fire_hydrant}  category
  ${real_cat_id}=  Get From Dictionary  ${category}  id
  Should Be Equal  ${real_cat_id}  ${cat_id}
  Fire Hydrant '${fire_hydrant}' 'latitude' Should Be '${lat}'
  Fire Hydrant '${fire_hydrant}' 'longitude' Should Be '${long}'
  Fire Hydrant '${fire_hydrant}' 'description' Should Be '${desc}'
  Fire Hydrant '${fire_hydrant}' 'trunk_line_diameter' Should Be '${trunk_line}'

Get Fire Hydrant
  [Arguments]  ${session}  ${id}
  ${data}=  Get  ${session}  /fire-hydrant/${id}/
  [Return]  ${data}  ${data.json()}