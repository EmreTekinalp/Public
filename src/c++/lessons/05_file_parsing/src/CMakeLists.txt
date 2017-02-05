set(SOURCE_FILES "main.cpp")

find_package(Boost)
if(Boost_FOUND)
	include_directories(${Boost_INCLUDE_DIRS})
endif()

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

if(Boost_FOUND)
	target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})
endif()
