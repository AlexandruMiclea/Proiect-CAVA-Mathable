import cv2 as cv
import numpy as np
import os
import Constants
 
img_rgb = cv.imread('imagini_generate/antrenare-patratele-1456/3_50.jpg.jpg')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

tabla_finala = Constants.get_matrice_fara_piese()
tabla_voturi = [[[] for x in range(14)] for x in range(14)]

template_files = sorted(os.listdir("imagini_generate/extras-cifre"))

for file in template_files:
    rez = img_rgb.copy()
    if file[-3:] == 'jpg':
        number = int(file[:2])
        #print(number)

        template = cv.imread(f'imagini_generate/extras-cifre/{file}', cv.IMREAD_GRAYSCALE)
        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

        threshold = 0.9
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            x_bin = max((pt[1] + 52), 0) // 104
            y_bin = max((pt[0] + 52), 0) // 104
            tabla_voturi[x_bin][y_bin].append(number)
            #cv.rectangle(rez, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        #print('du')
        #cv.imwrite(f'imagini_generate/template_matching_grayscale/TM_CCOEFF_NORMED_09/{file}',rez)

for (idx_y,linie) in enumerate(tabla_voturi):
    for (idx_x,lista) in enumerate(linie):
        nparray = np.array(lista, dtype=np.int64)
        try:
            tabla_finala[idx_y][idx_x] = np.bincount(nparray).argmax()
        except:
            tabla_finala[idx_y][idx_x] = -1

print(tabla_finala)
