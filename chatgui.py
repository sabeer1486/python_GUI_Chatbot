import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from song_lyrics import song_lyrics
from get_music import music
from news import get_news
from weather import get_weather_data
from quotations import get_quotations
import webbrowser
from google_search import search

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


# chatbot responses giving function
def getResponse(msg, ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(tag == "lyrics"):
            response = random.choice(i['responses'])
            ChatLog.insert(END, "Chatty: " + response + '\n\n')
            content = song_lyrics(msg)
            if type(content) == str:
                ChatLog.insert(END, "Chatty: " + content + '\n\n')
                return "here are you results."
            elif type(content) == tuple:
                for data in content:
                    ChatLog.insert(END, "Chatty: " + data + '\n\n')
                return "here are you results."

        elif(tag == "music"):
            content = music(msg)
            if type(content) == str:
                ChatLog.insert(END, "Chatty: " + content + '\n\n')
            elif type(content) == tuple:
                title, flink, vlink = content

                def audio_link():
                    # import vlc
                    # p = vlc.MediaPlayer(flink)
                    # p.play()
                    webbrowser.open_new(flink)

                def video_link():
                    webbrowser.open_new(vlink)

                ChatLog.insert(END, "Chatty: " + title + '\n\n')
                ChatLog.insert(END, "Audio link: " + flink + '\n\n', hyperlink.add(audio_link))
                ChatLog.insert(END, "Video link: " + vlink + '\n\n', hyperlink.add(video_link))
            return "here are you results."

        elif(tag == 'news'):
            title, description, short_link = get_news()
            for i in range(5):
                def news_link():
                    webbrowser.open_new(short_link[i])
                ChatLog.insert(END, "News: " + title[i] + ' - \n' + description[i])
                ChatLog.insert(END, "\nclick here for brief.\n\n", hyperlink.add(news_link))
            return "here are your result."
        
        elif(tag == 'weather'):
            weather_report = get_weather_data(msg)
            ChatLog.insert(END, "Chatty: " + weather_report + '\n\n')
            return "here are your results"
        
        elif(tag == 'quotations'):
            quoto = get_quotations()
            ChatLog.insert(END, "Chatty: " + quoto + '\n\n')
            return "here are your result"

        elif(tag == 'search'):
            search(msg)
            return "open your browser if it's not opened automatically"

        elif(i['tag'] == tag):
            result = random.choice(i['responses'])
            return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(msg, ints, intents)
    return res


#Creating GUI with tkinter
import tkinter
from tkinter import *

# class for creationg hyperlinks
class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        res = chatbot_response(msg)
        ChatLog.insert(END, "Chatty: " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("Chatty *_*")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)


#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
hyperlink = HyperlinkManager(ChatLog)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )
#  creating a function for sendButton
def enter_function(event):
    SendButton.invoke()

# going to bind main window with enter key...
base.bind('<Return>', enter_function)

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()
