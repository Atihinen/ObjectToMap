from bottle import Bottle, response, request, run, route, HTTPResponse, hook
import json
import traceback
from lib.db import engine, plugin, sqlalchemy, db
from models import Category, FireHydrant
from utils.formatter import convert_to_integer
from utils.validator import ErrorMessages


app = Bottle()

app.install(plugin)

required_values = ["category_id", "latitude", "longitude"]

def set_cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

@route('/', method="GET")
def index():
    _entities = db.query(Entity).all()
    data = []
    for entity in _entities:
        cont = {
            'name': entity.name
        }
        data.append(cont)
    json_val = json.dumps(data)
    response.content_type = "application/json"
    return json_val

@route('/category/', method=['OPTIONS', 'GET'])
def get_categories():
    data = []
    _categories = db.query(Category).all()
    for category in _categories:
        data.append(category.get_data())
    response.content_type = "application/json"
    json_val = json.dumps(data)
    return json_val

@route('/category/<id>/', method="GET")
def get_category(id):
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406, body={})
    c = db.query(Category).get(id)
    if not c:
        return setHTTPResponse(status=404, body={})
    response.content_type = "application/json"
    return c.to_json()

@route('/category/<id>/', method=['OPTIONS', 'DELETE'])
def delete_category(id):
    if request.method == 'OPTIONS':
        return setHTTPResponse(status=200)
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406)
    c = db.query(Category).get(id)
    if not c:
        return setHTTPResponse(status=404)
    try:
        db.delete(c)
        db.commit()
        return setHTTPResponse(status=200)
    except:
        print "Something went wrong"
        traceback.print_exc()
        return setHTTPResponse(status=500)

@route('/category/<id>/', method=['OPTIONS', 'PUT'])
def update_category(id):
    if request.method == 'OPTIONS':
        return setHTTPResponse(status=200)
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406, body=json.dumps({'id': 'NOT_NUMBER'}))
    if not "name" in request.forms:
        return setHTTPResponse(status=400)
    name = request.forms.get("name")
    _name = db.query(Category).filter_by(name=name).first()
    if _name:
        return setHTTPResponse(status=409, body=json.dumps({'name': 'DUBLICATE'}))
    c = db.query(Category).get(id)
    c.name = name
    if not c.validate():
        try:
            db.commit()
            return setHTTPResponse(status=200)
        except Exception as err:
            traceback.print_exc()
            return setHTTPResponse(status=500)
    return setHTTPResponse(status=406, body=json.dumps(c.validate()))



@route('/category/new', method=['OPTIONS', 'POST'])
def new_category():
    if "name" in request.forms:
        name = request.forms.get('name')
        _name = db.query(Category).filter_by(name=name).first()
        if _name:
            return setHTTPResponse(status=409, body=json.dumps({"name": "DUBLICATE"}))
        c = Category(name)
        if not c.validate():
            try:
                db.add(c)
                db.commit()
                return setHTTPResponse(status=200)

            except Exception as err:
                traceback.print_exc()
                return setHTTPResponse(status=500)
        return setHTTPResponse(status=406, body=json.dumps(c.validate()))
    return setHTTPResponse(status=400)

@route('/fire-hydrant/', method=["OPTIONS","GET"])
def get_fire_hydrants():
    if request.method == "OPTIONS":
        return setHTTPResponse(status=200)
    _fire_hydrants = db.query(FireHydrant).all()
    data = []
    for fh in _fire_hydrants:
        data.append(fh.get_data())
    return json.dumps(data)

@route('/fire-hydrant/new/', method=["OPTIONS", "POST"])
def new_fire_hydrant():
    if request.method == "OPTIONS":
        return setHTTPResponse(status=200)
    req_flag = False
    for req in required_values:
        if not req in request.forms:
            req_flag = True
    if req_flag:
        return setHTTPResponse(status=400)
    cat_id = request.forms.get('category_id')
    lat = request.forms.get('latitude')
    long = request.forms.get('longitude')
    description = ""
    try:
        description = request.forms.get('description')
    except:
        pass
    trunk_line = ""
    try:
        trunk_line = request.forms.get('trunk_line_diameter')
    except:
        pass
    fh = FireHydrant(description, trunk_line, cat_id, lat, long)
    errs = fh.validate()
    if errs:
        return setHTTPResponse(status=406, body=errs)
    try:
        db.add(fh)
        db.commit()
        return setHTTPResponse(200)
    except:
        db.rollback()
        traceback.print_exc()
        return setHTTPResponse(status=500)

@route('/fire-hydrant/<id>/', method=["OPTIONS", "DELETE"])
def delete_fire_hydrant(id):
    if request.method == "OPTIONS":
        return setHTTPResponse(status=200)
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406)
    fh = db.query(FireHydrant).get(id)
    if not fh:
        return setHTTPResponse(status=404)
    try:
        db.delete(fh)
        db.commit()
        return setHTTPResponse(status=200)
    except Exception:
        db.rollback()
        traceback.print_exc()
        return setHTTPResponse(status=500)

@route('/fire-hydrant/<id>/', method=["OPTIONS", "PUT"])
def update_fire_hydrant(id):
    if request.method == "OPTIONS":
        return setHTTPResponse(status=200)
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406, body=json.dumps({'id': 'NOT_NUMBER'}))
    req_flag = False
    for req in required_values:
        if not req in request.forms:
            req_flag = True
    if req_flag:
        return setHTTPResponse(status=400)
    cat_id = request.forms.get('category_id')
    lat = request.forms.get('latitude')
    long = request.forms.get('longitude')
    description = ""
    try:
        description = request.forms.get('description')
    except:
        pass
    trunk_line = ""
    try:
        trunk_line = request.forms.get('trunk_line_diameter')
    except:
        pass
    fh = db.query(FireHydrant).get(id)
    if not fh:
        return setHTTPResponse(status=404)
    fh.category_id = cat_id
    fh.description = description
    fh.latitude = lat
    fh.longitude = long
    fh.trunk_line_diameter = trunk_line
    errs = fh.validate()
    if errs:
        return setHTTPResponse(status=406, body=errs)
    try:
        db.commit()
        return setHTTPResponse(status=200)
    except:
        traceback.print_exc()
        db.rollback()
        return setHTTPResponse(status=500)



def setHTTPResponse(status, body=None):
    response = None
    if body != None:
        response = HTTPResponse(status=status, body=body)
    else:
        response = HTTPResponse(status=status)
    set_cors(response)
    return response



if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
