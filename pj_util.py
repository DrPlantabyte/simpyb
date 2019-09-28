#!/usr/bin/python3

import sys, os, shutil
from os import path
from urllib.request import pathname2url
import subprocess
from subprocess import call
import sys
import re

COLORS_ENABLED = True
if 'win' in sys.platform:
	OPERATING_SYSTEM = 'windows'
	COLORS_ENABLED = False # PowerShell does not support \...[...m color codes
elif 'linux' in sys.platform:
	OPERATING_SYSTEM = 'linux'
elif 'darwin' in sys.platform:
	OPERATING_SYSTEM = 'mac'
else:
	OPERATING_SYSTEM = 'unknown'

def info(*args, **kwargs):
	if(COLORS_ENABLED == True):
		print('\033[1;34m', end='')
	print(*args, **kwargs)
	if(COLORS_ENABLED == True):
		print('\033[0m', end='')
def warn(*args, **kwargs):
	if(COLORS_ENABLED == True):
		print('\033[1;33m', end='')
	print(*args, **kwargs)
	if(COLORS_ENABLED == True):
		print('\033[0m', end='')
def error(*args, **kwargs):
	if(COLORS_ENABLED == True):
		print('\033[1;31m', end='')
	print(*args, **kwargs)
	if(COLORS_ENABLED == True):
		print('\033[0m', end='')
def good(*args, **kwargs):
	if(COLORS_ENABLED == True):
		print('\033[1;32m', end='')
	print(*args, **kwargs)
	if(COLORS_ENABLED == True):
		print('\033[0m', end='')
def action(*args, **kwargs):
	if(COLORS_ENABLED == True):
		print('\033[1;35m', end='')
	print(*args, **kwargs)
	if(COLORS_ENABLED == True):
		print('\033[0m', end='')

def write_and_print(text_str, file_out):
	action(text_str, end='')
	file_out.write(text_str)

def download_maven_dependencies(download_dir, list_of_gradle_strings, maven_command='mvn', working_dir='.', localCacheDir='./temp'):
	"""
	download_maven_dependencies(download_dir, list_of_gradle_strings, maven_command='mvn', working_dir='.')
	
	Downloads .jar library files from the maven repositories, with 
	dependency resolution, and places them in the specified download directory.
	Returns True or False to indicate success
	
	For example:
	success = download_maven_dependencies('./libs', ['org.openjfx:javafx-fxml:12-ea+2', 'org.junit.jupiter:junit-jupiter-api:5.3.1'])
	
	download_dir - filepath of destination folder
	list_of_gradle_strings - list of gradle-style repository strings, in the 
	format of 'groupId:artifactId:version'
	maven_command - (optional) path to or name of maven command. Default: 'mvn'
	working_dir - (optional) in which directory to run this command
	localCacheDir - This is where the temporary pom.xml file will be stored
	
	returns: True if the operation was a success, False otherwise
	"""
	if(len(list_of_gradle_strings) <= 0):
		# no deps, do nothing
		return True
	if not path.exists(download_dir):
		os.makedirs(download_dir)
	pom_file = path.join(localCacheDir, 'mock-pom.xml')
	make_parent_dir(pom_file)
	with open(pom_file, 'w') as pout:
		pout.write('<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"> <modelVersion>4.0.0</modelVersion> <groupId>project</groupId> <artifactId>dependency</artifactId> <version>list</version> \n<dependencies>\n')
		for lib_str in list_of_gradle_strings:
			tokens = lib_str.strip().split(':')
			action('groupId: %s; artifactId: %s; version: %s' % tuple(tokens) )
			if(len(tokens) != 3):
				error('invalid maven dependency string "%s"\nmaven dependencies must be in format of "groupId:artifactId:version"' % lib_str)
				return False
			pout.write(' <dependency>')
			pout.write('  <groupId>%s</groupId>' % tokens[0])
			pout.write('  <artifactId>%s</artifactId>' % tokens[1])
			pout.write('  <version>%s</version>' % tokens[2])
			pout.write(' </dependency>')
		pout.write('</dependencies> </project>')
	bool_result = command([maven_command, '-f', str(path.abspath(pom_file)), 'dependency:copy-dependencies', '-DoutputDirectory=%s' % path.abspath(download_dir)], working_dir=working_dir)
	if bool_result == False:
		error('failed to run mvn command')
	return bool_result
	
def list_filetree(dirpath):
	"""
	list_filetree(dirpath)
	
	Returns a list of all files inside a directory (recursive scan)
	
	dirpath - filepath of directory to scan
	"""
	file_list = []
	for base, directories, files in os.walk(dirpath):
		for f in files:
			file_list.append(path.join(base,f))
	return file_list
