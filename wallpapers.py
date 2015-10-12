#WallPaperSorter.py
#@author Rakitov Stanislav
#@URL https://github.com/MrRakitov/WallPaperSorter

import glob

#Get all file names in current directory
# Получить имена всех файлов в папке. Внести их в массив.
filenames = glob.glob('samplepic\*.jpg')

#print all file names of current directory
#i do not need it yet
#print (filenames)

#Print each file name separately.
for fname in filenames:
	print (fname)


# Пройтись по массиву. 
# 	Открыть каждый файл.
# 	Прочесть заголовок. 
# 	Размер файла внести во временную переменную.
# 	Закрыть файл.
# 	Вывести название файла + размер.
