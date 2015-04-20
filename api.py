from bottle import Bottle, response, run, route
import json
from lib.db import engine, plugin, sqlalchemy, db
from models import Entity


app = Bottle()


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

if __name__ == "__main__":
    run(host='127.0.0.1', port=8080)
