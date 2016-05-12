#include "offsetcurve.h"

MTypeId OffsetCurve::id(0x3974621);
MObject OffsetCurve::aInCurve;
MObject OffsetCurve::aInMatrix;
MObject OffsetCurve::aOffset;
MObject OffsetCurve::aInitUpVector;
MObject OffsetCurve::aInitCurveData;
MObject OffsetCurve::aOutTranslate;
MObject OffsetCurve::aOutRotate;


OffsetCurve::OffsetCurve(){}
OffsetCurve::~OffsetCurve(){}

void* OffsetCurve::creator()
{
    return new OffsetCurve();
}

MStatus OffsetCurve::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;

    // inCurve
    aInCurve = tAttr.create("inCurve", "ic", MFnData::kNurbsCurve);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInCurve));

    // inMatrix
    aInMatrix = mAttr.create("inMatrix", "im");
    mAttr.setKeyable(false);
    mAttr.setReadable(false);
    mAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInMatrix));

    //offset
    aOffset = nAttr.create("offset", "off", MFnNumericData::kFloat, 0.0);
    nAttr.setReadable(true);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aOffset));

    //initUpVector
    aInitUpVector = nAttr.createPoint("initUpVector", "iup");
    nAttr.setKeyable(true);
    nAttr.setWritable(true);
    nAttr.setReadable(true);
    CHECK_MSTATUS(addAttribute(aInitUpVector));

    //initCurveData
    aInitCurveData = tAttr.create("initCurveData", "icd", MFnData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setStorable(true);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInitCurveData));

    //outTranslate
    aOutTranslate = nAttr.createPoint("outTranslate", "ot");
    nAttr.setArray(true);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutTranslate));

    //outRotate
    aOutRotate = nAttr.createPoint("outRotate", "or");
    nAttr.setArray(true);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutRotate));

    attributeAffects(aInCurve, aOutTranslate);
    attributeAffects(aInMatrix, aOutTranslate);
    attributeAffects(aOffset, aOutTranslate);
    attributeAffects(aInitUpVector, aOutTranslate);
    attributeAffects(aInitCurveData, aOutTranslate);

    attributeAffects(aInCurve, aOutRotate);
    attributeAffects(aInMatrix, aOutRotate);
    attributeAffects(aOffset, aOutRotate);
    attributeAffects(aInitUpVector, aOutRotate);
    attributeAffects(aInitCurveData, aOutRotate);

    return MS::kSuccess;
}


MStatus OffsetCurve::compute(const MPlug& plug, MDataBlock& dataBlock)
{
	MStatus status;

	if (plug == aOutTranslate || plug == aOutRotate)
	{
		// Get the inCurve
		MObject oInCurve = dataBlock.inputValue(aInCurve).asNurbsCurve();
		if (oInCurve.isNull())
		{
			return MS::kSuccess;
		}

		// Get inMatrix
		MMatrix mCurve = dataBlock.inputValue(aInMatrix, &status).asMatrix();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		// Get offset
		float fOffset = dataBlock.inputValue(aOffset, &status).asFloat();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		// Get initCurveData
		MFloatVector fvInitCurveData = dataBlock.inputValue(aInitCurveData, &status).asFloatVector();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		MFnNurbsCurve fnCurve(oInCurve);
		MPointArray paInitPoints, paFinalPoints;
		status = fnCurve.getCVs(paInitPoints);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		paFinalPoints.setLength(paInitPoints.length());
		MDoubleArray daParam(paInitPoints.length());

		// Get and populate the initCurveData
		MDataHandle hInitCurveData = dataBlock.inputValue(aInitCurveData, &status);
		MObject oInitCurveData = hInitCurveData.data();
		if (!oInitCurveData.hasFn(MFn::kDoubleArrayData))
		{
			for (unsigned int d=0; d < paInitPoints.length(); d++)
			{
				status = fnCurve.getParamAtPoint(paInitPoints[d], daParam[d], MSpace::kObject);
				CHECK_MSTATUS_AND_RETURN_IT(status);
			}
			// We need to populate the pointArray attribute
			MFnDoubleArrayData fnaDoubleData;
			MObject oInitDoubleData = fnaDoubleData.create(daParam);
			status = hInitCurveData.set(oInitDoubleData);
			CHECK_MSTATUS_AND_RETURN_IT(status);
		}
		else
		{
			MFnDoubleArrayData fnaDoubleData(oInitCurveData);
			daParam = fnaDoubleData.array();
		}

		MArrayDataHandle hOutTranslate = dataBlock.outputArrayValue(aOutTranslate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);

		MArrayDataHandle hOutRotate = dataBlock.outputArrayValue(aOutRotate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);

		// Get normals by using parallelFrameTransportation
		MVectorArray vaNormals = parallelFrameNormals(paInitPoints.length(), fvInitCurveData, fnCurve);
		MVectorArray vaTangent(paInitPoints.length());
		double dParam, rotation[3];

		for ( unsigned int i=0; i<paInitPoints.length(); i++ )
		{
			// Set position
			dParam = fmod(daParam[i] + fOffset, fnCurve.numSpans());
			if (dParam < 0.0)
			{
				dParam += fnCurve.numSpans();
			}

			status = fnCurve.getPointAtParam(dParam, paFinalPoints[i], MSpace::kTransform);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			paFinalPoints[i] *= mCurve;

			MFloatVector fvFinalPoints = paFinalPoints[i];

			hOutTranslate.jumpToArrayElement(i);
			hOutTranslate.outputValue().set(fvFinalPoints);

			// Set rotation
			vaTangent[i] = fnCurve.tangent(dParam, MSpace::kTransform, &status);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			status = vaTangent[i].normalize();
			CHECK_MSTATUS_AND_RETURN_IT(status);
			status = vaNormals[i].normalize();
			CHECK_MSTATUS_AND_RETURN_IT(status);

			// Take in curve worldMatrix into account
			vaTangent[i] *= mCurve;
			vaNormals[i] *= mCurve;

			cout << vaTangent[i].x << vaTangent[i].y << vaTangent[i].z << endl;
			cout << vaNormals[i].x << vaNormals[i].y << vaNormals[i].z << endl;
			calculateRotation(vaNormals[i], vaTangent[i], rotation);

			hOutRotate.jumpToArrayElement(i);
			hOutRotate.outputValue().set(rotation[0], rotation[1], rotation[2]);
			fnCurve.updateCurve();
		}
		dataBlock.setClean(plug);
	}

    return MS::kSuccess;
}


