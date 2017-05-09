import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_jsglue import JSGlue

jsglue = JSGlue()
app = Flask(__name__)
jsglue.init_app(app)
app.secret_key = 'abcdefgjklmnopqrstuvwxyz1234567'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(app.root_path, 'ap.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {

	'sens': 'mysql://roma:2424sdsd@127.0.0.1:3306/projectdb'
}
db = SQLAlchemy(app)

en = db.get_engine(bind='sens')
try:
	con = en.connect()
except sqlalchemy.exc.OperationalError, er:
	print er

import views










