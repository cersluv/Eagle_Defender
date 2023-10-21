import os
import numpy as np

import facebook_messages
from facebook_messages import postTextToPage

def getMatrixScores():
    HoFpath = os.getcwd() + "\\Data\\hallOfFame.txt"
    HoFFile = open(HoFpath, "r", encoding='utf-8')
    scores = HoFFile.read().splitlines()
    matrixScores = []
    for score in scores:
        p = score.split(" ")
        matrixScores.append(p)

    return matrixScores

def checkNewHighscores(user1, user2, time, newscore, language):
    HoFpath = os.getcwd() + "\Data\hallOfFame.txt"
    HoFFile = open(HoFpath, "r", encoding='utf-8')
    scores = HoFFile.read().splitlines()
    HoFFile.close()
    matrixScores = []
    for score in scores:
        p = score.split(" ")
        matrixScores.append(p)
    print(matrixScores[4][1])
    if newscore <= int(matrixScores[4][1]):
        print("esoooon´t") # no pasa nada.
    else:
        print("esoooo") #se llama acá a la publicación de facebook.
        facebook_messages.postTextToPage(user1, user2, time, language)
        matrixScores.append([user1, newscore])
        numpyMatrix = np.array(matrixScores)
        sortedMatrix = numpyMatrix[numpyMatrix[:, 1].argsort()[::-1]]
        sortedMatrix = sortedMatrix.tolist()
        archivo = open(HoFpath, "w", encoding='utf-8')
        for x in sortedMatrix:
            archivo.write(x[0]+" " + x[1] + "\n")
        archivo.close()
#checkNewHighscores("carlos", 500)