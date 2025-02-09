cmake_minimum_required(VERSION 3.10)
project(sofm)

set (CMAKE_CXX_STANDARD 17)

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

set(CMAKE_CXX_FLAGS "-O2")

include_directories(
    src
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${EIGEN3_INCLUDE_DIR}
)


add_library(online_fuzzy_art
    src/sofm/art/OnlineFuzzyART.cpp
)

target_link_libraries(online_fuzzy_art PRIVATE
    pybind11::module
    pybind11::lto
    pybind11::windows_extras
    Eigen3::Eigen
)

add_subdirectory(pybind11)
pybind11_add_module(${PROJECT_NAME} module.cpp)

target_link_libraries(${PROJECT_NAME} PRIVATE
    online_fuzzy_art
)