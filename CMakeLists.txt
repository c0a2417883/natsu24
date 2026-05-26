cmake_minimum_required(VERSION 3.8)
project(natsu24)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-O3 -Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake_auto REQUIRED)

ament_auto_find_build_dependencies()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_auto_add_executable(natsu24 src/natsu24.cpp)

install(
  DIRECTORY config include launch models urdf world
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS
  natsu24
  DESTINATION lib/${PROJECT_NAME}
)

ament_auto_package()
