import os

import cv2

path = 'background'

# os.path.join(cwd, f)

arr = [os.path.join(path, i) for i in os.listdir(path)]

for i in arr:
    print(i)
    img = cv2.imread(i)
    print(img.shape)
    cv2.imshow('i',img)
    img = cv2.resize(img,(1280,720))
    cv2.imshow('j',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()