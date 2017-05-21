import time
import datetime
from __init__ import app, db, sqlalchemy
from flask import Flask, render_template, request, url_for, escape, session, redirect, flash, make_response, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import *
from models import *
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from sqlalchemy import func
import numpy as np

PER_PAGE = 20

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
@app.route('/index/<int:page>', methods=['POST', 'GET'])
@login_required
def index(page=1):
	'''index page'''
	if request.method == 'POST':
		if request.form.get('default'):
			session.pop('fromdate', None)
			session.pop('todate', None)
		else:
			try:
				if request.form.get('fromdate'):
					fromdate = datetime.datetime.strptime(request.form.get('fromdate'),'%d/%m/%y')
					session['fromdate'] = fromdate
	
				if request.form.get('todate'):
					todate = datetime.datetime.strptime(request.form.get('todate'),'%d/%m/%y')
					session['todate'] = todate
			except:
				flash('Inputed wrong data!!!')
				return redirect(url_for('index'))
			if session.get('fromdate') and session.get('todate'):
				flash(str(session.get('fromdate')) +" to " + str(session.get('todate')+datetime.timedelta(days=1)))	

	if not (session.get('fromdate') and session.get('todate')):
		try:
			rows = Sensor.query.order_by(Sensor.ids.desc()).paginate(page, PER_PAGE)
		except:
			rows = None
	else:
		try:
			rows = Sensor.query.filter(Sensor.ts > session['fromdate'], Sensor.ts < session['todate'] + datetime.timedelta(days=1)).order_by(Sensor.ids.desc()).paginate(page, PER_PAGE)
		except:
			rows = None
	if rows:
		for row in rows.items:
			row.abh = abs_hum(row.humid, row.temp1, row.press/100)
	settings = User.query.get(session.get('user_id')).settings
	return render_template('index.html', rows = rows, settings=settings)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	''' Login '''
	session.clear()
	error = None
	if request.method == 'POST':
		if not request.form.get('Email') or not ('@' in request.form.get('Email')):
			error = 'NO EMAIL'
		elif not User.query.filter_by(email=request.form.get('Email')).first():
			error = 'User doesn\'t exist'
		elif not request.form.get('Password') or not check_password_hash(User.query.filter_by(email= request.form.get('Email')).first().psw, request.form.get('Password') ):
			error = 'Worng password'
		else:
			session['Email'] = request.form.get('Email')
			session['user_id'] = User.query.filter_by(email=session.get('Email')).first().id
			flash('Welcome to site')
			return redirect(url_for('index'))

	return render_template('signin.html', error= error)

@app.route('/logout')
def logout():
	''' Logout '''
	session.clear()
	return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'] )
def register():
	''' Register user'''
	error = None
	if request.method == 'POST':
		if not request.form.get('Email') or not ('@' in request.form.get('Email')):
			error = 'NO EMAIL'
		elif User.query.filter_by(email=request.form.get('Email')).first():
			error = 'Email exists'
		elif not request.form.get('Password') or request.form.get('Passwordagain') != request.form.get('Password') :
			error = 'Wrong password'
		else:
			user = User(request.form.get('Email'), request.form.get("Password"))
			db.session.add(user)
			db.session.commit()
			session['Email'] = request.form.get('Email')
			session['user_id'] = User.query.filter_by(email=session.get('Email')).first().id
			flash('User successfully added')
			return redirect(url_for('index'))
	
	return render_template('register.html',error = error)

