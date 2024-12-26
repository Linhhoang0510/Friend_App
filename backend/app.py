#TODO: UPDATE this file to deployment

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__) # create an instance of the Flask class with the name of the running application as the argument
CORS(app) # enable CORS for the app

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///friends.db" # set the database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable tracking modifications so that the app runs faster and uses less memory

db = SQLAlchemy(app) # create an instance of the SQLAlchemy class with the app as the argument

import routes # import the routes module

# create all tables in the database
with app.app_context(): # ensure that the app-level resources (like the database, configurations, or other components) are accessible outside of a request-response cycle.
    db.create_all() 

if __name__ == '__main__': # If this app.py script is run directly then run the app in debug mode
    app.run(debug=True)