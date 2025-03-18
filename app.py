from flask import Flask

from backend.database import db #5th step from database.py


app=None 

def new_app():
    app=Flask(__name__)
    app.debug=True
    
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///quiz_test.sqlite3'  #3rd step database
    db.init_app(app) #4th step from database.py

    app.secret_key = "your_secret_key"
    app.app_context().push() # bring everything under the  context of flask
    return app

app=new_app()
from backend.controller import * #2nd step from controller.py
# from backend.models import * # indirect connection between controllers.py and models.py to app.py
if __name__ == '__main__':
    app.run()
