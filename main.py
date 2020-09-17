import speech_recognition as sr
from pynput import keyboard
import pyautogui
import time
import re
r = sr.Recognizer()
mic = sr.Microphone()
text = ""
record_key = keyboard.Key.home
typing_key = keyboard.Key.enter
summoners = {"f": 300, "flash": 300}
list_timers = []

class Timers:
    def __init__(self, game_component, start):
        self.game_component = game_component
        self.start = start
        self.end = summoners[game_component] + self.start

    def get_end(self):
        return self.end

def on_press(key):
    global text
    text_holder = ""
    try:
        if key == record_key:
            with mic as source:
                audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language='en-CA')
                start_time = re.match('.*?([0-9]+)$', text).group(1)
                summoner = re.match('^([\w]+)', text).group(1)
                print(summoner)
                timer_object = Timers(summoner, int(start_time[:2])*60 + int(start_time[2:]))
                list_timers.append(timer_object)
            except sr.UnknownValueError:
                return True
        elif key == typing_key:
            for o in list_timers:
                text_holder = text_holder + str(o.get_end())
            pyautogui.typewrite(text_holder)
            return False
    except AttributeError:
        return True


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

