import cv2
import numpy as np
import reference as ref


# def getContours(img):
#     contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         # print(area)
#         if area > 500:
#             cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
#             peri = cv2.arcLength(cnt, True)
#             # print(peri)
#             approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
#
#             objCor = len(approx)
#             x, y, w, h = cv2.boundingRect(approx)
#
#             if objCor == 4:
#                 objectType = "Card"
#             else:
#                 objectType = ""
#
#             cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(imgContour, objectType,
#                         (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5,
#                         (0, 0, 255), 2)
#
#             cv2.putText(imgBlank, "hmmm",
#                         (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5,
#                         (0, 0, 255), 2)
#             cv2.imshow("?", im)


def getContours(img):
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(approx)

            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 4:
                objectType = "Card"
                width, height = 250, 350
                # new = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
                new = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
                p1s = np.float32(approx)
                # if len(p1s) == 4:
                #     print("hello")
                #     p1s = np.float32(ref.format_points(approx))
                warped_canny = ref.warp(imgCanny, p1s, new, width, height)
                warped = ref.warp(img, p1s, new, width, height)
                # warped_dilated = cv2.dilate(warped, kernel=np.ones((3, 3), np.uint8), iterations=1)
                cv2.imshow("warped1", warped_canny)
                cv2.imshow("warped orig", warped)
            else:
                objectType = ""

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgContour, objectType,
                        (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 0, 255), 2)



vid = cv2.VideoCapture(1)
vid.set(3, 1000)
vid.set(4, 600)
while True:
    success, img = vid.read()
    imgContour = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)

    # imgBlank = img.copy()
    imgBlank = np.zeros_like(img)
    getContours(img)
    imgStack = ref.stack_images(0.8, ([img, imgGray, imgBlur],
                                      [imgCanny, imgContour, imgBlank]))

    cv2.imshow("Stack", imgStack)
    cv2.waitKey(1)