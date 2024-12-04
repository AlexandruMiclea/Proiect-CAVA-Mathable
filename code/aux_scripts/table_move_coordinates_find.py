import cv2 as cv
import numpy as np

imagine_0 = "imagini_generate/antrenare-patratele-1456/1_02.jpg.jpg"
imagine_1 = "imagini_generate/antrenare-patratele-1456/1_03.jpg.jpg"

imagine_0 = cv.cvtColor(cv.imread(imagine_0), cv.COLOR_BGR2GRAY)
imagine_1 = cv.cvtColor(cv.imread(imagine_1), cv.COLOR_BGR2GRAY)

imagine_diferenta = np.abs(np.array(imagine_0) - np.array(imagine_1))

cv.imshow('a',imagine_diferenta)
cv.waitKey(0)

thresh_high = 220
thresh_low = 100

imagine_diferenta_thresh = imagine_diferenta.copy()
imagine_diferenta_thresh[imagine_diferenta_thresh < thresh_low] = 0
imagine_diferenta_thresh[imagine_diferenta_thresh > thresh_high] = 0
imagine_diferenta_thresh[imagine_diferenta_thresh != 0] = 255

cv.imshow('a',imagine_diferenta_thresh)
cv.waitKey(0)

ker = np.ones((3,3))

imagine_diferenta_thresh = cv.erode(imagine_diferenta_thresh, ker)

cv.imshow('a',imagine_diferenta_thresh)
cv.waitKey(0)

mean_matrix = np.ndarray((14,14))

window_size = 124 # 104 + 10 px padding

window_coordinates = list()

for i in range(0, 1455, 104):
    for j in range(0, 1455, 104):
        # x min x max y min y max
        x_min = max(j - 10,0)
        x_max = min(j + 114,1455)
        y_min = max(i - 10,0)
        y_max = min(i + 114,1455)
        window_coordinates.append([x_min, x_max, y_min, y_max])

# imagine_diferenta_erodata = cv.cvtColor(imagine_diferenta_erodata, cv.COLOR_GRAY2BGR)

# for (idx,elem) in enumerate(window_coordinates):
#     if (idx % 3 == 0):
#         cv.rectangle(imagine_diferenta_erodata, (elem[0],elem[2]), (elem[1], elem[3]), (0,0,255), 1)
#     elif (idx % 3 == 1):
#         cv.rectangle(imagine_diferenta_erodata, (elem[0],elem[2]), (elem[1], elem[3]), (0,255,0), 1)
#     else:
#         cv.rectangle(imagine_diferenta_erodata, (elem[0],elem[2]), (elem[1], elem[3]), (255,0,0), 1)

# cv.imshow('a',imagine_diferenta_erodata)
# cv.waitKey(0)

print(np.array(window_coordinates).shape)

