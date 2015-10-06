# -*- coding: utf-8 -*-
from bottle import Bottle, response, request, run, route, HTTPResponse, hook, static_file
import json
import traceback
from lib.db import engine, plugin, sqlalchemy, db
from models import Category, FireHydrant
from utils.formatter import convert_to_integer
from utils.validator import ErrorMessages
from utils.writer import CSVWriter
import sys
import os

app = Bottle()

app.install(plugin)
required_values = ["category_id", "latitude", "longitude"]
csv_file = None
def set_cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

@hook('after_request')
def delete_csv():
    global csv_file
    if csv_file:
        try:
            os.remove(csv_file)
        except:
            pass
        finally:
            csv_file = None

@route('/', method="GET")
def index():
    _path = os.path.join('.','views')
    print _path
    return static_file("api.html", root=_path)

@route('/v1/category/', method=['OPTIONS', 'GET'])
def get_categories():
    data = []
    _categories = db.query(Category).all()
    for category in _categories:
        data.append(category.get_data())
    response.content_type = "application/json"
    json_val = json.dumps(data)
    return json_val

@route('/v1/category/<id>/', method="GET")
def get_category(id):
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406, body={})
    c = db.query(Category).get(id)
    if not c:
        return setHTTPResponse(status=404, body={})
    response.content_type = "application/json"
    return c.to_json()

@route('/v1/category/<id>/', method=['OPTIONS', 'DELETE'])
def delete_category(id):
    if request.method == 'OPTIONS':
        return setHTTPResponse(status=200)
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406)
    c = db.query(Category).get(id)
    _fire_hydrants = db.query(FireHydrant).filter_by(category_id=id)
    if _fire_hydrants:
        for fh in _fire_hydrants:
            try:
                db.delete(fh)
                db.commit()
            except:
                db.rollback()
                traceback.print_exc()
                return setHTTPResponse(500, body={"msg": "CHILD_FAILED"})

    if not c:
        return setHTTPResponse(status=404)
    try:
        db.delete(c)
        db.commit()
        return setHTTPResponse(status=200)
    except:
        db.rollback()
        traceback.print_exc()
        return setHTTPResponse(status=500)

@route('/v1/category/<id>/', method=['OPTIONS', 'PUT'])
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
            db.rollback()
            traceback.print_exc()
            return setHTTPResponse(status=500)
    return setHTTPResponse(status=406, body=json.dumps(c.validate()))



@route('/v1/category/new', method=['OPTIONS', 'POST'])
def new_category():
    if "name" in request.forms:
        name = request.forms.getunicode('name')
        print type(name)
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
                db.rollback()
                traceback.print_exc()
                return setHTTPResponse(status=500)
        return setHTTPResponse(status=406, body=json.dumps(c.validate()))
    return setHTTPResponse(status=400)

@route('/fire-hydrant/', method=["OPTIONS","GET"])
def get_fire_hydrants():
    if request.method == "OPTIONS":
        return setHTTPResponse(status=200)
    db.flush()
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
        return setHTTPResponse(status=400, body=json.dumps({'msg': 'REQUIRED_VALUES'}))
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
    #Store previous values
    _cat_id= fh.category_id
    _lat = fh.latitude
    _long = fh.longitude
    _desc = fh.description
    _trunk_line = fh.trunk_line_diameter
    #Update with new values
    fh.category_id = cat_id
    fh.description = description
    fh.latitude = lat
    fh.longitude = long
    fh.trunk_line_diameter = trunk_line
    errs = fh.validate()
    if errs:
        #Restore previuous values
        fh.category_id = _cat_id
        fh.latitude = _lat
        fh.longitude = _long
        fh.description = _desc
        fh.trunk_line_diameter = _trunk_line
        return setHTTPResponse(status=406, body=errs)
    else:
        try:
            db.commit()
            return setHTTPResponse(status=200)
        except:
            db.rollback()
            traceback.print_exc()
            return setHTTPResponse(status=500)

@route('/fire-hydrant/<id>/', method=['OPTIONS', 'GET'])
def get_fire_hydrant(id):
    if request.method == "OPTIONS":
        return setHTTPResponse(status=200)
    id = convert_to_integer(id)
    if id == ErrorMessages.NOT_NUMBER:
        return setHTTPResponse(status=406, body=json.dumps({'id': 'NOT_NUMBER'}))
    fh = db.query(FireHydrant).get(id)
    if not fh:
        return setHTTPResponse(status=404, body=json.dumps({'msg': 'NOT_FOUND'}))
    return fh.to_json()

@route('/fire-hydrant/csv', method=['OPTIONS', 'GET'])
def get_fire_hydrant_csv():
    global csv_file
    fire_hydrants = db.query(FireHydrant).all()
    rows = []
    #first line
    rows.append(["Id", "Lat", "Lon", "Name", "Note", "Text"])
    for fire_hydrant in fire_hydrants:
        rows.append([
            fire_hydrant.id,
            fire_hydrant.latitude,
            fire_hydrant.longitude,
            fire_hydrant.get_category_name().encode('utf-8'),
            fire_hydrant.description,
            fire_hydrant.trunk_line_diameter
        ])
        print type(fire_hydrant.get_category_name())
    csvw = CSVWriter()
    _file, _path = csvw.write_csv(rows)
    csv_file = _path
    return static_file(_file, root=os.path.join(os.sep, "tmp"))



def setHTTPResponse(status, body=None):
    response = None
    if body != None:
        response = HTTPResponse(status=status, body=body)
    else:
        response = HTTPResponse(status=status)
    set_cors(response)
    return response



if __name__ == "__main__":
    port = 8080
    ip = '0.0.0.0'
    try:
        port = sys.argv[1]
    except:
        pass
    try:
        ip = sys.argv[2]
    except:
        pass
    run(host=ip, port=port)
