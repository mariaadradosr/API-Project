from bottle import route, run, get, post, request
import mongodb
import sentiment
import recommend

database = 'API_Project'
db, users = mongodb.connectCollection(database, 'users')
db, chats = mongodb.connectCollection(database, 'chats')
db, messages = mongodb.connectCollection(database, 'messages')

@get('/')
def index():
    return {
        'Welcome to my API! :) '
    }

@get('/chat/<chat>/<tipo>')
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
    elif tipo =='sentiment':
        coll = chats
        coll_messages = messages
        analysis = sentiment.getChatSentiment(chat, coll, coll_messages)
        return analysis
        
@get('/user/<user_id>/recommend')
def getUserRecommendation(user_id):
    coll = messages
    users_coll = users
    return recommend.getUserRecommendation(user_id, coll, users_coll)     

@get('/create/user')
def insert_name():
    return '''<form method="GET" action="/create/user">
                <input type="submit" />
              </form>'''

@get('/create/user')
def insert_name():
    return '''<form method="POST" action="/create/user">
                Insert a new name: <input name="name"     type="text" />
                <input type="submit" />
              </form>'''

@get('/create/chat')
def insert_name():
    return '''<form method="POST" action="/create/chat">
                <input type="submit" />
              </form>'''


@post('/create/<tipo>')
def create(tipo):
    if tipo == 'user':
        print(dict(request.forms))
        name=request.forms.get("name")
        coll=users
        return {
            "inserted_doc": str(mongodb.addUser(name, coll))
            }
    elif tipo == 'chat':
        coll=chats
        #doc = coll.insert_one({})
        #i = doc.inserted_id
        #return {'inserted_doc': str(i)}
        return {
            'inserted_doc': str(mongodb.addChat(coll))
        }

@post('/chat/<chat>/<tipo>')
def addMember(chat, tipo):
    if tipo == 'addMember':
        coll = chats
        print(dict(request.forms))
        member_id = request.forms.get('member_id')
        return mongodb.addMember(member_id,chat,coll)
    elif tipo == 'addMessage':
        coll = messages
        chat_coll = chats
        print(dict(request.forms))
        author_id = request.forms.get('author_id')
        markdown = request.forms.get('markdown')
        return mongodb.addMessage(author_id,chat,markdown,coll,chat_coll)

@error(404)
def error404(error):
    return {'error': 'oops'}


port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")

run(host="0.0.0.0", port=port, debug=True)