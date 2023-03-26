import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Ustawienie rozmarów wyświetlanych obrazów
plt.rcParams["figure.figsize"] = (18, 10)

image = cv.imread("images/example.jpg").astype(np.float32) / 255
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

ccm = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.689, 0.168],
    [0.272, 0.534, 0.131]
])

output = np.matmul(image, ccm)

for i in range(len(output)):
    for j in range(len(output[0])):
        for k in range(3):
            if output[i, j, k] > 1:
                output[i, j, k] = 1

fig, ax = plt.subplots(1, 2)
ax[0].imshow(image)
ax[1].imshow(output)
plt.show()