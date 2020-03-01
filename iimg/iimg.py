#!/usr/bin/python3
import os
import sys
import getopt
import glob

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
import threading

# import definitions and classes
from class_ExifTool import ExifTool

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "eho:",["extract","help","import"]) 
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-e", "--extract"):
			with ExifTool() as e:
				parallel_processing(e.extract_embedded_jpg, args)
		elif o in ("-o"):
			outputdir = a
		elif o in ("--import"):
			with ExifTool() as e:
				parallel_processing(lambda file: e.import_raw(file, outputdir), args)


def usage():
	print("iimg options <filelist>")
	print("")
	print("available options")
	print("-e, --extract     extract embedded .jpg from .cr2")


def parallel_processing(function, items, num_splits=config['general'].getint('processes')):
	split_size = len(items) // num_splits
	threads = []
	for i in range(num_splits):
		start = i * split_size
		end = None if i+1 == num_splits else (i+1) * split_size                 
		threads.append(
			threading.Thread(target=process, args=(function, items, start, end)))
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
