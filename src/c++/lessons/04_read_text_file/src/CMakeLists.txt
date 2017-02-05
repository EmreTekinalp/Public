set(SOURCE_FILES "main.cpp")

find_package(Boost 1.55.0 REQUIRED)
if(Boost_FOUND)
	set(Boost_INCLUDE_DIR ${Boost_INCLUDE_DIRS}/boost)
	set(Boost_LIBRARY_DIR ${Boost_INCLUDE_DIRS}/lib)
	include_directories(${Boost_INCLUDE_DIRS})
endif()

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

message(STATUS ${Boost_filesystem_LIBRARY})

if(Boost_FOUND)
	target_link_libraries(${PROJECT_NAME}
						  ${Boost_LIBRARIES})
endif()
