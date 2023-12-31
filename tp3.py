

from machine import I2C, Pin
from I2C_LCD import I2CLcd
import json, os
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

# Fonction qui permet de retourner la lettre qui est relié au bouton cliqué
def lire_reponse_bouton():
    while True:
        if not btnA.value():
            ledA.value(1)
            sleep(1)
            ledA.value(0)
            return "a"
        elif not btnB.value():
            ledB.value(1)
            sleep(1)
            ledB.value(0)
            return "b"
        elif not btnC.value():
            ledC.value(1)
            sleep(1)
            ledC.value(0)
            return "c"

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

# Boucle qui valide si le nom du joueur 1 est vide
while len(nom_joueur1) == 0:
    nom_joueur1 = input("Nom du joueur 1: ")
    print("")
    
nom_joueur2 = input("Nom du joueur 2: ")
print("")

# Boucle qui valide si le nom du joueur 2 est vide
while len(nom_joueur2) == 0:
    nom_joueur2 = input("Nom du joueur 2: ")
    print("")

formatted_time = "{:02d}/{:02d}/{} {:02d}:{:02d}".format(
    utime.localtime()[2],   # jour du mois
    utime.localtime()[1],   # mois
    utime.localtime()[0],   # année
    utime.localtime()[3],   # heure
    utime.localtime()[4]    # minute
)
Partie = Partie(formatted_time,nom_joueur1, nom_joueur2, list([]), list([]), 0, 0, 0, 0)

# Cette partie du code sert à faire l'ordre de jeu des deux joueurs aléatoirement
listeJoueur = [nom_joueur1, nom_joueur2]
listeJoueur.sort(key=lambda x: random.random())

print("|-----------------------------------------------------------------|")
print("|                 Ordre de réponse aux questions                  |")
print("|-----------------------------------------------------------------|")
print("| 1- ", listeJoueur[0], "                                          ")
print("| 2- ", listeJoueur[1], "                                          ")
print("|-----------------------------------------------------------------|")
print("")

