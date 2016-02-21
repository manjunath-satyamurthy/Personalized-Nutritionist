import redis
import os, json, random, math

from flask import Flask, request, render_template
from flask import Flask, session
from flask.ext.session import Session

from py2neo import Graph, Path, authenticate
from py2neo import Node, Relationship

from pymongo import MongoClient


#Redis Connection setup
redisConn=redis.StrictRedis(host="localhost",port="6379",db=0)

#Neo4j Connection setup
authenticate("localhost:7474", "neo4j", "Abcdef1234")
graph = Graph()

#MongoDB Connection setup
client = MongoClient('localhost', 27017)
db = client.nutritionFacts
nutFacts = db.facts
rootdir = '/home/manju/nutritionist/A New Hope'

#Flask Application configuaration
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'bullbull'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)





