#include "etWireDeformer.h"


MTypeId EtWireDeformer::id(0x516723);
MObject EtWireDeformer::aInCurve;
MObject EtWireDeformer::aInCurveMatrix;
MObject EtWireDeformer::aInitCurveData;
MObject EtWireDeformer::aInitUpVector;
MObject EtWireDeformer::aInitUpVectorX;
MObject EtWireDeformer::aInitUpVectorY;
MObject EtWireDeformer::aInitUpVectorZ;
MObject EtWireDeformer::aTwist;
MObject EtWireDeformer::aOffset;


EtWireDeformer::EtWireDeformer(){}
EtWireDeformer::~EtWireDeformer(){}

void* EtWireDeformer::creator()
{
    return new EtWireDeformer();
}

MStatus EtWireDeformer::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;
    MFnMatrixAttribute mAttr;

    //inEtWireDeformer
    aInCurve = tAttr.create("inCurve", "ic", MFnData::kNurbsCurve);
    nAttr.setKeyable(false);
    nAttr.setReadable(false);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInCurve));

    //inCurveMatrix
    aInCurveMatrix = mAttr.create("inCurveMatrix", "icm");
    mAttr.setKeyable(false);
    mAttr.setReadable(false);
    mAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInCurveMatrix));

    //initEtWireDeformerData
    aInitCurveData = tAttr.create("initCurveData", "icd", MFnData::kPointArray);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setStorable(true);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInitCurveData));

    //initUpVector
    aInitUpVectorX = nAttr.create("initUpVectorX", "iux", MFnNumericData::kFloat, -1.0);
    CHECK_MSTATUS(addAttribute(aInitUpVectorX));
    aInitUpVectorY = nAttr.create("initUpVectorY", "iuy", MFnNumericData::kFloat, 0.0);
    CHECK_MSTATUS(addAttribute(aInitUpVectorY));
    aInitUpVectorZ = nAttr.create("initUpVectorZ", "iuz", MFnNumericData::kFloat, 0.0);
    CHECK_MSTATUS(addAttribute(aInitUpVectorZ));

    //twist
    aTwist = nAttr.create("twist", "tw", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aTwist));

    //offset
    aOffset = nAttr.create("offset", "off", MFnNumericData::kFloat, 1.0);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aOffset));

    //attribute affects
    attributeAffects(aInCurve, outputGeom);
    attributeAffects(aInCurveMatrix, outputGeom);
    attributeAffects(aInitCurveData, outputGeom);
    attributeAffects(aInitUpVectorX, outputGeom);
    attributeAffects(aInitUpVectorY, outputGeom);
    attributeAffects(aInitUpVectorZ, outputGeom);
    attributeAffects(aTwist, outputGeom);
    attributeAffects(aOffset, outputGeom);

    // Make the deformer weights paintable
    MGlobal::executeCommand( "makePaintable -attrType multiFloat -sm deformer etWireDeformer weights;" );

    return MS::kSuccess;
}

MStatus EtWireDeformer::deform(MDataBlock& block, MItGeometry& iter, const MMatrix&  mat, unsigned int mutiIndex)
{
	MStatus status;

	// Get the envelope
	float fenv = block.inputValue(envelope).asFloat();

	// Get the offset
	float foffset = block.inputValue(aOffset).asFloat();

	// Get the inCurve
	MObject oInCurve = block.inputValue(aInCurve).asNurbsCurve();
	if (oInCurve.isNull())
	{
		return MS::kSuccess;
	}
	MFnNurbsCurve fnCurve(oInCurve);

	// Get the inCurveMatrix
	MMatrix mInCurve = block.inputValue(aInCurveMatrix).asMatrix();
	MTransformationMatrix mtInCurve(mInCurve);
	MVector vTrans = mtInCurve.getTranslation(MSpace::kTransform);
	MPoint pTrans = vTrans;

	MPointArray pointArray;
	MDoubleArray daParam;
	MPoint pInPosition, pPosition, pCvPosition;
	MVector vNormal, vTangent;
	double paramU;

	// Check initial curve data attribute for value
	MDataHandle hInitCurveData = block.inputValue(aInitCurveData, &status);
	MObject oInitCurveData = hInitCurveData.data();
	if (!oInitCurveData.hasFn(MFn::kPointArrayData))
	{
		fnCurve.getCVs(pointArray);
		// We need to populate the pointArray attribute
		MFnPointArrayData fnaPointData;
		MObject oInitPointData = fnaPointData.create(pointArray);
		hInitCurveData.set(oInitPointData);
	}
	else
	{
		MFnPointArrayData fnaPointData(oInitCurveData);
		pointArray = fnaPointData.array();
	}

	for (unsigned int i = 0; i < pointArray.length(); i ++)
	{
		for (; !iter.isDone(); iter.next())
		{
			pInPosition = iter.position();
			MPoint pt = fnCurve.closestPoint(pInPosition, &paramU, 0.1, MSpace::kWorld);
//			closestTangentUAndDistance(fnCurve, pInPosition, pPosition, vNormal, vTangent, paramU, distance);
//			cout << "inPosition: " << pInPosition.x << " " << pInPosition.y << " " << pInPosition.z << endl;
			cout << " position: " << pt.x << " " << pt.y << " " << pt.z << endl;
//			cout << " distance: " << distance << " paramU: " << paramU << endl;

			fnCurve.getPointAtParam(paramU, pCvPosition, MSpace::kTransform);

			cout << (pointArray[i] - pCvPosition).x << (pointArray[i] - pCvPosition).y << (pointArray[i] - pCvPosition).z << endl;
//			pInPosition -= vTrans;
//			pInPosition += ((pointArray[i] - pTrans) * fenv);
			pInPosition += ((pointArray[i] - pCvPosition) * foffset * fenv);
			cout << "finalPosition: " << pInPosition.x << " " << pInPosition.y << " " << pInPosition.z << endl;
			iter.setPosition(pInPosition);
		}
	}

	return MS::kSuccess;
}


void EtWireDeformer::closestTangentUAndDistance(MFnNurbsCurve& curveFn, MPoint inPosition,
												MPoint& position, MVector normal, MVector tangent,
												double& paramU, double& distance)
{
   // FIND THE CLOSEST POSITION AND PARAMETER-U FROM THE INPUT POSITION:
   position = curveFn.closestPoint(inPosition, &paramU, 0.0, MSpace::kWorld);

   // FIND THE NORMAL, TANGENT AND DISTANCE FROM THE CLOSEST POINT:
   normal = curveFn.normal(paramU, MSpace::kWorld);
   tangent = curveFn.tangent(paramU, MSpace::kWorld);
   distance = curveFn.distanceToPoint(inPosition, MSpace::kWorld);
}
