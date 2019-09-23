#!/usr/bin/python3

from os import path


this_file = path.realpath(__file__)
this_dir = path.dirname(this_file)

rootDir = path.dirname(path.abspath(__file__)) # change if this file is not in project root directory

#project settings
name = 'myapp'
compileDir = 'compile'
jarDir = 'out'
runDir = 'run'
localCacheDir = 'cache'
srcDirs = ['src/main/java']
resourceDirs = ['src/main/resources']
dependencyDirs = ['libs']
mavenDependencies = ['org.openjfx:javafx-fxml:11.0.2']
testSrcDirs = ['src/test/java']
testResourcesDirs = ['src/test/resources']
testDependencyDirs = ['test-libs']
testRunDir = 'test-run'
testReportDir = 'test-reports'
testCompileDir = 'test-compile'
testMavenDependencies = ['org.junit.platform:junit-platform-console-standalone:1.4.2']
manifestFile = None
mainClass = 'myorg.myapp.App'



# binaries
javaExec = 'java'
javacExec = 'javac'
jarExec = 'jar'
mvnExec = 'mvn'
pythonExec = 'python3'

# hooks for custom modifications
def pre_clean():
	pass
def post_clean():
	pass
def pre_build():
	pass
def post_build():
	pass
def pre_jar():
	pass
def post_jar():
	pass
def pre_run():
	pass
def post_run():
	pass
def pre_junit():
	pass
def post_junit():
	pass

# OS-specific mods
import sys
if 'win' in sys.platform:
	# windows
	pythonExec = 'python.exe'
	pass
elif 'linux' in sys.platform:
	# linux
	pass
elif 'darwin' in sys.platform:
	# mac
	pass
else:
	# unknown
	pass

