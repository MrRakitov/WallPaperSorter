#WallPaperSorter.py
#@author Rakitov Stanislav
#@URL https://github.com/MrRakitov/WallPaperSorter

import glob
import imghdr

#Get all file names in current directory
# Получить имена всех файлов в папке. Внести их в массив.
#Use sample folder
filenames = glob.glob('samplepic\*.jpg') #or use just current folder filenames = glob.glob('*.jpg')

#Print each file name separately.
for fname in filenames:
  image_type = imghdr.what(fname)
  if not image_type:
    print ("error")
  else:
    print (image_type)
  
  print (fname)


# Пройтись по массиву. 
# 	Открыть каждый файл.
# 	Прочесть заголовок. 
# 	Размер файла внести во временную переменную.
# 	Закрыть файл.
# 	Вывести название файла + размер.
