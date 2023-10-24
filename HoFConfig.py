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

def checkNewHighScores(user1, user2, time, newscore, language):
    HoFpath = os.getcwd() + "\Data\hallOfFame.txt"
    HoFFile = open(HoFpath, "r", encoding='utf-8')
    scores = HoFFile.read().splitlines()
    HoFFile.close()
    matrixScores = []
    for score in scores:
        p = score.split(" ")
        matrixScores.append(p)
    #print(matrixScores)
    if newscore <= float(matrixScores[4][1]):
        return 0
    else:
        facebook_messages.postTextToPage(user1, user2, time, language)
        matrixScores.append([user1, newscore])
        #print(matrixScores)
        sortedMatrix = sorted(matrixScores, key=lambda x: float(x[1]))
        sortedMatrix.reverse()
        archivo = open(HoFpath, "w", encoding='utf-8')
        for x in sortedMatrix:
            archivo.write(x[0]+" " + str(x[1]) + "\n")
        archivo.close()
        return 1


#checkNewHighScores("ESTEBAN", "Felipe", 100, 7895, "es")

