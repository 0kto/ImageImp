#!/usr/bin/python3

import sys, getopt, os
# get configuration
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
import threading

# import definitions and classes
from class_ExifTool import ExifTool

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
			split_extract_embedded_jpg(args)


def usage():
	print("iimg options <filelist>")
	print("")
	print("available options")
	print("-e, --extract     extract embedded .jpg from .cr2")


def split_extract_embedded_jpg(items, num_splits=4):
	split_size = len(items) // num_splits
	threads = []
	with ExifTool() as e:
		for i in range(num_splits):
			start = i * split_size
			end = None if i+1 == num_splits else (i+1) * split_size                 
			threads.append(
				threading.Thread(target=process, args=(e.extract_embedded_jpg, items, start, end)))
			threads[-1].start()
		for t in threads:
			t.join()
			
def process(function, items, start, end):
	for item in items[start:end]:
		try:
			function(item)
		except Exception:
			print('error with item')


			
if __name__ == "__main__":
	main()