# Affichage de l'ordre des joueurs dans le LCD
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
    
    # Affichage du tour de jeu dans le LCD 
    lcd.backlight_on()
    lcd.putstr("C'est le tour de")
    lcd.putstr(joueurEnJeu)
    sleep(2)
    lcd.clear()
    
    compteur += 1
    print(str(compteur) + ") " +question["q"])
    print("<a>" + question["a"])
    print("<b>" + question["b"])
    print("<c>" + question["c"])
    print("")
    
    print(joueurEnJeu + ", entrez votre réponse en cliquant sur le bouton relié à la lettre voulu (a/b/c)")
    print("")
    
    # La variable reponse prend la valeur retourné de la méthode lire_reponse_bouton()
    reponse = lire_reponse_bouton()
    
    if reponse == "a" or reponse == "b" or reponse == "c":
        
        # Affichage de la lettre entrée par le joueur dans le LCD
        lcd.backlight_on()
        lcd.putstr(joueurEnJeu +  " a entrer" + "\n" + "la lettre " + reponse )
        sleep(2)
        lcd.clear()  
         
        # Condition si la réponse du joueur est bonne
        if reponse == question["rep"]:
            if joueurEnJeu == nom_joueur1:
                
                # Affichage du message "Bonne reponse" dans le LCD si la réponse du joueur est bonne
                lcd.backlight_on()
                lcd.putstr("Bonne reponse!")
                sleep(2)
                lcd.clear() 
                
                Partie.pointageJ1 = Partie.pointageJ1 + question["pts"]
                Partie.nb_bonnesrepJ1 = Partie.nb_bonnesrepJ1 + 1
                Partie.listeReponsesJ1.append(question[reponse])
                
                # Condition pour afficher le pointage du tour si le compteur de question est moins de 10 dans le LCD et pour afficher le pointage final si le compteur de question est égale à 10 dans le LCD
                if compteur == 10:
                    lcd.backlight_on()
                    lcd.putstr("Pointage final\n")
                    lcd.putstr("des deux joueurs")
                    sleep(3)
                    lcd.clear()
                    lcd.backlight_on()
                    lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                    lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                    sleep(2)
                    break
                else:
                    lcd.backlight_on()
                    lcd.putstr("Pointage du tour")
                    lcd.putstr("des deux joueurs")
                    sleep(3)
                    lcd.clear()
                    lcd.backlight_on()
                    lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                    lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                    sleep(3)
                    lcd.clear() 
            elif joueurEnJeu == nom_joueur2:
                
                # Affichage du message "Bonne reponse" dans le LCD si la réponse du joueur est bonne
                lcd.backlight_on()
                lcd.putstr("Bonne reponse!")
                sleep(2)
                lcd.clear()
                
                Partie.pointageJ2 = Partie.pointageJ2 + question["pts"]
                Partie.nb_bonnesrepJ2 = Partie.nb_bonnesrepJ2 + 1
                Partie.listeReponsesJ2.append(question[reponse])
                
                # Condition pour afficher le pointage du tour si le compteur de question est moins de 10 dans le LCD et pour afficher le pointage final si le compteur de question est égale à 10 dans le LCD
                if compteur == 10:
                    lcd.backlight_on()
                    lcd.putstr("Pointage final\n")
                    lcd.putstr("des deux joueurs")
                    sleep(3)
                    lcd.clear()
                    lcd.backlight_on()
                    lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                    lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                    sleep(2)
                    break
                else:        
                    lcd.backlight_on()
                    lcd.putstr("Pointage du tour")
                    lcd.putstr("des deux joueurs")
                    sleep(3)
                    lcd.clear()
                    lcd.backlight_on()
                    lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                    lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                    sleep(3)
                    lcd.clear() 
            
        # Condition si la réponse du joueur est fausse
        else:
            if joueurEnJeu == nom_joueur1:  
                Partie.listeReponsesJ1.append(question[reponse])
                joueurEnJeu = listeJoueur.pop(0)
                listeJoueur.append(joueurEnJeu)
                
                # Affichage du message "Mauvaise reponse" et "Replique de" dans le LCD si la réponse du joueur est mauvaise
                lcd.backlight_on()
                lcd.putstr("Mauvaise reponse")
                sleep(2)
                lcd.clear()
                lcd.backlight_on()
                lcd.putstr("Replique de \n")
                lcd.putstr(joueurEnJeu)
                sleep(2)
                lcd.clear()
                
                # La variable reponseReplique prend la valeur retourné de la méthode lire_reponse_bouton()
                reponseReplique = lire_reponse_bouton()
                
                # Affichage de la lettre entrée par le joueur dans le LCD
                lcd.backlight_on()
                lcd.putstr(joueurEnJeu +  " a entrer" + "\n" + "la lettre " + reponseReplique )
                sleep(2)
                lcd.clear()  
                
                if reponseReplique == question["rep"]:
                    
                    # Affichage du message "Bonne reponse" dans le LCD si la réponse du joueur est bonne
                    lcd.backlight_on()
                    lcd.putstr("Bonne reponse!")
                    sleep(2)
                    lcd.clear()
                    
                    Partie.pointageJ2 = Partie.pointageJ2 + question["pts"]
                    Partie.nb_bonnesrepJ2 = Partie.nb_bonnesrepJ2 + 1
                    Partie.listeReponsesJ2.append(question[reponseReplique])
                    
                    # Condition pour afficher le pointage du tour si le compteur de question est moins de 10 dans le LCD et pour afficher le pointage final si le compteur de question est égale à 10 dans le LCD
                    if compteur == 10:
                        lcd.backlight_on()
                        lcd.putstr("Pointage final\n")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(2)
                        break
                    else:        
                        lcd.backlight_on()
                        lcd.putstr("Pointage du tour")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(3)
                        lcd.clear() 
                    
                else:
                    # Condition pour faire clignoter la lumière led attribué à la lettre qui représente la bonne réponse lorsque les deux joueurs ont eu une mauvaise réponse
                    if question["rep"] == "a":
                        for i in range(4):
                            ledA.value(1)
                            sleep(0.5)
                            ledA.value(0)
                            sleep(0.5)
                    elif question["rep"] == "b":
                        for i in range(4):
                            ledB.value(1)
                            sleep(0.5)
                            ledB.value(0)
                            sleep(0.5)
                    elif question["rep"] == "c":
                        for i in range(4):
                            ledC.value(1)
                            sleep(0.5)
                            ledC.value(0)
                            sleep(0.5)
                    
                    Partie.listeReponsesJ2.append(question[reponseReplique])
                    
                    # Condition pour afficher le pointage du tour si le compteur de question est moins de 10 dans le LCD et pour afficher le pointage final si le compteur de question est égale à 10 dans le LCD
                    if compteur == 10:
                        lcd.backlight_on()
                        lcd.putstr("Pointage final\n")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(2)
                        break
                    else:        
                        lcd.backlight_on()
                        lcd.putstr("Pointage du tour")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(3)
                        lcd.clear() 
            elif joueurEnJeu == nom_joueur2:
                Partie.listeReponsesJ2.append(question[reponse])
                joueurEnJeu = listeJoueur.pop(0)
                listeJoueur.append(joueurEnJeu)
                
                # Affichage du message "Mauvaise reponse" et "Replique de" dans le LCD si la réponse du joueur est mauvaise
                lcd.backlight_on()
                lcd.putstr("Mauvaise reponse")
                sleep(2)
                lcd.clear()
                lcd.backlight_on()
                lcd.putstr("Replique de \n")
                lcd.putstr(joueurEnJeu)
                sleep(2)
                lcd.clear()
                
                # La variable reponseReplique prend la valeur retourné de la méthode lire_reponse_bouton()
                reponseReplique = lire_reponse_bouton()
                
                # Affichage de la lettre entrée par le joueur dans le LCD
                lcd.backlight_on()
                lcd.putstr(joueurEnJeu +  " a entrer" + "\n" + "la lettre " + reponseReplique )
                sleep(2)
                lcd.clear() 
                  
                if reponseReplique == question["rep"]:
                    
                    # Affichage du message "Bonne reponse" dans le LCD si la réponse du joueur est bonne
                    lcd.backlight_on()
                    lcd.putstr("Bonne reponse!")
                    sleep(2)
                    lcd.clear()
                    
                    Partie.pointageJ1 = Partie.pointageJ1 + question["pts"]
                    Partie.nb_bonnesrepJ1 = Partie.nb_bonnesrepJ1 + 1
                    Partie.listeReponsesJ1.append(question[reponseReplique])
                    
                    # Condition pour afficher le pointage du tour si le compteur de question est moins de 10 dans le LCD et pour afficher le pointage final si le compteur de question est égale à 10 dans le LCD
                    if compteur == 10:
                        lcd.backlight_on()
                        lcd.putstr("Pointage final\n")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(2)
                        break
                    else:        
                        lcd.backlight_on()
                        lcd.putstr("Pointage du tour")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(3)
                        lcd.clear()  
                else:
                    # Condition pour faire clignoter la lumière led attribué à la lettre qui représente la bonne réponse lorsque les deux joueurs ont eu une mauvaise réponse
                    if question["rep"] == "a":
                        for i in range(4):
                            ledA.value(1)
                            sleep(0.5)
                            ledA.value(0)
                            sleep(0.5)
                    elif question["rep"] == "b":
                        for i in range(4):
                            ledB.value(1)
                            sleep(0.5)
                            ledB.value(0)
                            sleep(0.5)
                    elif question["rep"] == "c":
                        for i in range(4):
                            ledC.value(1)
                            sleep(0.5)
                            ledC.value(0)
                            sleep(0.5)
                    
                    Partie.listeReponsesJ1.append(question[reponseReplique])
                    
                    # Condition pour afficher le pointage du tour si le compteur de question est moins de 10 dans le LCD et aussi pour afficher le pointage final si le compteur de question est égale à 10 dans le LCD
                    if compteur == 10:
                        lcd.backlight_on()
                        lcd.putstr("Pointage final\n")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(2)
                        break
                    else:        
                        lcd.backlight_on()
                        lcd.putstr("Pointage du tour")
                        lcd.putstr("des deux joueurs")
                        sleep(3)
                        lcd.clear()
                        lcd.backlight_on()
                        lcd.putstr(nom_joueur1 + " : "+str(Partie.pointageJ1) + " ptns\n")
                        lcd.putstr(nom_joueur2 + " : "+str(Partie.pointageJ2) + " ptns\n")
                        sleep(3)
                        lcd.clear() 

# Affichage des informations concernant la partie            
Partie.afficherPartie() 

