

from machine import I2C, Pin
from I2C_LCD import I2CLcd
import json, os
#import datetime
from time import sleep
import utime
import random
from moduleTP3 import Partie

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]

lcd = I2CLcd(i2c, I2C_ADDR, 2, 16)

ledA = Pin(13, Pin.OUT)
ledB = Pin(12, Pin.OUT)
ledC = Pin(10, Pin.OUT)
btnA = Pin(16, Pin.IN, Pin.PULL_UP)
btnB = Pin(17, Pin.IN, Pin.PULL_UP)
btnC = Pin(18, Pin.IN, Pin.PULL_UP)

print("|-----------------------------------------------------------------|")
print("|    Travail pratique 1 - Quiz 4B5 - Abdelhadi Mejdoubi           |")
print("|-----------------------------------------------------------------|")
print("| Choisissez la bonne réponse pour chaque question (a/b/c)        |")
print("| 2 joueurs max, droit de réplique si mauvaise réponse            |")
print("|-----------------------------------------------------------------|")
print("")

compteur = 0
fichierQuestions = "questions.json"

nom_joueur1 = input("Nom du joueur 1: ")
print("")
nom_joueur2 = input("Nom du joueur 2: ")

"""annee = datetime.datetime.now().year
mois = datetime.datetime.now().month
jour = datetime.datetime.now().day
heure = datetime.datetime.now().hour
minute = datetime.datetime.now().minute
seconde = datetime.datetime.now().second"""
#formatted_time = "{:02d}/{:02d}/{} {:02d}:{:02d}".format(current_time[2], current_time[1], current_time[0], current_time[3], current_time[4])
Partie = Partie(utime.localtime(),nom_joueur1, nom_joueur2, list([]), list([]), 0, 0, 0, 0)

# Cette partie du code sert à faire l'ordre de jeu des deux joueurs aléatoirement
listeJoueur = [nom_joueur1, nom_joueur2]
#random.shuffle(listeJoueur)
listeJoueur.sort(key=lambda x: random.random())

print("|-----------------------------------------------------------------|")
print("|                 Ordre de réponse aux questions                  |")
print("|-----------------------------------------------------------------|")
print("| 1- ", listeJoueur[0], "                                          ")
print("| 2- ", listeJoueur[1], "                                          ")
print("|-----------------------------------------------------------------|")
print("")

lcd.backlight_on()
lcd.putstr("Ordre joueurs : ")
sleep(2)
lcd.clear()
lcd.backlight_on()
lcd.putstr("1-" + listeJoueur[0] + "\n")
lcd.putstr("2-" + listeJoueur[1])
sleep(3)
lcd.clear()

# Importation des questions du fichier questions.json
with open(fichierQuestions, encoding='utf-8') as fic: 
    les_questions = json.load(fic)

# Boucle qui affiche les questions une par une
for question in les_questions:
    
    joueurEnJeu = listeJoueur.pop(0)
    listeJoueur.append(joueurEnJeu)
    
    
    
    compteur += 1
    print(str(compteur) + ") " +question["q"])
    print("<a>" + question["a"])
    print("<b>" + question["b"])
    print("<c>" + question["c"])
    print("")
    
    # Cette partie du code sert à donner le tour de jeu a chaque personne selon l'ordre de jeu ci-haut 
    
    
    reponse = input(joueurEnJeu + ", entrez votre réponse (a/b/c): ")
    
    if reponse == "a" or reponse == "b" or reponse == "c":
        
         
         
        # Condition si la réponse du joueur est bonne
        if reponse == question["rep"]:
            if joueurEnJeu == nom_joueur1:
                print("Bonne réponse!")
                print("")
                
                Partie.pointageJ1 = Partie.pointageJ1 + question["pts"]
                Partie.nb_bonnesrepJ1 = Partie.nb_bonnesrepJ1 + 1
                Partie.listeReponsesJ1.append(question[reponse])
                
            elif joueurEnJeu == nom_joueur2:
                print("Bonne réponse!")
                print("")
               
                Partie.pointageJ2 = Partie.pointageJ2 + question["pts"]
                Partie.nb_bonnesrepJ2 = Partie.nb_bonnesrepJ2 + 1
                Partie.listeReponsesJ2.append(question[reponse])
                
            
        # Condition si la réponse du joueur est fausse
        else:
            if joueurEnJeu == nom_joueur1:  
                Partie.listeReponsesJ1.append(question[reponse])
                joueurEnJeu = listeJoueur.pop(0)
                listeJoueur.append(joueurEnJeu)
                
                reponseReplique = input("Mauvaise réponse. Réplique à " + joueurEnJeu + " entrez votre réponse (a/b/c) ")
                
                 
                
                if reponseReplique == question["rep"]:
                    print("Bonne réponse!")
                    print("")
                    
                    Partie.pointageJ2 = Partie.pointageJ2 + question["pts"]
                    Partie.nb_bonnesrepJ2 = Partie.nb_bonnesrepJ2 + 1
                    Partie.listeReponsesJ2.append(question[reponseReplique])
                    
                    
                else:
                    print("Aucun joueur n'a eu la bonne réponse, la bonne réponse est " + question["rep"])
                    print("")
                    Partie.listeReponsesJ2.append(question[reponseReplique])
                    
            elif joueurEnJeu == nom_joueur2:
                Partie.listeReponsesJ2.append(question[reponse])
                joueurEnJeu = listeJoueur.pop(0)
                listeJoueur.append(joueurEnJeu)
                
                reponseReplique = input("Mauvaise réponse. Réplique à " + joueurEnJeu + " entrez votre réponse (a/b/c) ")
                
                  
                if reponseReplique == question["rep"]:
                    print("Bonne réponse!")
                    print("")
                    
                    Partie.pointageJ1 = Partie.pointageJ1 + question["pts"]
                    Partie.nb_bonnesrepJ1 = Partie.nb_bonnesrepJ1 + 1
                    Partie.listeReponsesJ1.append(question[reponseReplique])
                    
                else:
                    print("Aucun joueur n'a eu la bonne réponse, la bonne réponse est " + question["rep"])
                    print("")
                    Partie.listeReponsesJ1.append(question[reponseReplique])
                    

# Affichage des informations concernant la partie            
Partie.afficherPartie() 

