cmake_minimum_required(VERSION 3.9)

# set the toolchain file.
# toolchain file should be set before "project" command.
# the toolchain file can also be set via "cmake -DCMAKE_TOOLCHAIN_FILE=path/to/file".
set(CMAKE_TOOLCHAIN_FILE gcc_arm_none_eabi_toolchain.cmake)

project(stm32f4_discovery_blinky)
enable_language(C CXX ASM)

# load and run the CMake code from the given file to specify project specific options.
include(gcc_arm_none_eabi_opts.cmake)


# export the executable target through a variable to CMakeLists.txt files in subdirectories.
# update the dependent sources.
add_executable(stm32f4_discovery_blinky.elf
    ""
)

# export the name of executable target via a variable to CMakeLists.txt files in subdirectories.
set(CURRENT_EXE_NAME ${PROJECT_NAME}.elf)
# load and run the CMake code from subdirectories for current target.
include(Drivers/CMakeLists.txt)
include(Inc/CMakeLists.txt)
include(Middlewares/CMakeLists.txt)
include(Src/CMakeLists.txt)
include(startup/CMakeLists.txt)


# if compiler is GNU gcc/g++, then generate *.bin & *.hex files.
if ("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU")
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
endif()