liste=[100,520,1,97,34,76,541,87,45,12,9,67,89,150]

"""On donne au variable les premieres valeurs de la liste"""
indice_maximun=0
maximun=liste[indice_maximun]
#On parcourt toute la liste
for i in range(len(liste)):
    #Si la valeur actuelle est plus grande que le maximum
    if liste[i]>maximun:
        #alors on met a jour l'indice du maximum et la valeur du maximum
        indice_maximun=i
        maximun=liste[indice_maximun]
        
print(indice_maximun,maximun)