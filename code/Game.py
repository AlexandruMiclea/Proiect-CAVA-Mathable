import os
import cv2 as cv
import numpy as np
import GameState
import Constants

class Game:

    # directorul cu plansele
    # directorul unde se scrie
    # start joc
    # lista de game states
    # numarul jocului
    # functii care prelucreaza game states
    # fisierul de turns
    # matrice joc finala

    def __init__(self, numar_joc, director_train, director_rezultat, director_sabloane, cale_tabla_goala):

        print(f'Am inceput jocul cu numarul {numar_joc}')

        self.numar_joc = numar_joc
        self.director_train = director_train
        self.director_rezultat = director_rezultat
        self.director_sabloane = director_sabloane
        self.cale_tabla_goala = cale_tabla_goala
        self.lista_cai_imagini = self.get_lista_cai_imagini()
        self.placi_de_joc = self.extrage_placi_de_joc()
        self.matrice_finala = self.get_matrice_finala(self.placi_de_joc[50])
        self.stari_de_joc = self.genereaza_stari_de_joc()
        self.scrie_mutare_si_pozitie()
        self.scrie_scor_tura()

        print(f'Am completat jocul cu numarul {numar_joc}')

    def get_lista_cai_imagini(self):
        return sorted([img for img in os.listdir(self.director_train) if img[0] == self.numar_joc and img[-3:] == 'jpg'])
    
    def extrage_placi_de_joc(self):

        print(f'Am inceput prelucrarea planselor de joc')

        placi_de_joc = list()
        for i in range(51):
            if i == 0:
                placi_de_joc.append(self.extrage_teren_de_joc(self.cale_tabla_goala))
            else:
                placi_de_joc.append(self.extrage_teren_de_joc(f'{self.director_train}/{self.lista_cai_imagini[i-1]}'))

            print(f'Plansa {i} prelucrata')

        return placi_de_joc


    def genereaza_stari_de_joc(self):
        print('Incep analiza turelor de joc')

        stari_joc = list()
        matrice_aux = Constants.get_matrice_fara_piese()

        for i in range(1, 51):
            stare_joc = GameState.GameState(self.placi_de_joc[i - 1], self.placi_de_joc[i], i)

            pozitie = stare_joc.pozitie

            stare_joc.set_piece(self.matrice_finala[pozitie[0]][pozitie[1]])
            stare_joc.set_matrice_mutare_precedenta(matrice_aux.copy())

            matrice_aux[pozitie[0]][pozitie[1]] = self.matrice_finala[pozitie[0]][pozitie[1]]

            stari_joc.append(stare_joc)

        return stari_joc


    def extrage_teren_de_joc(self, cale_fisier):

        imagine = cv.imread(cale_fisier)

        imagine_hsv = cv.cvtColor(imagine,cv.COLOR_BGR2HSV)
        imagine_hsv[:,:,0] = (imagine_hsv[:,:,0] + 22) % 180
        imagine_thresh = cv.cvtColor(imagine_hsv, cv.COLOR_HSV2BGR)
        imagine_thresh = cv.cvtColor(imagine_thresh, cv.COLOR_BGR2GRAY)

        kernel = np.ones((3,3), np.float32) / 9
        imagine_thresh = cv.filter2D(imagine_thresh,-1,kernel)

        imagine_thresh[imagine_thresh < 165] = 0
        
        kernel = np.ones((15, 15), np.uint8)
        imagine_zone = cv.dilate(imagine_thresh, kernel)
        contururi, _ = cv.findContours(imagine_zone,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        zona_maximala = 0

        for i in range(len(contururi)):
            if(len(contururi[i]) > 3):
                stanga_sus_posibil = None
                dreapta_jos_posibil = None
                for punct in contururi[i].squeeze():
                    if stanga_sus_posibil is None or punct[0] + punct[1] < stanga_sus_posibil[0] + stanga_sus_posibil[1]:
                        stanga_sus_posibil = punct

                    if dreapta_jos_posibil is None or punct[0] + punct[1] > dreapta_jos_posibil[0] + dreapta_jos_posibil[1] :
                        dreapta_jos_posibil = punct

                diferenta = np.diff(contururi[i].squeeze(), axis = 1)
                dreapta_sus_posibil = contururi[i].squeeze()[np.argmin(diferenta)]
                stanga_jos_posibil = contururi[i].squeeze()[np.argmax(diferenta)]
                if cv.contourArea(np.array([[stanga_sus_posibil],[dreapta_sus_posibil],[dreapta_jos_posibil],[stanga_jos_posibil]])) > zona_maximala:
                    zona_maximala = cv.contourArea(np.array([[stanga_sus_posibil],[dreapta_sus_posibil],[dreapta_jos_posibil],[stanga_jos_posibil]]))
                    stanga_sus = stanga_sus_posibil
                    dreapta_jos = dreapta_jos_posibil
                    dreapta_sus = dreapta_sus_posibil
                    stanga_jos = stanga_jos_posibil

        latime = 1456 # divizibil cu un patrat de 104x104
        inaltime = 1456

        # pentru ca in coltul de stanga pot fi prezente artefacte, 
        # deduc coordonatele dupa celelalte puncte

        stanga_sus[0] = dreapta_sus[0] - latime
        stanga_sus[1] = stanga_jos[1] - inaltime

        careu_original = np.array([stanga_sus, dreapta_sus, stanga_jos, dreapta_jos], dtype= np.float32)
        careu_rezultat = np.array([[0,0], [latime, 0], [0, inaltime], [latime, inaltime]], dtype = np.float32)
        M = cv.getPerspectiveTransform(careu_original, careu_rezultat)
        rezultat = cv.warpPerspective(imagine, M, (latime, inaltime), flags = cv.INTER_LINEAR)

        return rezultat
    

    def get_matrice_finala(self, careu_joc_final):

        print(f'Prelucrez ultima mutare pentru a prelua configuratia finala a pieselor pe tabla')

        imagine_rgb = careu_joc_final
        imagine_grayscale = cv.cvtColor(imagine_rgb, cv.COLOR_BGR2GRAY)

        tabla_finala = Constants.get_matrice_fara_piese()
        tabla_voturi = [[[] for x in range(14)] for x in range(14)]

        cai_sabloane = sorted([img for img in os.listdir(self.director_sabloane) if img[-3:] == 'jpg'])

        for fisier in cai_sabloane:
            numar = int(fisier[:2])

            sablon = cv.imread(f'{self.director_sabloane}/{fisier}', cv.IMREAD_GRAYSCALE)

            res = cv.matchTemplate(imagine_grayscale,sablon,cv.TM_CCOEFF_NORMED)

            threshold = 0.9
            # 7 mai da rateuri, fac thresholdul mai mic
            if numar == 7:
                threshold = 0.8
            loc = np.where(res >= threshold)

            for punct_vot in zip(*loc):
                idx_lin = max((punct_vot[0] + 52), 0) // 104
                idx_col = max((punct_vot[1] + 52), 0) // 104
                tabla_voturi[idx_lin][idx_col].append(numar)

        for (idx_y,linie) in enumerate(tabla_voturi):
            for (idx_x,lista) in enumerate(linie):
                nparray = np.array(lista, dtype=np.int64)
                try:
                    tabla_finala[idx_y][idx_x] = np.bincount(nparray).argmax()
                except:
                    tabla_finala[idx_y][idx_x] = -1

        tabla_finala[6][6] = 1
        tabla_finala[6][7] = 2
        tabla_finala[7][6] = 3
        tabla_finala[7][7] = 4

        return tabla_finala
    
    def scrie_mutare_si_pozitie(self):

        for stare_joc in self.stari_de_joc:

            numar_miscare = stare_joc.numar_miscare
            pozitie_miscare = stare_joc.pozitie

            piesa = self.matrice_finala[pozitie_miscare[0]][pozitie_miscare[1]]

            stare_joc.get_scor_mutare()

            linie = str(pozitie_miscare[0] + 1)
            coloana = chr(65 + pozitie_miscare[1])

            len_nume = len(self.lista_cai_imagini[numar_miscare - 1])

            fisier_ans = self.lista_cai_imagini[numar_miscare - 1][:len_nume-3] + 'txt'

            with open(f'{self.director_rezultat}/{fisier_ans}', 'w') as file:
                file.write(f'{linie}{coloana} {piesa}')

    def scrie_scor_tura(self):

        sfarsit_ture = list()

        with open(f'{self.director_train}/{self.numar_joc}_turns.txt', 'r') as fisier_in:
            continut = fisier_in.readlines()
            for (idx,linie) in enumerate(continut):
                jucator, tura = linie.split(' ')
                if idx == 0:
                    jucator_1 = jucator

                sfarsit_ture.append(int(tura))

        sfarsit_ture.append(51)
        jucator_curent = jucator_1

        fisier_out = open(f'{self.director_rezultat}/{self.numar_joc}_scores.txt', 'w')

        for i in range(len(sfarsit_ture) - 1):
            scor_cumulat = 0

            prima_tura = sfarsit_ture[i]
            ultima_tura = sfarsit_ture[i + 1]

            for j in range(prima_tura, ultima_tura):
                scor_cumulat += self.stari_de_joc[j - 1].scor_total_mutare

            if i != len(sfarsit_ture) - 2:
                fisier_out.write(f"{jucator_curent} {prima_tura} {scor_cumulat}\n")
            else:
                fisier_out.write(f"{jucator_curent} {prima_tura} {scor_cumulat}")

            if (jucator_curent == 'Player1'):
                jucator_curent = 'Player2'
            else:
                jucator_curent = 'Player1'

        fisier_out.close()