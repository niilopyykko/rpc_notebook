import xmlrpc.client
import datetime

class Topic:
    def __init__(self, title, text, timestamp):
        self.title = title
        self.text = text
        self.timestamp = timestamp


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        main_menu(proxy)
    return


def main_menu(proxy):
    while True:
        print("1) add topic")
        print("2) get topic")
        print("0) Exit")

        user_input = int(input("pelase give me input"))
        if user_input == 0:
            exit()
        elif user_input == 1:
            add_topic(proxy) 
        
        elif user_input == 2:
            get_topic(proxy)

        else:
            print("option does not exist, try again")

def add_topic(proxy):
    title = input("PLEASE GIVE ME TITLE")
    text = input("PLEASE GIVE ME text")
    timestamp = datetime.datetime.today()
    topic = Topic(title, text, timestamp)
    proxy.add_topic(topic.__dict__)
    return


def get_topic(proxy):
    
    return
    







if __name__ == "__main__":
    main()