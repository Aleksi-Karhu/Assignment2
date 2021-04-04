import xmlrpc.client
import datetime

#Define localhost as the proxy
proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

#Function for creating a note
def createNote():

    #Asking the user for the topic, title and text
    try:
        print("Enter a topic, title and content for the note")
        contentTopic = input("Topic: ")

        #Checking for empty strings
        if contentTopic == "":
            print("Topic cannot be empty")
            return
        contentTitle = input("Title: ")
        if contentTitle == "":
            print("Title cannot be empty")
            return
        contentText = input("Text: ")
        if contentText == "":
            print("Text cannot be empty")
            return

        #Calculating the timestamp with datetime
        contentTimestamp = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

        #Creating a list and saving it 
        noteContent = [contentTopic, contentTitle, contentText, contentTimestamp]

        #Sending the list of content to the server by calling its function. Waiting for a response
        response = proxy.addNote(noteContent)
        
        #Printing the response that can be a confirmation or error message
        print(response)

    except Exception as e:
        print(e)
        return


#Function for getting the contents of a topic
def getTopic():
    try:

        #Asking the user for the topic name
        topic = input("What topic you want to find? ")

        if topic == "":
            print("Please enter a valid topic name")
            return
            
        #Sending the topic name to the server
        results = proxy.getNote(topic)

        #Printing the notes, error message on info that there are no notes with the topic name
        print(results)

    except Exception:
        print("An error occured")
   

#Main function of the client
def main():
    print("Welcome to the notebook application!")

    #Menu for the user
    while True:
        print("\nSelect the desired operation:")
        print("1) Add a note to the notebook")
        print("2) Get the notes of a topic")
        print("0) Close the program")
        selection = input()
        
        #Selection calls the correct function
        if (selection == "1"):
            createNote()
        elif (selection == "2"):
            getTopic()
        elif (selection == "0"):
            print("Thank you for using the application!")
            exit(0)
        else:
            print("Invalid command")


main()