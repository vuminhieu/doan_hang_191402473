import cv2
import numpy as np

def equalize_brightness(img, alpha, beta):
    img_equalized = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return img_equalized

def phan_doan_bang_cat_nguong(img, threshold_value):
    m, n = img.shape[:2]
    img_phan_doan_cat_nguong = np.zeros([m, n])
    for i in range(m):
        for j in range(n):
            if (img[i, j] < threshold_value):
                img_phan_doan_cat_nguong[i, j] = 0
            else:
                img_phan_doan_cat_nguong[i, j] = 255  # tương đương gt 1 trong công thức 1
    return img_phan_doan_cat_nguong