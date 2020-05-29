from flask import Flask, request
import json
from datetime import date 
# from dateutil import parser
import re

from flask import request, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify
# mysql = MySQL(app)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'licenta'

from app import stupina
from app import stup
from app import user
from app import controlveterinar
from app import hranire
from app import tratamente
from app import arduinoData
