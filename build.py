#!/usr/bin/python3

import os
from os import path
from tempfile import NamedTemporaryFile
import subprocess
import pj_util as util
import config

this_file = path.realpath(__file__)
this_dir = path.dirname(this_file)
if __name__ == '__main__':
	os.chdir(config.rootDir)

	success = True

	util.good('\n\n-----',__file__,'-----\n\n')

	# do nothing if no files have changed since last time
	cacheFile = path.join(config.localCacheDir, 'build-timestamps.txt')
	check_list = config.srcDirs + config.resourceDirs + config.dependencyDirs + [config.compileDir] + [config.this_file, this_file]
	if(util.detect_file_changes(cacheFile, check_list) == False):
		# no file changes, skip building
		util.info('no file changes detected, skipping build')
		exit(0)

	# make dirs
	if not path.exists(config.compileDir):
		os.makedirs(config.compileDir)
	if not path.exists(config.testCompileDir):
		os.makedirs(config.testCompileDir)

	# clean before build
	success = util.command([config.pythonExec, path.join(this_dir, 'clean.py')])

	try:
		config.pre_build()
	except Exception as ex:
		util.error(ex)
		success = False

	# maven dependency download
	if(success == True):
		print() # add a little space
		util.info('fetching maven dependencies')
		success = util.download_maven_dependencies(config.dependencyDirs[0], config.mavenDependencies, config.mvnExec)

	# module check
	if(success == True):
		print() # add a little space
		util.info('checking module requirements')
		mod_info_file_list = util.get_files(config.srcDirs, ['module-info.java'])
		if(len(mod_info_file_list) < 1):
			# no module info (will cause problems)
			util.error('no module-info.java file found, cannot check module requirements')
			success = False
		elif(len(mod_info_file_list) > 1):
			# multiple module info files (not allowed)
			util.error('multiple module-info.java files found, but only 1 is allowed per module')
			success = False
		else:
			# just right
			command_list = [config.javaExec]
			command_list += ['--module-path',  os.pathsep.join(
				util.get_files(config.dependencyDirs, ['.jar', '.zip'])
			)]
			command_list += ['--list-modules']
			std_output, success = util.command_output(command_list)
			util.good(('available modules:\n'+std_output).replace('\n','\n\t'))
			success, list_of_missing, list_of_unused = util.check_modules(std_output, mod_info_file_list[0])
			if(len(list_of_unused) > 0):
				util.warn('non-required modules in module path: %s' % list_of_unused)
			if(len(list_of_missing) > 0):
				util.error('error, required modules not found in module path: %s' % list_of_missing)
		


	# compile
	if(success == True):
		print() # add a little space
		util.info('compiling sources')
		arg_file = NamedTemporaryFile().name
		#command_list = [config.javacExec]
		command_list = []
		command_list += ['-d', config.compileDir]
		command_list += ['--module-path',  os.pathsep.join(
			util.get_files(config.dependencyDirs, ['.jar', '.zip'])
		)]
		command_list += util.get_files(config.srcDirs,['.java'])

		with open(arg_file, 'w') as fout:
			util.info('writing compiler options to temporary file %s' % arg_file)
			util.write_and_print(' '.join(map(util.safe_quote_string, command_list)), fout)
			print() # add line spacing
			print() # add line spacing

		#success = util.command(command_list)
		success = util.command([config.javacExec, '@'+arg_file])
		
		util.del_file(arg_file)

	# copy resources
	if(success == True):
		print() # add a little space
		util.info('copying resources')
		try:
			for resource_dir in config.resourceDirs:
				util.copy_dir_contents(resource_dir, config.compileDir)
		except Exception as ex:
			util.error(ex)
			util.error('failed to copy one or more resource files')
			success = False

	try:
		config.post_build()
	except Exception as ex:
		util.error(ex)
		success = False

	if(success == True):
		# update file-changed cache
		print() # linespace
		util.info('updating timestamp cache')
		util.detect_file_changes(cacheFile, check_list)

	print() # add a little space
	if(success == True):
		util.good('build successful')
		exit(0)
	else:
		util.error('build failed')
		exit(1)
