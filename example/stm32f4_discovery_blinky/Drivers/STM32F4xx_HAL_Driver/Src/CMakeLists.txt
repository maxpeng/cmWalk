# add source and header files when compiling the given target.
# although it is not necessary to add header files, we also do that for easing the management of IDE.
target_sources(${CURRENT_EXE_NAME}
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_cortex.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_dma.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_dma_ex.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_flash.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_flash_ex.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_flash_ramfunc.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_gpio.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_pwr.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_pwr_ex.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_rcc.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_rcc_ex.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_tim.c
        ${CMAKE_CURRENT_LIST_DIR}/stm32f4xx_hal_tim_ex.c
)

# add current directory to the compiler included directories when compiling the given target.
target_include_directories(${CURRENT_EXE_NAME} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

