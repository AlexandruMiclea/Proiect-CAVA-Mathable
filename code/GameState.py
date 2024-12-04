import cv2 as cv
import numpy as np
import Constants

class GameState:

    # imaginea din care am extras careul
    # imaginea de la miscarea precedenta
    # numarul miscarii
    # coordonatele la care s-a facut miscarea

    def __init__(self, careu_mutare_precedenta, careu_mutare_curenta, numar_miscare):
        self.numar_miscare = numar_miscare
        self.pozitie = self.calculeaza_pozitie_mutare(careu_mutare_precedenta, careu_mutare_curenta)
        self.multiplicatori = Constants.get_matrice_reguli()

    def set_matrice_mutare_precedenta(self, matrice):
        self.matrice_mutare_precedenta = matrice

    def set_piece(self, numar_piesa):
        self.numar_piesa = numar_piesa

    def calculeaza_pozitie_mutare(self, careu_mutare_precedenta, careu_mutare_curenta):

        print(f'Calculez pozitia mutarii pentru tura {self.numar_miscare}')

        careu_mutare_precedenta = cv.cvtColor(careu_mutare_precedenta, cv.COLOR_BGR2GRAY)
        careu_mutare_curenta = cv.cvtColor(careu_mutare_curenta, cv.COLOR_BGR2GRAY)

        imagine_diferenta = np.abs(np.array(careu_mutare_precedenta) - np.array(careu_mutare_curenta))

        thresh_high = 220
        thresh_low = 100

        imagine_diferenta_thresh = imagine_diferenta.copy()
        imagine_diferenta_thresh[imagine_diferenta_thresh < thresh_low] = 0
        imagine_diferenta_thresh[imagine_diferenta_thresh > thresh_high] = 0
        imagine_diferenta_thresh[imagine_diferenta_thresh != 0] = 255

        ker = np.ones((3,3))
        imagine_diferenta_thresh = cv.erode(imagine_diferenta_thresh, ker)
        coordonate_ferestre = list()

        for i in range(0, 1455, 104):
            for j in range(0, 1455, 104):
                # x min x max y min y max
                x_min = max(j - 10,0)
                x_max = min(j + 114,1455)
                y_min = max(i - 10,0)
                y_max = min(i + 114,1455)
                coordonate_ferestre.append([x_min, x_max, y_min, y_max])

        idx_max = -1
        val_max = -1

        for (idx,elem) in enumerate(coordonate_ferestre):
            val = np.mean(imagine_diferenta_thresh[elem[2]:elem[3], elem[0]:elem[1]])
            if (np.isnan(val)):
                continue
            if (val > val_max):
                val_max = val
                idx_max = idx

        return (idx_max // 14, idx_max % 14)
    
    def get_scor_mutare(self):

        valoare = self.numar_piesa
        valoare *= self.get_indice_multiplicare_expresii()

        if self.multiplicatori[self.pozitie[0]][self.pozitie[1]] in ["2", "3"]:
            multiplicator = int(self.multiplicatori[self.pozitie[0]][self.pozitie[1]])

            valoare *= multiplicator

        self.scor_total_mutare = valoare

        return valoare
    
    def verifica_constrangere_expresie(self, coordonate_1, coordonate_2):
        piesa_1 = self.matrice_mutare_precedenta[coordonate_1[0]][coordonate_1[1]]
        piesa_2 = self.matrice_mutare_precedenta[coordonate_2[0]][coordonate_2[1]]

        if (piesa_1 == -1 or piesa_2 == -1):
            return 0
        
        op_ceruta = self.multiplicatori[self.pozitie[0]][self.pozitie[1]]

        if (op_ceruta in ['/', '*', '+', '-']):
            if (op_ceruta == '+'):
                if (int(piesa_1) + int(piesa_2) == int(self.numar_piesa)):
                    return 1
                else:
                    return 0
            if (op_ceruta == '-'):
                if (abs(int(piesa_1) - int(piesa_2)) == int(self.numar_piesa)):
                    return 1
                else:
                    return 0

            if (op_ceruta == '*'):
                if (int(piesa_1) * int(piesa_2) == int(self.numar_piesa)):
                    return 1
                else:
                    return 0

            if (op_ceruta == '/'):
                if (piesa_2 != 0):
                    if (int(piesa_1) // int(piesa_2) == int(self.numar_piesa)):
                        return 1
                if (piesa_1 != 0):
                    if (int(piesa_2) // int(piesa_1) == int(self.numar_piesa)):
                        return 1
                return 0    
        else:
            if (int(piesa_1) + int(piesa_2) == int(self.numar_piesa)):
                return 1
            
            if (abs(int(piesa_1) - int(piesa_2)) == int(self.numar_piesa)):
                return 1
            
            if (int(piesa_1) * int(piesa_2) == int(self.numar_piesa)):
                return 1
            
            if (piesa_2 != 0):
                if (int(piesa_1) // int(piesa_2) == int(self.numar_piesa)):
                    return 1
            
            if (piesa_1 != 0):
                if (int(piesa_2) // int(piesa_1) == int(self.numar_piesa)):
                    return 1

        return 0
    
    def get_indice_multiplicare_expresii(self):
        pozitie = list(self.pozitie)

        numar_expresii = 0

        if (pozitie[1] >= 2):
            pozitie_1 = pozitie.copy()
            pozitie_2 = pozitie.copy()
            pozitie_1[1] = pozitie_1[1] - 1
            pozitie_2[1] = pozitie_2[1] - 2
            numar_expresii += self.verifica_constrangere_expresie(pozitie_1, pozitie_2)

        if (pozitie[1] <= 11):
            pozitie_1 = pozitie.copy()
            pozitie_2 = pozitie.copy()
            pozitie_1[1] = pozitie_1[1] + 1
            pozitie_2[1] = pozitie_2[1] + 2
            numar_expresii += self.verifica_constrangere_expresie(pozitie_1, pozitie_2)

        if (pozitie[0] >= 2):
            pozitie_1 = pozitie.copy()
            pozitie_2 = pozitie.copy()
            pozitie_1[0] = pozitie_1[0] - 1
            pozitie_2[0] = pozitie_2[0] - 2
            numar_expresii += self.verifica_constrangere_expresie(pozitie_1, pozitie_2)

        if (pozitie[0] <= 11):
            pozitie_1 = pozitie.copy()
            pozitie_2 = pozitie.copy()
            pozitie_1[0] = pozitie_1[0] + 1
            pozitie_2[0] = pozitie_2[0] + 2
            numar_expresii += self.verifica_constrangere_expresie(pozitie_1, pozitie_2)

        return numar_expresii