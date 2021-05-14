# # returns grayscale, blurred, adaptively thresholded image
# # Adaptive thresholding: background pixel in the center top of the image is sampled to determine
# # its intensity. The adaptive threshold is set at THRESH_C higher than that
# def preprocess_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     img_w, img_h = np.shape(image)[:2]
#     bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
#     thresh_level = bkg_level + THRESH_C
#     retval, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY)
#     return thresh


# isolates the cards in an image
# gs = whether or not want in grayscale (true/false)
# returns array of card images
# def isolate(img, shapes, dir_shape, dir_all):
#     img_contour = img.copy()
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img_blur = cv2.GaussianBlur(img_gray, (17, 17), 5)
#     img_w, img_h = np.shape(img)[:2]
#     bkg_level = img_gray[int(1)][int(1)]
#     thresh_level = bkg_level + THRESH_C
#     retval, img_bw = cv2.threshold(img_blur, thresh_level, 255, cv2.THRESH_BINARY)
#     img_canny = cv2.Canny(img_bw, CANNY_THRESH, CANNY_THRESH)
#     img_dilated = cv2.dilate(img_canny, kernel=np.ones((5, 5), np.uint8), iterations=2)
#     contours, hierarchy = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     img_stack = stack_images(1, ([img, img_gray, img_blur],
#                                       [img_bw, img_contour, img_dilated]))
#     card_imgs = []
#     matches = []
#     for cnt in contours:
#         shapes = load_shapes(dir_shape, True)
#         area = cv2.contourArea(cnt)
#         if area > CARD_MIN_AREA:
#             cv2.drawContours(img_contour, cnt, -1, (255, 0, 0), 3)
#             peri = cv2.arcLength(cnt, True)
#             # print(peri)
#             approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
#             # print(approx)
#
#             num_corners = len(approx)
#             x, y, w, h = cv2.boundingRect(approx)
#             m = [-1, "idk"]
#             full = [-1, "idk"]
#             if num_corners == 4:
#                 # do card identification & warping
#                 width, height = CARD_WIDTH, CARD_HEIGHT
#                 new = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
#                 p1s = np.float32(format_points(approx))
#                 # p1s = np.float32(approx)
#                 warped_canny = warp(img_canny, p1s, new, width, height)
#                 # warped = None
#                 warped = warp(img, p1s, new, width, height)
#                 warped_gs = warp(img_bw, p1s, new, width, height)
#
#                 # if gs:
#                 #     warped = warp(img_bw, p1s, new, width, height)
#                 # else:
#                 #     warped = warp(img, p1s, new, width, height)
#                 # card_imgs.append(warped)
#
#                 # do matching
#                 card = Card()
#                 card.img = warped_gs
#                 m = match(card, shapes, True)
#
#                 # shape identifier (ex 0__0 is 1 oval)
#                 s = m[1]
#                 cv2.imshow("help",card.img)
#                 card.img = warped
#                 cv2.imshow("nin", card.img)
#                 cv2.waitKey(300)
#                 shapes = load_shapes(dir_all + "/" + s, False)
#                 full = match(card, shapes, False)
#                 matches.append(name_from_id(full[1]))
#                 # cv2.imshow("lol", warped)
#                 # cv2.waitKey(1000)
#
#                 # cv2.imwrite("test/test" + m[1] + ".jpg", card.img)
#             else:
#                 obj_type = ""
#
#             cv2.rectangle(img_contour, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(img_contour, name_from_id(full[1]),
#                         (x + (w // 2) - 150, y + (h // 2) - 10), cv2.FONT_HERSHEY_SIMPLEX, FONT_SIZE,
#                         (0, 0, 0), 5)
#
#     cv2.imshow("Stack", img_stack)
#     cv2.waitKey(WAIT_TIME)
#     return card_imgs, matches, img_contour

# returns color id
# def match_color(card):
#     image = card.img
#     img_results = []
#     img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     for i in range(3):
#         color_vals = ref.VALS_DICT[i]
#         lower = np.array([color_vals[0], color_vals[2], color_vals[4]])
#         upper = np.array([color_vals[1], color_vals[3], color_vals[5]])
#         mask = cv2.inRange(img_hsv, lower, upper)
#         img = cv2.bitwise_and(image, image, mask=mask)
#         img_results.append(img)
#
#     stack = ref.stack_images(1, img_results)
#     ref.show_wait("maps", stack, ref.WAIT_TIME)
#     cv2.imwrite("test/maps.jpg", stack)
#
#     color = 0
#     black = cv2.imread("reference/black.jpg")
#     # want most different
#     best_match_diff = -1
#     for i in range(len(img_results)):
#         color_name = ref.COLOR_DICT[i]
#         # print(color_name)
#         diff_img = cv2.absdiff(black, img_results[i])
#         diff = int(np.sum(diff_img) / 255)
#         # print(diff)
#
#         if diff > best_match_diff:
#             best_match_diff = diff
#             color = i
#
#     return color


# matches card object with shape (to do: color)
# def match(card, shapes, gs):
#     best_shape_match_diff = 100000
#     best_shape_name = "tbd"
#     if len(card.img) != 0:
#         # Difference the query card shape from each shape image; store the result with the least difference
#         for shape in shapes:
#             # print(len(card.img.shape))
#             # print(len(shape.img.shape))
#             diff_img = cv2.absdiff(card.img, shape.img)
#             shape_diff = int(np.sum(diff_img) / 255)
#             if shape_diff < best_shape_match_diff:
#                 best_shape_match_diff = shape_diff
#                 #print("jello")
#                 if gs:
#                     best_shape_name = shape.name[0] + "__" + shape.name[3]
#                 else:
#                     best_shape_name = shape.name
#                 # print(best_shape_match_diff, best_shape_name)
#     # print(best_shape_name)
#     # print("-----")
#     return best_shape_match_diff, best_shape_name

