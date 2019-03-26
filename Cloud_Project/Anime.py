from flask import Flask, request, jsonify, render_template, url_for, redirect,session
from passlib.apps import custom_app_context as pwd_context
#from httplib import responses
from http.client import responses
from collections import OrderedDict
import json
import requests
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel

try:
    cluster = Cluster()
    session = cluster.connect()

except:
    status = "Cassandra Error"

KEYSPACE = "mykey"
TABLENAME = "tabletable"

# create keyspace if not exist
session.execute("""
 CREATE KEYSPACE IF NOT EXISTS %s
 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}
 """ % KEYSPACE)
print ("{} has been created".format(KEYSPACE))
# create table if not exist
session.execute("""
 CREATE TABLE IF NOT EXISTS {}.{} (
     Column1 text PRIMARY KEY,
     Column2 int,
     Column3 boolean
 )""".format(KEYSPACE, TABLENAME))
print ("{} has been created".format(TABLENAME))

app = Flask(__name__)


api_url = 'https://ghibliapi.herokuapp.com'        #base API url
films_url = 'https://ghibliapi.herokuapp.com/films'
film_id_url = 'https://ghibliapi.herokuapp.com/films/{id}'

@app.route('/', methods=['GET', 'POST'])  #login page
def hello():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('homepage.html')
            #return redirect(url_for('hello'))
    return render_template('login.html', error=error) #html template and return
    #return render_template('homepage.html')
    #{}"<h1>Welcome to the Anime film directory!</h1>"

@app.route('/home') #homepage
def home():
    return render_template('homepage.html') #html and return

#@app.route('/login', methods=['GET', 'POST'])
#def login():
    #error = None
    #if request.method == 'POST':
        #if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            #error = 'Invalid Credentials. Please try again.'
        #else:
            #return redirect(url_for('hello'))
    #return render_template('login.html', error=error)

@app.route('/films', methods=['GET'])
def films():
    response = requests.get(films_url).json()
    films = {'FilmTitle': [], 'FilmID': [], 'Description': []}
    for x in response:
        films['FilmTitle'].append(x['title'])
        films['FilmID'].append(x['id'])
        #films['Description'].append(x['description'])
        #films['ReleaseDate'].append(x['release_date'])
    #return jsonify(films)
    return render_template('result.html', result = response)

@app.route('/films/<filmname>', methods=['GET']) #returns name of film and further details
def film_name(filmname):
    url = film_id_url.format(id=filmname)
    response2 = requests.get(url)
    if response2.status_code == 200:
        jsondata = response2.json()
        film_name = {'FilmID': jsondata['id'], 'FilmName': jsondata['title'], 'Descritpion': jsondata['description'], 'Film release date': jsondata['release_date']}
        #return jsonify(film_name)
        return render_template('results2.html', results2 = jsondata)
    else:
        return render_template("404.html"), 404







if __name__ == '__main__':
	app.run(port=5050, debug=True)
