#include "nurbsRivetNode.h"

float maxi = 1000000.0;
float mini = -1000000.0;


MTypeId NurbsRivetNode::id(0x3565632);
MObject NurbsRivetNode::aInSurface;
MObject NurbsRivetNode::aInMatrix;
MObject NurbsRivetNode::aOperator;
MObject NurbsRivetNode::aParameterU;
MObject NurbsRivetNode::aParameterV;
MObject NurbsRivetNode::aInput;

MObject NurbsRivetNode::aOutTranslate;
MObject NurbsRivetNode::aOutRotateX;
MObject NurbsRivetNode::aOutRotateY;
MObject NurbsRivetNode::aOutRotateZ;
MObject NurbsRivetNode::aOutRotate;


NurbsRivetNode::NurbsRivetNode(){}
NurbsRivetNode::~NurbsRivetNode(){}

void* NurbsRivetNode::creator()
{
    return new NurbsRivetNode();
}

MStatus NurbsRivetNode::initialize()
{
    MFnEnumAttribute eAttr;
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;
    MFnMatrixAttribute mAttr;

    //inSurface
    aInSurface = tAttr.create("inSurface", "is", MFnData::kNurbsSurface);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInSurface));

    //inMatrix
    aInMatrix = mAttr.create("inMatrix", "im");
    mAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInMatrix));

    //operator
    /*
    aOperator = eAttr.create("Modulus", "mo");
    eAttr.addField("None", 0);
    eAttr.addField("U", 1);
    eAttr.addField("V", 2);
    eAttr.addField("UV", 3);
    eAttr.setStorable(true);
    CHECK_MSTATUS(addAttribute(aOperator));
	*/

    //parameterU
    aParameterU = nAttr.create("parameterU", "pu", MFnNumericData::kDouble, 0.0);
    nAttr.setStorable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    CHECK_MSTATUS(addAttribute(aParameterU));

    //parameterV
    aParameterV = nAttr.create("parameterV", "pv", MFnNumericData::kDouble, 0.0);
    nAttr.setStorable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    CHECK_MSTATUS(addAttribute(aParameterV));

    //input
    aInput = cAttr.create("parameterUV", "puv");
    cAttr.addChild(aParameterU);
    cAttr.addChild(aParameterV);
    cAttr.setArray(true);
    CHECK_MSTATUS(addAttribute(aInput));

    //outTranslate
    aOutTranslate = nAttr.createPoint("outTranslate", "ot");
    nAttr.setArray(true);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutTranslate));

    // Set up rotate outputs
    aOutRotateX = uAttr.create("outRotateX", "orx", MFnUnitAttribute::kAngle, 0.0);
    CHECK_MSTATUS(addAttribute(aOutRotateX));

    aOutRotateY = uAttr.create("outRotateY", "ory", MFnUnitAttribute::kAngle, 0.0);
    CHECK_MSTATUS(addAttribute(aOutRotateY));

    aOutRotateZ = uAttr.create("outRotateZ", "orz", MFnUnitAttribute::kAngle, 0.0);
    CHECK_MSTATUS(addAttribute(aOutRotateZ));

    aOutRotate = nAttr.create("outRotate", "or", aOutRotateX, aOutRotateY, aOutRotateZ);
    nAttr.setArray(true);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutRotate));

    //attribute affects
    attributeAffects(aInSurface, aOutTranslate);
    attributeAffects(aInSurface, aOutRotate);

    attributeAffects(aInMatrix, aOutTranslate);
    attributeAffects(aInMatrix, aOutRotate);

    //attributeAffects(aOperator, aOutTranslate);
    //attributeAffects(aOperator, aOutRotate);

    attributeAffects(aParameterU, aOutTranslate);
    attributeAffects(aParameterU, aOutRotate);

    attributeAffects(aParameterV, aOutTranslate);
    attributeAffects(aParameterV, aOutRotate);

    attributeAffects(aInput, aOutTranslate);
    attributeAffects(aInput, aOutRotate);

    return MS::kSuccess;
}

