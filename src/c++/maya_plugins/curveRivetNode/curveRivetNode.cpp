#include "curveRivetNode.h"

float maxi = 1000000.0;
float mini = -1000000.0;
float PI = 3.14159265359;


MTypeId CurveRivetNode::id(0x2323145);
MObject CurveRivetNode::aInCurve;
MObject CurveRivetNode::aInMatrix;
MObject CurveRivetNode::aParameterU;
MObject CurveRivetNode::aOperator;

MObject CurveRivetNode::aOutTranslate;
MObject CurveRivetNode::aOutRotateX;
MObject CurveRivetNode::aOutRotateY;
MObject CurveRivetNode::aOutRotateZ;
MObject CurveRivetNode::aOutRotate;


CurveRivetNode::CurveRivetNode(){}
CurveRivetNode::~CurveRivetNode(){}

void* CurveRivetNode::creator()
{
    return new CurveRivetNode();
}

MStatus CurveRivetNode::initialize()
{
    MFnEnumAttribute eAttr;
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnMatrixAttribute mAttr;

    //inMesh
    aInCurve = tAttr.create("inCurve", "ic", MFnData::kNurbsCurve);
    CHECK_MSTATUS(addAttribute(aInCurve));

    //inMatrix
    aInMatrix = mAttr.create("inMatrix", "ima");
    CHECK_MSTATUS(addAttribute(aInMatrix));
    mAttr.setHidden(true);

    //parameterU
    aParameterU = nAttr.create("parameterU", "pu", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aParameterU));

    //modulusU
    aOperator = eAttr.create("Modulus", "mo");
    eAttr.addField("None", 0);
    eAttr.addField("U", 1);
    eAttr.addField("V", 2);
    eAttr.addField("UV", 3);
    eAttr.setKeyable(true);
    eAttr.setStorable(true);
    CHECK_MSTATUS(addAttribute(aOperator));

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
    attributeAffects(aInCurve, aOutTranslate);
    attributeAffects(aInCurve, aOutRotate);

    attributeAffects(aInMatrix, aOutTranslate);
    attributeAffects(aInMatrix, aOutRotate);

    attributeAffects(aParameterU, aOutTranslate);
    attributeAffects(aParameterU, aOutRotate);

    attributeAffects(aOperator, aOutTranslate);
    attributeAffects(aOperator, aOutRotate);

    return MS::kSuccess;
}

MStatus CurveRivetNode::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;
	//Check the output for dirt
	if (plug == aOutTranslate || plug == aOutRotate)
	{
		//Check the inMesh value
		MObject oInCurve = data.inputValue(aInCurve).asNurbsCurve();
		if (oInCurve.isNull())
		{
			return MS::kSuccess;
		}
		//Check the inMatrix value
		MMatrix mInMatrix = data.inputValue(aInMatrix).asMatrix();
		//Get the Parameter values
		float fParameterU = data.inputValue(aParameterU).asFloat();

		//Get DataHandles for the outputs
		MDataHandle hOutTranslate = data.outputValue(aOutTranslate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		MDataHandle hOutRotate = data.outputValue(aOutRotate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);

		if (oInCurve.hasFn(MFn::kNurbsCurve))
		{
			MFnNurbsCurve fnInCurve(oInCurve, &status);
			if (status != MS::kSuccess)
			{
				MGlobal::displayWarning("Initializing NurbsSurface failed!");
				return MS::kSuccess;
			}
			double dParamU = fParameterU;
			MPoint pPosition;
			MVector vUp, vForward;

			cout << dParamU << endl;
			//Get position at the given U parameter
			fnInCurve.getPointAtParam(dParamU, pPosition);
			cout << pPosition.x << " " << pPosition.y << " " << pPosition.z << endl;
			//Get the normal
			vUp = fnInCurve.normal(dParamU, MSpace::kTransform, &status);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			//Get the tangent
			vForward = fnInCurve.tangent(dParamU, MSpace::kTransform, &status);
			CHECK_MSTATUS_AND_RETURN_IT(status);

			//Normalize and multiply with inMatrix
			vUp.normalize();
			vUp *= mInMatrix;
			vForward *= mInMatrix;

			//Calculate rotation
			double dRotation[3];
			float fRotation[3];
			calculateRotation(vUp, vForward, dRotation, fRotation);

			MVector vQuaternionA(0,1,0), vQuaternionB(1,0,0), vQuaternionC(0,0,1);
			float fDegreesA = 90;
			float fDegreesB = 45;
			MQuaternion quaternionA, quaternionB, quaternionC;

			getQuaternion(vQuaternionA, fDegreesA, quaternionA);
			getQuaternion(vQuaternionB, fDegreesB, quaternionB);

			quaternionC = quaternionB * quaternionA;

			cout << "A: " << quaternionA.w << " " << quaternionA.x << " " << quaternionA.y << " " << quaternionA.z << endl;
			cout << "B: " << quaternionB.w << " " << quaternionB.x << " " << quaternionB.y << " " << quaternionB.z << endl;
			cout << "C: " << quaternionC.w << " " << quaternionC.x << " " << quaternionC.y << " " << quaternionC.z << endl;
			invertQuaternion(quaternionC);
			cout << "C inverse: " << quaternionC.w << " " << quaternionC.x << " " << quaternionC.y << " " << quaternionC.z << endl;
			vQuaternionC *= quaternionC;
			cout << "vector: " << vQuaternionC.x << " " << vQuaternionC.y << " " << vQuaternionC.z << endl;

			//Set rotation
			hOutRotate.set(dRotation[0], dRotation[1], dRotation[2]);

			//Set outTranslate
			pPosition *= mInMatrix;
			float fPosition[3];
			fPosition[0]= pPosition.x;
			fPosition[1]= pPosition.y;
			fPosition[2]= pPosition.z;
			hOutTranslate.set(fPosition[0], fPosition[1], fPosition[2]);
			data.setClean(plug);
		}
	}
	return MS::kSuccess;
}


