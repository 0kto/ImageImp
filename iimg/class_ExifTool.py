import subprocess
import json
import os


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
		basename, ext = os.path.splitext(filename)
		if not os.path.isfile(f"{basename}.cr2"):
			print(f"ignoring '{basename}'")

		elif os.path.isfile(f"{basename}.jpg"):
			print(f"pre-existing '{basename}'.jpg")

		else:
			self.execute("-b", "-PreviewImage", "-w", ".jpg", f"{basename}.cr2")
			print(f"extracted {basename}.jpg")

	def import_raw(self, filename, output_dir):
		basename, ext = os.path.splitext(filename)
		self.execute(
			"-d", f"{output_dir}/%Y/%V/%Y-%m-%d_%H-%M-%S",
			"-FileName<${CreateDate}_${MyModel}_${FileIndex}.%le",
			f"{filename}")