@app.route("/graph")
@login_required
def graph():
	'''render graph'''
	try:
		rows = Sensor.query.order_by(Sensor.ids.desc()).all()
	except:
		rows = None
	divs = None
	settings = User.query.get(session.get('user_id')).settings
	if rows:
		tempr, dat, hum, pres, dust = list( list(y) for y in zip(*[[x.temp1, x.ts, x.humid, x.press, x.dust] for x in rows]))
		# making graf for temperature and humidity
		if settings.h_and_t_plot == True:
			lines = []
			line = make_line(x=dat, y=tempr, name="temperature, deg C")
			lines.append(line)
			line = make_line(x=dat, y=hum, color="#ce043d", name="humidity, %")
			lines.append(line)
			data = go.Data(lines)
			layout = make_layout(xname="Date and time", yname="Value", title=" Humidity and temperature")
			figure = go.Figure(data=data, layout=layout)
			div = plotly.offline.plot(figure, output_type="div", include_plotlyjs=True, link_text=False, show_link=False)
			divs = []
			divs.append(div)
		#making graf for pressure
		if settings.press_plot == True:
			lines = []
			line = make_line(x=dat, y =pres, color="##3b0070", name="pressure, Pa" )
			lines.append(line)
			data = go.Data(lines)
			layout = make_layout(xname="Date and time", yname="Value", yrange=[90000,max(pres)+max(pres)*0.2], title="Atmospheric pressure")
			figure = go.Figure(data=data, layout=layout)
			div = plotly.offline.plot(figure, output_type="div", include_plotlyjs=True, link_text=False, show_link=False)
			divs.append(div)
		# making graf for dust
		if settings.dust_plot == True:
			lines = []
			line = make_line(x=dat, y=dust, color="#8c6600", name="duster, mg/m3")
			lines.append(line)
			data = go.Data(lines)
			layout = make_layout(xname="Date and time", yname="Value", yrange=[0, 0.5], title=" Dust")
			figure = go.Figure(data=data, layout=layout)
			div = plotly.offline.plot(figure, output_type='div', include_plotlyjs=True, link_text=False, show_link=False)
			divs.append(div)
	return render_template('graph.html', divs= divs)

@app.route('/get_csv', methods = ['GET'])
@login_required
def get_csv():
	''' export csv file'''
	try:
		rows = Sensor.query.order_by(Sensor.ids.desc()).all()
	except:
		rows = None
	file_bs = create_csv(rows)
	
	with open(os.path.join(app.root_path, file_bs), 'r') as f:
		csv = f.read()
	
	response = make_response(csv, 200)
	response.headers['Content-Description'] = 'File Transfer'
	response.headers['Cache-Control'] = 'no-cache'
	response.headers['Content-Type'] = 'text/csv'
	response.headers['Content-Disposition'] = 'attachment; filename={}.csv'.format(time.ctime())

	return response

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	'''settings'''
	if request.method == "POST":
		truelist = request.form.getlist('table') + request.form.getlist("graphs")
		options = [i for i in dir(Settings) if not (i.startswith("__") or i.startswith("_") or i in ["id","users","metadata","query","query_class"])]
		filter = { i: True if i in truelist else False for i in options }
		find = Settings.query.filter_by(**filter)
		if find.first() == None:
			new_setting = Settings(**filter)
			db.session.add(new_setting)
			User.query.get(session.get("user_id")).settings_id = find.first().id
		else:
			User.query.get(session.get("user_id")).settings_id = find.first().id
		db.session.commit()
		return redirect(url_for('index'))
		
	return render_template('settings.html')

@app.route('/help')
@login_required
def help():
	return render_template('help.html')
					
