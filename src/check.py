from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson import json_util, ObjectId
import json

#Database
client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]


def checkUser(chat_id, user_id, text):
    #Check the User and Chat exists and the user exists in this chat
    mycol = mydb["users"]
    find_user = mycol.find({"_id": {"$eq": ObjectId(user_id)}})
    mycol = mydb["chat"]
    find_chat = mycol.find({"_id": {"$eq": ObjectId(chat_id)}})
    mycol = mydb["chat"]
    find_user_chat = mycol.find({"$and":[ {"_id":{"$eq": ObjectId(chat_id)}}, {"users_ids":{"$eq" : ObjectId(user_id)}}]})
    if find_user.count() <= 0:
        raise NameError(f"Not found User with this Id: {user_id}")
    elif find_chat.count() <= 0:
        raise NameError(f"Not found Chat with this Id: {chat_id}")
    elif find_user_chat.count() <= 0:
        raise NameError(f"Not found User with this Id {user_id} in this chat: {chat_id}")
    else:
        mycol = mydb["messages"]
        add_mess = mycol.insert_one({'chat_id':ObjectId(chat_id), "user_id": ObjectId(user_id), "text": text}).inserted_id
        return str(add_mess)


def listMessages(chat_id):
    #List all messages in the chat and check chat exists
    mycol = mydb["chat"]
    find_chat = mycol.find({"_id": {"$eq": ObjectId(chat_id)}})
    if find_chat.count() == 0:
        raise NameError(f"Not found Chat with this Id: {chat_id}")
    else:
        mycol = mydb["messages"]
        all_messages = list(mycol.find({"chat_id": {"$eq": ObjectId(chat_id)}}, {"_id": 0,"user_id":1 ,"text": 1}))
        all_messages = json.loads(json_util.dumps(all_messages))
    return all_messages


def listMessagesUser(chat_id,user_id):
    #List all messages for one user in a chat
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
        all_messages_user = list(mycol.find({"$and": [{"chat_id": {"$eq": ObjectId(chat_id)}}, {"user_id": {"$eq": ObjectId(user_id)}}]}, {"_id": 0,"user_id": 1,"text": 1}))
        all_messages_user = json.loads(json_util.dumps(all_messages_user))
    return all_messages_user


def listAllUsers(chat_id):
    #List all users in a chat
    mycol = mydb["chat"]
    find_chat = mycol.find({"_id": {"$eq": ObjectId(chat_id)}})
    if find_chat.count() <= 0:
        raise NameError(f"Not found Chat with this Id: {chat_id}")
    else:
        mycol = mydb["chat"]
        all_users = mycol.find({"_id": {"$eq": ObjectId(chat_id)}}, {"_id":0,"users_ids": 1})
        all_users = json.loads(json_util.dumps(all_users))
    return all_users


def changeIdForName(data):
    #Change User_id for name in DB with all users
    mycol = mydb["users"]
    names = []
    for i in data:
        for j in i['users_ids']:
            user_id = j['$oid']
            name_user = mycol.find({"_id": {"$eq": ObjectId(user_id)}}, {"_id": 0,"name":1})
            names.append(name_user)
        names = json.loads(json_util.dumps(names))
        return names


def changeId(data):
    #Change User_id for name with only user_id
    mycol = mydb['users']
    names= []
    for user_id in data:
        name_user = mycol.find({"_id": {"$eq": ObjectId(user_id)}}, {"_id": 0,"name":1})
        names.append(name_user)
        names = json.loads(json_util.dumps(names))
    return names
