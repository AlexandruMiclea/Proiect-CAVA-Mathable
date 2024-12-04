import cv2 as cv
import numpy as np
import os

def show_image(title,image):
    image=cv.resize(image,(0,0),fx=0.3,fy=0.3)
    cv.imshow(title,image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def extract_playing_board(filepath, fileout):

    image = cv.imread(filepath)

    hsv_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    hsv_image[:,:,0] = (hsv_image[:,:,0] + 22) % 180
    threshold_image = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
    threshold_image = cv.cvtColor(threshold_image, cv.COLOR_BGR2GRAY)

    #kernel = np.ones((2, 2), np.uint8)
    #threshold_image = cv.erode(threshold_image, kernel)

    kernel = np.ones((3,3), np.float32) / 9
    threshold_image = cv.filter2D(threshold_image,-1,kernel)

    threshold_image[threshold_image < 165] = 0
    
    #threshold_image = cv.Canny(threshold_image, 0, 0)
    kernel = np.ones((15, 15), np.uint8)
    areas_image = cv.dilate(threshold_image, kernel)

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

    width = bottom_right[0] - bottom_left[0]
    height = bottom_left[1] - top_left[1]
    puzzle = np.array([top_left, top_right, bottom_left, bottom_right], dtype= np.float32)
    destination = np.array([[0,0], [width, 0], [0, height], [width, height]], dtype = np.float32)
    M = cv.getPerspectiveTransform(puzzle, destination)
    result = cv.warpPerspective(image, M, (width, height), flags = cv.INTER_LINEAR)

    cv.imwrite(fileout, result)

files = sorted(os.listdir('antrenare'))
#print(files)

for file in files:
    if file[-3:] == 'jpg':
        image_path = f'antrenare/{file}'
        image_out_path = f'antrenare-patratele/{file}'

        extract_playing_board(image_path, image_out_path)