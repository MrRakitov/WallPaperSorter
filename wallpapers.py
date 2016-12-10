#!/usr/bin/python3
#WallPaperSorter.py
#@author Rakitov Stanislav
#@URL https://github.com/MrRakitov/WallPaperSorter

import glob
import imghdr
import struct
import os #For directory creation
import shutil #for file moving

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
                return str("Unknown")
        else:
            return str("Unknown")
        return str(width) + "x" + str(height)

#Directory creation (If not exists)
def dirCreate (directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print ("Making " + directory)

#Move file(s) to directory
def fileMove (filename, directory):
    shutil.move(filename, directory)
    print ("Moving " + filename + " into " + directory)

#Returns aspect ratio
def aspectSize (size):
    if size in ('640x360','720x405','854x480','960x540','1024x576','1280x720','1366x768','1600x900','1920x1080','2048x1152','2560x1440','2880x1620','3200x1800','3840x2160','4096x2304','5120x2880','7680x4320','15360x8640'):
        aspect = "16x9"
    elif size in('1280x800','1440x900','1680x1050','1920x1200','2560x1600') :
        aspect = "16x10"
    elif size in ('640x480','800x600','1024x768','1152x864','1280x960','1400x1050','1600x1200','2048x1536','3200x2400','4000x3000','6400x4800'):
        aspect = "4x3"
    else:
        aspect = "other"
    return aspect

#Get all file names in current directory
filenames = glob.glob('*.*')

#Check file. Is it an image or not. If yes - proceed.
for fname in filenames:
  image_type = imghdr.what(fname)
  if image_type:
    size = get_image_size(fname) #Get image size
    aspect = aspectSize(size) #Get aspect ratio
    directory = "./sorted/" + aspect + "/" + size
    #print (fname + " " + size + " " + aspect + directory)
    dirCreate(directory)
    fileMove(fname, directory)

  else:
    print (fname + " is NOT a picture")

