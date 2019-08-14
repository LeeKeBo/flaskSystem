from flask import Flask
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
#app.config['SESSION_KEY'] = 'jiumi this is a key'
app.config['SECRET_KEY'] = 'this is a secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/flaskLearn'

