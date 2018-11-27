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
	
	util.info('creating new java module project')
	
	# folders
	util.info('\ncreating directories')
	dir_list = list(config.srcDirs + config.resourceDirs + config.dependencyDirs 
			+ [config.compileDir, config.runDir, config.jarDir]
			+ config.testSrcDirs + config.testResourcesDirs + config.testDependencyDirs
			+ [config.testCompileDir + config.testRunDir + config.testReportDir]
			+ [config.localCacheDir]) # list workaround for python being new-line sensitive
	for new_dir in dir_list:
		if not path.exists(new_dir):
			os.makedirs(new_dir)
	
	# sample source code
	util.info('\ncreating source code')
	app_file = path.join(config.srcDirs[0], str(config.mainClass).replace('.', os.sep) + '.java')
	app_test_file = path.join(config.testSrcDirs[0], str(config.mainClass).replace('.', os.sep) + 'Test.java')
	class_name = config.mainClass.split('.')[-1]
	package_name = '.'.join(config.mainClass.split('.')[0:-1])
	module_name = package_name
	module_file = path.join(config.srcDirs[0], str(package_name).replace('.', os.sep) + os.sep + 'module-info.java')
	if not path.exists(app_file):
		util.make_parent_dir(app_file)
		util.info('\n%s:' % app_file)
		with open(app_file, 'w') as fout:
			util.write_and_print("""
package %s;
class %s {
	public static void main(String[] args){
		%s inst = new %s();
		System.out.println(inst.getNumber());
	}
	public int getNumber(){
		return 1;
	}
}
""" % (package_name, class_name, class_name, class_name), fout)
	if not path.exists(module_file):
		util.make_parent_dir(module_file)
		util.info('\n%s:' % module_file)
		with open(module_file, 'w') as fout:
			util.write_and_print("""
module %s {
	exports %s;
}
""" % (module_name, package_name), fout)

	if not path.exists(app_test_file):
		util.make_parent_dir(app_test_file)
		util.info('\n%s:' % app_test_file)
		with open(app_test_file, 'w') as fout:
			util.write_and_print("""
package %s;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class %sTest {
	static %s inst;
	
	@BeforeAll
	static void setup(){
		inst = new %s();
	}

    @Test
    public void numberTest() {
        assertEquals(1, inst.getNumber(), "error: number not equal to 1!");
    }
}
""" % (package_name, class_name, class_name, class_name), fout)
	
	# ignores for hg and git
	util.info('\ncreating DVCS ignore files')
	ignore_list = list([config.compileDir, config.runDir, config.jarDir]
			+ [config.testCompileDir + config.testRunDir + config.testReportDir]
			+ [config.localCacheDir, '__pycache__']) # list workaround for python being new-line sensitive
	util.info('\n.gitignore:')
	with open('.gitignore', 'w') as fout:
		util.write_and_print('\n'.join(map(
				lambda x: str(x).replace('\\', '/')
		, ignore_list)), fout)
		util.write_and_print('\n', fout)
	util.info('\n.hgignore:')
	with open('.hgignore', 'w') as fout:
		util.write_and_print('syntax: glob\n', fout)
		util.write_and_print('\n'.join(map(
				lambda x: str(x).replace('\\', '/')
		, ignore_list)), fout)
		util.write_and_print('\n', fout)
	
# done
