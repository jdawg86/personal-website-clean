from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import mysql.connector as mysql
import os
from pyramid.response import Response
import pyramid.httpexceptions as exc
import json
import random

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def get_home(req):
  # Connect to the database and retrieve the users

  return render_to_response('templates/home.html', [], request=req)

def welcome(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select first_name, last_name, email, comment from Users;")
  records = cursor.fetchall()
  db.close()

  return render_to_response('templates/welcome.html', {'users': records}, request=req)

def add_user(req):
  req_fields = ["first_Name", "last_Name", "email", "comment"]
  new_user = req.POST.mixed
  print(new_user)

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("INSERT INTO Users (firstName, lastName, email, comment) VALUES (%s, %s, %s, %s)", (new_user[0], new_user[1], new_user[2], new_user[3]))
  records = cursor.fetchall()
  db.close()  

  return render_to_response('templates/cv.html', [], request=req)


def cv(req):
  return render_to_response('templates/cv.html', [], request=req)

def about(req):
  return render_to_response('templates/about.html', [], request=req)

''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('welcome', '/welcome')
  config.add_view(welcome, route_name='welcome')

  config.add_route('cv', '/cv')
  config.add_view(cv, route_name='cv')

  config.add_route('add_user', '/add_user')
  config.add_view(add_user, route_name='add_user')

  config.add_route('about', '/about')
  config.add_view(about, route_name='about')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()