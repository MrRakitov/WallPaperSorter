import os
import sys
import imghdr
import shutil
import struct

#Default names for directories
DEFAULT_WORK_DIR = "wallpapers"
DEFAULT_SORT_DIR = ".sorted"

#Default directory name for broken and unsorted files
DEFAULT_BROKE_DIR = "broke_and_unsort"

#Directory delimiter. Windows style.
DEFAULT_PATH_SEPARATOR = "\\"

#Default indexes for command line arguments.
#1 - Working directory
#2 - sorted directory
DEFAULT_WORK_DIR_ARGUMENT_INDEX = 1
DEFAULT_SORT_DIR_ARGUMENT_INDEX = 2

#Set the work directory
#(Starting directory that contains all images and subdirs)
def set_work_dir():
    '''Returns working directory or returns default value of working dir'''
    work_dir_argument = get_start_arguments(DEFAULT_WORK_DIR_ARGUMENT_INDEX)
    if work_dir_argument:
        return work_dir_argument
    else:
        return DEFAULT_WORK_DIR

#Set directory for sorted images.
def set_sorted_dir(work_directory):
    '''Returns directory for sorted images'''
    sorted_dir_argument = get_start_arguments(DEFAULT_SORT_DIR_ARGUMENT_INDEX)
    if sorted_dir_argument:
        return sorted_dir_argument
    else:
        return work_directory + DEFAULT_SORT_DIR

#get value of index from command line if any or False
def get_start_arguments(argument_index):
    '''Returns an argument with index <argument_index>
    or False if argument index does not exists'''
    if len(sys.argv) == 1:
        return False
    else:
        try:
            return sys.argv[argument_index]
        except IndexError:
            return False

def get_full_list_of_dirs(work_dir):
    '''Returns a list[] with all subdirectories in <work_dir>'''
    return [x[0] for x in os.walk(work_dir)]


def get_full_list_of_files(directory):
    '''returns full list[] of jpg's files in <directory>'''
    #return [x for x in os.listdir(directory) if x.endswith(".jpg")]
    return [x for x in os.listdir(directory) if x.lower().endswith(".jpg") or x.lower().endswith(".jpeg")]

def check_file_type(file):
    '''Returns True if <file> is a "jpeg" or False otherwise'''
    try:
        return imghdr.what(file) == "jpeg"
    except FileNotFoundError:
        #print("File error " + file)
        return False
    #return imghdr.what(file) == "jpeg"

def read_file_header(file):
    '''Read file header and returns firs 24 bytes'''
    pass

def proceed_a_file(files_list, files_directory, sort_directory=DEFAULT_SORT_DIR):
    '''Proceed each file in a list of files'''
    #Set a directory for unsorted and broken files
    unsorted_directory = sort_directory + DEFAULT_PATH_SEPARATOR + DEFAULT_BROKE_DIR
    #create_a_directory(unsorted_directory)

    for file in files_list:
        #make a filename with relative path
        full_path_file = files_directory + DEFAULT_PATH_SEPARATOR + file
        #if file is not a jpg file move them to unsort directory
        if not check_file_type(full_path_file):
            create_a_directory(unsorted_directory)
            move_a_file(full_path_file, unsorted_directory)
        #If the file is a jpg move them to the right directory
        else:
            #Get size of the image
            image_size = get_image_size(full_path_file)
            #Get aspect ratio for image_size
            aspect = get_aspect_ratio(image_size)
            #set full path where file should be moved
            directory_to_move = sort_directory + DEFAULT_PATH_SEPARATOR + aspect + DEFAULT_PATH_SEPARATOR + image_size
            #Create a directory
            create_a_directory(directory_to_move)
            move_a_file(full_path_file, directory_to_move)

def create_a_directory(directory_path):
    '''Create a directory'''
    os.makedirs(directory_path, exist_ok=True)

def move_a_file(file, directory):
    '''Move a <file> to specified <directory>'''
    try:
        shutil.move(file, directory)
    except:
        #I do not understand yet what to do with existing files
        pass

def delete_a_directory(directory):
    '''Delete a specified <directory> and its parent(s) if they are empty'''
    shutil.rmtree(directory)

'''
    try:
        os.removedirs(directory)
    except OSError:
        print("Directory " + directory + " cannot be deleted")
'''

def proceed(directories, sort_directory=DEFAULT_SORT_DIR):
    '''Proceed all directories'''
    create_a_directory(sort_directory)
    #Reverse a list for later use
    #directories.reverse()
    for directory in directories:
        files_in_directory = get_full_list_of_files(directory)
        proceed_a_file(files_in_directory, directory, sort_directory)
        #delete_a_directory(directory)

#Returns aspect ratio
def get_aspect_ratio (size):
    '''Returns a string with aspect ratio'''
    if size in ('640x360','720x405','854x480','960x540',
                '1024x576','1280x720','1366x768','1600x900',
                '1920x1080','2048x1152','2560x1440','2880x1620',
                '3200x1800','3840x2160','4096x2304','5120x2880',
                '7680x4320','15360x8640'
                ):
        return "16x9"
    elif size in('1280x800','1440x900','1680x1050','1920x1200','2560x1600') :
        return "16x10"
    elif size in ('640x480','800x600','1024x768','1152x864',
                '1280x960','1400x1050','1600x1200','2048x1536',
                '3200x2400','4000x3000','6400x4800'
                ):
        return "4x3"
    else:
        return DEFAULT_BROKE_DIR

#Original of this code lies here
#http://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib
def get_image_size(file):
    '''Determine the image type of file_handle and return its size'''
    with open(file, 'rb') as file_handle:
        try:
            file_handle.seek(0) # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                file_handle.seek(size, 1)
                byte = file_handle.read(1)
                while ord(byte) == 0xff:
                    byte = file_handle.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', file_handle.read(2))[0] - 2
            # We are at a SOFn block
            file_handle.seek(1, 1)  # Skip `precision' byte.
            height, width = struct.unpack('>HH', file_handle.read(4))
        except Exception: #IGNORE:W0703
            return "Unknown"
        #Return height and width as a string
        return str(width) + "x" + str(height)

def main():
    '''Default main'''
    #set work directory
    work_directory = set_work_dir()
    #set directory for sorted images
    sort_directory = set_sorted_dir(work_directory)
    #Get a full list of subdirs
    full_list_of_dirs = get_full_list_of_dirs(work_directory)
    proceed(full_list_of_dirs, sort_directory)

    #Finally delete the source directory if it is empty
    delete_a_directory(work_directory)

if __name__ == "__main__":
    main()
