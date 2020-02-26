#!/usr/bin/python3

import sys, getopt, os
from multiprocessing import Pool

# import definitions and classes
import class_ExifTool

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "he",["help","extract"]) 
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-e", "--extract"):
			with Pool(5) as p:
				p.map(extract_embedded_jpg, args)

def usage():
	print("iimg options <filelist>")
	print("")
	print("available options")
	print("-e, --extract     extract embedded .jpg from .cr2")

def extract_embedded_jpg(file):
	basename, ext = os.path.splitext(file)
	if not os.path.isfile(f"{basename}.cr2"):
		print(f"ignoring '{basename}'")

	elif os.path.isfile(f"{basename}.jpg"):
		print(f"pre-existing '{basename}'.jpg")

	else:
		with ExifTool() as e:
			metadata = e.extract_embedded_jpg(f"{basename}.cr2")
		print(f"extracted {basename}.jpg")

if __name__ == "__main__":
	main()