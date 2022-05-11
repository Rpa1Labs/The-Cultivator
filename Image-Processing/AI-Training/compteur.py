import cv2
import sys
import numpy as np

datapath = "./result/"

def dataset(mask_image,name,iname):

    image_blurred = cv2.medianBlur(mask_image,15)

    ret, monochome_image = cv2.threshold(image_blurred, 127, 255, cv2.THRESH_BINARY)

    #Contouring
    contours, hierarchy = cv2.findContours(monochome_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print("Il y a {} salades".format(len(contours)))

    i=0

    image_for_crop = mask_image.copy()

    datasets = []

    #get image size
    height, width = mask_image.shape

    for c in contours:
        #get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        mask_image = cv2.rectangle(mask_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #crop image
        cropped_image = image_for_crop[y:y+h, x:x+w]

        #get the number of white pixels
        nb_white_pixels = np.sum(cropped_image == 255)

        #put label 
        cv2.putText(mask_image, "id: "+str(i) + " taille: " + str(nb_white_pixels), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        i+=1

        xm = x + w/2
        ym = y + h/2

        #normalize coordinates
        xn  = round(xm/width,7)
        yn  = round(ym/height,7)
        wn  = round(w/width,7)
        hn  = round(h/height,7)

        #add to datasets
        datasets.append(["0", str(xn), str(yn), str(wn), str(hn)])

    print(datasets)

    #create new dataset file
    with open(datapath + iname + ".txt", "w") as f:
        for dataset in datasets:
            f.write(" ".join(dataset) + "\n")

    #cv2.imwrite(datapath+iname+"-result.jpg", mask_image)