MStatus NurbsRivetNode::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;
	//Check the output for dirt
	if (plug == aOutTranslate || plug == aOutRotate)
	{
		//Check the inMesh value
		MObject oInSurface = data.inputValue(aInSurface).asNurbsSurface();
		if (oInSurface.isNull() || !oInSurface.hasFn(MFn::kNurbsSurface))
		{
			MGlobal::displayWarning("Initializing NurbsSurface failed!");
			return MS::kUnknownParameter;
		}
		MFnNurbsSurface fnInSurface(oInSurface);
		//Get the worldMatrix value of the surface
		MMatrix mInMatrix = data.inputValue(aInMatrix).asMatrix();

		//Get input handle
		MArrayDataHandle hInput = data.inputArrayValue(aInput, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		//int iOperator = data.inputValue(aOperator).asShort();

		//Get DataHandles for the outputs
		MArrayDataHandle hOutTranslate = data.outputArrayValue(aOutTranslate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		MArrayDataHandle hOutRotate = data.outputArrayValue(aOutRotate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);

		for (unsigned int i=0; i<hOutTranslate.elementCount(); i++)
		{
			if (! hInput.elementCount())
			{
				return MS::kUnknownParameter;
			}

			status = hInput.jumpToArrayElement(i);
			CHECK_MSTATUS_AND_RETURN_IT(status);

			double dParamU = hInput.inputValue().child(aParameterU).asDouble();
			double dParamV = hInput.inputValue().child(aParameterV).asDouble();

			dParamU *= fnInSurface.numPatchesInU();
			dParamV *= fnInSurface.numPatchesInV();

			// Define parameters
			MPoint pPosition;

			//Calculate Modulus
			//dParamU = calculateModulus(dParamU, fnInSurface, iOperator);

			//Get Point at given parameters
			fnInSurface.getPointAtParam(dParamU, dParamV, pPosition, MSpace::kObject);

			// Set outTranslate
			pPosition *= mInMatrix;
			MFloatVector fvPosition = pPosition;
			status = hOutTranslate.jumpToArrayElement(i);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			hOutTranslate.outputValue().set(fvPosition);

			// Define parameters
			MVector vUp, vForward, vTangentV;
			//Get normal
			vUp = fnInSurface.normal(dParamU, dParamV, MSpace::kTransform, &status);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			vUp.normalize();
			vUp *= mInMatrix;
			//Get U tangent
			fnInSurface.getTangents(dParamU, dParamV, vForward, vTangentV, MSpace::kTransform);
			vForward.normalize();
			vTangentV.normalize();
			vForward *= mInMatrix;

			//Calculate rotation
			double dRotation[3];
			calculateRotation(vUp, vForward, dRotation);

			//Set rotation
			if (hOutRotate.jumpToArrayElement(i))
			{
				status = hOutRotate.jumpToArrayElement(i);
				CHECK_MSTATUS_AND_RETURN_IT(status);
				hOutRotate.outputValue().set(dRotation[0], dRotation[1], dRotation[2]);
			}
		}
		data.setClean(plug);
	}
	return MS::kSuccess;
}


double NurbsRivetNode::calculateModulus(double paramU, MFnNurbsSurface& surface, int operatorIndex)
{
	MFnNumericAttribute nAttrU;
	MFnNumericAttribute nAttrV;

	int iNumSpans = surface.numSpansInU();
	double dNumSpans = iNumSpans;
	int iSections = surface.numSpansInV();

	nAttrU.setObject(aInput);
	nAttrV.setObject(aInput);
	nAttrU.child(0);
	nAttrV.child(1);
	if (operatorIndex == 0)
	{
		/////////// NONE ///////////
		//Limit the parameterU attribute
		nAttrU.setMin(0.0);
		nAttrU.setMax(iNumSpans);
		//Get number of spans to calculate modulus of the UParameter
		if (paramU != iNumSpans)
		{
			if (paramU < 0.0)
			{
				paramU *= -1.0;
			}
			paramU = fmod(paramU, dNumSpans);
		}
		//Limit the parameterV attribute
		nAttrV.setMin(0.0);
		nAttrV.setMax(iSections);
	}
	else if (operatorIndex == 1)
	{
		///////// MODULUS U /////////
		//Limit the parameterV attribute
		nAttrV.setMin(0.0);
		nAttrV.setMax(iSections);

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
		nAttrU.setMax(iNumSpans);
		//Get number of spans to calculate modulus of the UParameter
		if (paramU != iNumSpans)
		{
			if (paramU < 0.0)
			{
				paramU *= -1.0;
			}
			paramU = fmod(paramU, dNumSpans);
		}

		//Parameter V
		nAttrV.setMin(mini);
		nAttrV.setMax(maxi);
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

		//ParameterV
		nAttrV.setMin(mini);
		nAttrV.setMax(maxi);
	}
	return paramU;
}


void NurbsRivetNode::calculateRotation(MVector up, MVector forward, double rotation[3])
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
