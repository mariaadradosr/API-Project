import nltk
from bottle import route, run, get, post, request
import mongodb
import sentiment
import recommend
import os
import dotenv
dotenv.load_dotenv()
nltk.download('vader_lexicon')

database = 'API_Project'
db, users = mongodb.connectCollection(database, 'users')
db, chats = mongodb.connectCollection(database, 'chats')
db, messages = mongodb.connectCollection(database, 'messages')


@get('/')
def index():
    return {
        'Welcome to my API! :) '
    }


@get('/chat')
def getAllChats():
    coll = chats
    return {
        str(list(coll.find({})))
    }


@get('/chat/<tipo>/<chat>')
def getFromChat(chat, tipo):
    if tipo == 'members':
        coll = chats
        users_coll = users
        return {
            str(mongodb.getMembers(chat, coll, users_coll))
        }
    elif tipo == 'messages':
        coll = messages
        return (mongodb.getMessages(chat, coll))
    elif tipo == 'sentiment':
        coll = chats
        coll_messages = messages
        analysis = sentiment.getChatSentiment(chat, coll, coll_messages)
        return analysis


@get('/user/recommend/<user_id>')
def getUserRecommendation(user_id):
    coll = messages
    users_coll = users
    return recommend.getUserRecommendation(user_id, coll, users_coll)


@post('/create/<tipo>')
def create(tipo):
    if tipo == 'user':
        print(dict(request.forms))
        name = request.forms.get("name")
        coll = users
        return {
            "inserted_doc": str(mongodb.addUser(name, coll))
        }
    elif tipo == 'chat':
        coll = chats
        #doc = coll.insert_one({})
        #i = doc.inserted_id
        # return {'inserted_doc': str(i)}
        return {
            'inserted_doc': str(mongodb.addChat(coll))
        }


@post('/chat/<tipo>')
def addMember(tipo):
    if tipo == 'addMember':
        print(dict(request.forms))
        chat_id = request.forms.get('chat_id')
        member_id = request.forms.get('member_id')
        coll = chats
        user_coll = users
        return mongodb.addMember(member_id, chat_id, coll, user_coll)
    elif tipo == 'addMessage':
        coll = messages
        chat_coll = chats
        print(dict(request.forms))
        chat_id = request.forms.get('chat_id')
        author_id = request.forms.get('author_id')
        markdown = request.forms.get('markdown')
        return mongodb.addMessage(author_id, chat_id, markdown, coll, chat_coll)


port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)
