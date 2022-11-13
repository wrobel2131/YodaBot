
"""
Example data for training bot is in yodaConvs folder, if you want to add your example training data, name it: yoda_conv<number_of_file>.txt, for example yoda_conv10.txt
"""
import os

yoda_convs = []
directory = "yodaConvs"

for file_name in os.listdir(directory):
    f = os.path.join(directory, file_name)
    if os.path.isfile(f):
        print(f)
        for j,line in enumerate(open(f, 'r+')):
            yoda_convs.append(str(line.replace("\n", "")))


from chatterbot import ChatBot
from tkinter import *
from PIL import Image, ImageTk
from chatterbot.trainers import ListTrainer


chatbot = ChatBot("YodaBot", storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
        'import_path': 'chatterbot.logic.BestMatch',
        "statement_comparison_function": 'chatterbot.comparisons.LevenshteinDistance',
        'default_response': 'Sorry padawan, still learning I am!',
        'maximum_similarity_threshold': 0.80,
        },
        {
        'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        'input_text': 'May the force be with you.',
        'output_text': 'May the force be with you.'
        }
    ],
    preprocessors=['chatterbot.preprocessors.clean_whitespace'],
    # database_uri='sqlite:///database.sqlite3'
)



trainer = ListTrainer(chatbot)
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")
trainer.train(yoda_convs)

""" 
Simple GUI using tkinter
"""

GREEN = "#457459"
root = Tk()
root.geometry("600x600")
root.title("Chat with YodaBot")
root.config(bg=GREEN)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

headerFrame = Frame(root, bg=GREEN, width=500, height=200)
headerFrame.grid(row=1, column=0, pady=10)
headerFrame.grid_rowconfigure(1, weight=1)
headerFrame.grid_columnconfigure(1, weight=1)

centerFrame = Frame(root, bg=GREEN, width=500, height=400)
centerFrame.grid(row=2, column=0, pady=10)
centerFrame.grid_rowconfigure(1, weight=1)
centerFrame.grid_columnconfigure(1, weight=1)

bottomFrame = Frame(root, bg=GREEN, width=500, height=150)
bottomFrame.grid(row=3, column=0, pady=10)
bottomFrame.grid_rowconfigure(1, weight=1)
bottomFrame.grid_columnconfigure(1, weight=1)


#header
image=Image.open('yoda.png')

img=image.resize((200, 150))

logo=ImageTk.PhotoImage(img)
logoLabel = Label(headerFrame, image=logo, bg=GREEN)
logoLabel.grid(row=0, column=1, sticky = W)

logoText = Label(headerFrame, text="YodaBot", bg=GREEN, fg="white", font=("Arial", 35))
logoText.grid(row=0, column=2, sticky= E)

#center
scroll = Scrollbar(centerFrame)
scroll.pack(side=RIGHT)

textarea=Text(centerFrame,font=('Arial', 20),height=10,yscrollcommand=scroll.set
              ,wrap='word')
textarea.pack(side=LEFT)
scroll.config(command=textarea.yview)

#bottom
userInput = Entry(bottomFrame, font=('Arial', 20))
userInput.pack(side=LEFT, fill=X, padx=10)

def reply():
    user = userInput.get()
    user = user.capitalize()
    botResponse = chatbot.get_response(user)
    textarea.insert(END, 'You: '+user+'\n\n')
    textarea.insert(END, 'YodaBot: '+str(botResponse)+'\n\n')
    userInput.delete(0, END)

button = Button(bottomFrame, text="Send", command=reply)
button.pack(side=RIGHT)

def click(event):
    button.invoke()

root.bind('<Return>', click)
root.mainloop()
