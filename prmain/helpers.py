
import os
from flask import redirect, render_template, request, session, url_for
from __init__ import app
from functools import wraps
import math

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("Email") is None:
            
            return redirect(url_for("login", next=request.url))    
        return f(*args, **kwargs)
    return decorated_function

def abs_hum(rh,t,p):

  fp = 1.0016 + 3.15 * 10**-6 -0.074 /p
  ew = 6.112 * math.e **(17.62*t/(243.12 + t))
  return ew * rh / (461.5 * (t+273))

def create_csv(data):
  """ creat csv"""
  file_basename = 'output.csv'
  server_path = app.root_path
  w_file = open(os.path.join(server_path, file_basename),'w')
  w_file.write('id;humidity;temperature1;temperature2;pressure;dust;timestamp\n')
  if data:
    for row in data:
        row_as_string = str((row.ids, row.humid, row.temp1, row.temp2, row.press, row.dust, str(row.ts)))
        w_file.write((row_as_string[1:-1] + '\n').replace(',',';')) ## row_as_string[1:-1] because row is a tuple

  w_file.close()
  
  return file_basename

def make_line(x = [], y = [],  color = '#0a2daa',  dash = 'solid', name = "name_line" ):
    ''' define line for plot'''
    return {
    "x": x,
    "y": y,
    "error_x": {
      "color": "black", 
      "copy_ystyle": True, 
      "thickness": "1", 
      "width": "2"
    }, 
    "error_y": {
      "color": "rgb(212, 189, 74)", 
      "thickness": 1, 
      "width": 1
    }, 
    "fill": "none", 
    "line": {
      "color": color, 
      "dash": dash, 
      "shape": "linear", 
      "width": 2
    }, 
    "marker": {
      "color": "rgb(4, 158, 215)", 
      "line": {
        "color": "white", 
        "width": 0
      }, 
      "size": 6, 
      "symbol": "dot"
    }, 
    "name": name, 
    "opacity": 1, 
    "type": "scatter", 
    
  }

def make_layout(yrange = [0, 100], title = "title name", yname = "yname", xname = "xname" ):
    '''difine addtional information for plot'''
    return {
    "autosize": True, 
    "bargap": 0.2, 
    "dragmode": "zoom", 
    "font": {
      "color": "#444", 
      "family": "\"Open sans\", verdana, arial, sans-serif", 
      "size": 12
    }, 
    "height": 700, 
    "hidesources": False, 
    "hovermode": "x", 
    "legend": {
      "x": 1.02, 
      "y": 1, 
      "bgcolor": "#fff", 
      "bordercolor": "#444", 
      "borderwidth": 0, 
      "font": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 12
      }, 
      "traceorder": "normal"
    }, 
    "paper_bgcolor": "#fff", 
    "plot_bgcolor": "#fff", 
    "separators": ".,", 
    "showlegend": True, 
    "title": title, 
    "titlefont": {
      "color": "#444", 
      "family": "\"Open sans\", verdana, arial, sans-serif", 
      "size": 17
    }, 
    "width": 600, 
    "xaxis": {
      "autorange": True, 
      "autotick": True, 
      "dtick": 1, 
      "gridcolor": "#eee", 
      "gridwidth": 1, 
      "linecolor": "rgb(34,34,34)", 
      "linewidth": 1, 
      "mirror": "allticks", 
      "nticks": 0, 
      "range": [0, 1000], 
      "rangemode": "normal", 
      "showgrid": True, 
      "showline": False, 
      "showticklabels": True, 
      "tick0": 0, 
      "tickangle": "auto", 
      "tickcolor": "rgba(0, 0, 0, 0)", 
      "tickfont": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 12
      }, 
      "ticklen": 6, 
      "ticks": "", 
      "title": xname, 
      "titlefont": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 14
      }, 
      "type": "date", 
      "zeroline": True, 
      "zerolinecolor": "#444", 
      "zerolinewidth": 1
    }, 
    "yaxis": {
      "autorange": False, 
      "autotick": True, 
      "dtick": 1, 
      "exponentformat": "B", 
      "gridcolor": "#eee", 
      "gridwidth": 1, 
      "linecolor": "rgb(34,34,34)", 
      "linewidth": 1, 
      "mirror": "allticks", 
      "nticks": 0, 
      "range": yrange, 
      "rangemode": "normal", 
      "showexponent": "all", 
      "showgrid": True, 
      "showline": False, 
      "showticklabels": True, 
      "tick0": 0, 
      "tickangle": "auto", 
      "tickcolor": "rgba(0, 0, 0, 0)", 
      "tickfont": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 12
      }, 
      "ticklen": 6, 
      "ticks": "", 
      "title": yname, 
      "titlefont": {
        "color": "#444", 
        "family": "\"Open sans\", verdana, arial, sans-serif", 
        "size": 14
      }, 
      "type": "linear", 
      "zeroline": True, 
      "zerolinecolor": "#444", 
      "zerolinewidth": 1
    }
  }
