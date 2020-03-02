# ImageImp
python wrapper for ExifTool that helps importing images into an image repository, and extracts embedded jpg files from raw files.
This script processes multiple files at the same time, which should make it faster than plain ExifTool, that is not making use of multithreading.