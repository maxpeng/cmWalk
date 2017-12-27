# add source and header files when compiling the given target.
# although it is not necessary to add header files, we also do that for easing the management of IDE.
target_sources(${CURRENT_EXE_NAME}
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/croutine.c
        ${CMAKE_CURRENT_LIST_DIR}/event_groups.c
        ${CMAKE_CURRENT_LIST_DIR}/list.c
        ${CMAKE_CURRENT_LIST_DIR}/queue.c
        ${CMAKE_CURRENT_LIST_DIR}/tasks.c
        ${CMAKE_CURRENT_LIST_DIR}/timers.c
)

# add current directory to the compiler included directories when compiling the given target.
target_include_directories(${CURRENT_EXE_NAME} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

# load and run the CMake code from subdirectories for current target.
include(${CMAKE_CURRENT_LIST_DIR}/CMSIS_RTOS/CMakeLists.txt)
include(${CMAKE_CURRENT_LIST_DIR}/include/CMakeLists.txt)
include(${CMAKE_CURRENT_LIST_DIR}/portable/CMakeLists.txt)
