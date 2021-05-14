import cv2
import numpy as np

WAIT_TIME = 3000


# shows image
def show_wait(img_name, img, time):
    cv2.imshow(img_name, img)
    # waits (ms). 0 = forever
    cv2.waitKey(time)


# pts1 contains input corners, pts2 contains output corners. width, height is for output image
def warp(img, pts1, pts2, width, height):
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, width, height)
    return output


# horizontal/vertical stacking
# imgHor = np.hstack((img1, img2))
# show_wait("Horizontally Stacked", imgHor, WAIT_TIME)
# same thing but with vstack
# limitations: no resizing; both must be same type (ex grayscale or rgb)

# # reading image
# image = cv2.imread("img/0__1.jpg")
# show_wait("Normal Image", image, WAIT_TIME)
#
# # grayscaling
# img_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# show_wait("Grayscale Image", img_gs, WAIT_TIME)
#
# # blurring; (7,7) is how much to blur (must be odd)
# img_blur = cv2.GaussianBlur(image, (69, 69), 0)
# show_wait("Blurred Image", img_blur, WAIT_TIME)

# canny edge thing
# img_canny = cv2.Canny(image, 275, 275)
# show_wait("Canny Image", img_canny, WAIT_TIME)
#
# # dilation w/canny
# img_dilated = cv2.dilate(img_canny, kernel=np.ones((5,5), np.uint8), iterations=2)
# show_wait("Dilated Image", img_dilated, WAIT_TIME)

# erosion: same as dilation but with .erode

# resize: img_resized = cv2.resize(image, (width, hight)
# crop: img_cropped = image[h0:h, w0:w]

# # creating color image
# img = np.zeros((512, 512, 3), np.uint8)
# # sets to blue. can set limits in the brackets
# img[:] = 255, 0, 0
# show_wait("img", img, WAIT_TIME)

def video():
    # reading video from static
    # vid = cv2.VideoCapture("pathname")
    # reading video from camera
    vid = cv2.VideoCapture(1)
    # set width
    vid.set(3, 640)
    # set height
    vid.set(4, 480)

    # frame by frame
    while True:
        success, img = vid.read()
        img_canny = cv2.Canny(img, 350, 350)
        cv2.imshow("Video name", img_canny)
        # check for q keybind to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# video()
def empty(dummy):
    print(dummy)


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver



path = "img/0201.jpg"

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 840, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

# while True:
#     cv2.imshow("TrackBars", img)
#     b = cv2.getTrackbarPos("Sat Max", "TrackBars")
#     g = cv2.getTrackbarPos("Val Min", "TrackBars")
#     r = cv2.getTrackbarPos("Val Max", "TrackBars")
#     img[:] = [b, g, r]
#     cv2.waitKey(1)
img = cv2.imread(path)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


video()

# while True:
#     h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
#     h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
#     s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
#     s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
#     v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
#     v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
#     #print(h_min, h_max, s_min, s_max, v_min, v_max)
#     lower = np.array([h_min, s_min, v_min])
#     upper = np.array([h_max, s_max, v_max])
#     mask = cv2.inRange(imgHSV, lower, upper)
#     imgResult = cv2.bitwise_and(img, img, mask=mask)
#
#     # cv2.imshow("Original",img)
#     # cv2.imshow("HSV",imgHSV)
#     # cv2.imshow("Mask", mask)
#     # cv2.imshow("Result", imgResult)
#
#     imgStack = stackImages(0.6, ([img, imgHSV], [mask, imgResult]))
#     cv2.imshow("TrackBars", imgStack)
#     cv2.waitKey(1)

# cv2.waitKey(0)
