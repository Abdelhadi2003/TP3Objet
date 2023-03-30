class Partie:
    "classe qui comprend les informations sur la partie (date de la partie, nom, réponses, bonnes réponses et pointage de chacun des joueurs)"
   
    # Constructeur de la classe
    def __init__(self, datePartie, nomJoueur1, nomJoueur2, listeReponsesJ1, listeReponsesJ2, nb_bonnesrepJ1, nb_bonnesrepJ2, pointageJ1, pointageJ2):
        self.datePartie = datePartie
        self.nomJoueur1 = nomJoueur1
        self.nomJoueur2 = nomJoueur2
        self.listeReponsesJ1 = listeReponsesJ1
        self.listeReponsesJ2 = listeReponsesJ2
        self.nb_bonnesrepJ1 = nb_bonnesrepJ1
        self.nb_bonnesrepJ2 = nb_bonnesrepJ2 
        self.pointageJ1 = pointageJ1
        self.pointageJ2 = pointageJ2
    
    # Méthode qui retourne la date et le nom des joueurs de la partie pour représenter l’objet dans les boîtes de liste ou autres
    def __repr__(self):
        return self.datePartie + self.nomJoueur1 + self.nomJoueur2
    
    # Méthode qui permet de retourner dans la console, tous les attributs de l’objet sur une ou plusieurs lignes
    def afficherPartie(self):
        print("La date: "+ str(self.datePartie))
        print("Le nom du joueur 1: "+ self.nomJoueur1)
        print("Le nom du joueur 2: "+ self.nomJoueur2)
        print("La liste des réponses du joueur 1: "+ str(self.listeReponsesJ1))
        print("La liste des réponses du joueur 2: "+ str(self.listeReponsesJ2))
        print("Le nombre de bonnes reponses du joueur 1: " + str(self.nb_bonnesrepJ1))
        print("Le nombre de bonnes reponses du joueur 2: " + str(self.nb_bonnesrepJ2))
        print("le pointage du joueur 1: " + str(self.pointageJ1))
        print("le pointage du joueur 2: " + str(self.pointageJ2))