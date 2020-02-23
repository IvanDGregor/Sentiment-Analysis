from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson import json_util, ObjectId
from check import listMessages
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]

sia = SentimentIntensityAnalyzer()
#Analyze the sentiment of each chat message independently
def analyzeResult(chat_id):
    all_messages = listMessages(chat_id)
    result_analyze = []
    for i in all_messages:
        score = sia.polarity_scores(i['text'])
        result_analyze.append((i['user_id']['$oid'],score))
    return result_analyze

#Analyze the sentiment of all chat message
def analyzeAllResult(chat_id):
    all_messages = listMessages(chat_id)
    total_score = {'id': chat_id,'neg': 0.0, 'neu': 0.0, 'pos': 0.0}
    for i in all_messages:
        score = sia.polarity_scores(i['text'])
        total_score['neg'] += score['neg']
        total_score['pos'] += score['pos']
        total_score['neu'] += score['neu']
    return total_score
