# simbyp
A simple JDK11 compatible Java module build tool (written entirely in Python).

## Requirements
* JDK v11+
* Python v3+ (python3)
* Maven (mvn)
* JAVA_HOME set to location of JDK

## Quick-start
Start your modular java or JavaFX project in 5 easy steps:
1. Open the command-line terminal and change into the project directory
```bash
mkdir MyJavaProject
cd MyJavaProject
```

2. Check that the operating system environment variable `JAVA_HOME` is properly configured (depending how you installed java, it may need to be manually assigned)
```bash
echo "$JAVA_HOME"
>> /etc/alternatives/java_sdk_openjdk/
```

3. Copy the **simpyb** python files into your project directory
```bash
git clone https://github.com/cyanobacterium/simpyb.git
cp simpyb/*.py .
rm -rf simpyb
```

4. Edit *config.py* to change the module name(s) and add Maven dependencies.

5. Run either *new-standard-project.py* or *new-jfx-project.py*, then test your new project with *run.py*
```bash
./new-standard-project.py
./run.py
```
(on Windows, you need to put *python.exe* in front of each command)

**Congratulations!** You now have a complete java project and build environment. You can run your program by running the *run.py* script.

## How it works
Just copy all of the *.py* files into the root of a folder, edit *config.py* to suit your preferences, and then run the *new-...-project.py*. This will generate a sample java project with modules.

### The scripts
To install this build tool, simply copy these python scripts into your module folder. These scripts are designed to compile a single module. 

In the default configuration, you will have a *modules* folder which contains each module named in *config.py*. Each of the module folders has its own source and resource folder for code and other files, respectively. All modules share the same folders for dependencies, though the actual dependencies are specified in each modules *module-info.java* file.

#### config.py
This file describes your module and includes hooks for custom or platform-specific behavior. Edit this file and change **my.project** to your project's package name. You my edit other variables in this file too, to tailor the project to your needs.

Note that Maven sependencies are specified here in the standard *Gradle* format of *groupId:artifactId:version*

*Modify this file!*

#### clean.py
Deletes all generated files. 

*You do not need to modify this file.*

#### build.py
Compiles your module, automatically retrieving Maven dependencies and copying the relevant library .jar files (with secondary dependencies) into your dependencies folder defined in *config.py*. 

*build.py* will use **jlink** to compile your java program to a platform-specific "image" folder containing binary executables. This "image" can then be used to by OS-specific tools (e.g. *Wix* or *dpkg*) to create an installer package (not covered by simpyb).

*You do not need to modify this file, unless you are cross-compiling for other plaftorms.*

#### run.py
Runs the module in the run directory specified in *config.py*.

This script will automatically run *build.py* if necessary to create an up-to-date executable, and then runs it.

*You do not need to modify this file.*

#### new-standard-project.py
Uses the information in *config.py* to create a new command-line project, that is ready to run with *run.py*

#### new-jfx-project.py
Uses the information in *config.py* to create a new JavaFX project, complete with platform-specific jmod dependencies (downloaded from Gluon's OpenJFX page), FXML view and controller, and language localization file. After this script is complete, you are ready to run it with *run.py* to see the JavaFX sample application.

#### pyb_util.py
This is a utility script file that defines functions used by the other scripts. **Don't modify this file unless you really know what you are doing.**

#### pyb_java.py
This is a utility script file that defines functions used by the other scripts. **Don't modify this file unless you really know what you are doing.**

#### pyb_maven.py
This is a utility script file that defines functions used by the other scripts. **Don't modify this file unless you really know what you are doing.**

