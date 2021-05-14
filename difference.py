import cv2
import reference as ref
import numpy as np
import sys
import os
# card dimensions: 2.25 x 3.5

shapes = ref.load_shapes("shape/")
image = cv2.imread("test/IMG_0517.JPG")
imgs, matches, output = ref.isolate(image, shapes)
num_cards = len(imgs)
# print(num_cards)
stack = ref.stack_images(1, [imgs])
cv2.imshow("processed", stack)
cv2.imshow("output", output)
#
# for shape in shapes:
#     ref.show_wait("f", shape.img, 1000)

cv2.waitKey(0)
