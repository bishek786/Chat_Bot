from pynput.keyboard import Key, Listener
import ctypes
import pyperclip
import openai, pyautogui

class Key_listening:
    def __init__(self,fuction):
        self.caps_lock = self.is_capslock_on()
        self.shift = False
        self.alf = False
        self.num = False
        self.ACTION = Action(fuction=fuction)
    def is_capslock_on(self):
        return True if ctypes.WinDLL("User32.dll").GetKeyState(0x14) else False
    
    def on_press(self,key):
        cher = str(key)
        if ("'" in cher):
            cher = cher.replace("'","")
            if cher == '""':
                cher = "'"
            cher = cher.upper() if self.caps_lock else cher
            if len(cher) < 3 :
                self.alf = cher
                self.ACTION.action(self.caps_lock, self.shift, self.alf, self.num)

        elif ("<" and ">") in cher :
            cher = cher.replace("<","")
            cher = cher.replace(">","")
            li = ['96','97','98','99','100','101','102','103','104','105']
            if cher in li:
                cher = str(li.index(cher))
                self.num = cher
                self.ACTION.action(self.caps_lock, self.shift, self.alf, self.num)
            elif cher == "110":
                cher = "."
                self.ACTION.action(self.caps_lock, self.shift, self.alf, self.num)
        else:
            if cher == "Key.shift" or cher == "Key.shift_r" or cher == "Key.shift_l":
                self.shift = True
                # self.ACTION.action(self.caps_lock, self.shift, self.alf, self.num)
            else:
                pass
        

    def on_release(self,key):
        cher = str(key)
        if cher == "Key.caps_lock":
            self.caps_lock = self.is_capslock_on()
        elif cher == "Key.shift" or cher == "Key.shift_r" or cher == "Key.shift_l":
                self.shift = False
        elif key == Key.esc:
            return False
        # self.alf = False
        # self.num = False

    def key_listen(self, on):
        if on:
            with Listener(on_press=self.on_press,on_release=self.on_release) as l :
                try:
                    l.join()
                except:
                    pass
        else:
            pass


class Action:
    def __init__(self,fuction) -> None:
        self.fuction = fuction 
        pass

    def action(self,caps_lock,shift,alf,num):
        # print(caps_lock,shift,alf,num)
        if caps_lock and shift and alf in ["s","S"] :
            self.fuction("start",None)
            num
        


def Option(option,index):
    if option == "start":
        copied = pyperclip.paste()
        try:
            with open("api.txt",'r') as file:
                api = file.read().strip("\n")
            openai.api_key = api
            model_engine = 'text-davinci-003'

            prompt = copied

            completion = openai.Completion.create(engine = model_engine, prompt=prompt, max_tokens=1024, stop=None, temperature=0.5)
            response = completion.choices[0].text

            pyautogui.press("capslock")
            pyautogui.sleep(0.5)
            pyautogui.write(response)
            
        except:
            pyautogui.press("capslock")
            pyautogui.sleep(0.5)
            pyautogui.write("Error! open ai not responsing")
        
        
        

scane = Key_listening(Option)
scane.key_listen(True)
