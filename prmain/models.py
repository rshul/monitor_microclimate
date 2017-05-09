from __init__ import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import BIGINT

class User(db.Model):
	"""Docstring for User"""
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	psw = db.Column(db.String(260))
	settings_id = db.Column(db.Integer, db.ForeignKey('settings.id'), default=1)
	def __init__(self, email, psw):
		self.email = email
		self.psw = generate_password_hash(psw)
		
	def __repr__(self):
		return '<User %r>' % self.email

class Sensor(db.Model):
	"""docstring for Sensor"""
	__bind_key__ = 'sens'
	__tablename__ = 'sensor_data'
	ids = db.Column('id_data',db.Integer, primary_key=True, nullable=False, autoincrement=True)
	humid = db.Column('hum', db.Float)
	temp1 = db.Column('temp1', db.Float)
	temp2 = db.Column('temp2', db.Float)
	press = db.Column('pres', db.Integer)
	dust = db.Column('dust', db.Float)
	ts = db.Column('send_time', db.DateTime)

	def __init__(self, ids, humid, temp1, temp2, press, dust, ts):
		self.ids = ids
		self.humid = humid
		self.temp1 = temp1
		self.temp2 = temp2
		self.press = press
		self.dust = dust
		self.ts = ts
	def __repr__(self):
		return '<Sensor %r>' % self.ts

class Settings(db.Model):
	"""docstring for Settings"""
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	hum = db.Column(db.Boolean, default=True, nullable=False)
	abs_hum = db.Column(db.Boolean, default=True, nullable=False)
	temp = db.Column(db.Boolean, default=True, nullable=False)
	press = db.Column(db.Boolean, default=True, nullable=False)
	press_Hg = db.Column(db.Boolean, default=True, nullable=False)
	dust = db.Column(db.Boolean, default=True, nullable=False)
	h_and_t_plot = db.Column(db.Boolean, default=True, nullable=False)
	press_plot = db.Column(db.Boolean, default=True, nullable=False)
	dust_plot = db.Column(db.Boolean, default=True, nullable=False)
	users = db.relationship('User', backref='settings', lazy='dynamic')

	def __init__(self, hum, abs_hum, temp, press, press_Hg, dust, h_and_t_plot, press_plot, dust_plot):
		
		self.hum = hum
		self.abs_hum = abs_hum
		self.temp = temp
		self.press = press
		self.press_Hg = press_Hg
		self.dust = dust
		self.h_and_t_plot = h_and_t_plot
		self.press_plot = press_plot
		self.dust_plot = dust_plot
	
	def __repr__(self):
			return '<Settings %r>' % self.id	