MVectorArray OffsetCurve::parallelFrameNormals(int samples, MVector upvec, MFnNurbsCurve& fnCurve)
{
	// Return an array of normals perpendicular to the tangentVector of the curve
	MStatus status;

	MVectorArray normals(samples);
	MVector vtangent, vcross1, vcross2;
	MVector vnormal = upvec;
	double param;
	vnormal.normalize();

	for (unsigned int n=0; n<samples; n++)
	{
		param = fmod((fnCurve.findParamFromLength(fnCurve.length()) / samples) * n, fnCurve.numSpans());
		vtangent = fnCurve.tangent(param, MSpace::kObject);
		vtangent.normalize();
		vcross1 = vnormal ^ vtangent;
		vcross1.normalize();
		vcross2 = vtangent ^ vcross1;
		vcross2.normalize();
		vnormal = vcross2;
		normals[n] = vcross2;
	}
	return normals;
}


void OffsetCurve::calculateRotation(MVector up, MVector forward, double rotation[3])
{
	MVector vOrthogonal;
	MVector vNewForward;
	//Check if the vectors are orthogonal
	if (fabs(up * forward) > 0.001)
	{
		//Cross product calculation
		vOrthogonal = up ^ forward;
		vNewForward = vOrthogonal ^ up;
		if (forward * vNewForward < 0.0)
		{
			//Reverse vector
			vNewForward *= -1.0;
		}
		forward = vNewForward;
	}

	//Calculate first rotation
	MTransformationMatrix tmFirstRotation;
	MVector vRotAxis = MVector::yAxis ^ up;
	vRotAxis.normalize();
	up.normalize();
	tmFirstRotation.setToRotationAxis(vRotAxis, MVector::yAxis.angle(up));

	//Calculate second rotation
	MTransformationMatrix tmSecondRotation;
	MVector vTransformedForward = tmFirstRotation.asMatrix() * forward;
	vTransformedForward.normalize();
	double angle = vTransformedForward.angle(MVector::zAxis);
	if (vTransformedForward.x < 0.0)
	{
		angle *= -1.0;
	}
	tmSecondRotation.setToRotationAxis(up, angle);

	//Get final rotation matrix
	MTransformationMatrix tmResult = tmFirstRotation.asMatrix() * tmSecondRotation.asMatrix();
	MTransformationMatrix::RotationOrder rotOrder = MTransformationMatrix::kXYZ;
	tmResult.reorderRotation(rotOrder);
	tmResult.getRotation(rotation, rotOrder, MSpace::kTransform);
}
