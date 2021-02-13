import cv2 as cv
import numpy as np

np.set_printoptions(threshold=np.inf)

# calculates size and intensity of inner outer box
def size_intensity_calculator(img):
	big, _ = img.shape
	big_i = img[0][0]

	thresh = 3
	max_x = 0
	small_i = 0
	top_left = (0, 0)

	h = 0
	# iterate over image pixels from left most pixel, until intensity rise by a value more than thresh
	for row in img:
		w = 0
		for x in row:
			x_i = int(x)
			# print(x_i)
			if x_i - max_x >= thresh:
				# print("reached")
				max_x = x_i
				top_left = (w, h)
				small_i = x_i
			w += 1
		h += 1

	small = big - 2*top_left[0]
	return small, big, small_i, big_i

# Create concentric boxes just as the example image
def concentric_box(small, big, small_i, big_i):
	img = np.ones([big, big], dtype=np.uint8) * big_i
	for i in range(big//2-small//2, big//2+small//2+1):
		for j in range(big//2-small//2, big//2+small//2+1):
			img[i][j] = small_i
	return img

# Overwrite pixels intensity of outer box i.e. background
def bg_change(small, big, big_i, img):
	for i in range(0, big):
		for j in range(0, big):
			if (big//2-small//2 >= i or i >= big//2+small//2+1) or (big//2-small//2+1 >= j or j >= big//2+small//2+1):
				img[i][j] = big_i

if __name__ == "__main__":
	img = cv.imread("example.png", cv.IMREAD_GRAYSCALE)
	small, big, small_i, big_i = size_intensity_calculator(img)
	print("small square size: {}, big square size: {}, small intensity: {}, big intensity: {}".format(small, big, small_i, big_i))
	new_img = concentric_box(small, big, small_i, big_i)

	while True:
		bg_intensity = int(input("enter background intensity: "))
		weber = 100*abs(small_i - bg_intensity)/bg_intensity
		print("weber ratio: {}%".format(weber))
		if bg_intensity < 0 or bg_intensity > 255:
			break
		bg_change(small, big, bg_intensity, new_img)
		# concat_img = np.concatenate((img, new_img))
		# cv.imshow("concatenated images", concat_img)
		cv.imshow("images", new_img)
		cv.imwrite("bg-change-bgi-{}-fgi-{}-wbr-{}.png".format(bg_intensity, small_i, weber), new_img)
		k = cv.waitKey(1)
