#!/usr/bin/python3

import os
from os import path
import sys

this_os_arch='unknown'
if 'win' in sys.platform: this_os_arch='windows-x64'
if 'linux' in sys.platform: this_os_arch='linux-x64'
if 'darwin' in sys.platform: this_os_arch='osx-x64'


module_list=[
	'my.project.core', 
	'my.project.gui', 
	'my.project.testing']
main_module='my.project.gui'
main_class='my.project.gui.App'


temp_dir = 'temp'
build_dir = 'out'
run_dir = path.join(build_dir,'run')
module_dir='modules'

maven_dep_dir=path.join('dependencies','maven')
jar_dep_dir=path.join('dependencies','jars')
universal_jmod_dep_dir=path.join('dependencies','jmods')
native_jmod_dep_dir=path.join('dependencies','native','jmods',this_os_arch)
dependency_dirs=[
	jar_dep_dir,
	maven_dep_dir,
	universal_jmod_dep_dir,
	native_jmod_dep_dir,
	path.join(os.environ['JAVA_HOME'], 'jmods') ,
]
timestamp_cachefile=path.join(temp_dir, 'file_timestamp_cache.json')

sources_dirname = 'src'
resources_dirname = 'resources'

maven_deps = ['com.google.code.gson:gson:2.8.6',]

java_exec='java'
javac_exec='javac'
jlink_exec='jlink'
python_exec='python'
maven_exec='mvn'

this_file = path.realpath(__file__)
this_dir = path.dirname(this_file)
root_dir = path.dirname(path.abspath(__file__))


