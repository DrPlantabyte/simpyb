#!/usr/bin/python3

import os
from os import path
import pj_util as util
import config

this_file = path.realpath(__file__)
this_dir = path.dirname(this_file)
def make_project():
	intellij_filename = str(config.name)+'.iml'
	manifest_file = path.join(config.srcDirs[0], 'META-INF', 'MANIFEST.MF')
	if not path.exists(intellij_filename):
		util.make_parent_dir(intellij_filename)
		util.info('\n%s:' % intellij_filename)
		with open(intellij_filename, 'w') as fout:
			util.write_and_print("""<?xml version="1.0" encoding="UTF-8"?>
<module type="JAVA_MODULE" version="4">
  <component name="NewModuleRootManager" inherit-compiler-output="true">
    <exclude-output />
    <content url="file://$MODULE_DIR$">
""" , fout)
			for e in config.srcDirs:
				util.write_and_print('      <sourceFolder url="file://$MODULE_DIR$/%s" isTestSource="false" />\n' % (e), fout)
			for e in config.resourceDirs:
				util.write_and_print('      <sourceFolder url="file://$MODULE_DIR$/%s" type="java-resource" />\n' % (e), fout)
			## NOTE: unit-testing doesn't carry over well, so it is omitted
##			for e in config.testSrcDirs:
##				util.write_and_print('      <sourceFolder url="file://$MODULE_DIR$/%s" isTestSource="true" />\n' % (e), fout)
##			for e in config.testResourcesDirs:
##				util.write_and_print('      <sourceFolder url="file://$MODULE_DIR$/%s" type="java-test-resource" />\n' % (e), fout)
			util.write_and_print("""
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
""" , fout)
	for lib_jar in util.get_files(config.dependencyDirs, ['.jar']):
		jar_name = path.basename(lib_jar)
		xml_file = '.idea/libraries/'+jar_name.replace('.','_')+'.xml'
		util.make_parent_dir(xml_file)
		with open(xml_file, 'w') as fout:
			util.write_and_print("""
<component name="libraryTable">
  <library name="%s">
    <CLASSES>
      <root url="jar://$PROJECT_DIR$/%s!/" />
    </CLASSES>
    <JAVADOC />
    <SOURCES />
  </library>
</component>
""" % (jar_name.replace('.jar',''), lib_jar), fout)
	# note: artifact requires manifest
	if not path.exists(manifest_file) and (config.manifestFile == None or not path.exists(str(config.manifesFile))):
		util.make_parent_dir(manifest_file)
		util.write_manifest(manifest_file, main_class=config.mainClass, libs_list=util.get_files(config.dependencyDirs, ['.jar']))
	arti_file = '.idea/artifacts/%s_jar.xml' % (config.name)
	util.make_parent_dir(arti_file)
	with open(arti_file, 'w') as fout:
		util.write_and_print("""
<component name="ArtifactManager">
  <artifact type="jar" name="%s:jar">
    <output-path>$PROJECT_DIR$/out/artifacts/%s_jar</output-path>
    <root id="archive" name="%s.jar">
      <element id="module-output" name="%s" />
    </root>
  </artifact>
</component>
""" % (config.name, config.name, config.name, config.name), fout)
	mod_file = '.idea/modules.xml'
	util.make_parent_dir(mod_file)
	with open(mod_file, 'w') as fout:
		util.write_and_print("""<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/%s" filepath="$PROJECT_DIR$/%s" />
    </modules>
  </component>
</project>
""" % (intellij_filename, intellij_filename), fout)
	out_file = '.idea/encodings.xml'
	util.make_parent_dir(out_file)
	with open(out_file, 'w') as fout:
		util.write_and_print("""<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="Encoding" addBOMForNewFiles="with NO BOM">
    <file url="PROJECT" charset="UTF-8" />
  </component>
</project>
""" , fout)
	out_file = '.idea/misc.xml'
	util.make_parent_dir(out_file)
	with open(out_file, 'w') as fout:
		util.write_and_print("""<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="EntryPointsManager">
    <entry_points version="2.0" />
  </component>
  <component name="ProjectRootManager" version="2" languageLevel="JDK_11" default="true" project-jdk-type="JavaSDK">
    <output url="file://$PROJECT_DIR$/%s" />
  </component>
</project>
""" % (config.jarDir) , fout)
#
if __name__ == '__main__':
	pass

