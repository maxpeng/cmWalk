# cmWalk

## Table of Conents:
<!-- TOC -->

- [cmWalk](#cmwalk)
    - [Table of Conents:](#table-of-conents)
    - [Introduction](#introduction)
    - [Usage](#usage)
    - [Configuration File](#configuration-file)
        - [Supported properties of `cmwalk.json`](#supported-properties-of-cmwalkjson)
    - [Example of generated CMakeLists.txt](#example-of-generated-cmakeliststxt)
        - [References:](#references)

<!-- /TOC -->

## Introduction

`cmWalk` is a python script to walk the directory tree of a C/C++ project of embedded system to generate CMakeLists.txt files for building the executable.

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

- **cmakeToolchainFile**

  Specifying the toolchain file of the used compiler for current project. You can also set the used toolchain file
  by invoking `cmake` with the command line parameter `-DCMAKE_TOOLCHAIN_FILE=path/to/file`.

  Refer cmake documentation [cmake-toolchains(7)](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html) for the details.

- **cmakeCompilerOptionsFile**

  Specifying a file that contains the additional compiler settings which be inclued in the top-level CMakeLists.txt file.

  For example:

  ```cmake
  set(EXTRA_COMMON_FLAGS "-mcpu=cortex-m4 -mthumb-interwork -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DUSE_HAL_DRIVER -DSTM32F429xx")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${EXTRA_COMMON_FLAGS}")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${EXTRA_COMMON_FLAGS}")

  set(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} -mcpu=cortex-m4 -mthumb-interwork -mfloat-abi=hard -mfpu=fpv4-sp-d16")

  set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/app/STM32F429ZITx_FLASH.ld)
  set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Map=${CMAKE_BINARY_DIR}/${PROJECT_NAME}.map -T${LINKER_SCRIPT}")
  ```

- **sourceDirectories**

   A list of source directories.

   If `sourceDirs` is specified in `cmwalk.json`, then only the specified directories will be included for parsing.

   To specify the source subdirectories for `cmake` build system:

   ```json
   {
       "sourceDirs": ["apps", "libs"]
   }
   ```

- **ignoredDirectories** - A list of ignored directories.
   `sourceDirs` property has higher priority than `ignoredDirs` property. If both of `sourceDirs`
   and `ignoredDirs` properties are specified in `cmwalk.json`, `ignoredDirs` property has no effect.

   To exclude subdirectories for `cmake` build system:

   ```json
   {
       "ignoredDirs": ["docs"]
   }
   ```

- **ignoredFiles** - A list of ignored files.

   To exclude a file for `cmake` build system:

   ```json
   {
       "ignoredFiles": ["cfg.h.template"]
   }
   ```


## Example of generated CMakeLists.txt

This is an example of generated top-level `CMakeLists.txt`:
```cmake
cmake_minimum_required(VERSION 3.9)

# set the toolchain file.
# toolchain file should be set before "project" command.
# the toolchain file can also be set via "cmake -DCMAKE_TOOLCHAIN_FILE=path/to/file".
set(CMAKE_TOOLCHAIN_FILE gcc_arm_none_eabi_toolchain.cmake)

project(nucleo_f429zi_freertos_lwip)
enable_language(C CXX ASM)

# load and run the CMake code from the given file to specify project specific options.
include(gcc_arm_none_eabi_opts.cmake)


# export the executable target through a variable to CMakeLists.txt files in subdirectories.
# update the dependent sources.
add_executable(nucleo_f429zi_freertos_lwip.elf
    ""
)

# export the name of executable target via a variable to CMakeLists.txt files in subdirectories.
set(CURRENT_EXE_NAME ${PROJECT_NAME}.elf)
# load and run the CMake code from subdirectories for current target.
include(app/CMakeLists.txt)
include(libs/CMakeLists.txt)


# generate the hex file from the built target.
set(HEX_FILE ${PROJECT_NAME}.hex)
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
    COMMENT "Building ${HEX_FILE}...")

# generate the bin file from the built target.
set(BIN_FILE ${PROJECT_NAME}.bin)
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
    COMMENT "Building ${BIN_FILE}...")
```

### References:

1. [Enhanced source file handling with target_sources() – Crascit](https://crascit.com/2016/01/31/enhanced-source-file-handling-with-target_sources/)
2. [CLion for embedded development | CLion Blog](https://blog.jetbrains.com/clion/2016/06/clion-for-embedded-development/)

