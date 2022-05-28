from flask import Flask       #Flask is a web framework that provides libraries to build lightweight web applications in python.
from flask_restful import Api
import pytesseract

from database import database
from flask_cors import CORS
from Routes import  UserRouter, UserListRouter
pytesseract.pytesseract.tesseract_cmd="C:\Program Files\Tesseract-OCR\tesseract.exe"

from database import database
from flask_cors import CORS
from Routes import  UserRouter, UserListRouter

app = Flask(__name__)
cors=CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://pmynxvdhcorntx:49bbbb25b382f891d2926756b988207de8db4357c14c7eb00fbfb10f460d215a@ec2-54-146-82-179.compute-1.amazonaws.com:5432/d9qdm3l3pbug25'
app.secret_key = 'secret string'
database.init_app(app)
with app.app_context():
    database.create_all()
api.add_resource(UserRouter, "/user/<string:National_id>")           #get the user and data with a particular id
api.add_resource(UserListRouter, "/user")                #get all data



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

