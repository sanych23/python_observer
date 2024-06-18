from time import time

count_message = 1


class Chat:
    name = str()
    users = list()
    messages = list()
        
    def __init__(self, name) -> None:
        self.name = name

    def receiveMessage(self, message):
        global count_message
        self.messages.append({
            "id": message.id,
            "author": message.owner,
            "message": message.text,
            "time": message.time,
            "text": f"{message.owner.name}: {message.text}"
        })
        count_message += 1

    def deleteMessage(self, user, message_id):
        for message in self.messages:
            if message_id == message["id"]:
                if user == message["author"]:
                    self.messages.remove(message)
                    print("сообщение удалено")

    def sendActualMessage(self, user):
        if not user in self.users:
            print("у пользователя нет доступа к чату!")
            return 

        print(f"\n-Запрос сообщений пользователя {user.name}-")
        for message in self.messages:
            if message["id"] > user.last_requests_chat[self.name]:
                print(message["text"])
        user.changeLastRequestChat(self, self.messages[-1]["id"])
        

    def addToChat(self, user):
        self.users.append(user)
        if len(self.messages) > 0:
            self.sendActualMessage(user)
        else:
            user.changeLastRequestChat(self, 0)
        

    def removeFromChat(self, user):
        self.users.remove(user)



class Message:
    id = int()
    text = str()
    time = None
    owner = None

    def makeMessage(self, user, text):
        global count_message
        self.id = count_message
        self.owner = user
        self.text = text
        self.time = int(time() * 1000)
        return self



class User:
    name = str()
    messages = list()
    last_requests_chat = None

    def __init__(self, name) -> None:
        self.name = name
        self.last_requests_chat = {}

    def sendMessage(self, message: str, chat: Chat):
        message = Message().makeMessage(self, message)
        chat.receiveMessage(message)

    def deleteMessage(self, chat: Chat ,message_id):
        chat.deleteMessage(self, message_id)

    def requestNewMessage(self, chat: Chat):
        chat.sendActualMessage(self)

    def changeLastRequestChat(self, chat, id):
        self.last_requests_chat[chat.name] = id




# создаем 2 пользователей
user_one = User("user_one")
user_two = User("user_two")

# создаем чат
chat1 = Chat("chat1")

# добавляем пользователей в чат
chat1.addToChat(user_one)
chat1.addToChat(user_two)


# первый пользователь отправляет сообщение
user_one.sendMessage("hello", chat1)
user_one.sendMessage("hello user2", chat1)
user_one.sendMessage("how are you", chat1)

# второй пользователь отправляет сообщения
user_two.sendMessage("hello user1", chat1)
user_two.sendMessage("im fine", chat1)


# первый пользователь запрашивает актуальные ообщения
user_one.requestNewMessage(chat1)
user_one.requestNewMessage(chat1)


# первый пользователь удаляет 2 первых своих сообщения
user_one.deleteMessage(chat1, 1)
user_one.deleteMessage(chat1, 2)

# второй пользователь запрашивает актуальные сообщения
user_two.requestNewMessage(chat1)


