from flask import Flask, request, jsonify
import json
import pytest
import pickle
import requests
from flask_sqlalchemy import SQLAlchemy
# from pip._vendor import requests

app = Flask('my-flask')

# project_dir = os.path.dirname('C:/Users/This_user/PycharmProjects')
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
#
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = database_file
#
# db = SQLAlchemy(app)


class Message(object):
    def __init__(self, application_id, session_id, message_id, participants, content, **entries):
        self._dict = entries
        self.application_id = application_id
        self.session_id = session_id
        self.message_id = message_id
        self.participants = participants
        self.content = content

    def __str__(self):
        return 'Message: application id :{}, session id: {}, message id: {} ,participants: {} , content: {}'.format(self.application_id,self.session_id,self.message_id,self.participants,self.content)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Application:
    def __init__(self):
        self.__messages_list = []
        self.read()

    # קריאה
    def read(self):
        print("read")
        with open('messages.json') as json_file:
            self.__messages_list = json.load(json_file)
        for ind, msg in enumerate(self.__messages_list):
            self.__messages_list[ind] = Message(**msg)
        print(self.__messages_list[0])
        print(self.get_len())

    # כתיבה
    def write(self):
        print("write")
        messages = self.__messages_list
        for ind, msg in enumerate(self.__messages_list):
            messages[ind] = msg.__dict__
            del messages[ind]['_dict']
            print(messages[ind])
        with open('messages.json', 'w')as json_file:
            json.dump(messages, json_file)
        self.read()

    def get_message(self, attr, idN):
        print("get message---------")
        print(attr, idN)
        field_name = str(attr)
        if field_name=='application_id':
            idN = int(idN)
        msg_list = list(filter(lambda m: getattr(m, field_name) == idN, self.__messages_list))
        #msg_list=[i for i in self.__messages_list if getattr(i, attr) == idN]
        json_string=" "
        json_string = json.dumps([ob.__dict__ for ob in msg_list])
        print(json_string)
        print(type(msg_list))
        print(len(msg_list))
        #print(type(msg_list[0]))
        return str(json_string)

    def append(self, new_message):
        self.__messages_list.append(new_message)
        self.write()

    def delete(self, attr, idN):
        print("delete")
        if attr=='application_id':
            idN = int(idN)
        self.__messages_list = [i for i in self.__messages_list if not (getattr(i, attr) == idN)]
        self.write()
        self.print_list()
        return str(self.get_len())

    def print_list(self):
        print("messages-list:")
        for m in self.__messages_list:
            print(m)

    def get_len(self):
        return len(self.__messages_list)


myApp = Application()
myApp.print_list()

@app.route('/GetMessage/')
def getById():
    print("getById----------")
    args_value = request.args
    dictA = dict(args_value)
    return myApp.get_message(list(dictA.keys())[0], list(dictA.values())[0])


@app.route('/AddMessage/', methods=['POST'])
def add_message():
    print("post")
    print("data: ",request.json)
    message = request.get_json()
    new_message = Message(**message)
    myApp.append(new_message)
    print("after append:")
    myApp.print_list()
    return str(myApp.get_len())


@app.route('/DeleteMessage/', methods=['DELETE'])
def delete_message():
    print("delete-----------")
    dictA = dict(request.args)
    res = myApp.delete(list(dictA.keys())[0], list(dictA.values())[0])
    myApp.print_list()
    print("messages_list len: ", myApp.get_len())
    return res


app.run()
