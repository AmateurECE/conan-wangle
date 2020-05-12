cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++17")

add_executable(wangletest wangletest.cpp)
target_link_libraries(wangletest ${CONAN_LIBS})
target_include_directories(wangletest PRIVATE "${CONAN_INCLUDE_DIRS}")

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
