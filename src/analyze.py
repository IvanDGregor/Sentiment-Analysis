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
def analyzeResult(chat_id):
    all_messages = listMessages(chat_id)
    result_analyze = []
    for i in all_messages:
        score = sia.polarity_scores(i['text'])
        result_analyze.append((i['user_id']['$oid'],score))
    return result_analyze

