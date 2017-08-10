set(SOURCE_FILES
	"pftCurve.cpp"
	"pluginMain.cpp")
set(HEADER_FILES
	"pftCurve.h")

	
find_package(Maya REQUIRED)

include_directories(${MAYA_INCLUDE})	
link_directories(${MAYA_LIBRARY})

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES} ${HEADER_FILES})
target_link_libraries(${PROJECT_NAME} ${MAYA_LIBS})

MAYA_PLUGIN(${PROJECT_NAME})