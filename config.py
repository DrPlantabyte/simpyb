#!/usr/bin/python3

from os import path


this_file = path.realpath(__file__)
this_dir = path.dirname(this_file)

rootDir = path.dirname(path.abspath(__file__)) # change if this file is not in project root directory

#project settings
name = 'myapp' # module name
compileDir = 'compile' # intermediary compiled files (ie .class files) are sotered here
jarDir = 'out' # compiled binaries (aka artifects) go here
runDir = 'run' # working directory when using the run script
localCacheDir = 'cache' # temporary generated files
srcDirs = ['src/main/java'] # code files
resourceDirs = ['src/main/resources'] # non-code files that should be included with the generated binaries
dependencyDirs = ['libs'] # libraries (.jar files/modules)
mavenDependencies = [ # maven dependencies in format groupId:artifactId:version		# Below are some popular maven libraries. Change to suit your particular project!		'org.ojalgo:ojalgo:47.3.1',		'com.google.guava:guava:28.1-jre',		'commons-io:commons-io:2.6',
		'org.apache.logging.log4j:log4j-core:2.12.1',
		'org.apache.logging.log4j:log4j-api:2.12.1',		'com.google.code.gson:gson:2.8.6',		'org.openjfx:javafx-base:11.0.2',
		'org.openjfx:javafx-controls:11.0.2',
		'org.openjfx:javafx-fxml:11.0.2',
		'org.json:json:20190722'] 
testSrcDirs = ['src/test/java'] # source code for tests
testResourcesDirs = ['src/test/resources'] # testing resources
testDependencyDirs = ['test-libs'] # testing-only libs
testRunDir = 'test-run' # working directory for testing
testReportDir = 'test-reports' # test reports go here
testCompileDir = 'test-compile' # compiled test code
testMavenDependencies = ['org.junit.platform:junit-platform-console-standalone:1.4.2'] # junit and other test maven deps
manifestFile = None # if None, then a manifest file will be auto-generated, 
# otherwise this is the filepath of the anifest file
mainClass = 'myorg.myapp.App' # classpath for the main(...) method



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

