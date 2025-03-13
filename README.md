# RCPepTelegram
Remote Control Bot, inspired to the previous creation named "Peppino", this one offers much many features, including some pretty original pranks.
(only tested on Windows10/11)
```
/help: 
id - Get Owner Chat ID.  
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
invertedscreen - Shows inverted colors screenshot.
execute - Run system command.  
microphone - Record mic audio.  
browser - Open URL in browser.
quickmenu - Opens a quick menu.
waitforface - Send a webcam photo when face is detected till timeout.
keylogger - Records pressed keys on keyboard.
livekeylogger - Sends live updates about what's being typed on the keyboard.
```
*sending a photo* - Displays the photo on the screen as a pop-up.
*sending an audio/voice* - Will play the audio/voice in the background.
*sending a file that ends with '.dd' - will execute it as duckyscript. (send /duckyhelp to get commands)

You can run multiple commands at the same time by sending them in the same message but separated by a comma.
For example this command: "/fullclip 10; /jumpscare" will start the recording, waits 5 seconds, then sends a
jumpscare while recording screen and webcam.

# Config
secret.json
```json
{
    "token":"<YOUR TOKEN>",
    "chatid":youchatid
}
```


# BUILD
I used nuitka to build a light executable, only problem I had was including directories in it and I haven't managed to do it yet.
```bash
nuitka pep2.py --windows-console-mode=disable --onefile --follow-imports --msvc=latest
```