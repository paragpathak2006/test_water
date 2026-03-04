cmake_minimum_required(VERSION 3.16)
project(cgal_module)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Release)

find_package(CGAL REQUIRED)
find_package(pybind11 REQUIRED)

pybind11_add_module(cgal_module src/CPP/module.cpp)
target_link_libraries(cgal_module PRIVATE CGAL::CGAL)

