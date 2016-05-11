#include "quaternions.h"

float PI = 3.14159265359;


MTypeId Quaternions::id(0x5157698);
MObject Quaternions::aInMatrix;

MObject Quaternions::aOutTranslate;
MObject Quaternions::aOutRotateX;
MObject Quaternions::aOutRotateY;
MObject Quaternions::aOutRotateZ;
MObject Quaternions::aOutRotate;


Quaternions::Quaternions(){}
Quaternions::~Quaternions(){}

void* Quaternions::creator()
{
    return new Quaternions();
}

MStatus Quaternions::initialize()
{
    MFnEnumAttribute eAttr;
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnMatrixAttribute mAttr;

    //inMatrix
    aInMatrix = mAttr.create("inMatrix", "ima");
    CHECK_MSTATUS(addAttribute(aInMatrix));
    mAttr.setHidden(true);;

    //outTranslate
    aOutTranslate = nAttr.createPoint("outTranslate", "ot");
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutTranslate));

    // Set up rotate outputs
    aOutRotateX = uAttr.create("outRotateX", "orx", MFnUnitAttribute::kAngle, 0.0);
    nAttr.setWritable(false);
    uAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutRotateX));

    aOutRotateY = uAttr.create("outRotateY", "ory", MFnUnitAttribute::kAngle, 0.0);
    nAttr.setWritable(false);
    uAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutRotateY));

    aOutRotateZ = uAttr.create("outRotateZ", "orz", MFnUnitAttribute::kAngle, 0.0);
    nAttr.setWritable(false);
    uAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutRotateZ));

    aOutRotate = nAttr.create("outRotate", "or", aOutRotateX, aOutRotateY, aOutRotateZ);
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutRotate));

    //attribute affects
    attributeAffects(aInMatrix, aOutTranslate);
    attributeAffects(aInMatrix, aOutRotate);

    return MS::kSuccess;
}

MStatus Quaternions::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;
	//Check the output for dirt
	if (plug == aOutTranslate || plug == aOutRotate)
	{
		cout << "I'm in babe!" << endl;
	}
	return MS::kSuccess;
}

void Quaternions::getQuaternion(MVector& n, float a, MQuaternion& quaternion)
{
	//Convert degrees into radians to deal with Quaternions
	a = a / 360 * PI * 2;

	quaternion.w = cos(a/2);
	quaternion.x = n.x*sin(a/2);
	quaternion.y = n.y*sin(a/2);
	quaternion.z = n.z*sin(a/2);
}

void Quaternions::invertQuaternion(MQuaternion& quaternion)
{
	//Convert degrees into radians to deal with Quaternions
	quaternion.w *= 1.0;
	quaternion.x *= -1.0;
	quaternion.y *= -1.0;
	quaternion.z *= -1.0;
}
