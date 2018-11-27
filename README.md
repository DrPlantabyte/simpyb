# simbyp
Simple Python Buildscripts. Python-based build scripts aimed at JDK 11

# Requirements
* Python v3+ (python3)
* Maven (mvn)

## Quick-start
Just copy all of the *.py* files into the root of a folder, edit *config.py* to suit your preferences, and then run the *new-module.py*. This will generate a sample java module, including unit tests.

## The scripts
To install this build tool, simply copy these python scripts into your module folder. These scripts are designed to compile a single module. 

For multiple-module projects, put each module in its own folder. Edit each *config.py* to add the output jar folders of other modules to the *dependencyDirs* list and then edit the **pre_build()** function in each to call the *jar.py* script of dependency modules.

### config.py
This file describes your module and includes hooks for custom or platform-specific behavior. 

*Modify this file!*

### clean.py
Deletes all generated files. 

*You do not need to modify this file.*

### build.py
Compiles your module, automatically retrieving Maven dependencies and copying the relevant library .jar files (with secondary dependencies) into your dependencies folder defined in *config.py*. If no files changes are detected since it was last run, compilation will be skipped to save time. 

*You do not need to modify this file.*

### jar.py
Packages your module into a .jar file. If you have a main class defined in *config.py*, then you should be able to run the .jar file by simmply issuing **java -jar path/to/file.jar** in the terminal. 

This script will automatically run *build.py* if necessary to create an up-to-date .jar file.

*You do not need to modify this file.*

### junit.py
Compiles and tests your module by patching-in the test source-code and Jupiter JUnit v5 testing framework.

*If not using Jupiter JUnit 5, then you may need to modify this file.*

### new-module.py
This is a quick-start script to make a template project with all of the folders from the project structure defined in *config.py*.

### pj_util.py
This is a utility script file that defines functions used by the other scripts. Don't modify this file unless you really know what you are doing.
