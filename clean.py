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

	util.good('\n\n-----',__file__,'-----\n\n')

	try:
		config.pre_clean()
	except Exception as ex:
		util.error(ex)
		success = False

	try:
		util.del_contents(config.compileDir)
		print() # add a little space
		util.del_contents(config.jarDir)
		print() # add a little space
		util.del_contents(config.runDir)
		print() # add a little space
		util.del_contents(config.testCompileDir)
		print() # add a little space
		util.del_contents(config.testRunDir)
		print() # add a little space
		util.del_contents(config.testReportDir)
		print() # add a little space
		util.del_contents(config.localCacheDir)
	except Exception as ex:
		util.error(ex)
		success = False

	try:
		config.post_clean()
	except Exception as ex:
		util.error(ex)
		success = False

	print() # add a little space
	if(success == True):
		util.good('clean successful')
		exit(0)
	else:
		util.error('clean failed')
		exit(1)
