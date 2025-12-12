from random import*
from collections import Counter

class Jeux:
    def __init__(self):
        self.motSecret=""
        self.nombreTentative=10
        self.listeLettreTest=[]
        self.motTester=0

    def lettrePresent(self,lettre,mot):
        if lettre in mot:
            return True
        return False

    def erreurMot(self):
        result=0
        for lettre in self.listeLettreTest:
            if not self.lettrePresent(lettre,self.motSecret):
                result+=1
        return result

    def motIncomplet(self):
        result=""
        for lettre in self.motSecret:
            if lettre in self.listeLettreTest:
                result+=f'{lettre} '
            else:
                result+="_ "
        return result

    def motPareil(self,mot2):
        if self.motSecret.lower()==mot2.lower():
            return True
        return False
    
    def reset(self):
        self.motSecret=""
        self.nombreTentative=10
        self.listeLettreTest=[]
        self.motTester=0
    def show(self):
        totalErreur=self.erreurMot()+2*self.motTester
        self.nombreTentative=10-totalErreur
        return self.motIncomplet()
    
    def coup(self,motUtilisateur):
        if self.motPareil(motUtilisateur):
            return True
        else:
            self.motTester+=1
            return False
        
class Bot:

    def __init__(self):
        self.alphabet=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.contenu=self.listMot()

    
    def listMot(self):
        with open('mot.txt', 'r') as f:
            contenu = f.readlines()
        contenu=[a.strip() for a in contenu]
        return contenu
        
    def taillePareil(self,longeur):
        self.contenu=[a for a in self.contenu if len(a)==longeur]
    
    def bonMot(self,motIncomplet):
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
        compteur=Counter()
        for mot in self.contenu:
            for lettre in set(mot):
                if lettre in self.alphabet:
                    compteur[lettre]+=1
        return compteur.most_common(1)[0][0]