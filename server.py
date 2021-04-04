from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET

#Parse the data structure/database
tree = ET.parse("db.xml")
root = tree.getroot()


#Function for adding a new topic
def writeNewTopic(tree, topic, title, text, timestamp):
    try:
        #Define the root and link the topic to it
        root = tree.getroot()
        newTopic = ET.SubElement(root, "topic", name = topic)
        
        #Define the title, text and timestamp and make correct linking
        newNote = ET.SubElement(newTopic,"note", name = title)
        newText = ET.SubElement(newNote, "text").text = text
        newTimestamp = ET.SubElement(newNote, "timestamp").text = timestamp

        #write the note to the database
        tree.write("db.xml")      
        return
    except Exception as e:
        print(e)
        return


#function for creating a new note in an existing topic
def writeOldTopic(tree, topic, title, text, timestamp):
    try:
        #Define the title, text and timestamp and link them together
        newNote = ET.SubElement(topic, "note", name = title)
        newText = ET.SubElement(newNote, "text").text = text
        newTimestamp = ET.SubElement(newNote, "timestamp").text = timestamp

        #write to database
        tree.write("db.xml")
        return
    except Exception as e:
        print(e)
        return


#Function for receiving the command and determining the correct function to call
def addNote(contentNote):
    try:
        #Search for the topic in the datastructure
        tree = ET.parse("db.xml")
        for topic in tree.findall("topic"):
            if topic.attrib["name"] == contentNote[0]:
                
                #If a match is found then the correct function is called and a string response is given to the client
                writeOldTopic(tree, topic, contentNote[1], contentNote[2], contentNote[3])             
                return "Note added!"
        
        #If no matching topic is found then a new topic has to be created
        writeNewTopic(tree, contentNote[0], contentNote[1], contentNote[2], contentNote[3])
        return "Note added!"
    except Exception as e:
        print(e)
        return "Adding the note failed!"


#Function for getting all of the notes to a topic
def getNote(userTopic):
    try:
        tree = ET.parse("db.xml")
        root = tree.getroot()
        notes = ""

        #The topic is searched for in the tree structure
        for topic in tree.findall("topic"):
            if topic.attrib["name"] == userTopic:

                #If a matching topic is found then all elements inside of the note are being looped through
                for elem in topic.findall("note"):
                    
                    #All found elements are appended to a string. Inserts linebreak between different notes 
                    notes += "Title: " + elem.attrib["name"] + "\n"
                    notes += "Text: " + elem.find("text").text + "\n"
                    notes += "Timestamp: " + elem.find("timestamp").text + "\n\n"

        #If no topics are found, sends a message to the client as a response
        if notes == "":
            notes = "No notes on the topic could be found\n"

        return notes
    except Exception as e:
        print(e)
        
        #Prints the error message and sends another one to the client 
        notes = "Error fetching notes"
        return notes


#Main function for running the server
def main():

    #Define server to localhost and port 8000
    server = SimpleXMLRPCServer(("localhost", 8000))

    #Register functions for client to use
    server.register_function(addNote)
    server.register_function(getNote)
    
    #Server activated and listening
    print("Server listening...")
    server.serve_forever()


main()