import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Ustawienie rozmarów wyświetlanych obrazów
plt.rcParams["figure.figsize"] = (18, 10)

image = cv.imread("images/example.jpg")
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

img = np.float32(image)

ccm = np.array([
    [0.229, 0.587, 0.114],
    [0.500, -0.418, -0.082],
    [-0.168, -0.331, 0.500]
])

ccm2 = np.array([0, 128, 128])

outputYCrCb = cv.transform(img, ccm)
outputYCrCb = outputYCrCb + ccm2

fig, ax = plt.subplots(1, 2)
ax[0].imshow(image)
ax[1].imshow(outputYCrCb.astype('uint8'))
plt.show()