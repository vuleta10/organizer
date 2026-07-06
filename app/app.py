import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

from app.swagger import api

from app.routes.users import users_ns
from app.routes.tasks import tasks_ns

from app.database import create_tables


app = Flask(__name__)


@app.route("/")
def home():

    return {
        "application": "Organizer API",
        "version": "1.0",
        "swagger": "/swagger.html"
    }


api.init_app(app)

api.add_namespace(users_ns)
api.add_namespace(tasks_ns)

create_tables()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    )