cmake_minimum_required(VERSION 3.27)
project(key_10000cal)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(key_10000cal
        main.cpp
#        GF28.h
        validate.cpp
#        validate.h
        GF28.cpp
        gen_dc.cpp
        BASIC_OP.cpp
        CONST.cpp
        key_sch.cpp)
