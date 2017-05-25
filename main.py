import cv2
import numpy as np

black_image = np.zeros((512, 512, 3), np.uint8)

r = 200
for theta in range(0, 360):
    radian = theta*np.pi/180
    x = np.cos(radian)*r
    y = np.sin(radian)*r
    cv2.line(black_image, (250, 250), (int(x+250), int(y+250)), (255, 0, 0), 1)

cv2.imshow("image", black_image)

cv2.waitKey(0)
