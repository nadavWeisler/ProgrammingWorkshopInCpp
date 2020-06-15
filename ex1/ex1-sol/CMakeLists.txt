cmake_minimum_required(VERSION 3.16)
project(ex1_sol)

set(CMAKE_CXX_STANDARD 14)

add_executable(ex1_sol Matrix.cpp Dense.cpp MlpNetwork.cpp Activation.cpp)