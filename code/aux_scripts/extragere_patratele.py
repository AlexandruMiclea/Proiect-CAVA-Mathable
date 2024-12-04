import cv2 as cv
import numpy as np

def show_image(title,image):
    image=cv.resize(image,(0,0),fx=0.3,fy=0.3)
    cv.imshow(title,image)
    cv.waitKey(0)
    cv.destroyAllWindows()

filepath = 'antrenare/4_01.jpg'

image = cv.imread(filepath)

hsv_image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
hsv_image[:,:,1] = 0
threshold_image = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
threshold_image = cv.cvtColor(threshold_image, cv.COLOR_BGR2GRAY)
threshold_image[threshold_image < 140] = 0
edges =  cv.Canny(threshold_image ,0,0)
kernel = np.ones((3, 3), np.uint8)
areas = cv.dilate(edges, kernel)
contours, _ = cv.findContours(areas,  cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
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

show_image("warped playing table",result)