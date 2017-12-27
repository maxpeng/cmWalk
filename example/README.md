# cmwalk Example

## Description

`stm32f4_discovery_blinky` directory contains an example about how to use `cmwalk` to generate `CMakeLists.txt` files to build the executable using `CMake`.

Above example was generate by [STM32CubeMX](http://www.st.com/en/development-tools/stm32cubemx.html) for [STM32F4-DISCOVERY board](http://www.st.com/en/evaluation-tools/stm32f4discovery.html), it does a simple task - blinks a red LED every 1 second.


## Requirements

1. [GNU Arm Embedded Toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm):
2. [CMake](https://cmake.org/)


## Preparation

1. Install [GNU Arm Embedded Toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm), and add `<gnu_arm_embedded_toolchain_install_dir>\bin` to PATH environment variable.
2. Install [CMake](https://cmake.org/), and add `<cmake_install_dir>\bin` to PATH environment variable.
3. Install `cmwalk` by using this command - `pip install cmwalk`.


## Building the example

1. Open a DOS command prompt, change the working directory to `example\stm32f4_discovery_blinky`.
2. Type `cmake .` to generate `CMakeLists.txt` files.
3. Create a `build` directory under `example\stm32f4_discovery_blinky` directory. 
4. Type `cmake .. -DCMAKE_BUILD_TYPE=Debug -G "CodeBlocks - MinGW Makefiles"` to generate the makefiles. 
5. Type `cmake --build . --target all -- VERBOSE=1` to build the example. If cmake could build the targets sucessfully, you should see `stm32f4_discovery_blinky.elf`, `stm32f4_discovery_blinky.bin`, `stm32f4_discovery_blinky.hex` are generated.
6. Program the generated executable to STM32F4-Discovery board, you should the red LED blinks every 1 second.