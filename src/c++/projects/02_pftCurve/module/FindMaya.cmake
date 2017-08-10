if (NOT DEFINED MAYA_VERSION)
	set(MAYA_VERSION 2016 CACHE STRING "Maya Version")
endif()

set(MAYA_INCLUDE_SUFFIX "include")
set(MAYA_LIBRARY_SUFFIX "lib")
set(MAYA_COMPILE_DEFINITIONS "REQUIRE_IOSTREAM;_BOOL")
set(MAYA_LIBS OpenMaya OpenMayaAnim OpenMayaFX OpenMayaRender OpenMayaUI Foundation)

if (WIN32)
	set(MAYA_INSTALL_PATH "C:/Program Files/autodesk")
	set(OPENMAYA "OpenMaya.lib")
	set(MAYA_COMPILE_DEFINITIONS "${MAYA_COMPILE_DEFINITIONS};NT_PLUGIN")
	set(MAYA_PLUGIN_SUFFIX ".mll")
elseif(APPLE)
	set(MAYA_INSTALL_PATH "Application/autodesk")
	set(MAYA_PLUGIN_SUFFIX ".bundle")
else()
	set(MAYA_INSTALL_PATH "usr/autodesk")
	set(MAYA_PLUGIN_SUFFIX ".so")
endif()

set(MAYA_BASE_INSTALL_PATH ${MAYA_INSTALL_PATH}/maya${MAYA_VERSION} CACHE STRING "Maya Root")
set(MAYA_LOCATION ${MAYA_BASE_INSTALL_PATH})


find_path(MAYA_INCLUDE maya/MFn.h
		  PATHS ${MAYA_LOCATION}
		        $ENV{MAYA_LOCATION}
		  PATH_SUFFIXES "${MAYA_INCLUDE_SUFFIX}/"
		  DOC "Maya include path")
# end maya include path

find_path(MAYA_LIBRARY ${OPENMAYA}
		  PATHS ${MAYA_LOCATION}
		        $ENV{MAYA_LOCATION}
		  PATH_SUFFIXES "${MAYA_LIBRARY_SUFFIX}/"
		  DOC "Maya library path")		  
# end maya library path


include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Maya DEFAULT_MSG MAYA_LIBRARY MAYA_INCLUDE MAYA_LIBS)

function(MAYA_PLUGIN _target)
	if (WIN32)
		set_target_properties(${_target} PROPERTIES
							  LINK_FLAGS "/export:initializePlugin /export:uninitializePlugin")
	endif()
	set_target_properties(${_target} PROPERTIES
						  COMPILE_DEFINITIONS ${MAYA_COMPILE_DEFINITIONS}
						  SUFFIX ${MAYA_PLUGIN_SUFFIX})
endfunction()						  