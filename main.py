import speech_recognition as sr
from pynput import keyboard
import pyautogui
r = sr.Recognizer()
mic = sr.Microphone()
text = "hello"
record_key = keyboard.Key.home
typing_key = keyboard.Key.enter


def on_press(key):
    global text
    try:
        if key == record_key:
            with mic as source:
                audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio, language='en-CA')
            except sr.UnknownValueError:
                return True
        elif key == typing_key:
            pyautogui.typewrite(text)
            return False
    except AttributeError:
        return True


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

