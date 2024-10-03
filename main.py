from flask import Flask
from router.user import user_route
from router.animal import animal_route



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(animal_route)
app.register_blueprint(user_route)