for (idx,elem) in enumerate(window_coordinates):
    val = np.mean(imagine_diferenta_thresh[elem[2]:elem[3], elem[0]:elem[1]])
    cv.rectangle(imagine_diferenta_thresh, (elem[0],elem[2]), (elem[1], elem[3]), (255,255,255), 1)
    mean_matrix[idx // 14][idx % 14] = val

    # cv.imshow('a',imagine_diferenta_thresh)
    # cv.waitKey(0)


mean_matrix[np.isnan(mean_matrix)] = 0

print(mean_matrix)
print(mean_matrix[8][7])
print(mean_matrix.argmax())

#print(*window_coordinates, sep='\n')
    #print(lista_coordonate_patrate)

    # for (idx,coordonate) in enumerate(lista_coordonate_patrate):
    #     linie = str((idx // 15) + 1)
    #     coloana = chr(65 + (idx % 15))

    #     #print(linie + ' ' + coloana)

    #     file_aux = fileout + filename[:4] + f'_{linie}{coloana}' + '.jpg'

    #     x = coordonate[1]
    #     y = coordonate[0]

    #     result_piece = result[x:x+104,y:y+104,:]

    #     cv.imwrite(file_aux, result_piece)

# # Load the image
# image_path = "antrenare/1_07.jpg"
# image = cv2.imread(image_path)

# if image is None:
#     print("Error: Could not read the image. Make sure the file exists and the path is correct.")
#     exit()

# hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# cv2.namedWindow("HSV Adjustments")
# cv2.namedWindow("Grayscale Adjustments")
# cv2.namedWindow("Edge Filter")

# # Callback function for trackbars (does nothing but required by OpenCV)
# def nothing(x):
#     pass

# cv2.createTrackbar("Hue", "HSV Adjustments", 20, 180, nothing)
# cv2.createTrackbar("Saturation", "HSV Adjustments", 255, 255, nothing)
# cv2.createTrackbar("Value", "HSV Adjustments", 255, 255, nothing)

# cv2.createTrackbar('Upper threshold', "Grayscale Adjustments", 255, 255, nothing)
# cv2.createTrackbar('Lower threshold', "Grayscale Adjustments", 175, 255, nothing)

# cv2.createTrackbar('First param', "Edge Filter", 0, 1000, nothing)
# cv2.createTrackbar('Second param', "Edge Filter", 0, 1000, nothing)

# # H 20 S max V max
# # upper max lower 170
# # la canny las totul 0

# while True:
    
#     # Get the current positions of the trackbars
#     hue_offset = cv2.getTrackbarPos("Hue", "HSV Adjustments")
#     sat_offset = cv2.getTrackbarPos("Saturation", "HSV Adjustments")
#     val_offset = cv2.getTrackbarPos("Value", "HSV Adjustments")

#     upper_offset = cv2.getTrackbarPos('Upper threshold', "Grayscale Adjustments")
#     lower_offset = cv2.getTrackbarPos('Lower threshold', "Grayscale Adjustments")
    
#     # Apply the offsets to the HSV image
#     adjusted_hsv = hsv_image.copy()
#     adjusted_hsv[:, :, 0] = (adjusted_hsv[:, :, 0] + hue_offset) % 180  # Adjust Hue
#     adjusted_hsv[:, :, 1] = np.clip(adjusted_hsv[:, :, 1] * (sat_offset / 255), 0, 255).astype(np.uint8)  # Adjust Saturation
#     adjusted_hsv[:, :, 2] = np.clip(adjusted_hsv[:, :, 2] * (val_offset / 255), 0, 255).astype(np.uint8)  # Adjust Value

#     # Convert back to BGR for display
#     adjusted_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)

#     adjusted_image_rs = cv2.resize(adjusted_image, (0,0), fx=0.3, fy=0.3)

#     # Show the adjusted image
#     cv2.imshow("HSV Adjustments", adjusted_image_rs)

#     gray_adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

#     gray_adjusted_image[gray_adjusted_image < lower_offset] = 0
#     gray_adjusted_image[gray_adjusted_image > upper_offset] = 255

#     gray_adjusted_image_rs = cv2.resize(gray_adjusted_image, (0,0), fx=0.3, fy=0.3)

#     cv2.imshow("Grayscale Adjustments", gray_adjusted_image_rs)

    

#     gray_adjusted_image_rs = cv2.resize(gray_adjusted_image, (0,0), fx=0.3, fy=0.3)

#     cv2.imshow("altceva", gray_adjusted_image_rs)

#     param_1 = cv2.getTrackbarPos('First param', "Edge Filter")
#     param_2 = cv2.getTrackbarPos('Second param', "Edge Filter")

#     edge_image = cv2.Canny(gray_adjusted_image, param_1, param_2)
#     kernel = np.ones((3,3), np.uint8)
#     thresh = cv2.erode(gray_adjusted_image, kernel)

#     gray_adjusted_image_rs = cv2.resize(thresh, (0,0), fx=0.3, fy=0.3)

#     cv2.imshow("altceva 2", gray_adjusted_image_rs)

#     kernel = np.ones((5,5), np.uint8)
#     edge_image = cv2.dilate(thresh, kernel)


#     edge_image_rs = cv2.resize(edge_image, (0,0), fx=0.3, fy=0.3)

#     cv2.imshow('Edge Filter', edge_image_rs)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Cleanup
# cv2.destroyAllWindows()

