from random import*
from collections import Counter

class Jeux:
    def __init__(self):
        """methode pour initialiser les parametre de la class Jeux"""
        self.motSecret=""
        self.nombreTentative=10
        self.listeLettreTest=[]
        self.motTester=0

    def lettrePresent(self,lettre,mot):
        """methode pour verifier si une lettre est dans un mot"""
        if lettre in mot:
            return True
        return False

    def erreurMot(self):
        """methode pour calculer le nombre d'erreur en comparant un liste avec des lettres a un mots"""
        result=0
        for lettre in self.listeLettreTest:
            if not self.lettrePresent(lettre,self.motSecret):
                result+=1
        return result

    def motIncomplet(self):
        """methode pour mettre a jour le mot incomplet en regardant si des lettres d'une liste sont dans le mots (mettre un _ si la lettre n'es pas present dans le mot)"""
        result=""
        for lettre in self.motSecret:
            if lettre in self.listeLettreTest:
                result+=f'{lettre} '
            else:
                result+="_ "
        return result

    def motPareil(self,mot2):
        """methode pour voir si 2 mots sont pareil"""
        if self.motSecret.lower()==mot2.lower():
            return True
        return False
    
    def reset(self):
        """methode pour reset les parametre de la class"""
        self.motSecret=""
        self.nombreTentative=10
        self.listeLettreTest=[]
        self.motTester=0
    def show(self):
        """methode pour calculer le nombre de coup restant et renvoyer le mot incomplet"""
        totalErreur=self.erreurMot()+2*self.motTester
        self.nombreTentative=10-totalErreur
        return self.motIncomplet()
    
    def coup(self,motUtilisateur):
        """methode pour tester un mot"""
        if self.motPareil(motUtilisateur):
            return True
        else:
            self.motTester+=1
            return False
        
class Bot:
    def __init__(self):
        """methode pour initialiser les parametre de la class Bot"""
        self.alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.contenu=self.listMot()
    
    def listMot(self):
        """methode pour recuperer tout les mots de mot.txt"""
        with open('./donnee/mot.txt','r') as f:
            contenu = f.readlines()
        contenu=[a.strip() for a in contenu]
        return contenu
        
    def taillePareil(self,longeur):
        """methode pour garder que les mots de la même taille que le mots secret"""
        self.contenu=[a for a in self.contenu if len(a)==longeur]
    
    def bonMot(self,motIncomplet):
        """methode pour garder que les mots qui on les meme lettre que les lettre decouverte du mot secret au bonne place"""
        nouvelleListe=[]
        for mot in self.contenu:
            correct=True
            for lettre in range(len(motIncomplet)):
                if motIncomplet[lettre]!='_' and mot[lettre]!=motIncomplet[lettre]:
                    correct=False
                    break
            if correct:
                nouvelleListe.append(mot)
        self.contenu=nouvelleListe
        self.bonneLettre()
    def bonneLettre(self):
        """methode pourpour garder que les lettre presente dans les mots restant"""
        nouveauxAlphabet=[]
        for lettre in self.alphabet:
            correct=False
            for mot in self.contenu:
                 if lettre in mot:
                     correct=True
                     break
            if correct:
                nouveauxAlphabet.append(lettre)
        self.alphabet=nouveauxAlphabet
    def lettrePlusFrequente(self):
        """methode pour renvoyer la lettre la plus presentes"""
        compteur=Counter()
        for mot in self.contenu:
            for lettre in set(mot):
                if lettre in self.alphabet:
                    compteur[lettre]+=1
        return compteur.most_common(1)[0][0]