from bottle import Bottle, response, request, run, route, HTTPResponse, hook
import json
import traceback
from lib.db import engine, plugin, sqlalchemy, db
from models import Category
from utils.formatter import convert_to_integer
from utils.validator import ErrorMessages


app = Bottle()

app.install(plugin)

def set_cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
    response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
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

@route('/category/<id>/', method="DELETE")
def delete_category(id):
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

@route('/category/<id>/', method="PUT")
def update_category(id):
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406)
    if not "name" in request.forms:
        return setHTTPResponse(status=400)
    name = request.forms.get("name")
    c = db.query(Category).get(id)
    c.name = name
    if not c.validate():
        try:
            db.commit()
            return HTTPResponse(staus=200)
        except Exception as err:
            traceback.print_exc()
            return setHTTPResponse(status=500)
    return setHTTPResponse(status=406)



@route('/category/new', method=['OPTIONS', 'POST'])
def new_category():
    if "name" in request.forms:
        name = request.forms.get('name')
        _name = db.query(Category).filter_by(name=name).first()
        if _name:
            return setHTTPResponse(status=409)
        c = Category(name)
        if not c.validate():
            try:
                db.add(c)
                db.commit()
                return setHTTPResponse(status=200)

            except Exception as err:
                traceback.print_exc()
                return setHTTPResponse(status=500)
        return setHTTPResponse(status=406)
    return setHTTPResponse(status=400)

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
