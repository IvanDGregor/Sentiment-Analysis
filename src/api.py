from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson.objectid import ObjectId
from check import checkUser, listMessages, listMessagesUser, listAllUsers, changeIdForName
from analyze import analyzeResult, analyzeAllResult, analyzeResultUser, analyzeUsers, analyzeRecommendUsers
import json

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]



@jsonErrorHandler
@app.route('/user/create/<name>')
def insertUser(name):
    #Create user
    mycol = mydb["users"]
    user_id = mycol.insert_one({"name": name}).inserted_id
    return str(user_id)


@jsonErrorHandler
@app.route('/chat/create/<name>')
def insertChat(name):
    #Create chat
    mycol = mydb["chat"]
    chat_id = mycol.insert_one({"name": name,"users_ids": []}).inserted_id
    return str(chat_id)


@jsonErrorHandler
@app.route('/chat/<chat_id>/adduser/<user_id>')
def insertUserChat(chat_id, user_id):
    #Add user to chat
    mycol = mydb["chat"]
    add_user = mycol.update({'_id':ObjectId(chat_id)}, {"$push": {"users_ids": ObjectId(user_id)}})
    return str(add_user)


@jsonErrorHandler
@app.route('/messages/<chat_id>/addmessage/<user_id>/<text>')
def insertMessage(chat_id, user_id,text):
    #Add a message in chat
    return checkUser(chat_id,user_id,text)


@jsonErrorHandler
@app.route('/chat/list/<chat_id>')
def listMessaggesChat(chat_id):
    #List all messages in chat
    ok = listMessages(chat_id)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/chat/list/user/messages/<chat_id>/<user_id>')
def listMessagesUserChat(chat_id, user_id):
    #List all messages from a single user in a chat
    ok = listMessagesUser(chat_id, user_id)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/chat/list/users/<chat_id>')
def listAllUsersChat(chat_id):
    #List all users in a chat
    ok = listAllUsers(chat_id)
    ok = changeIdForName(ok)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/chat/analyze/each/<chat_id>')
def analyzeMessages(chat_id):
    #Analyze each chat message independently with 'NLTK' sentiment analysis
    ok = analyzeResult(chat_id)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/chat/analyze/all/<chat_id>')
def analyzeAllMessages(chat_id):
    #Analyze all chat messages with 'NLTK' sentiment analysis
    ok = analyzeAllResult(chat_id)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/chat/analyze/all/user/<chat_id>/<user_id>')
def analyzeAllMessagesUser(chat_id, user_id):
    #Analyze all chat messages with 'NLTK' sentiment analysis for a specific user
    ok = analyzeResultUser(chat_id, user_id)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/chat/analyze/all/each_user/<chat_id>')
def analyzeAllUsers(chat_id):
    #Analyze all chat messages with 'NLTK' sentiment analysis for each user
    ok = analyzeUsers(chat_id)
    return json.dumps(ok)


@jsonErrorHandler
@app.route('/user/<user_id>/recommend/<chat_id>')
def recommendUsers(user_id, chat_id):
    #Recommend 3 users for a specific user
    ok = analyzeRecommendUsers(user_id, chat_id)
    return json.dumps(ok)

app.run("0.0.0.0", 5000, debug=True)