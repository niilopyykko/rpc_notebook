import xmlrpc.client

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        main_menu(proxy)
    return


def main_menu(proxy):
    while True:
        print("----Main menu----")
        print("1) Add topic")
        print("2) Get topic")
        print("0) Exit\n")

        user_input = int(input("pelase give me input: "))
        print("")
        if user_input == 0:
            exit()
        elif user_input == 1:
            add_topic(proxy) 
        
        elif user_input == 2:
            list_topics(proxy)
            get_topic(proxy)
        else:
            print("option does not exist, try again\n")
    
def add_topic(proxy):
    title = input("Topic name: ")
    note_name = input("Note title: ")
    text = input("Note text: ")

    topic_data = {
        "title": title,
        "note_name": note_name,
        "text": text
    }

    proxy.add_topic(topic_data)
    print("Topic added.\n")
    return


def get_topic(proxy):
    title = input("Topic name to fetch: ")
    data = proxy.get_topic(title)
    if not data:
        print("Topic not found.\n")
        return

    print(f"\nTopic: {data['title']}")
    print("Notes: ")
    for note in data["notes"]:
        print(f"    Note: {note['name']}")
        print(f"    Text: {note['text']}")
        print(f"    Time: {note['timestamp']}\n")
    return

def list_topics(proxy):
    print("#### Available topics ####\n")
    topics_list = proxy.list_topics()
    for topic in topics_list:
        print(topic)
    print("\n#### Available topics ####\n")
    return


if __name__ == "__main__":
    main()