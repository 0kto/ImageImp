import subprocess
import json
import os
import glob

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# from https://stackoverflow.com/questions/10075115/call-exiftool-from-a-python-script
class ExifTool(object):
	"""Class that initializes an ExifTool object and passes jobs to it."""
	sentinel = "{ready}\n"

	def __init__(self, executable="exiftool"):
		"""Initialize ExifTool"""
		self.executable = executable

	def __enter__(self):
		"""open object and make ExifTools stay open"""
		self.process = subprocess.Popen(
			[self.executable, "-stay_open", "True",  "-@", "-"],
			universal_newlines=True,
			stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		return self

	def  __exit__(self, exc_type, exc_value, traceback):
		"""close ExifTool object"""
		self.process.stdin.write("-stay_open\nFalse\n")
		self.process.stdin.flush()

	def execute(self, *args):
		"""pass arbitrary commands to Exiftool"""
		args = args + ("-execute\n",)
		self.process.stdin.write(str.join("\n", args))
		self.process.stdin.flush()
		output = ""
		fd = self.process.stdout.fileno()
		while not output.endswith(self.sentinel):
			output += os.read(fd, 4096).decode('utf-8')
		return output[:-len(self.sentinel)]

	def extract_embedded_jpg(self, filename):
		"""function to extract embedded jpg from Canon cr2 files."""
		basename, ext = os.path.splitext(filename)
		if not ext in json.loads(config.get('ExifTool','rawformats')):
			print(f"'{filename}' ignored: not a raw format")

		elif os.path.isfile(f"{basename}.jpg"):
			print(f"'{filename}' ignored: pre-existing '.jpg'")

		else:
			self.execute("-PreviewImage", "-b", "-w", "%d%f.jpg", filename)
			print(f"'{filename}': embedded '.jpg' extracted")

	def import_raw(self, filename, output_dir):
		"""function to import directories and files"""
		basename, ext = os.path.splitext(filename)
		if ext in json.loads(config.get('ExifTool','rawformats')):
			sidecarfiles = glob.glob(f"{basename}.???")
			sidecarfiles.remove(filename)

			for sidecar in sidecarfiles + [filename]:
				self.execute(
					"-tagsfromfile", f"{filename}",
					"-d", f"{output_dir}/%Y/%V/%Y-%m-%d_%H-%M-%S",
					"-FileName<${CreateDate}_${MyModel}_${FileIndex}.%le",
					f"{sidecar}")
