import datetime
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

class Topic:
    def __init__(self, title, text, timestamp):
        self.title = title
        self.text = text
        self.timestamp = timestamp

def today():
    today = datetime.datetime.today()
    return xmlrpc.client.DateTime(today)

def add_topic(topic_data):
    title = topic_data["title"]
    text = topic_data["text"]
    timestamp = topic_data["timestamp"]
    return


server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(today, "today")
server.register_function(add_topic, "add_topic")
server.serve_forever()