def get_files(dir_list, suffix_list):
	"""
	get_files(dir_list, suffix_list)
	
	Recursively scans all of the given directories for files with the 
	given file endings and returns them as a list
	
	If suffix_list is an empty list, then all files will be included 
	instead of filtering by file extension
	
	dir_list - list of directories to scan
	suffix_list - list of valid file extensions (case-sensitive). Ex: ['.jar', '.zip']
	"""
	#info('scanning directories %s for files ending in %s' % (dir_list, suffix_list))
	allFiles = []
	for search_dir in dir_list:
		for f in list_filetree(search_dir):
			allFiles.append(f)
	filtered_files = []
	for f in allFiles:
		if(len(suffix_list) > 0):
			for ending in suffix_list:
				if(str(f).endswith(ending)):
					filtered_files.append(f)
		else:
			filtered_files.append(f)
	return filtered_files
def safe_quote_string(text):
	"""
	safe_quote_string(text)
	
	returns the text in quotes, with escapes for any quotes in the text itself
	
	text - input text to quote
	
	returns: text in quotes with escapes
	"""
	text2 = text.replace('\\', '\\\\')
	text3 = text2.replace('"', '\"')
	return '"'+text3+'"'

def command(command_and_args_list, working_dir='.'):
	"""
	command(command_and_args_list, working_dir='.')
	
	calls the first item in the list as a command and passes the rest as 
	arguments (should be a list of strings).
	
	Returns True if the command returned 0 (usually means success) and 
	False otherwise
	
	command_and_args_list - command and arguments as a list of string-like objects
	working_dir - (optional) in which directory to run this command
	
	returns: True|False (True if exit code from command is 0, False otherwise)
	"""
	action('\n%s $ ' % working_dir, ' '.join(command_and_args_list), '\n', sep='')
	bool_result = 0 == call(command_and_args_list, cwd=working_dir)
	return bool_result
def command_output(command_and_args_list, working_dir='.'):
	"""
	command_output(command_and_args_list, working_dir='.')
	
	calls the first item in the list as a command and passes the rest as 
	arguments (should be a list of strings), redirecting the stdout to an 
	internal pipe and returning the stdout buffer upon completion of the 
	command.
	
	command_and_args_list - command and arguments as a list of string-like objects
	working_dir - (optional) in which directory to run this command
	
	
	Returns: str, boolean
	str - the stdout buffer as a text string
	boolean - True if the returncode from the command was 0, False otherwise
	"""
	action('\n%s $ ' % working_dir, ' '.join(command_and_args_list), '', sep='')
	proc = subprocess.Popen(command_and_args_list, stdout=subprocess.PIPE)
	output, output_err = proc.communicate() # this is supposed to wait until process completes
	if(output_err != None and len(output_err) > 0):
		error(output_err)
	output_str = output.decode('utf8') # subprocess returns binary string in OS native encoding, so we need to convert it
	ret_bool = 0 == proc.returncode
	return output_str, ret_bool

def del_file(filepath):
	"""
	del_file(filepath):
	
	Deletes a file or recursively deletes a directory. Use with caution.
	
	filepath - path to file or directory to delete
	"""
	if(path.isdir(filepath)):
		for f in os.listdir(filepath):
			_del(path.join(filepath,f))
		info('deleting directory:',filepath)
		os.rmdir(filepath)
	elif(path.exists(filepath)):
		info('deleting file:',filepath)
		os.remove(filepath)

def _del(filepath):
	"""
	Deletes a file or recursively deletes a directory. Use with caution.
	"""
	if(path.isdir(filepath)):
		for f in os.listdir(filepath):
			_del(path.join(filepath,f))
		info('deleting directory:',filepath)
		os.rmdir(filepath)
	elif(path.exists(filepath)):
		info('deleting file:',filepath)
		os.remove(filepath)
def del_contents(dirpath):
	""" 
	del_contents(dirpath)
	
	Recursively deletes the contents of a directory, but not the directory itself
	
	dirpath - path to directory to clean-out
	"""
	if(path.isdir(dirpath)):
		for f in os.listdir(dirpath):
			del_file(path.join(dirpath,f))
def copy_dir_contents(src_dir, dest_dir):
	"""
	copy_dir_contents(src_dir, dest_dir)
	
	Copies the files in src_dir into dest_dir
	"""
	if not path.isdir(src_dir):
		return # do nothing
	for base, dirs, files in os.walk(src_dir):
		for f in files:
			src_file = path.join(base,f)
			dest_file = path.join(dest_dir, path.relpath(src_file, src_dir))
			copy_file(src_file, dest_file)
