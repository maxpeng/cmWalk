# cmWalk

A python script to walk subdirectories of a C/C++ project of embedded system to generate CMakeLists.txt files for building the executable.

## Usage

usage: cmwalk.py [-h] input_dir

A python script to generate CMakeLists.txt of a C/C++ project - 0.0.1.

positional arguments:
  input_dir   The base directory of C/C++ project.

optional arguments:
  -h, --help  show this help message and exit


## Configuration File

You can create a json file for each directory of project directory tree to configure how `cmwalk` to generate
'CMakeLists.txt'. The configuration filename of `cmwalk` is `cmwalk.json`. 

### Supported properties of `cmwalk.json`

- **"sourceDirs"**

   A list of source directories.

   If `sourceDirs` is specified in `cmwalk.json`, then only the specified directories will be included for parsing.

   To specify the source subdirectories for `cmake` build system:

   ```json
   {
       "sourceDirs": ["apps", "libs"]
   }

   ```

- **"ignoredDirs"** - A list of ignored directories.
   `sourceDirs` property has higher priority than `ignoredDirs` property. If both of `sourceDirs`
   and `ignoredDirs` properties are specified in `cmwalk.json`, `ignoredDirs` property has no effect.

   To exclude subdirectories for `cmake` build system:

   ```json
   {
       "ignoredDirs": ["docs"]
   }

   ```

- **"ignoredFiles"** - A list of ignored files.

   To exclude a file for `cmake` build system:

   ```json
   {
       "ignoredFiles": ["cfg.h.template"]
   }

   ```

### References:

1. [Enhanced source file handling with target_sources() – Crascit](https://crascit.com/2016/01/31/enhanced-source-file-handling-with-target_sources/)
2. [CLion for embedded development | CLion Blog](https://blog.jetbrains.com/clion/2016/06/clion-for-embedded-development/)

