#WallPaperSorter.py
#@author Rakitov Stanislav
#@URL https://github.com/MrRakitov/WallPaperSorter

import glob
import imghdr

#Get all file names in current directory
# Получить имена всех файлов в папке. Внести их в массив.
#Use sample folder
filenames = glob.glob('samplepic\*.*') #or use just current folder filenames = glob.glob('*.jpg')

#Print each file name separately. 
#check is file an image or not.
for fname in filenames:
  image_type = imghdr.what(fname)
  if not image_type:
    print (fname + " is NOT an image file")
  else:
    print (fname + " IS a " + image_type + " file")
    # print (fname)

