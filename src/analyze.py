from flask import Flask, request
from pymongo import MongoClient
from errorHandler import jsonErrorHandler
from bson import json_util, ObjectId
from check import listMessages, listMessagesUser, listAllUsers, changeId
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from scipy.spatial.distance import pdist, squareform

#Connect to DB
client = MongoClient("mongodb://localhost:27017")
mydb = client["sentiment"]

#NLTK
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

#Analyze the sentiment of each chat message independently
def analyzeResult(chat_id):
    all_messages = listMessages(chat_id)
    result_analyze = []
    for i in all_messages:
        score = sia.polarity_scores(i['text'])
        result_analyze.append((i['user_id']['$oid'],score))
    return result_analyze

#Analyze the sentiment of all chat messages
def analyzeAllResult(chat_id):
    all_messages = listMessages(chat_id)
    total_score = {'id': chat_id,'neg': 0.0, 'neu': 0.0, 'pos': 0.0}
    for i in all_messages:
        score = sia.polarity_scores(i['text'])
        total_score['neg'] += score['neg']
        total_score['pos'] += score['pos']
        total_score['neu'] += score['neu']
    return total_score

#Analyze the sentiment of all chat messages for especific user
def analyzeResultUser(chat_id, user_id):
    all_messages = listMessagesUser(chat_id, user_id)
    total_score = {'user_id': user_id, "chat_id": chat_id, 'neg': 0.0, 'neu': 0.0, 'pos': 0.0}
    for i in all_messages:
        score = sia.polarity_scores(i['text'])
        total_score['neg'] += score['neg']
        total_score['pos'] += score['pos']
        total_score['neu'] += score['neu']
    return total_score

#Analyze the sentiment for all users in a chat
def analyzeUsers(chat_id):
    all_users = listAllUsers(chat_id)
    all_scores = []
    for i in all_users:
        for j in i['users_ids']:
            score = analyzeResultUser(chat_id, j['$oid'])
            all_scores.append(score)
    return all_scores

#Analyze the sentiment for all users in a chat and return 3 user recommendation
def analyzeRecommendUsers(user_id, chat_id):
    scores = analyzeUsers(chat_id)
    df = pd.DataFrame(scores).set_index('user_id')
    df = df.drop(columns =['chat_id'])
    df = pd.pivot_table(df, index='user_id')
    distances = pd.DataFrame(1/(1 + squareform(pdist(df.T, 'euclidean'))), 
                         index=df.index, columns=df.index)
    for _ in distances:
        similarities = distances[user_id].sort_values(ascending=False)[1:4]
        recommend = list(similarities.index)
        recommend = json.loads(json_util.dumps(recommend))
    recommend = changeId(recommend)
    return recommend
