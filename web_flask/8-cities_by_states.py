#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask
from models import storage, State
from flask import render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exceptions):
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    state_obj = storage.all("State")
    city_obj = storage.all("City")
    states = list()
    cities = list()
    for state, value in state_obj.items():
        states.append(value)
    for city, value in city_obj.items():
        cities.append(value)
    return render_template("8-cities_by_states.html",
                           states=states,
                           cities=cities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
