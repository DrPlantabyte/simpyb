#!/usr/bin/python3

import os
from os import path
import pj_util as util
import config



this_file = path.realpath(__file__)
this_dir = path.dirname(this_file)
if __name__ == '__main__':
	os.chdir(config.rootDir)

	success = True

	# build jar before run
	success = util.command([config.pythonExec, path.join(this_dir, 'jar.py')])

	# make dirs
	if not path.exists(config.runDir):
		os.makedirs(config.runDir)
	if(success == True):
		# pre-run
		try:
			config.pre_run()
		except Exception as ex:
			util.error(ex)
			success = False
	
		# execute in run fulder
		jar_filepath = path.abspath(path.join(config.jarDir, str(config.name)+'.jar'))

		normal_exit = util.command([config.javaExec, '-jar', jar_filepath], working_dir=config.runDir)

		if not normal_exit:
			util.warn('application terminated with non-zero exit status') 

		# post-run
		try:
			config.post_run()
		except Exception as ex:
			util.error(ex)
			success = False

	print() # add a little space
	if(success == True):
		util.good('run successful')
		exit(0)
	else:
		util.error('run failed')
		exit(1)
