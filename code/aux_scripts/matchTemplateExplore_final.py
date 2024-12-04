import cv2 as cv
import numpy as np
import os
 
img_rgb = cv.imread('imagini_generate/antrenare-patratele-1456/1_50.jpg.jpg')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

template_files = sorted(os.listdir("imagini_generate/extras-cifre"))

for file in template_files:
    rez = img_rgb.copy()
    if file[-3:] == 'jpg':
        template = cv.imread(f'imagini_generate/extras-cifre/{file}', cv.IMREAD_GRAYSCALE)
        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

        threshold = 0.9
        if file[:2] == '07':
            threshold = 0.8

        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            cv.rectangle(rez, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        #print('du')
        cv.imwrite(f'imagini_generate/template_matching_grayscale/TM_CCOEFF_NORMED_09/{file}',rez)