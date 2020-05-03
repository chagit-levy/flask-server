The project include 2 main files:
1. flask-server
2. test_api

In flask-server declared all the functions and methods that implement the api server.
At the beginning of the running, the program create an instance of class 'Application' that reading the all messages that stored in a json file into a list of objects which are the class 'Message' type.

The test file, running by: 'pytest test_api.py' in the Terminal, apply the methods of the 'server' , check the results and ensure that Everything works as expected.
The 'GetMessage' method return list of messages according to the url parameter.
The 'Post' and 'Delete' methods return the size of the messages list after the change.

Part of the challenge was to sent & receive the data as json format beside implement oop and use the Message class objects.
In order to resolve this conflict, I converted from object to dictionary and from dictionary to object every time that needed.

It was very fun and interesting to learn and find so much new.
Thank you.

