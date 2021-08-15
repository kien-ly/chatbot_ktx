import requests
import speech_recognition as s 
from gtts import gTTS
from datetime import date, datetime
import os, string
import chatbot
import subprocess



# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 512
# RECORD_SECONDS = 6
# WAVE_OUTPUT_FILENAME = "./static/question.wav"
# device_index = 2
# audio = pyaudio.PyAudio()

# def record():
#     print("----------------------record device list---------------------")
#     info = audio.get_host_api_info_by_index(0)
#     numdevices = info.get('deviceCount')
#     for i in range(0, numdevices):
#             if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#                 print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

#     print("-------------------------------------------------------------")

#     index = int(input())
#     print("recording via index "+str(index))

#     stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,input_device_index = index, frames_per_buffer=CHUNK)
#     print ("recording started")
#     Recordframes = []
 
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         Recordframes.append(data)
#     print ("recording stopped")

   
    
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

#     waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     waveFile.setnchannels(CHANNELS)
#     waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#     waveFile.setframerate(RATE)
#     waveFile.writeframes(b''.join(Recordframes))
#     waveFile.close()

def botprocess(url):
    audio_data = requests.get(url, allow_redirects=True).content
    with open("./static/ques.mp4", 'wb+') as f:
        f.write(audio_data)
    command = "ffmpeg -y -y -hide_banner -loglevel error -i ./static/ques.mp4 -ab 160k -ac 2 -ar 44100 -vn ./static/question.wav"
    #command = "ffmpeg -y -hide_banner -loglevel error -i ./static/question.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 ./static/question.wav"
    subprocess.call(command, shell=True)

    robot_ear = s.Recognizer()
    robot_brain = ""
    filename = "./static/question.wav"
    with s.AudioFile(filename) as source:
        print("Robot: I'm listening")
        audio_data = robot_ear.record(source)
    you = robot_ear.recognize_google(audio_data,language='vi-VN').lower()
    
    print("you: " + you)

    if you != "":
        robot_brain, _ = chatbot.chatbot_response(you)
    else:
        robot_brain = "Tôi không nghe được bạn nói gì ! Hãy thử lại nhé !"
    
    print("Robot: " + robot_brain)

    tts=gTTS(text=robot_brain,lang='vi',slow=False)
    tts.save("./static/answer.mp3")

def voicebot(url):
    #record()
    return botprocess(url)
