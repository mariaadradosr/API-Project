#!/usr/bin/python3

from pymongo import MongoClient
import getpass
import json
import config
import os
import requests
from bson import ObjectId
import dotenv
dotenv.load_dotenv()

#Connect to DB


#connection=os.getenv("MONGODB_URL")
connection=os.getenv("ATLAS_URL")
print(connection)
client = MongoClient(connection)

def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll

#db, coll = connectCollection('datamad1019','chats')

#with open('my-application/input/chats.json') as f:
#    chats_json = json.load(f)
#coll.insert_many(chats_json)

#l='http://localhost:8080/add'




def addDocument(document, coll):
    doc = coll.insert_one(document)
    return doc.inserted_id

def addUser(name, coll):
    document = {'name': name}
    return addDocument(document, coll)

def addChat(coll):
    document = {'members':[]}
    return addDocument(document, coll)
    
def addMember(member_id, chat,coll):
    if member_id not in list(coll.find({'_id':ObjectId(chat)}))[0]['members']:
        filtro = {'_id':ObjectId(chat)}
        field = 'members'
        value = {'$push':{field:member_id}}
        coll.update_one(filtro, value) 
        return f'{member_id} has been added to chat {chat}'
    else: 
        return f'ERROR: {member_id} is already a member of chat {chat}'

def addMessage(author_id,chat,markdown,coll,chat_coll):
    if author_id in list(chat_coll.find({'_id':ObjectId(chat)}))[0]['members']:
        document = {
            'author_id': author_id,
            'chat_id': chat,
            'markdown': markdown
        }
        addDocument(document, coll)
        return f'Message has been added to chat {chat}'
    else:
        return f'{author_id} is not a member of chat {chat}'

def getMembers(chat, coll, users_coll):
    names = []
    try:
        for e in list(coll.find({'_id':ObjectId(chat)}))[0]['members']:
            names.append(list(users_coll.find({'_id':ObjectId(e)}))[0]['name'])
        return names
    except:
        return f'There is no member in chat {chat} yet'

def getMessages(chat, coll):
    mess = {}
    mess[chat] = []
    try:
        for e in list(coll.find({})):
            if e['chat_id'] == chat:
                mess[chat].append(e['markdown'])
        return mess
    except:
        return f'There is no message in chat {chat} yet'





# Adding multiple users to collection users

def createMultipleUsers(user_list):
    url = f'http://localhost:8080/create/user'
    for name in user_list:
        params = {
            'name' : name
        }
        print(name, requests.post(url, data=params).text)

# Adding multiple chats to collection chats

def createMultipleChats(n):
    url = f'http://localhost:8080/create/chat'
    for i in range(n):
        number = i + 1
        print(number, requests.post(url).text)

# Adding multiple members to chat documents

def addMultipleMembers(base_members):
    '''
    Base_members input has to be a dict json object:
    [{'chatId': ObjectId('5de296ee1821b6e70cb16f80'),
                  'userId': [ObjectId('5de280d633ba2628285db859'),
                            ObjectId('5de280d633ba2628285db85a')]}]
    '''
    for e in base_members:
        url = 'http://localhost:8080/chat/{}/addMember'.format(e['chatId'])
        for i in e['userId']:
            params = {
                'member_id':str(i)
            }
            print(requests.post(url, data=params).text)

# Adding multiple messages  to collection messages

def addMultipleMessages(db):
    '''
    [{
    'text': 'Hey Mike, whats up??',
    'userId': ObjectId('5de280d633ba2628285db859'),
    'chatId': ObjectId('5de296ee1821b6e70cb16f80')
    }]
    '''
    for e in db:
        url = 'http://localhost:8080/chat/{}/addMessage'.format(e['chatId'])
        params = {
            'author_id':str(e['userId']),
            'markdown':e['text']
        }
        print(requests.post(url, data=params).text)