from bluedot.btcomm import BluetoothClient
from time import sleep

import sys 
try:
    reload         # Python 2
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:  # Python 3
    from importlib import reload

import speech_recognition as sr
import tempfile
from gtts import gTTS
from pygame import mixer

r = sr.Recognizer()

def speak(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(loops)

def data_received(data):
    print(data)
    try:
        #sentence = 'Hello World'
        for sentence in data:
            if sentence == ' ':
                continue
            elif sentence == '.':
                speak('point','en')
                sleep(1)
                continue
            speak(sentence, 'en')
            sleep(1)
    except Exception as e:
        print(e)
    print('--------------------------------')

c = BluetoothClient("raspberrypi", data_received)
#c.send("potato")

timer = 1

while(timer):
    timer -= 1

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something: ")
        audio=r.listen(source)

    try:
        print("Google Speech Recognition thinks you said: ")
        sent = r.recognize_google(audio, language="zh-TW")
        print("{}".format(sent))
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print('No response from Google Speech Recognition service: {0}'.format(e))

    # send the text from speech to server device
    c.send(sent)
    sleep(1)
    pass