def make_parent_dir(file_path):
	"""
	make_parent_dir(file_path)
	
	Creates the parent directory for the specified filepath if it does not 
	already exist.
	
	file_path - path to some file
	"""
	parent_dir = path.dirname(file_path)
	if parent_dir == '': # means parent is working directory
		return
	if not path.isdir(parent_dir):
		info('creating directory %s' % parent_dir)
		os.makedirs(parent_dir)
def copy_file(src_file, dest_file, overwrite=True):
	"""
	copy_file(src_file, dest_file, overwrite=True)
	
	Copies a file, creating any necessary directories, and overwriting the desitnation 
	unless otherwise specified.
	
	src_file - the file to copy
	dest_file - the new file to create
	overwrite - if True, replace the existing if it exists, if False, do nothing
	if the existing file already exists
	"""
	if(path.exists(dest_file) == True and overwrite == False):
		return
	make_parent_dir(dest_file)
	action('copying %s to %s' % (src_file, dest_file))
	shutil.copy2(src_file, dest_file)

def write_manifest( manifest_path, main_class=None, libs_list=None ):
	"""
	write_manifest( manifest_path, main_class, libs_list )
	
	Writes a simple MANIFEST.MF file
	
	manifest_path - filepath of the file to create/write
	main_class - (optional) jar main class
	libs_list - (optional) list of dependency filepaths to include in the classpath
	"""
	action('creating manifest file %s' % manifest_path)
	with open(manifest_path, 'w') as mout:
		write_and_print('Manifest-Version: 1.0\n', mout)
		if(main_class != None):
			write_and_print('Main-Class: %s\n' % main_class, mout)
		if libs_list != None and len(libs_list) > 0:
			write_and_print('Class-Path: \n %s\n\n' % ('\n '.join( map(pathname2url, libs_list) )), mout)

def check_modules(java_list_modules_output, module_info_file):
	"""
	check_modules(java_list_modules_output, module_info_file)
	
	Parses the output of an invocation of the 'java --list-modules' command and 
	the content of the provided 'module-info.java' file and then returns True 
	if all of the reqiured modules in the 'module-info.java' file are available.
	
	java_list_modules_output - string output from the 'java --list-modules' command
	module_info_file - path to module-info.java file
	
	returns: True|False, list_of_missing, list_of_unused
	True|False- True if all required modules are represented in java_list_modules_output, 
	False otherwise (a False return indicates that 1 or more modules is missing)
	list_of_missing - list of missing modules
	list_of_unused - list of unused modules (modules avilable that are not required), 
	not including modules built-in to the java platform
	"""
	avilable_modules = []
	nonjdk_available_modules = []
	for module_line in java_list_modules_output.split('\n'):
		if(len(module_line.strip()) > 0):
			module_name, module_version, module_source, is_automatic = parse_module_list_line(module_line)
			avilable_modules.append(module_name)
			if(len(module_source) > 0):
				nonjdk_available_modules.append(module_name)
	mod_name, mod_exports, required_modules = parse_moduleinfo(module_info_file)
	list_of_missing = []
	list_of_unused = []
	for mod_req in required_modules:
		if not mod_req in avilable_modules:
			list_of_missing.append(mod_req)
	for avail_mod in nonjdk_available_modules:
		if not avail_mod in required_modules:
			list_of_unused.append(avail_mod)
	bool_good = len(list_of_missing) == 0
	return bool_good, list_of_missing, list_of_unused
def	decomment(java_text):
	"""
	removes java-style (aka C-style) comments from string
	"""
	content1 = re.sub('//.*\n','\n',java_text) # remove single-line comments
	content2 = re.sub('/\\*+[^*]*\\*+(?:[^/*][^*]*\\*+)*/','',content1) # remove multi-line comments
	return content2
def parse_module_list_line(module_line):
	"""
	parse_module_list_line(module_line)
	
	Parses a line from the 'java --list-modules' output, such as 'java.sql@11; or 
	'javafx.controlsEmpty@11.0.1 file:///javafx-controls-11.0.1.jar automatic' or 
	'com.grack.nanojson file:///nanojson.jar' and returns the module name, version, and source
	
	module_line - one line from the output of 'java --list-modules'

	returns: module_name, module_version, module_source, is_automatic
	module_name - name of the module
	module_version - version number of the module (0 if none specified)
	module_source - source url of the module (empty string for java built-in modules)
	is_automatic - True if the module is an automatic module (this usually means 
	it is a .jar file lacking a module-info declaration), False otherwise
	"""
	version = '0'
	name = 'ERROR'
	source = ''
	is_automatic = False
	tokens = re.split('\\s',module_line.strip())
	name_and_version = tokens[0].split('@')
	name = name_and_version[0]
	if(len(name_and_version) > 1):
		version = name_and_version[1]
	if(len(tokens) > 1):
		source = tokens[1]
	if('automatic' == tokens[-1]):
		is_automatic = True
	return name, version, source, is_automatic
