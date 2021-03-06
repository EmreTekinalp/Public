# Install script for directory: /Users/emretekinalp/Documents/GitHub/Maya/src/c++/projects/01_springSolver/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/Users/emretekinalp/Documents/GitHub/Maya/src/c++/projects/01_springSolver/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/plug-ins" TYPE SHARED_LIBRARY FILES "/Users/emretekinalp/Documents/GitHub/Maya/src/c++/projects/01_springSolver/build/src/SpringSolver.bundle")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/plug-ins/SpringSolver.bundle" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/plug-ins/SpringSolver.bundle")
    execute_process(COMMAND "/usr/bin/install_name_tool"
      -id "SpringSolver.bundle"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/plug-ins/SpringSolver.bundle")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Applications/Autodesk/maya2017/Maya.app/Contents/MacOS"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/plug-ins/SpringSolver.bundle")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/plug-ins/SpringSolver.bundle")
    endif()
  endif()
endif()

