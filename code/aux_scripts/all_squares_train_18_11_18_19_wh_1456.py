import cv2 as cv
import numpy as np
import os

def show_image(fileout,image):
    image=cv.resize(image,(0,0),fx=0.3,fy=0.3)
    cv.imwrite(fileout, image)

def extract_playing_board(filepath, fileout):

    image = cv.imread(filepath)

    show_image("Documentatie/poze/board_1.png", image)

    hsv_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    hsv_image[:,:,0] = (hsv_image[:,:,0] + 22) % 180

    image_documentatie = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
    show_image("Documentatie/poze/board_2.png", image_documentatie)

    threshold_image = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
    threshold_image = cv.cvtColor(threshold_image, cv.COLOR_BGR2GRAY)

    show_image("Documentatie/poze/board_3.png", threshold_image)

    #kernel = np.ones((2, 2), np.uint8)
    #threshold_image = cv.erode(threshold_image, kernel)

    kernel = np.ones((3,3), np.float32) / 9
    threshold_image = cv.filter2D(threshold_image,-1,kernel)

    show_image("Documentatie/poze/board_4.png", threshold_image)

    threshold_image[threshold_image < 165] = 0

    show_image("Documentatie/poze/board_5.png", threshold_image)
    
    #threshold_image = cv.Canny(threshold_image, 0, 0)
    kernel = np.ones((15, 15), np.uint8)
    areas_image = cv.dilate(threshold_image, kernel)

    show_image("Documentatie/poze/board_6.png", areas_image)

    contours, _ = cv.findContours(areas_image,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0

    # TODO refactor
    for i in range(len(contours)):
        if(len(contours[i]) > 3):
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1] :
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis = 1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    width = 1456 # divizibil cu un patrat de 104x104
    height = 1456

    # because the upper left corner is shady, I hardcode the values for it

    top_left[0] = top_right[0] - width
    top_left[1] = bottom_left[1] - height

    puzzle = np.array([top_left, top_right, bottom_left, bottom_right], dtype= np.float32)
    destination = np.array([[0,0], [width, 0], [0, height], [width, height]], dtype = np.float32)
    M = cv.getPerspectiveTransform(puzzle, destination)
    result = cv.warpPerspective(image, M, (width, height), flags = cv.INTER_LINEAR)

    # lines_horizontal=[]
    # lines_vertical=[]
    # for i in range(0,1457,104):
    #     l=[]
    #     l.append((0,i))
    #     l.append((1455,i))
    #     lines_horizontal.append(l)
    #     l=[]
    #     l.append((i,0))
    #     l.append((i,1455))
    #     lines_vertical.append(l)
    # for line in lines_vertical: 
    #     cv.line(result, line[0], line[1], (0, 255, 0), 5)
    #     for line in  lines_horizontal : 
    #         cv.line(result, line[0], line[1], (0, 0, 255), 5)

    show_image("Documentatie/poze/board_7.png", result)
    cv.imwrite(fileout, result)

files = ['01.jpg']
#print(files)

for file in files:
    if file[-3:] == 'jpg':
        image_path = f'imagini_auxiliare/{file}'
        print(image_path)
        image_out_path = f'imagini_generate/tabla_goala.jpg'

        extract_playing_board(image_path, image_out_path)