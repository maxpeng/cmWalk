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
