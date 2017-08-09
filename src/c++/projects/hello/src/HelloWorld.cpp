#include <iostream>

#include <maya/MSimple.h>
#include <maya/MIOStream.h>
#include <maya/MGlobal.h>


DeclareSimpleCommand(HelloWorld, "Autodesk", "2017");

MStatus HelloWorld::doIt(const MArgList&)
{
	std::cout << "Hello World\n" << std::endl;
    MGlobal::displayInfo("Hello Maya");
	return MS::kSuccess;
}