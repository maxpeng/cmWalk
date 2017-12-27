# add source and header files when compiling the given target.
# although it is not necessary to add header files, we also do that for easing the management of IDE.
target_sources(${CURRENT_EXE_NAME}
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/arm_common_tables.h
        ${CMAKE_CURRENT_LIST_DIR}/arm_const_structs.h
        ${CMAKE_CURRENT_LIST_DIR}/arm_math.h
        ${CMAKE_CURRENT_LIST_DIR}/cmsis_armcc.h
        ${CMAKE_CURRENT_LIST_DIR}/cmsis_armcc_V6.h
        ${CMAKE_CURRENT_LIST_DIR}/cmsis_gcc.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cm0.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cm0plus.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cm3.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cm4.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cm7.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cmFunc.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cmInstr.h
        ${CMAKE_CURRENT_LIST_DIR}/core_cmSimd.h
        ${CMAKE_CURRENT_LIST_DIR}/core_sc000.h
        ${CMAKE_CURRENT_LIST_DIR}/core_sc300.h
)

# add current directory to the compiler included directories when compiling the given target.
target_include_directories(${CURRENT_EXE_NAME} PUBLIC "${CMAKE_CURRENT_LIST_DIR}")

