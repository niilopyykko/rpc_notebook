import datetime
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import xml.etree.ElementTree as ET 
import threading
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    daemon_threads = True

# Thread safety lock for XML operations
xml_lock = threading.Lock()

###### public functions ######
def add_topic(topic_data):
    with xml_lock:
        print(f"incoming data: {topic_data}")

        title = topic_data["title"]
        note_name = topic_data["note_name"]
        text = topic_data["text"]
        timestamp = datetime.datetime.now().strftime("%y/%m/%d - %H:%M:%S")
        
        existing = search_tree(title)
        if existing is not None:
            note = ET.SubElement(existing, "note")
            note.set("name",note_name)
            ET.SubElement(note, "text").text = text
            ET.SubElement(note, "timestamp").text = timestamp
        elif root is not None:
            topic_element = ET.SubElement(root, "topic")
            topic_element.set("name", title)
            note = ET.SubElement(topic_element, "note")
            note.set("name", note_name)
            ET.SubElement(note, "text").text = text
            ET.SubElement(note, "timestamp").text = timestamp
            
        write_xml_to_file()
        return True

def list_topics():
    with xml_lock:
        if root is not None:
            return [topic.get("name") for topic in root.findall("topic")]

def get_topic(title):
    with xml_lock:
        topic_element = search_tree(title)
        if topic_element is None:
            return {}
        notes = []
        for note in topic_element.findall("note"):
            notes.append({
                "name": note.get("name", ""),
                "text": note.findtext("text", ""),
                "timestamp": note.findtext("timestamp", "")
            })
        return {"title": title, "notes": notes}

##### public functions ######


##### server internal functions ######

def search_tree(title):
    if root is not None:
        for topic in root.findall("topic"):
            if topic.get("name") == title:
                return topic
    return None
    
def read_xml_from_file(file):
    try:
        tree = ET.parse(file)
        return tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        return None
    

def write_xml_to_file():
    tree = ET.ElementTree(root)
    tree.write("tempfile.xml")


##### server internal functions ######

def main():
    global root
    root = read_xml_from_file("tempfile.xml")
    if root is None:
        root = ET.Element("data")
        ET.ElementTree(root).write("tempfile.xml")

    server = ThreadedXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    if root is not None:
        server.register_function(add_topic, "add_topic")
        server.register_function(list_topics, "list_topics")
        server.register_function(get_topic, "get_topic")
        server.serve_forever()

if __name__ == "__main__":
    main()
