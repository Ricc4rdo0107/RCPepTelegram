# RCPepTelegram
Remote Control Bot, inspired to the previous creation named "Peppino", this one offers much many features, including some pretty original pranks.
(only tested on Windows10/11)

# ⚠️ WARNING: Security and Ethical Risks ⚠️
This code is intended for educational purposes only and should not be used in any malicious, unethical, or unauthorized manner. The script contains functionalities that can potentially compromise the security and privacy of a system, including but not limited to:

Remote Control: The code allows for remote control of a system, including executing commands, capturing screenshots, recording audio/video, and more.

Keylogging: The script includes keylogging capabilities, which can record keystrokes and send them to a remote user.

Webcam Access: The script can access and record from the webcam without the user's explicit consent.

System Manipulation: The script can simulate system shutdowns, open message boxes, and perform other actions that could disrupt normal system operations.

Duckyscript Execution: The script can execute Duckyscript payloads, which are often used in penetration testing but can also be used maliciously.

Ethical Considerations
Unauthorized Access: Using this script to access or control a system without the owner's explicit permission is illegal and unethical.

Privacy Violation: Capturing audio, video, or screenshots without consent is a serious violation of privacy.

Potential for Abuse: This script can be easily modified for malicious purposes, such as spying, data theft, or system disruption.

Security Risks
Exposure of Sensitive Data: If the script is not properly secured, sensitive information such as Telegram API tokens, chat IDs, and recorded data could be exposed.

Remote Exploitation: If the script is deployed in an insecure environment, it could be exploited by attackers to gain unauthorized access to the system.

Recommendations
Use Responsibly: Only use this script in environments where you have explicit permission to do so, such as your own systems or systems you are authorized to test.

Secure Your Environment: Ensure that any API tokens, chat IDs, or other sensitive information are kept secure and not exposed to unauthorized users.

Legal Compliance: Be aware of and comply with all applicable laws and regulations regarding system access, privacy, and data protection.

By using this code, you acknowledge and accept full responsibility for any actions taken with it. The author of this code is not responsible for any misuse, damage, or legal consequences that may arise from its use.

Features
Screen Recording: Record the screen for a specified duration.

Webcam Recording: Record video from the webcam.

Keylogging: Log keystrokes and send them to the bot owner.

Remote Commands: Execute system commands remotely.

Duckyscript Execution: Execute Duckyscript payloads.

Audio Recording: Record audio from the microphone.

Screenshot Capture: Take screenshots of the system.

Message Boxes: Display custom message boxes on the system.

System Control: Simulate system shutdowns or other actions.


```
/help: 
stop - Stops the bot.
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