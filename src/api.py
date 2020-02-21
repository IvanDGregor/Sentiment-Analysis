from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]

@jsonErrorHandler
@app.route('/user/create/<name>')
def insertUser(name):
    mycol = mydb["users"]
    user_id = mycol.insert_one({"name": name}).inserted_id
    return str(user_id)

@jsonErrorHandler
@app.route('/chat/create')
def insertChat():
    mycol = mydb["chat"]
    chat_id = mycol.insert_one({"users_ids": ""}).inserted_id
    return str(chat_id)

@jsonErrorHandler
@app.route('/chat/<chat_id>/adduser/<user_id>')
def insertUserChat(chat_id, user_id):
    mycol = mydb["chat"]
    add_user = mycol.update_one({'_id':ObjectId(chat_id)}, {"$set": {"users_ids": ObjectId(user_id)}})
    return str(add_user)
app.run("0.0.0.0", 5000, debug=True)

@jsonErrorHandler
@app.route('/chat/<chat_id>/addmessage/<user_id>/<mess_id>')
def insertMessage(chat_id, user_id, mess_id):
    mycol = mydb["chat"]
    add_user = mycol.update_one({'_id':ObjectId(chat_id)}, {"$set": {"users_ids": ObjectId(user_id)}})
    return str(add_user)
app.run("0.0.0.0", 5000, debug=True)