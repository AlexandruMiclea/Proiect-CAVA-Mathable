import numpy as np

def get_matrice_fara_piese():

    matrice = np.ones((14,14), dtype=np.int64) * -1
    matrice[6][6] = 1
    matrice[6][7] = 2
    matrice[7][6] = 3
    matrice[7][7] = 4

    return matrice

def get_matrice_reguli():
    matrice = np.full((14,14)," ")

    matrice[0,0] = "3"
    matrice[0,6] = "3"
    matrice[0,7] = "3"
    matrice[0,13] = "3"
    matrice[6,0] = "3"
    matrice[6,13] = "3"
    matrice[7,0] = "3"
    matrice[7,13] = "3"
    matrice[13,0] = "3"
    matrice[13,6] = "3"
    matrice[13,7] = "3"
    matrice[13,13] = "3"

    for i in range(1,5):
        matrice[i,i] = "2"
        matrice[13-i,13-i] = "2"
        matrice[i, 13 - i] = "2"
        matrice[13 - i, i] = "2"

    matrice[1,4] = '/'
    matrice[1,9] = '/'
    matrice[12,4] = '/'
    matrice[12,9] = '/'
    matrice[4,1] = '/'
    matrice[4,12] = '/'
    matrice[9,1] = '/'
    matrice[9,12] = '/'

    matrice[2,5] = '-'
    matrice[2,8] = '-'
    matrice[11,5] = '-'
    matrice[11,8] = '-'
    matrice[5,2] = '-'
    matrice[5,11] = '-'
    matrice[8,2] = '-'
    matrice[8,11] = '-'

    matrice[3,6] = '+'
    matrice[4,7] = '+'
    matrice[10,7] = '+'
    matrice[9,6] = '+'
    matrice[6,4] = '+'
    matrice[6,10] = '+'
    matrice[7,3] = '+'
    matrice[7,9] = '+'

    matrice[3,7] = '*'
    matrice[4,6] = '*'
    matrice[10,6] = '*'
    matrice[9,7] = '*'
    matrice[6,3] = '*'
    matrice[6,9] = '*'
    matrice[7,4] = '*'
    matrice[7,10] = '*'

    matrice[6,6] = 'x'
    matrice[6,7] = 'x'
    matrice[7,6] = 'x'
    matrice[7,7] = 'x'

    return matrice
