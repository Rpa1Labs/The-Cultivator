from curses import window
import cv2
import numpy as np

import sys

image_name = sys.argv[1]

image = cv2.imread(image_name)

image_blurred = cv2.medianBlur(image,5)
#image_blurred = image

#Récupère les différents canneaux et le met en float pour les calculs
B = image_blurred[:, :, 0].astype(np.float32)
G = image_blurred[:, :, 1].astype(np.float32)
R = image_blurred[:, :, 2].astype(np.float32)


Total = R + G + B
#Pour éviter les divisions par 0
Total = np.where(Total == 0, 1, Total)

#Normalisation entre 0 et 1
b = B / Total
g = G / Total
r = R / Total

#Application exg
Exg = 255 * (2 * g - r - b)

#Evite les overflow ou le négatif
Exg = np.where(Exg < 0, 0, Exg)
Exg = np.where(Exg > 255, 255, Exg)

#Repasse les valeurs en 8 bits (de 0 à 255)
Exg = Exg.astype('uint8')


ret, result = cv2.threshold(Exg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)     
  

dim = (image.shape[0],image.shape[1])

#Contouring
contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_contours = np.zeros(dim)
mask_img = cv2.drawContours(img_contours, contours, -1, (255,255,255), -1)

mask_img = cv2.normalize(src=mask_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

image_cutted = cv2.bitwise_and(image,image,mask=mask_img)

#Enregistrement des images

file = "./exg/"
cv2.imwrite(file+image_name, image)
cv2.imwrite(file+"filter_"+image_name, Exg)
cv2.imwrite(file+"masque_"+image_name, mask_img)
cv2.imwrite(file+"resultat_"+image_name, image_cutted)

