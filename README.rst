cmWalk
======

1. Introduction
---------------

``cmWalk`` is a python script to walk the directory tree of a C/C++
project of embedded system to generate CMakeLists.txt files for building
the executable.

2. Usage
--------

usage: cmwalk.py [-h] input_dir

A python script to generate CMakeLists.txt of a C/C++ project - 0.0.1.

positional arguments: input_dir The base directory of C/C++ project.

optional arguments: -h, –help show this help message and exit

3. Configuration File
---------------------

You can create a json file for each directory of project directory tree
to configure how ``cmwalk`` to generate ‘CMakeLists.txt’. The
configuration filename of ``cmwalk`` is ``cmwalk.json``.

3.1 Supported properties of ``cmwalk.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **cmakeToolchainFile**

   Specifying the toolchain file of the used compiler for current
   project. You can also set the used toolchain file by invoking
   ``cmake`` with the command line parameter
   ``-DCMAKE_TOOLCHAIN_FILE=path/to/file``.

   Refer cmake documentation
   `cmake-toolchains(7) <https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html>`__
   for the details.

   Example:

   .. code:: json

        {
            "cmakeToolchainFile": "gcc_arm_none_eabi_toolchain.cmake"
        }

   An example of toolchain file:

   .. code:: cmake

       # refer https://cmake.org/Wiki/CMake_Cross_Compiling
       #include(CMakeForceCompiler)    # cmake_force_c_compiler and cmake_force_cxx_compiler are deprecated.

       set(CMAKE_SYSTEM_NAME Generic)
       set(CMAKE_SYSTEM_VERSION 1)
       set(CMAKE_SYSTEM_PROCESSOR "armv7-m")


       # refer https://cmake.org/pipermail/cmake-developers/2016-February/027871.html
       # about how to solve this problem: "arm-none-eabi-gcc.exe" is not able to compile a simple test program.
       set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

       # find the cross compiler and associated tools that we need:
       find_program(ARM_NONE_EABI_GCC arm-none-eabi-gcc)
       find_program(ARM_NONE_EABI_GPP arm-none-eabi-g++)
       find_program(ARM_NONE_EABI_OBJCOPY arm-none-eabi-objcopy)


       macro(gcc_program_notfound progname)
           message("**************************************************************************\n")
           message(" ERROR: the arm gcc program ${progname} could not be found\n")
           if(CMAKE_HOST_SYSTEM_NAME STREQUAL "Windows" OR CMAKE_HOST_SYSTEM_NAME STREQUAL "Linux")
               message(" you can install the ARM GCC embedded compiler tools from:")
               message(" https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads")
           elseif(CMAKE_HOST_SYSTEM_NAME STREQUAL "Darwin")
               message(" it is included in the arm-none-eabi-gcc package that you can install")
               message(" with homebrew:\n")
               message("   brew tap ARMmbed/homebrew-formulae")
               message("   brew install arm-none-eabi-gcc")
           endif()
           message("\n**************************************************************************")
           message(FATAL_ERROR "missing program prevents build")
           return()
       endmacro(gcc_program_notfound)

       if(NOT ARM_NONE_EABI_GCC)
           gcc_program_notfound("arm-none-eabi-gcc")
       endif()

       if(NOT ARM_NONE_EABI_GPP)
           gcc_program_notfound("arm-none-eabi-g++")
       endif()

       if(NOT ARM_NONE_EABI_OBJCOPY)
           gcc_program_notfound("arm-none-eabi-objcopy")
       endif()


       set(CMAKE_C_COMPILER arm-none-eabi-gcc)
       set(CMAKE_CXX_COMPILER arm-none-eabi-g++)

       set(C_FAMILY_FLAGS_INIT "-ffunction-sections -fdata-sections -g -fno-common -fmessage-length=0 --specs=nosys.specs --specs=nano.specs")
       set(CMAKE_C_FLAGS_INIT "${C_FAMILY_FLAGS_INIT} -std=c99")
       set(CMAKE_CXX_FLAGS_INIT "${C_FAMILY_FLAGS_INI} -std=c++11")
       set(CMAKE_ASM_FLAGS_INIT "-fno-exceptions -fno-unwind-tables -x assembler-with-cpp")
       set(CMAKE_EXE_LINKER_FLAGS_INIT "-Wl,-gc-sections,-print-memory-usage")

-  **cmakeCompilerOptionsFile**

   Specifying a file that contains the additional compiler settings
   which be inclued in the top-level CMakeLists.txt file.

   Example:

   .. code:: json

       {
           "cmakeCompilerOptionsFile": "gcc_arm_none_eabi_opts.cmake"
       }

   An example of compiler option files for `GNU Arm Embedded
   Toolchain <https://developer.arm.com/open-source/gnu-toolchain/gnu-rm>`__:

   .. code:: cmake

       set(EXTRA_COMMON_FLAGS "-mcpu=cortex-m4 -mthumb-interwork -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DUSE_HAL_DRIVER -DSTM32F429xx")
       set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${EXTRA_COMMON_FLAGS}")
       set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${EXTRA_COMMON_FLAGS}")

       set(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} -mcpu=cortex-m4 -mthumb-interwork -mfloat-abi=hard -mfpu=fpv4-sp-d16")

       set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/app/STM32F429ZITx_FLASH.ld)
       set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Map=${CMAKE_BINARY_DIR}/${PROJECT_NAME}.map -T${LINKER_SCRIPT}")

-  **sourceDirectories**

   A list of source directories.

   If ``sourceDirectories`` is specified in ``cmwalk.json``, then only
   the specified directories will be included for parsing, other
   directories will be excluded. If ``sourceDirectories`` does not exist
   but ``ignoredDirectories`` exist, then all the directories except
   those specified by ``ignoredDirectories`` will be excluded.

   An example of specifying the source subdirectories for searching the
   source files:

   .. code:: json

       {
            "sourceDirectories": ["app", "libs"]
       }

-  **ignoredDirectories** - A list of ignored directories.

   ``sourceDirs`` property has higher priority than ``ignoredDirs``
   property. If both of ``sourceDirs`` and ``ignoredDirs`` properties
   are specified in ``cmwalk.json``, ``ignoredDirs`` property has no
   effect.

   An example of excluding subdirectories for searching the source
   files:

   .. code:: json

       {
            "ignoredDirs": ["docs"]
       }

-  **ignoredFiles** - A list of ignored files.

   An example of excluding a file from ``cmake`` build system:

   .. code:: json

       {
            "ignoredFiles": ["cfg.h.template"]
       }


4. Example of generated CMakeLists.txt
--------------------------------------

This is an example of generated top-level ``CMakeLists.txt``:

.. code:: cmake

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

5. References
-------------

1. `Enhanced source file handling with target_sources() –
   Crascit <https://crascit.com/2016/01/31/enhanced-source-file-handling-with-target_sources/>`__
2. `CLion for embedded development \| CLion
   Blog <https://blog.jetbrains.com/clion/2016/06/clion-for-embedded-development/>`__
