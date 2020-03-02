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
"""handles setting of options, and dispatching of tasks for parallel processing."""
	try:
		opts, args = getopt.getopt(sys.argv[1:], "eho:",["extract","help","import","outputdir"]) 
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
			if not 'outputdir' in locals():
				outputdir = "."
			with ExifTool() as e:
				parallel_processing(lambda file: e.import_raw(file, outputdir), args)
		else:
			usage()
			sys.exit()



def usage():
"""print usage and implemented options"""
	print("imageimp options <filelist>")
	print("")
	print("available options (always specify short-options first!)")
	print("-e, --extract     extract embedded .jpg from .cr2")
	print("-o, --outputdir   specify output directory")
	print("    --import      import .cr2 files")


def parallel_processing(function, items, num_splits=config['general'].getint('processes')):
"""wrapping to execute an arbitrary functions acting on a list of items in parallel"""
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
"""target process loop for the prarallel_processing function"""
	for item in items[start:end]:
		try:
			function(item)
		except Exception:
			print('error with item')
			
if __name__ == "__main__":
	main()
