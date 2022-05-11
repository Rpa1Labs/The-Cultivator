import cv2
import numpy as np

# TODO: Implement AI image processing here and return the surface area of the object 
def process_image(image):
    
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

    #Seuillage adaptatif via la méthode de Otsu
    ret, result = cv2.threshold(Exg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)     

    #Récupère les dimensions de l'image
    dim = (image.shape[0],image.shape[1])

    #Première passe de contouring
    contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = np.zeros(dim)
    mask_img = cv2.drawContours(img_contours, contours, -1, (255,255,255), -1)

    #Normalisation
    mask_img = cv2.normalize(src=mask_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        
    #Calcul de la surface
    surfaceArea = calculateSurface(mask_img)

    return surfaceArea


def calculateSurface(mask_image):

    image_blurred = cv2.medianBlur(mask_image,5)

    image_blurred = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)

    ret, monochome_image = cv2.threshold(image_blurred, 127, 255, cv2.THRESH_BINARY)

    #Deuxième passe de contouring (enlève les contours parasites)
    contours, hierarchy = cv2.findContours(monochome_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_for_crop = mask_image.copy()

    surfaces = {}

    #Récupère les dimensions de l'image
    height, width, channels = mask_image.shape

    #Parcours les contours
    for cnt in contours:
        #Récupère les coordonées du rectangle englobant le contour
        x,y,w,h = cv2.boundingRect(cnt)
        #Récupère le centre du rectangle
        center_x = x + w/2
        center_y = y + h/2
        #Calcul la distance entre le centre du rectangle et le centre de l'image
        distance = np.sqrt((height/2 - center_y)**2 + (width/2 - center_x)**2)
        #Découpe l'image
        cropped_image = image_for_crop[y:y+h, x:x+w]
        #Récupère le nombre de pixels blancs dans l'image découpée
        nb_white_pixels = np.sum(cropped_image == 255)
        #Ajoute la surface au dictionnaire en fonction de la distance
        surfaces[distance] =  nb_white_pixels
        

    #Tri les distances par ordre croissant
    sorted_distances = sorted(surfaces.keys())
    #Récupère la surface la plus proche du centre de l'image (la distance la plus petite)
    most_centered_surface = surfaces[sorted_distances[0]]

    return most_centered_surface