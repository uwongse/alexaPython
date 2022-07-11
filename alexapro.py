import datetime
import pywhatkit
import speech_recognition as sr
import pyttsx3 as pytt
import wikipedia
from pygame import mixer
import keyboard
from datetime import date, timedelta
import webbrowser
import serial
import operator
import random
import os
import pyautogui
import cv2 
import pyautogui
import numpy as np
import time
import colors as colors
import subprocess as sub

listener = sr.Recognizer()
rec = sr.Microphone()

engine =pytt.init()

voices =engine.getProperty('voices')
rate = engine.getProperty('rate')  
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate', 130)

sites={
    'google':'google.com',
    'youtube':'youtube.com',
    'facebook':'facebook.com',
    'twitter':'twitter.com',
    'orange':'orangetv.orange.es',

}


name ='alexa'

class Alexa:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.rec = sr.Microphone()

    def talk(self,text):
        engine.say(text)
        engine.runAndWait()

    def start_conversation_log(self):
        today = str(date.today())
        today = today

        with open(r'Conversation_Log.txt', "a") as f:
            f.write("Conversation started on: " + today + "\n")

    def remember(self, command):
        with open(r"Conversation_Log.txt", "a") as f:
            f.write("usuario: " + command + "\n")


    def captura(self):
        hora= datetime.datetime.now().strftime('%d %m %H %M %S')
        captura=pyautogui.screenshot()
        namecaptura="captura"+str(hora)+".png"
        captura.save(namecaptura)
        self.talk("captura realizada, este es el resultado")
        sub.Popen(namecaptura, shell=True)

    def capturaVideo(self):
        hora= datetime.datetime.now().strftime('%H %M %S')
        filename="Grabacion"+str(hora)+".avi"
        codec = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, codec , 60, (1920, 1080))
        cv2.namedWindow("Grabando", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Grabando", 480, 270)
        
        while True:
            img = pyautogui.screenshot() # tomamos un pantallazo
            frame = np.array(img) # convertimos la imagen a un arreglo de numeros
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convertimos la imagen BGR a RGB
            out.write(frame) # adjuntamos al archivo de video
            cv2.imshow('Grabando', frame) # mostramos el cuadro que acabamos de grabar
            if cv2.waitKey(1) == ord('s'): # si el usuario presiona q paramos de grabar.
                
                break
                

        out.release() # cerrar el archivo de video
        cv2.destroyAllWindows() # cerrar la ventana    
        self.talk("listo, este es el resultado")
        sub.Popen(filename, shell=True)

    def wishMe(self):
        hour=datetime.datetime.now().hour
        if hour>=6 and hour<13:
            self.talk("hola, buenos dias soy alexa")
            
        elif hour>=13 and hour<20:
            self.talk("hola, buenas tardes soy alexa")
            
        else:
            self.talk("hola, buenas noches soy alexa")

    def write(self,file):
        self.talk("¿que quieres que escriba?")
        rec_write= self.listen()

        file.write(rec_write )
        time.sleep(5)
        self.talk("listo, puede revisarlo")
        file.close()


    
    def listen(self):
        
        while True:
           
            try:
                with rec as source:

                    print("Escuchando...")
                    
                    listener.adjust_for_ambient_noise(source)
                    listener.dynamic_energy_threshold = 3000
                    
                    audio = listener.listen(source, timeout=9.0)
                    command = listener.recognize_google(audio, language="es")
                    command = command.lower()
                    if name in command:
                        command= command.replace(name,'')
                        self.remember(command)
                    
            except :
                pass
            return command

    def run(self,rec):   

        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            self.talk('Reproduciendo ' + music)
            pywhatkit.playonyt(music, use_api=True)

        elif 'busca en wikipedia' in rec:
            order=rec.replace('busca en wikipedia', '')
            wikipedia.set_lang("es")
            info=wikipedia.summary(order, 2)
            self.talk(info)
            
        elif 'hora es' in rec:
            hora= datetime.datetime.now().strftime('%I:%M %p')
            self.talk("son las " +hora)
            
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    self.talk(f'abriendo{site}')
                    
        elif 'descargas' in rec:
            self.talk("abriendo descargas")
            os.startfile(r"C:\Users\mario\Downloads")

        elif 'mis documentos' in rec:
            self.talk("abriendo mis documentos")
            os.startfile(r"C:\Users\mario\Documents")

        elif 'captura de pantalla' in rec:
            self.captura()
            
        elif 'graba pantalla' in rec:
            self.capturaVideo()  

        elif 'captura de vídeo' in rec:
            self.capturaVideo() 

        elif 'cámara de colores' in rec:
            self.talk("abriendo camara")
            colors.capture()
        elif 'escribe una nota' in rec:    
            try:
                hora= datetime.datetime.now().strftime('%d %m %H %M ')
                nota="nota"+str(hora)+".txt"
                with open(nota,'a')as f:
                    self.write(f)
            except FileNotFoundError as e:
                file=open(nota, 'a')
                self.write(file)
            sub.Popen(nota, shell=True)

        elif 'alarma' in rec:
            alarma=rec.replace('alarma', '')
            alarma=alarma.strip()
            self.talk("alarma activada a las "+ alarma +" horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M')==alarma:
                    print("despierta")
                    mixer.init()
                    mixer.music.load(r"alarma.mp3")
                    mixer.music.play()
                    if keyboard.read_key=="s":
                        mixer.music.stop()
                        break

        
        else:
            self.talk("no le escucho")
            
if __name__ == "__main__":
    s=Alexa()
    s.start_conversation_log()
    s.wishMe()
    while True:
        try:
            oido=s.listen()
            s.run(oido)                     
        except:
            pass   