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

R = np.where(R == 0, 1, R)
G = np.where(G == 0, 1, G)
B = np.where(B == 0, 1, B)


#Normalisation entre 0 et 1
b = B / Total
g = G / Total
r = R / Total

#Exg
Exg = 255 * (2 * g - r - b)

#CIVE
CIVE = 255*(0.441*r + 0.811*g + 0.385*b ) + 18.78745

#VEG
a=0.667
VEG = (G/(pow(R,a)*pow(B,1-a)))


#Application COM
COM = 0.36*Exg + 0.53*CIVE + 0.11*VEG

#Evite les overflow ou le négatif
COM = np.where(COM < 0, 0, COM)
COM = np.where(COM > 255, 255, COM)

#Repasse les valeurs en 8 bits (de 0 à 255)
COM = COM.astype('uint8')


window = int(len(image)/8)
if window%2==0:
    window=window+1

#Seuillage
ret, result = cv2.threshold(COM, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)     

dim = (image.shape[0],image.shape[1])


#Contouring
contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_contours = np.zeros(dim)
mask_img = cv2.drawContours(img_contours, contours, -1, (255,255,255), -1)


mask_img = cv2.normalize(src=mask_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

image_cutted = cv2.bitwise_and(image,image,mask=mask_img)

#Enregistrement des images

file = "./COM/"
cv2.imwrite(file+image_name, image)
cv2.imwrite(file+"filter_"+image_name, COM)
cv2.imwrite(file+"masque_"+image_name, mask_img)
cv2.imwrite(file+"resultat_"+image_name, image_cutted)