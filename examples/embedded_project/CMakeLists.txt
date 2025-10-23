cmake_minimum_required(VERSION 3.15)
project(EmbeddedProject)

# Find packages
find_package(Boost 1.75 REQUIRED COMPONENTS system filesystem)
find_package(OpenSSL 3.0 REQUIRED)

# FetchContent for external projects
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.14.0
)

add_executable(embedded_app main.cpp)
target_link_libraries(embedded_app Boost::system OpenSSL::SSL)