@app.route('/analytics')
@login_required
def analytics():
	''' analyze table data and return json'''
	try:
		nmeas = Sensor.query.count()
		maxval = db.session.query(func.max(Sensor.ts)).one()[0]
		minval = db.session.query(func.min(Sensor.ts)).one()[0]
		selected = None
		# check if selected range in session
		if session.get('fromdate') and session.get('todate'):
			selected = Sensor.query.filter(Sensor.ts > session['fromdate'], Sensor.ts < session['todate'] + datetime.timedelta(days=1))
			selnmeas = selected.count()
			smaxval = selected.from_self(func.max(Sensor.ts)).one()[0]
			sminval = selected.from_self(func.min(Sensor.ts)).one()[0]
		else:
			selnmeas = nmeas
			smaxval = maxval
			sminval = minval
		if not selected:
			selected = Sensor.query	
		# select data for humidity	
		hmaxdate, humidity_max = selected.from_self(Sensor.ts, Sensor.humid).filter(Sensor.humid == func.max(Sensor.humid).select()).first()
		hmindate, humidity_min = selected.from_self(Sensor.ts, Sensor.humid).filter(Sensor.humid == func.min(Sensor.humid).select()).first()
		hdata = selected.from_self(Sensor.humid).all()
		# select data for temperature
		tmaxdate, temp_max = selected.from_self(Sensor.ts, Sensor.temp1).filter(Sensor.temp1 == func.max(Sensor.temp1).select()).first()
		tmindate, temp_min = selected.from_self(Sensor.ts, Sensor.temp1).filter(Sensor.temp1 == func.min(Sensor.temp1).select()).first()
		tdata = selected.from_self(Sensor.temp1).all()
		# select data for pressure
		pmaxdate, press_max = selected.from_self(Sensor.ts, Sensor.press).filter(Sensor.press == func.max(Sensor.press).select()).first()
		pmindate, press_min = selected.from_self(Sensor.ts, Sensor.press).filter(Sensor.press == func.min(Sensor.press).select()).first()
		pdata = selected.from_self(Sensor.press).all()
		# select data for dust
		dmaxdate, dust_max = selected.from_self(Sensor.ts, Sensor.dust).filter(Sensor.dust == func.max(Sensor.dust).select()).first()
		dmindate, dust_min = selected.from_self(Sensor.ts, Sensor.dust).filter(Sensor.dust == func.min(Sensor.dust).select()).first()
		ddata = selected.from_self(Sensor.dust).all()

	except:
		return jsonify({
		"firsttable": {
						"nmeas": None,
						"dr":{"from": None, "to": None},
						"selnmeas": None,
						"sdr":{"from": None, "to":None}
						},
		"secondtable": {
						"humidity": {
									"max": None,
									"min": None,
									"mean": None,
									"dev": None,
									"mindate": None,
									"maxdate": None
									},
						"temperature": {
									"max": None,
									"min": None,
									"mean": None,
									"dev": None,
									"mindate": None,
									"maxdate":None
										},
						"pressure": {
									"max": None,
									"min": None,
									"mean": None,
									"dev": None,
									"mindate": None,
									"maxdate":None
									},
						"dust": {
									"max": None,
									"min": None,
									"mean": None,
									"dev": None,
									"mindate": None,
									"maxdate":None
								}
						}
		})
	return jsonify({
		"firsttable": {
						"nmeas": nmeas,
						"dr":{"from": minval.isoformat(' '), "to": maxval.isoformat(' ')},
						"selnmeas": selnmeas,
						"sdr":{"from": sminval.isoformat(' '), "to":smaxval.isoformat(' ')}
						},
		"secondtable": {
						"humidity": {
									"max": round(humidity_max, 3),
									"min": round(humidity_min, 3),
									"mean": np.round(np.mean(hdata),3),
									"dev": np.round(np.std(hdata),3),
									"mindate": hmindate.isoformat(' '),
									"maxdate": hmaxdate.isoformat(' ')
									},
						"temperature": {
									"max": round(temp_max, 3),
									"min": round(temp_min, 3),
									"mean": np.round(np.mean(tdata), 3),
									"dev": np.round(np.std(tdata), 3),
									"mindate": tmindate.isoformat(' '),
									"maxdate":tmaxdate.isoformat(' ')
										},
						"pressure": {
									"max": round(press_max, 3),
									"min": round(press_min, 3),
									"mean": np.round(np.mean(pdata), 3),
									"dev": np.round(np.std(pdata), 3),
									"mindate": pmindate.isoformat(' '),
									"maxdate":pmaxdate.isoformat(' ')
									},
						"dust": {
									"max": round(dust_max, 3),
									"min": round(dust_min, 3),
									"mean": np.round(np.mean(ddata), 3),
									"dev": np.round(np.std(ddata), 3),
									"mindate": dmindate.isoformat(' '),
									"maxdate":dmaxdate.isoformat(' ')
								}
						}
		})
			
