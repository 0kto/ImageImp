# ImageImp
python wrapper for ExifTool that helps importing images into an image repository, and extracts embedded jpg files from raw files.
This script processes multiple files at the same time, which should make it faster than plain ExifTool, that is not making use of multithreading.

## Configuration
All configuration should occur in the `config.ini` file. It defaults to

    [general]
    # number of parallel threads
    processes = 8

    [ExifTool]
    # date-format used during file import
    dateformat = "%Y/%V/%Y-%m-%d_%H-%M-%S"
    # currently only Canon raw files are supported
    rawformats = [".cr2", ".CR2"]
    
## Usage
### help
    imageimp -h / --help
    
### extract embedded JPG files from RAW files
    imageimp --extract <file-list>

### import RAW files and sidecars
    imageimp [-o <path/to/archive>] --import <file-list>
