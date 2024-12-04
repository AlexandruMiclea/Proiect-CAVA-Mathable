import cv2 as cv
import numpy as np

imagine_0 = "imagini_generate/antrenare-patratele-1456/1_08.jpg.jpg"
imagine_1 = "imagini_generate/antrenare-patratele-1456/1_09.jpg.jpg"

imagine_0 = cv.cvtColor(cv.imread(imagine_0), cv.COLOR_BGR2GRAY)
imagine_1 = cv.cvtColor(cv.imread(imagine_1), cv.COLOR_BGR2GRAY)

imagine_diferenta_start = np.abs(np.array(imagine_0) - np.array(imagine_1))

cv.namedWindow("Grayscale Adjustments")

# Callback function for trackbars (does nothing but required by OpenCV)
def nothing(x):
    pass

cv.createTrackbar('Upper threshold', "Grayscale Adjustments", 190, 255, nothing)
cv.createTrackbar('Lower threshold', "Grayscale Adjustments", 000, 255, nothing)

while True:

    imagine_diferenta = imagine_diferenta_start.copy() 
    
    upper_offset = cv.getTrackbarPos('Upper threshold', "Grayscale Adjustments")
    lower_offset = cv.getTrackbarPos('Lower threshold', "Grayscale Adjustments")

    imagine_diferenta[imagine_diferenta > upper_offset] = 0
    imagine_diferenta[imagine_diferenta < lower_offset] = 0

    gray_adjusted_image_rs = cv.resize(imagine_diferenta, (0,0), fx=0.3, fy=0.3)

    cv.imshow("Grayscale Adjustments", gray_adjusted_image_rs)

    # Break the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# cv.imshow('a',imagine_diferenta)
# cv.waitKey(0)

# ker = np.ones((5,5))
# imagine_diferenta_erodata = cv.erode(imagine_diferenta, ker)

# cv.imshow('a',imagine_diferenta_erodata)
# cv.waitKey(0)

# thresh = 150

# imagine_diferenta_thresh = imagine_diferenta_erodata.copy()
# imagine_diferenta_thresh[imagine_diferenta_thresh < thresh] = 0
# imagine_diferenta_thresh[imagine_diferenta_thresh >= thresh] = 255

# cv.imshow('a',imagine_diferenta_thresh)
# cv.waitKey(0)

# mean_matrix = np.ndarray((14,14))

# window_size = 124 # 104 + 10 px padding

# window_coordinates = list()

# for i in range(0, 1455, 104):
#     for j in range(0, 1455, 104):
#         # x min x max y min y max
#         x_min = max(j - 10,0)
#         x_max = min(j + 114,1455)
#         y_min = max(i - 10,0)
#         y_max = min(i + 114,1455)
#         window_coordinates.append([x_min, x_max, y_min, y_max])

# # imagine_diferenta_erodata = cv.cvtColor(imagine_diferenta_erodata, cv.COLOR_GRAY2BGR)

# # for (idx,elem) in enumerate(window_coordinates):
# #     if (idx % 3 == 0):
# #         cv.rectangle(imagine_diferenta_erodata, (elem[0],elem[2]), (elem[1], elem[3]), (0,0,255), 1)
# #     elif (idx % 3 == 1):
# #         cv.rectangle(imagine_diferenta_erodata, (elem[0],elem[2]), (elem[1], elem[3]), (0,255,0), 1)
# #     else:
# #         cv.rectangle(imagine_diferenta_erodata, (elem[0],elem[2]), (elem[1], elem[3]), (255,0,0), 1)

# # cv.imshow('a',imagine_diferenta_erodata)
# # cv.waitKey(0)

# print(np.array(window_coordinates).shape)

# for (idx,elem) in enumerate(window_coordinates):
#     val = np.mean(imagine_diferenta_thresh[elem[2]:elem[3], elem[0]:elem[1]])
#     cv.rectangle(imagine_diferenta_thresh, (elem[0],elem[2]), (elem[1], elem[3]), (255,255,255), 1)
#     mean_matrix[idx // 14][idx % 14] = val

#     cv.imshow('a',imagine_diferenta_thresh)
#     cv.waitKey(0)


# mean_matrix[np.isnan(mean_matrix)] = 0

# print(mean_matrix)
# print(mean_matrix[8][7])
# print(mean_matrix.argmax())