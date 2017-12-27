# add source and header files when compiling the given target.
# although it is not necessary to add header files, we also do that for easing the management of IDE.
target_sources(${CURRENT_EXE_NAME}
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_cortex.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_def.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_dma.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_dma_ex.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_flash.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_flash_ex.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_flash_ramfunc.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_gpio.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_gpio_ex.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_pwr.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_pwr_ex.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_rcc.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_rcc_ex.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_tim.h
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_tim_ex.h
)

# add current directory to the compiler included directories when compiling the given target.
target_include_directories(${CURRENT_EXE_NAME} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

# load and run the CMake code from subdirectories for current target.
include(${CMAKE_CURRENT_LIST_DIR}/Legacy/CMakeLists.txt)
