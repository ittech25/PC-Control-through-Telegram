"""
Attenzione, usando questo codice ti assumi la
responsabilità dei danni che puoi provocare.
Io, Davide Galilei, non mi assumo alcuna
responsabilità dell'uso che ne sarà fatto.
"""

apiId =  # Lo puoi trovare su my.telegram.org/apps
apiHash = "" # Idem per apiId
admin = [239556789] # Il tuo id di telegram
botToken = "" # Il token del bot che puoi trovare da @BotFather

start_message = (":) fai /help") # Messaggio iniziale
import os
import time
from pyrogram import Client, Filters
from pygame import mixer
import psutil
import pyscreenshot as ImageGrab
import random

start = """Sciao, ecco i comandi:
Spegni il pc /spegni
Check status /status
Killa fortnite /killfort
Kill epic launcher /killepic
Screenshot del pc /screenshot

Killa un processo:
€nomeprocesso secondi
Fai partire un suono:
!nomesuono secondi
Esegui un comando:
&secondi comando
Rimuovi un file:
-percorsofile

Invia un immagine con un caption (perc. file) per scaricarla.
:)"""

def greenSquare():
    return u'\U00002705'
def redSquare():
    return u'\U0000274C'
def notifyTelegramPoint():
    bot.send_message(admin[0], 'Fatto :)))))')

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def killFortnite():
    if(fortniteRunning()):
        os.system("taskkill /f /im FortniteClient-Win64-Shipping.exe")

def fortniteRunning():
    return checkIfProcessRunning("FortniteClient-Win64-Shipping.exe")

def killFortniteLauncher():
    if(fortniteLauncherRunning()):
        os.system("taskkill /f /im EpicGamesLauncher.exe")

def fortniteLauncherRunning():
    return checkIfProcessRunning("EpicGamesLauncher.exe")

def status():
    status = "Ecco lo stato:\n"
    if(fortniteLauncherRunning()):
        status = (status + "Epic Launcher " + greenSquare() + "\n")
    else:
        status = (status + "Epic Launcher " + redSquare() + "\n")

    if (fortniteRunning()):
        status = (status + "Fortnite " + greenSquare() + "\n")
    else:
        status = (status + "Fortnite " + redSquare() + "\n")
    bot.send_message(admin[0], status)
    
bot = Client(
    ":memory:",
    api_id=apiId,
    api_hash=apiHash,
    bot_token=botToken,
    workers=10)

@bot.on_message(Filters.user(admin) & Filters.text)
def run(Client, msg):
    text = msg['text']
    if not (msg.chat.id == admin[0]):
        bot.send_message(admin[0], "Questo bot è privato.")
        bot.send_message(admin[0], "qualcuno mi ha contattato, ecco le sue info:\n%s" %msg.chat.id)
    elif(text == '/status'):
        status()
        notifyTelegramPoint()
    elif (text == '/start'):
        bot.send_message(admin[0], start)
    elif(text == '/spegni'):
        bot.send_message(admin[0], "Sto spegnendo...")
        shutdownPc()
        notifyTelegramPoint()
    elif(text[0:9] == '/killfort'):
        time.sleep(int(text[10:]))
        killFortnite()
        notifyTelegramPoint()
    elif(text == '/screenshot'):
        im = ImageGrab.grab()
        im.save('screenshot.png')
        bot.send_photo(admin[0], "screenshot.png")
        os.remove("screenshot.png")
        notifyTelegramPoint()
    elif(text[0] == '€'): #Killa un processo
        temp = text.split()
        time.sleep(int(temp[1]))
        bot.send_message(admin[0], "Killo: %s" %temp[0][1:])
        os.system("taskkill /f /im " + temp[0][1:])
    elif(text[0] == '!'): #Fa partire un suono
        temp = text.split()
        time.sleep(int(temp[1]))
        bot.send_message(admin[0], "Suono: %s" %temp[0][1:])
        mixer.init()
        mixer.music.load(r"%s" %temp[0][1:])
        mixer.music.play()
    elif(text[0] == '&'): #Esegue un comando
        temp = text.split()
        time.sleep(int(temp[0][1:]))
        temp2 = [temp[i+1] for i in range(len(temp)-1)]
        temp2 = (r"%s" %" ".join(temp2))
        bot.send_message(admin[0], "Eseguo: %s" %temp2)
        os.system(r"%s" %temp2)
    elif(text[0] == '-'):
        bot.send_message(admin[0], "Rimuovo: %s" %text[1:])
        os.remove(r"%s" %text[1:])
    else:
        bot.send_message(admin[0], start)

@bot.on_message(Filters.user(admin) & Filters.media) #Serve per far scaricare file al bot quando li riceve
def download(Client, msg):
    text = msg.caption
    msg.download(text)
        
bot.run()
startAlert = 0
while (startAlert == 0):
    time.sleep(120) #Aspetta 2 minuti prima di avvisare, per essere sicuri che pyrogram sia partito
    bot.send_message(admin[0], "Computer avviato.")
    startAlert = 1
