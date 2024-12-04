import cv2
import numpy as np

# Load the image
image_path = "antrenare/1_02.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Error: Could not read the image. Make sure the file exists and the path is correct.")
    exit()

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

cv2.namedWindow("HSV Adjustments")
cv2.namedWindow("Grayscale Adjustments")
cv2.namedWindow("Edge Filter")

# Callback function for trackbars (does nothing but required by OpenCV)
def nothing(x):
    pass

cv2.createTrackbar("Hue", "HSV Adjustments", 20, 180, nothing)
cv2.createTrackbar("Saturation", "HSV Adjustments", 255, 255, nothing)
cv2.createTrackbar("Value", "HSV Adjustments", 255, 255, nothing)

cv2.createTrackbar('Upper threshold', "Grayscale Adjustments", 255, 255, nothing)
cv2.createTrackbar('Lower threshold', "Grayscale Adjustments", 170, 255, nothing)

cv2.createTrackbar('First param', "Edge Filter", 0, 1000, nothing)
cv2.createTrackbar('Second param', "Edge Filter", 400, 1000, nothing)

# H 20 S max V max
# upper max lower 170
# la canny las totul 0

while True:
    
    # Get the current positions of the trackbars
    hue_offset = cv2.getTrackbarPos("Hue", "HSV Adjustments")
    sat_offset = cv2.getTrackbarPos("Saturation", "HSV Adjustments")
    val_offset = cv2.getTrackbarPos("Value", "HSV Adjustments")

    upper_offset = cv2.getTrackbarPos('Upper threshold', "Grayscale Adjustments")
    lower_offset = cv2.getTrackbarPos('Lower threshold', "Grayscale Adjustments")
    
    # Apply the offsets to the HSV image
    adjusted_hsv = hsv_image.copy()
    adjusted_hsv[:, :, 0] = (adjusted_hsv[:, :, 0] + hue_offset) % 180  # Adjust Hue
    adjusted_hsv[:, :, 1] = np.clip(adjusted_hsv[:, :, 1] * (sat_offset / 255), 0, 255).astype(np.uint8)  # Adjust Saturation
    adjusted_hsv[:, :, 2] = np.clip(adjusted_hsv[:, :, 2] * (val_offset / 255), 0, 255).astype(np.uint8)  # Adjust Value

    # Convert back to BGR for display
    adjusted_image = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)

    adjusted_image_rs = cv2.resize(adjusted_image, (0,0), fx=0.3, fy=0.3)

    # Show the adjusted image
    cv2.imshow("HSV Adjustments", adjusted_image_rs)

    gray_adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

    gray_adjusted_image[gray_adjusted_image < lower_offset] = 0
    gray_adjusted_image[gray_adjusted_image > upper_offset] = 255

    gray_adjusted_image_rs = cv2.resize(gray_adjusted_image, (0,0), fx=0.3, fy=0.3)

    cv2.imshow("Grayscale Adjustments", gray_adjusted_image_rs)

    kernel = np.ones((7,7), np.uint8)
    gray_adjusted_image = cv2.dilate(gray_adjusted_image, kernel)

    param_1 = cv2.getTrackbarPos('First param', "Edge Filter")
    param_2 = cv2.getTrackbarPos('Second param', "Edge Filter")

    edge_image = cv2.Canny(gray_adjusted_image, param_1, param_2)
    kernel = np.ones((7,7), np.uint8)
    edge_image = cv2.dilate(edge_image, kernel)


    edge_image_rs = cv2.resize(edge_image, (0,0), fx=0.3, fy=0.3)

    cv2.imshow('Edge Filter', edge_image_rs)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