double CurveRivetNode::calculateModulus(double paramU, int numSpans, int operatorIndex)
{
	MFnNumericAttribute nAttrU;
	MFnNumericAttribute nAttrV;

	double dNumSpans = numSpans;

	nAttrU.setObject(aParameterU);
	if (operatorIndex == 0)
	{
		/////////// NONE ///////////
		//Limit the parameterU attribute
		nAttrU.setMin(0.0);
		nAttrU.setMax(numSpans);
		//Get number of spans to calculate modulus of the UParameter
		if (paramU != numSpans)
		{
			if (paramU < 0.0)
			{
				paramU *= -1.0;
			}
			paramU = fmod(paramU, dNumSpans);
		}
	}
	else if (operatorIndex == 1)
	{
		///////// MODULUS U /////////
		//Limit the parameterV attribute

		//ParameterU
		nAttrU.setMin(mini);
		nAttrU.setMax(maxi);
		//Get number of spans to calculate modulus for the ParameterU
		if (paramU < 0.0)
		{
			paramU *= -1.0;
			paramU = dNumSpans - (fmod(paramU, dNumSpans));
		}
		else
		{
			paramU = fmod(paramU, dNumSpans);
		}
	}
	else if (operatorIndex == 2)
	{
		///////// MODULUS V /////////
		//Limit the parameterU attribute
		nAttrU.setMin(0.0);
		nAttrU.setMax(numSpans);
		//Get number of spans to calculate modulus of the UParameter
		if (paramU != numSpans)
		{
			if (paramU < 0.0)
			{
				paramU *= -1.0;
			}
			paramU = fmod(paramU, dNumSpans);
		}
	}
	else
	{
		///////// MODULUS BOTH //////////
		//ParameterU
		nAttrU.setMin(mini);
		nAttrU.setMax(maxi);
		//Get number of spans to calculate modulus for the ParameterU
		if (paramU < 0.0)
		{
			paramU *= -1.0;
			paramU = dNumSpans - (fmod(paramU, dNumSpans));
		}
		else
		{
			paramU = fmod(paramU, dNumSpans);
		}
	}
	return paramU;
}


void CurveRivetNode::calculateRotation(MVector up, MVector forward, double rotation[3], float euler[3])
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

void CurveRivetNode::getQuaternion(MVector& n, float a, MQuaternion& quaternion)
{
	//Convert degrees into radians to deal with Quaternions
	a = a / 360 * PI * 2;

	quaternion.w = cos(a/2);
	quaternion.x = n.x*sin(a/2);
	quaternion.y = n.y*sin(a/2);
	quaternion.z = n.z*sin(a/2);
}

void CurveRivetNode::invertQuaternion(MQuaternion& quaternion)
{
	//Convert degrees into radians to deal with Quaternions
	quaternion.w *= 1.0;
	quaternion.x *= -1.0;
	quaternion.y *= -1.0;
	quaternion.z *= -1.0;
}