# def isolate(img, shapes):
#     img_contour = img.copy()
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img_blur = cv2.GaussianBlur(img_gray, (17, 17), 5)
#     img_w, img_h = np.shape(img)[:2]
#     bkg_level = img_gray[int(1)][int(1)]
#     thresh_level = bkg_level + THRESH_C
#     retval, img_bw = cv2.threshold(img_blur, thresh_level, 255, cv2.THRESH_BINARY)
#     img_canny = cv2.Canny(img_bw, CANNY_THRESH, CANNY_THRESH)
#     img_dilated = cv2.dilate(img_canny, kernel=np.ones((5, 5), np.uint8), iterations=2)
#     contours, hierarchy = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     img_stack = stack_images(1, ([img, img_gray, img_blur],
#                                       [img_bw, img_contour, img_dilated]))
#     card_imgs = []
#     matches = []
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area > CARD_MIN_AREA:
#             cv2.drawContours(img_contour, cnt, -1, (255, 0, 0), 3)
#             peri = cv2.arcLength(cnt, True)
#             # print(peri)
#             approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
#             # print(approx)
#
#             num_corners = len(approx)
#             x, y, w, h = cv2.boundingRect(approx)
#             m = [-1, "idk"]
#             full = [-1, "idk"]
#             if num_corners == 4:
#                 # do card identification & warping
#                 width, height = CARD_WIDTH, CARD_HEIGHT
#                 new = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
#                 p1s = np.float32(format_points(approx))
#                 # p1s = np.float32(approx)
#                 warped_canny = warp(img_canny, p1s, new, width, height)
#                 # warped = None
#                 warped = warp(img, p1s, new, width, height)
#                 warped_gs = warp(img_bw, p1s, new, width, height)
#
#                 # do matching
#                 card = Card()
#                 card.img = warped_gs
#                 m = match(card, shapes, True)
#                 matches.append(name_from_id(m[1], True))
#             else:
#                 obj_type = ""
#
#             cv2.rectangle(img_contour, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.putText(img_contour, name_from_id(m[1], True),
#                         (x + (w // 2) - 150, y + (h // 2) - 10), cv2.FONT_HERSHEY_SIMPLEX, FONT_SIZE,
#                         (0, 0, 0), 5)
#
#     cv2.imshow("Stack", img_stack)
#     cv2.waitKey(WAIT_TIME)
#     return card_imgs, matches, img_contour

# img_test = cv2.imread("all/0200.jpg")
# diff0 = cv2.absdiff(cv2.imread("all/IMG_0522.JPG"), img_test)
# diff1 = cv2.absdiff(cv2.imread("all/1100.jpg"), img_test)
# diff2 = cv2.absdiff(cv2.imread("all/IMG_0521.JPG"), img_test)
# shape_diff0 = int(np.sum(diff0) / 255)
# shape_diff1 = int(np.sum(diff1) / 255)
# shape_diff2 = int(np.sum(diff2) / 255)
# print(shape_diff0)
# print(shape_diff1)
# print(shape_diff2)


# def match_all(card, shapes):
#     best_match_diff = 100000
#     best_name = "tbd"
#     if len(card.img) != 0:
#         # Difference the query card shape from each shape image; store the result with the least difference
#         for shape in shapes:
#             # print(len(card.img.shape))
#             # print(len(shape.img.shape))
#             diff_img = cv2.absdiff(card.img, shape.img)
#             shape_diff = int(np.sum(diff_img) / 255)
#
#             if shape_diff < best_match_diff:
#                 best_match_diff = shape_diff
#                 best_name = ref.name_from_id(shape.name, True)
#     # print(best_shape_name)
#     return best_match_diff, best_name

# DIRECTORY = "shape"
# inp = cv2.imread("test/IMG_0544.JPG")
# dir_shape = "shape"
# dir_all = "all"
# shapes = ref.load_shapes("shape/", True)
# imgs, matches, output = ref.isolate(inp, shapes)
# print(matches)
# cv2.imshow("output", output)
# # cv2.waitKey(0)
# cv2.waitKey(0)

#cv2.imwrite("test/hmm.jpg", imgs[1])
# img_test = cv2.imread("test/hmm.jpg")
# diff0 = cv2.absdiff(cv2.imread("all/0__0/0100.jpg"), img_test)
# diff1 = cv2.absdiff(cv2.imread("all/0__0/0200.jpg"), img_test)
# shape_diff0 = int(np.sum(diff0) / 255)
# shape_diff1 = int(np.sum(diff1) / 255)
# print(shape_diff0)
# print(shape_diff1)

# shapes = ref.load_shapes("shape/", True)
# c = ref.Card()
# c.img = cv2.imread("test/2001.jpg")
# color = ref.match_color(c)
# print(ref.COLOR_DICT[color])
# match = ref.match(c, shapes)
# print(ref.name_from_id(match, False))


# if self.num < 0 or self.num > 2 or self.color < 0 or self.color > 2 or self.fill < 0 or self.fill > 2 or self.shape < 0 or self.shape > 2:
        #     return "bruh momen"
        # return ref.NUM_DICT[self.num] + " " + ref.COLOR_DICT[self.color] + " " + ref.FILL_DICT[self.fill] + " " + \
        #        ref.SHAPE_DICT[self.shape]