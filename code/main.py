import Game
import os

if __name__ == "__main__":
    
    director_train = 'antrenare'
    director_rezultat = 'evaluare/fisiere_solutie/331_Miclea_Alexandru'
    director_sabloane = 'imagini_auxiliare/extras-cifre'
    cale_tabla_goala = 'imagini_auxiliare/tabla_goala.jpg'
    numar_jocuri = 4

    if not os.path.exists(director_rezultat):
        os.makedirs(director_rezultat)

    for i in range(numar_jocuri):
        numar_joc = str(i + 1)
        x = Game.Game(numar_joc, director_train, director_rezultat, director_sabloane, cale_tabla_goala)
