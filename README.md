# WallPaperSorter
Easy python wallpaper sorter.

18.09.2017 Released Version 2


wallpapers.py [source_dir] [destination_dir]

- Runs in a parent folder with wallpapers.
- Can accept two command line arguments
	[source_dir] - folder with images. (default is "wallpapers")
	[destination_dir] - destination folder. (default is source directory + ".sorted")

- Moving all image files from the src folder to folders.
- Delete [source_dir] if it is empty at the end of run

- If the image size or aspect ratio is unrecognized, it creates a folder "broke_and_unsort"

Python 3.5.2.

I still have some issues with this e.g. moving existing files.
