import cv2 as cv

path = "3015_CHARLIE_ST_CLOUD_00.23.57.935-00.24.00.783@0.jpg"
img = cv.imread(path)
h, w, c = img.shape
x1, y1, x2, y2 = [0.13, 0.07, 0.32, 0.87]
x1 = x1 * w
y1 = y1 * h
x2 = x2 * w
y2 = y2 * h
img = cv.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
cv.imwrite("res.jpg", img)
