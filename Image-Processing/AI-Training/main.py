import os

from exg import process_image
from compteur import dataset

#rename all files in a directory

#get path of python script
path = "."

path = path + '/images/'
pathresult = path + '/result/'

#get all files in the directory
files = os.listdir(path)

i=0

#loop through all files
for file in files:
    #get file name
    name = os.path.splitext(file)[0]
    mask = process_image(path + file,str(i))
    dataset(mask, name,str(i))
    i+=1



