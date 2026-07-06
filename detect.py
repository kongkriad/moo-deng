import cv2
import numpy as np

img = cv2.imread('3.jpg')

def hsv_mask(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color1 = np.array([0, 30, 100])
    low1 = color1 - 30
    max1 = color1 + 30
    mask1 = cv2.inRange(hsv_img, low1, max1)
    
    contours, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    square = []
    
    for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            square.append((x, y, x + w, y + h))
    
    return square

def remove_overlapping_square(square, threshold=10):

    square = sorted(square)
    unique_square= []

    for current in square:
        is_overlapping = False
        for existing in unique_square:
            if (current[0] < existing[2] + threshold and current[2] > existing[0] - threshold and
                current[1] < existing[3] + threshold and current[3] > existing[1] - threshold):
                is_overlapping = True
                break
        
        if not is_overlapping:
            unique_square.append(current)

    return unique_square

def create_bounding_square(square):

    x_min = min(rect[0] for rect in square)
    y_min = min(rect[1] for rect in square)
    x_max = max(rect[2] for rect in square)
    y_max = max(rect[3] for rect in square)

    return [(x_min, y_min, x_max, y_max)]

def frame(image, square,draw_text=False):
    for (x1, y1, x2, y2) in square:
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) 
        if draw_text:
            text = "moo deng"
            cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2)
    return image

square = hsv_mask(img)
filtered_square = remove_overlapping_square(square)
bounding_square = create_bounding_square(filtered_square)
result_img = frame(img.copy(), bounding_square,draw_text=True)

cv2.imshow('Framed Image', result_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
