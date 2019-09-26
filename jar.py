#!/usr/bin/python3

import os
from os import path
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
	cacheFile = path.join(config.localCacheDir, 'jar-timestamps.txt')
	check_list = config.srcDirs + config.resourceDirs + config.dependencyDirs + [config.compileDir] + [config.jarDir] + [config.this_file, this_file]
	if(util.detect_file_changes(cacheFile, check_list) == False):
		# no file changes, skip building
		util.info('no file changes detected, skipping jar operation')
		exit(0)

	# make dirs
	if not path.exists(config.compileDir):
		os.makedirs(config.compileDir)
	if not path.exists(config.jarDir):
		os.makedirs(config.jarDir)

	# build before jar
	success = util.command([config.pythonExec, path.join(this_dir, 'build.py')])

	try:
		config.pre_jar()
	except Exception as ex:
		util.error(ex)
		success = False

	# make jar
	if(success == True):
		print() # add a little space
		util.info('creating jar file')
		command_list = [config.jarExec]
		command_list += ['-c']
		command_list += ['-f', path.join(config.jarDir, str(config.name)+'.jar') ]
		
		# manifest handling
		if(config.manifestFile != None and path.exists(config.manifestFile)):
			util.info('using manifest file %s' % config.manifestFile)
			command_list += ['-m', config.manifestFile ]
		else:
			util.info('generating manifest file')
			tmp_manifest_file = path.join(config.localCacheDir,'MANIFEST.MF')
			util.make_parent_dir(tmp_manifest_file)
			util.write_manifest( tmp_manifest_file, config.mainClass, util.get_files(config.dependencyDirs, ['.jar', '.zip']) )
			command_list += ['-m', tmp_manifest_file ]
		
		command_list += ['-C', config.compileDir ]
		command_list += ['.' ]

		success = util.command(command_list)
		
		if tmp_manifest_file != None:
			util.del_file(tmp_manifest_file)

	# copy libs
	if(success == True):
		try:
			print() # add a line space
			util.info('copying dependencies')
			for lib_dir in config.dependencyDirs:
				dest_dir = path.join(config.jarDir, lib_dir)
				util.copy_dir_contents(lib_dir, dest_dir)
		except Exception as ex:
			util.error(ex)
			util.error('failed to copy one or more depenndency files')
			success = False

	try:
		config.post_jar()
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
