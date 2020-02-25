#!/usr/bin/python3

import sys, getopt, os
import subprocess
import json

# from https://stackoverflow.com/questions/10075115/call-exiftool-from-a-python-script
class ExifTool(object):
	sentinel = "{ready}\n"

	def __init__(self, executable="exiftool"):
		self.executable = executable

	def __enter__(self):
		self.process = subprocess.Popen(
			[self.executable, "-stay_open", "True",  "-@", "-"],
			universal_newlines=True,
			stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		return self

	def  __exit__(self, exc_type, exc_value, traceback):
		self.process.stdin.write("-stay_open\nFalse\n")
		self.process.stdin.flush()

	def execute(self, *args):
		args = args + ("-execute\n",)
		self.process.stdin.write(str.join("\n", args))
		self.process.stdin.flush()
		output = ""
		fd = self.process.stdout.fileno()
		while not output.endswith(self.sentinel):
			output += os.read(fd, 4096).decode('utf-8')
		return output[:-len(self.sentinel)]

	def extract_embedded_jpg(self, filename):
		self.execute("-b", "-PreviewImage", "-w", ".jpg", filename)

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
			extract_embedded_jpg(args)

def usage():
	print("iimg options <filelist>")
	print("")
	print("available options")
	print("-e, --extract     extract embedded .jpg from .cr2")

def extract_embedded_jpg(files):
	for file in files:
		basename, ext = os.path.splitext(file)
		if not os.path.isfile(f"{basename}.cr2"):
			print(f"no .cr2 file for '{basename}' available.")
		elif os.path.isfile(f"{basename}.jpg"):
			print(f".jpg file already exists for '{basename}'")
		else:
			with ExifTool() as e:
				metadata = e.extract_embedded_jpg(f"{basename}.cr2")

if __name__ == "__main__":
	main()