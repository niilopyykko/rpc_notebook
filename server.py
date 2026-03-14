import datetime
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import xml.etree.ElementTree as ET 
import threading
from socketserver import ThreadingMixIn

# SimpleXMLRPCServer handles one request at a time by default.
# ThreadingMixIn makes it spawn a new thread per request instead.
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    daemon_threads = True
    request_queue_size = 200

# Thread safety lock for XML operations
xml_lock = threading.Lock()

###### public functions (exposed to RPC clients) ######

def add_topic(topic_data):
    with xml_lock:
        try:
            print(f"incoming data: {topic_data}")

            title = topic_data["title"]
            note_name = topic_data["note_name"]
            text = topic_data["text"]
            
            # timestamp is generated here so the server time is used, not client time.
            # clients could have wrong clocks or be in different timezones.
            timestamp = datetime.datetime.now().strftime("%y/%m/%d - %H:%M:%S")
            
            existing = search_tree(title)
            if existing is not None:
                # topic already exists, just append a new note under it
                # check if note name already exists under this topic
                for note in existing.findall("note"):
                    if note.get("name") == note_name:
                        return {"status": "error", "data": {"error": f"note '{note_name}' already exists under '{title}'\n"}}
                note = ET.SubElement(existing, "note")
                note.set("name",note_name)
                ET.SubElement(note, "text").text = text
                ET.SubElement(note, "timestamp").text = timestamp
            elif root is not None:
                # first note under this topic, create the topic element first            
                topic_element = ET.SubElement(root, "topic")
                topic_element.set("name", title)
                note = ET.SubElement(topic_element, "note")
                note.set("name", note_name)
                ET.SubElement(note, "text").text = text
                ET.SubElement(note, "timestamp").text = timestamp
                
            write_xml_to_file()
            return {"status": "ok", "data": {}}
        except Exception as e:
            print(f"add_topic failed: {e}")
            return {"status": "error", "data": {"error": str(e)}}


def list_topics():
    with xml_lock:
        try:
            if root is not None:
                return {"status": "ok", "data": {"topics": [topic.get("name") for topic in root.findall("topic")]}}
            return {"status": "ok", "data": {"topics": []}}
        except Exception as e:
            return {"status": "error", "data": {"error": str(e)}}

def get_topic(title):
    with xml_lock:
        try:
            topic_element = search_tree(title)
            if topic_element is None:
                return {"status": "ok", "data": {}}  # empty dict signals "not found" to client
            notes = []
            for note in topic_element.findall("note"):
                notes.append({
                    "name": note.get("name", ""),
                    "text": note.findtext("text", ""),
                    "timestamp": note.findtext("timestamp", "")
                })
            return {"status": "ok", "data": {"title": title, "notes": notes}}
        except Exception as e:
            return {"status": "error", "data": {"error": str(e)}}
            

##### server internal functions (not registered as RPC endpoints) ######

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
