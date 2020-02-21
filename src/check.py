from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson.objectid import ObjectId

#Database
client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]

#Check the User exists and Chat exists and the user exists in this chat
def checkUser(chat_id, user_id, text):
    mycol = mydb["users"]
    find_user = mycol.find({"_id": {"$eq": ObjectId(user_id)}})
    mycol = mydb["chat"]
    find_chat = mycol.find({"$and":[ {"_id":{"$eq": ObjectId(chat_id)}}, {"users_ids":{"$eq" : ObjectId(user_id)}}]})
    if find_user.count() <= 0:
        raise NameError(f"Not found User with this Id: {user_id}")
    elif find_chat.count() <= 0:
        raise NameError(f"Not found Chat with this Id: {chat_id}")
    else:
        mycol = mydb["messages"]
        add_mess = mycol.insert_one({'chat_id':ObjectId(chat_id), "user_id": ObjectId(user_id), "text": text}).inserted_id
        return str(add_mess)

#List all messages for one user
def listMessages(chat_id):
    mycol = mydb["chat"]
    find_chat = mycol.find({"_id": {"$eq": ObjectId(chat_id)}})
    if find_chat.count() <= 0:
        raise NameError(f"Not found Chat with this Id: {chat_id}")
    else:
        mycol = mydb["messages"]
        all_messages = list(mycol.find({"chat_id": {"$eq": ObjectId(chat_id)}}, {"_id": 0, "text": 1}))
        print(all_messages)
    return all_messages