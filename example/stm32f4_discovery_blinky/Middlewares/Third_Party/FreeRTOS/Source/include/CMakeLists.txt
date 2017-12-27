# add source and header files when compiling the given target.
# although it is not necessary to add header files, we also do that for easing the management of IDE.
target_sources(${CURRENT_EXE_NAME}
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/croutine.h
        ${CMAKE_CURRENT_LIST_DIR}/deprecated_definitions.h
        ${CMAKE_CURRENT_LIST_DIR}/event_groups.h
        ${CMAKE_CURRENT_LIST_DIR}/FreeRTOS.h
        ${CMAKE_CURRENT_LIST_DIR}/FreeRTOSConfig_template.h
        ${CMAKE_CURRENT_LIST_DIR}/list.h
        ${CMAKE_CURRENT_LIST_DIR}/mpu_prototypes.h
        ${CMAKE_CURRENT_LIST_DIR}/mpu_wrappers.h
        ${CMAKE_CURRENT_LIST_DIR}/portable.h
        ${CMAKE_CURRENT_LIST_DIR}/projdefs.h
        ${CMAKE_CURRENT_LIST_DIR}/queue.h
        ${CMAKE_CURRENT_LIST_DIR}/semphr.h
        ${CMAKE_CURRENT_LIST_DIR}/StackMacros.h
        ${CMAKE_CURRENT_LIST_DIR}/task.h
        ${CMAKE_CURRENT_LIST_DIR}/timers.h
)

# add current directory to the compiler included directories when compiling the given target.
target_include_directories(${CURRENT_EXE_NAME} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

