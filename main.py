import speech_recognition as sr
from pynput import keyboard
import pyautogui
import time
import re
import json
r = sr.Recognizer()
mic = sr.Microphone()
text = ""
json_file = None
record_key = keyboard.Key.home
typing_key = keyboard.Key.enter
summoners = {"flash": 300, "cleanse": 210, "exhaust": 210, "ghost": 210, "heal": 240, "ignite": 180,
             "barrier": 180}
keywords = ["top", "jungle", "mid", "middle", "bot", "bottom", "support", "flash", "cleanse", "exhaust", "ghost",
            "heal", "ignite", "barrier"]
list_timers = []


class Timers:
    def __init__(self, game_component, start, role):
        self.game_component = game_component
        self.start = start
        self.end = summoners[game_component] + self.start
        self.role = role

    def get_end(self):
        return self.role + " " + self.game_component + " " + time.strftime("%M:%S", time.gmtime(self.end))


def on_press(key):
    global text
    text_holder = ""
    try:
        if key == record_key:
            with mic as source:
                audio = r.listen(source, phrase_time_limit=4)
            try:
                json_file = r.recognize_google(audio, language='en-CA', show_all=True)
                most_likely = ""
                highest_count = 0
                for members in json_file["alternative"]:
                    for transcript in members:
                        current_count = 0
                        for keys in keywords:
                            if keys in str(members[transcript]).lower():
                                current_count += 1
                        if current_count > highest_count:
                            most_likely = members[transcript]
                            highest_count = current_count
                text = most_likely.replace("/", "")
                text = re.sub(r"([0-9]+)", r" \1 ", text.lower()).strip()
                start_time = re.match('.*?([0-9]+)$', text).group(1)
                role = re.match('^([\w]+) (\w+)', text).group(1)
                summoner = re.match('([\w]+?) (\w+)', text).group(2)
                print(role, summoner, start_time)
                timer_object = Timers(summoner, int(start_time)//100*60 + int(start_time)%100, role)
                list_timers.append(timer_object)
            except sr.UnknownValueError:
                print(key)
                return True
        elif key == typing_key:
            for o in list_timers:
                text_holder = text_holder + " " + str(o.get_end())
            pyautogui.typewrite(text_holder)
            return False
    except AttributeError:
        return True


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

