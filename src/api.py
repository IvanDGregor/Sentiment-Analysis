from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson.objectid import ObjectId
from check import checkUser, listMessages, listMessagesUser, listAllUsers
from analyze import analyzeResult
import json

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]

#Create user
@jsonErrorHandler
@app.route('/user/create/<name>')
def insertUser(name):
    mycol = mydb["users"]
    user_id = mycol.insert_one({"name": name}).inserted_id
    return str(user_id)

#Create chat
@jsonErrorHandler
@app.route('/chat/create')
def insertChat():
    mycol = mydb["chat"]
    chat_id = mycol.insert_one({"users_ids": ""}).inserted_id
    return str(chat_id)

#Add user to chat
@jsonErrorHandler
@app.route('/chat/<chat_id>/adduser/<user_id>')
def insertUserChat(chat_id, user_id):
    mycol = mydb["chat"]
    add_user = mycol.update({'_id':ObjectId(chat_id)}, {"$push": {"users_ids": ObjectId(user_id)}})
    return str(add_user)

#Add a message in chat
@jsonErrorHandler
@app.route('/messages/<chat_id>/addmessage/<user_id>/<text>')
def insertMessage(chat_id, user_id,text):
    return checkUser(chat_id,user_id,text)

#List all messages in chat
@jsonErrorHandler
@app.route('/chat/list/<chat_id>')
def listMessaggesChat(chat_id):
    ok = listMessages(chat_id)
    return json.dumps(ok)

#List all messages from a single user in a chat
@jsonErrorHandler
@app.route('/chat/list/user/messages/<chat_id>/<user_id>')
def listMessagesUserChat(chat_id, user_id):
    ok = listMessagesUser(chat_id, user_id)
    return json.dumps(ok)

#List all users in a chat
@jsonErrorHandler
@app.route('/chat/list/users/<chat_id>')
def listAllUsersChat(chat_id):
    ok = listAllUsers(chat_id)
    return json.dumps(ok)

#Analyze messages from chat with `NLTK` sentiment analysis
@jsonErrorHandler
@app.route('/chat/analyze/<chat_id>')
def analyzeMessages(chat_id):
    ok = analyzeResult(chat_id)
    return json.dumps(ok)

app.run("0.0.0.0", 5000, debug=True)