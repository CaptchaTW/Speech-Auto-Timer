import speech_recognition as sr
import pyperclip

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    audio = r.listen(source,phrase_time_limit = 4)

    text = r.recognize_google(audio, language= 'en-CA')

pyperclip.copy(text)