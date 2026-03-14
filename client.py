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

        user_input = int(input("Choose action: "))
        print("")
        if user_input == 0:
            exit()
        elif user_input == 1:
            list_topics(proxy)
            print("Choose from existing or add new\n")
            add_topic(proxy) 
        
        elif user_input == 2:
            # list first so user knows what topics exist before typing one
            if list_topics(proxy):
                get_topic(proxy)
            else:
                print("no topics\n")
        else:
            print("option does not exist, try again\n")
    
def add_topic(proxy):
    title = input("Topic name: ")
    
    # if topic exists, show existing notes so user knows what names are taken
    existing = call_server(proxy.get_topic, title)
    if existing and "notes" in existing:
        print(f"existing notes under '{title}':")
        for note in existing["notes"]:
            print(f"  {note['name']}")
        print()

    note_name = input("Note title: ")
    text = input("Note text: ")
    
    if not title.strip() or not note_name.strip() or not text.strip():
        print("fields cannot be empty\n")
        return

    topic_data = {
        "title": title,
        "note_name": note_name,
        "text": text
        # timestamp is server generated
    }
    
    data = call_server(proxy.add_topic, topic_data)
    if data is None:
        return
    print("Topic added.\n")
    return


def get_topic(proxy):
    title = input("Topic name to fetch: ")
    data = call_server(proxy.get_topic, title)
    if data is None:  # server error, call_server already printed the error
        return
    if not data:  # empty dict, topic does not exist
        print("Topic not found.\n")
        return
    
    print(f"\nTopic: {data["title"]}")
    print("Notes: ")
    for note in data["notes"]:
        print(f"===={note['name']}====")
        print(f"    Text: {note['text']}")
        print(f"    Time: {note['timestamp']}\n")
        print(f"==================")
    return

def list_topics(proxy):
    data = call_server(proxy.list_topics)
    if data is None:
        return
    if data["topics"]:
        print("#### Available topics ####\n")
        for topic in data["topics"]:
            print(topic)
        print("\n#### Available topics ####\n")
        return True
    return False

def call_server(func, *args):
    # *args passes any arguments through to the rpc function
    try:
        response: dict = func(*args)
    except Exception as e:
        print(f"no response from server: {e}")
        return None

    status: str = response["status"]
    data: dict = response["data"]

    if status == "error":
        print(f"error: {data}")
        return None

    return data  # None if not found, dict if ok


if __name__ == "__main__":
    main()