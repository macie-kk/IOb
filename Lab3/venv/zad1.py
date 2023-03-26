import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Ustawienie rozmarów wyświetlanych obrazów
plt.rcParams["figure.figsize"] = (18, 10)
image = cv.imread("images/example.jpg")

kernel = [
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
]

kernel = np.asarray(kernel)
filtered_image = cv.filter2D(image, -1, kernel=kernel) 

fig, ax = plt.subplots(1, 2)
ax[0].imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
ax[1].imshow(filtered_image)
plt.show()