#WallPaperSorter.py
#@author Rakitov Stanislav
#@URL https://github.com/MrRakitov/WallPaperSorter

import glob
import imghdr
import struct

#I've found this code here http://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib#
def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height


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