def get_module_declaration(search_dir_list):
	"""
	get_module_declaration(search_dir_list)
	
	Searches the given directories for the module-info.java file and parses is for required 
	and exported modules. For example:
	
	module_name, export_list, requires_list = parse_moduleinfo(['src/main/java'])
	
	returns module_name, export_list, requires_list
	module_name - name of this module
	export_list - exported java packages
	requires_list - required modules
	"""
	mod_info_file_list = get_files(search_dir_list, ['module-info.java'])
	if len(mod_info_file_list) == 0:
		raise FileNotFoundError('Unable to find module-info.java in [%s]' % (', '.join(search_dir_list)) )
	elif len(mod_info_file_list) != 1:
		raise FileNotFoundError('Multiple copies of module-info.java found in [%s]. Only one is allowed.' % (', '.join(search_dir_list)) )
	module_name, export_list, requires_list = parse_moduleinfo( mod_info_file_list[0] )
	return module_name, export_list, requires_list
	
def parse_moduleinfo(modinfo_filepath):
	"""
	parse_moduleinfo(modinfo_filepath)
	
	Parses a java module-info.java file to store the module name and 
	exported packages and required modules in a dictionary as follows:
	
	module_name, export_list, requires_list = parse_moduleinfo('src/main/module-info.java')
	
	returns module_name, export_list, requires_list
	module_name - name of this module
	export_list - exported java packages
	requires_list - required modules
	"""
	info('parsing module-info file %s...' % modinfo_filepath)
	results = {}
	with open(modinfo_filepath) as fin:
		content = fin.read()
	content = decomment(content)
	lines = re.split('{|}|;', content)
	modulename = None
	export_list = []
	require_list = []
	for ln in lines:
		line = ln.strip()
		tokens = re.split('\\s',line)
		if 'module' in line:
			modulename = str(tokens[-1]).strip() # TODO: check that this works for all valid module declarations
		if 'exports' in line:
			export_list.append(str(tokens[-1]).strip())
		if 'requires' in line:
			require_list.append(str(tokens[-1]).strip())
	return modulename, export_list, require_list
def detect_file_changes(cache_file, dir_and_file_list):
	"""
	detect_file_changes(cache_file, dir_and_file_list)
	
	Recursively scand the list of filepaths and returns True if any file 
	has changed since the last time this function was called (or if this is 
	the first time this function has been called).
	
	Note that calling this function updates the timestamp cache.
	
	cache_file - file to use for caching the file-scan data
	dir_and_file_list - list of directories and/or files
	
	returns: True|False (False only if no changes have been detected)
	"""
	change_detected = False
	# first, load the cache to a dict
	file_lut = {}
	if not path.exists(cache_file):
		change_detected = True
	else:
		with open(cache_file, 'r') as fin:
			for ln in fin.readlines():
				if os.pathsep in ln:
					parts = ln.split(os.pathsep)
					file_lut[parts[0]] = parts[1].strip()
	
	# then scan for missing, added, or changed files
	for filepath in dir_and_file_list:
		if path.isfile(filepath):
			# file
			filename = path.realpath(filepath)
			timestamp = str(path.getmtime(filename))
			if filename not in file_lut or file_lut[filename] != timestamp:
				change_detected = True
			file_lut[filename] = timestamp
		elif path.isdir(filepath):
			# directory
			for base, directories, files in os.walk(filepath):
				for f in files:
					filename = path.realpath(path.join(base,f))
					timestamp = str(path.getmtime(filename))
					if filename not in file_lut or file_lut[filename] != timestamp:
						change_detected = True
					file_lut[filename] = timestamp
		else:
			# file or directory does not exist
			change_detected = True
	# finally, write the new cache	
	make_parent_dir(cache_file)
	with open(cache_file, 'w') as fout:
		for reg_file in file_lut:
			fout.write(str(path.realpath(reg_file)))
			fout.write(os.pathsep)
			fout.write(str(file_lut[reg_file]))
			fout.write('\n')
	return change_detected
def exclude(input_list, regex_blacklist):
	"""
	exclude(input_list, regex_blacklist)
	
	filters the given list and returns a list that does not contain any 
	elements that match any of the regex patterns in the blacklist.
	
	input_list - list of strings
	regex_blacklist - list of regex strings
	
	returns: copy of input_list lacking any blacklist-matching elements
	"""
	output_list = []
	for e in input_list:
		good = True
		for ban in regex_blacklist:
			good = good and (re.match(ban, e) == None)
		if(good == True):
			output_list.append(e)
	return output_list
