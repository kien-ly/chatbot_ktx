# libraries
import pickle
import json, os, time, datetime
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from chatbot import chatbot_response
lemmatizer = WordNetLemmatizer()
import chatprocess, voicebot, chatbot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/getbot')
def get_bot_response():
    userText = request.args.get('msg')
    #answer, type_num =  chatbot.chatbot_response(userText)
    answer, type_num =  chatprocess.chatbot_response(userText)
    data = {'answer': answer, 'type':type_num}
    return json.dumps(data, ensure_ascii=False)
     

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

@app.route("/voicebot")
def get_record():
    voicebot.voicebot()
    id_file = dir_last_updated('./static')
    return id_file


if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
