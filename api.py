from bottle import Bottle, response, request, run, route, HTTPResponse
import json
import traceback
from lib.db import engine, plugin, sqlalchemy, db
from models import Category
from sqlalchemy.orm import Session


app = Bottle()
session = Session(engine)

app.install(plugin)

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

@route('/category/new', method="POST")
def new_category():
    if "name" in request.forms:
        name = request.forms.get('name')
        c = Category(name)
        if not c.validate():
            print "Validated"
            try:
                session.add(c)
                session.commit()
                return HTTPResponse(status=200)
            except Exception as err:
                traceback.print_exc()
                return HTTPResponse(status=500)
        return HTTPResponse(status=406)
    return HTTPResponse(status=400)



if __name__ == "__main__":
    run(host='127.0.0.1', port=8080)
