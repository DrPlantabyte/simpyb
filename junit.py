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

	junit_packageame = 'junit.platform.console.standalone'
	junit_launch_class = 'org.junit.platform.console.ConsoleLauncher'
	libBlacklist = ['.*apiguardian-api-.*\\.jar']

	# make dirs
	if not path.exists(config.compileDir):
		os.makedirs(config.compileDir)
	if not path.exists(config.testRunDir):
		os.makedirs(config.testRunDir)
	if not path.exists(config.testDependencyDirs[0]):
		os.makedirs(config.testDependencyDirs[0])
	if not path.exists(config.testReportDir):
		os.makedirs(config.testReportDir)
		

	# build before junit tests
	success = util.command([config.pythonExec, path.join(this_dir, 'build.py')])
	# then copy build to test-build directory (to keep the non-test build directory clean)
	util.info('copying latest compile to test compile directory')
	util.copy_dir_contents(config.compileDir, config.testCompileDir)
	print() # linespace


	try:
		config.pre_junit()
	except Exception as ex:
		util.error(ex)
		success = False

	# get module name
	mod_info_file_list = util.get_files(config.srcDirs, ['module-info.java'])
	if(len(mod_info_file_list) < 1):
		# no module info (will cause problems)
		util.error('no module-info.java file found, cannot check module information')
		success = False
	elif(len(mod_info_file_list) > 1):
		# multiple module info files (not allowed)
		util.error('multiple module-info.java files found, but only 1 is allowed per module')
		success = False
	else:
		# just right
		modulename, export_list, require_list = util.parse_moduleinfo(mod_info_file_list[0])

	# compile tests (if file changes detected)
	if(success == True):
		cacheFile = path.join(config.localCacheDir, 'junit-timestamps.txt')
		check_list = config.testSrcDirs + config.testResourcesDirs + config.testDependencyDirs + [config.testCompileDir] + [config.this_file, this_file]
		if(util.detect_file_changes(cacheFile, check_list) == True):
			# file changes detected, re-compile the tests!
			
			# get maven deps
			print() # add a little space
			util.info('fetching maven dependencies')
			success = util.download_maven_dependencies(config.testDependencyDirs[0], config.testMavenDependencies, config.mvnExec, localCacheDir=config.localCacheDir)
			
			if(success == True):
				# test compilation
				util.info('testing file changes detected, compiling junit tests')
				arg_file = path.join(config.localCacheDir, 'junit-javac-args.txt')
				util.make_parent_dir(arg_file)
				#command_list = [config.javacExec]
				command_list = []
				command_list += ['-d', config.testCompileDir]
				command_list += ['--module-path',  
						os.pathsep.join( util.get_files(config.dependencyDirs, ['.jar', '.zip']) 
						+ util.exclude(util.get_files(config.testDependencyDirs, ['.jar', '.zip']), libBlacklist) )
				]
				command_list += ['--add-modules', ','.join( [junit_packageame, modulename] )]
				for srcDir in config.testSrcDirs:
					command_list += ['--patch-module', '%s=%s' % (modulename, srcDir)]
				command_list += ['--add-reads', '%s=%s' % (modulename, junit_packageame)]
				command_list += util.get_files(config.testSrcDirs,['.java'])

				with open(arg_file, 'w') as fout:
					util.info('writing compiler options to temporary file %s' % arg_file)
					util.write_and_print(' '.join(map(util.safe_quote_string, command_list)), fout)
					print() # add line spacing
					print() # add line spacing

				#success = util.command(command_list)
				success = util.command([config.javacExec, '@'+arg_file])
				
			
			# copy test resources
			if(success == True):
				print() # linespace
				util.info('copying test resources')
				for rdir in config.testResourcesDirs:
					util.copy_dir_contents(rdir, config.testCompileDir)
			
			if(success == True):
				# update file timestamp cache
				util.info('updating timestamp cache')
				util.detect_file_changes(cacheFile, check_list)
		else:
			# no file changes, skip building
			util.info('no testing file changes detected, skipping junit compile phase')


	# run tests
	if(success == True):
		print() # add a little space
		util.info('starting junit tests')
		
		test_packages = []
		for sdir in config.testSrcDirs:
			test_packages += map(lambda x: str(path.dirname(path.relpath(x, sdir))).replace(os.sep, '.'), util.get_files([sdir],['.java']))
		test_packages = list(set(test_packages))
		util.info('test packages:', test_packages)
		
		arg_file = path.join(config.localCacheDir, 'test-javac-args.txt')
		util.make_parent_dir(arg_file)
		#command_list = [config.javaExec]
		command_list = []
		command_list += ['--module-path',  os.pathsep.join( map(lambda x: path.relpath(x, config.testRunDir), 
				[config.testCompileDir]
				+ util.get_files(config.dependencyDirs, ['.jar', '.zip'])
				+ util.exclude(util.get_files(config.testDependencyDirs, ['.jar', '.zip']), libBlacklist)
		))]
		command_list += ['--add-modules', ','.join( [junit_packageame, modulename] )]
		command_list += ['--patch-module', '%s=%s' % (modulename, path.relpath(config.testCompileDir, config.testRunDir))]
		command_list += ['--add-reads', '%s=%s' % (modulename, junit_packageame)]
		for test_package in test_packages:
			command_list += ['--add-opens', '%s/%s=%s' % (modulename, test_package, junit_packageame)]
		command_list += [junit_launch_class]
		command_list += ['--fail-if-no-tests'] # no discovered tests == failure
		command_list += ['--reports-dir=%s' % path.relpath(config.testReportDir, config.testRunDir)]
		for test_package in test_packages:
			command_list += ['--select-package=%s' % test_package]
		

		with open(arg_file, 'w') as fout:
			util.info('writing runtime options to temporary file %s' % arg_file)
			util.write_and_print(' '.join(map(util.safe_quote_string, command_list)), fout)
			print() # add line spacing
			print() # add line spacing


		util.good('----- JUNIT TESTS -----\n')
		success = util.command([config.javaExec, '@'+arg_file], working_dir=config.testRunDir)
		
		print()#linespacce
		util.del_file(arg_file)


	try:
		config.post_junit()
	except Exception as ex:
		util.error(ex)
		success = False

	print() # add a little space
	if(success == True):
		util.good('junit tests passed')
		exit(0)
	else:
		util.error('junit tests failed')
		exit(1)
