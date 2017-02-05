#include "curve.h"


MTypeId Curve::id(0x187564);
MObject Curve::aInMatrix;
MObject Curve::aInCurve;
MObject Curve::aInCurveMatrix;
MObject Curve::aInitCurveData;
MObject Curve::aInitUpVector;
MObject Curve::aInitDeltaData;
MObject Curve::aInitParamData;
MObject Curve::aSlider;
MObject Curve::aSliderType;
MObject Curve::aOffset;

MObject Curve::aOutTranslate;
MObject Curve::aOutRotateX;
MObject Curve::aOutRotateY;
MObject Curve::aOutRotateZ;
MObject Curve::aOutRotate;


Curve::Curve(){}
Curve::~Curve(){}


void* Curve::creator()
{
    return new Curve();
}


MStatus Curve::initialize()
{
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnCompoundAttribute cAttr;
    MFnEnumAttribute eAttr;
    MFnMatrixAttribute mAttr;

    //inMatrix
    aInMatrix = mAttr.create("inMatrix", "im");
    mAttr.setKeyable(false);
    mAttr.setReadable(false);
    mAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInMatrix));

    //inCurve
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

    //initCurveData
    aInitCurveData = tAttr.create("initCurveData", "icd", MFnData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setStorable(true);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInitCurveData));

    //initUpVector
    aInitUpVector = nAttr.createPoint("initUpVec", "iv");
    CHECK_MSTATUS(addAttribute(aInitUpVector));

    //initDeltaData
    aInitDeltaData = tAttr.create("initDeltaData", "initDeltaData", MFnData::kVectorArray);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setStorable(true);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInitDeltaData));

    //initParamData
    aInitParamData = tAttr.create("initParamData", "initParamData", MFnData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setStorable(true);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInitParamData));

    //slider
    aSlider = nAttr.create("slider", "sl", MFnNumericData::kFloat, 1.0);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aSlider));

    //sliderType
    aSliderType = eAttr.create("sliderType", "st");
    eAttr.addField("normal", 0);
    eAttr.addField("stepped", 1);
    eAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aSliderType));

    //offset
    aOffset = nAttr.create("offset", "off", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aOffset));

    //outTranslate
    aOutTranslate = nAttr.createPoint("outTranslate", "ot");
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setHidden(true);
    nAttr.setArray(true);
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
    nAttr.setArray(true);
    CHECK_MSTATUS(addAttribute(aOutRotate));

    //attribute affects
    attributeAffects(aInMatrix, outputGeom);

    attributeAffects(aInCurve, aOutTranslate);
    attributeAffects(aInCurve, aOutRotate);
    attributeAffects(aInCurve, outputGeom);

    attributeAffects(aInCurveMatrix, aOutTranslate);
    attributeAffects(aInCurveMatrix, aOutRotate);
    attributeAffects(aInCurveMatrix, outputGeom);

    attributeAffects(aInitCurveData, aOutTranslate);
    attributeAffects(aInitCurveData, aOutRotate);
    attributeAffects(aInitCurveData, outputGeom);

    attributeAffects(aInitUpVector, aOutTranslate);
    attributeAffects(aInitUpVector, aOutRotate);
    attributeAffects(aInitUpVector, outputGeom);

    attributeAffects(aInitDeltaData, outputGeom);
    attributeAffects(aInitParamData, outputGeom);

    attributeAffects(aSlider, aOutTranslate);
    attributeAffects(aSlider, aOutRotate);
    attributeAffects(aSlider, outputGeom);

    attributeAffects(aSliderType, aOutTranslate);
    attributeAffects(aSliderType, aOutRotate);
    attributeAffects(aSliderType, outputGeom);

    attributeAffects(aOffset, aOutTranslate);
    attributeAffects(aOffset, aOutRotate);
    attributeAffects(aOffset, outputGeom);

    MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer etcurve weights;");

    return MS::kSuccess;
}


MStatus Curve::deform(MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int multiIndex)
{
	MStatus status;

	// inputGeom
	MArrayDataHandle hMesh = data.outputArrayValue(input, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	status = hMesh.jumpToElement(multiIndex);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MObject oInputGeom = hMesh.outputValue().child(inputGeom).asMesh();
	if (! oInputGeom.hasFn(MFn::kMesh))
	{
		return MS::kUnknownParameter;
	}

	// inMatrix
	MMatrix mMatrix = data.inputValue(aInMatrix, &status).asMatrix();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// inCurve
	MObject oCurve = data.inputValue(aInCurve, &status).asNurbsCurve();
	if (oCurve.isNull())
	{
		return MS::kUnknownParameter;
	}

	// inCurveMatrix
	MMatrix mCurve = data.inputValue(aInCurveMatrix, &status).asMatrix();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// envelope
	float fenvelope = data.inputValue(envelope, &status).asFloat();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// offset
	float fOffset = data.inputValue(aOffset, &status).asFloat();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// slider
	float fslider = data.inputValue(aSlider, &status).asFloat();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// twist
	int islidertype = data.inputValue(aSliderType, &status).asShort();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// initUpVector
	MDataHandle hInitUpVec = data.inputValue(aInitUpVector, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MFloatVector fvinitupvec = hInitUpVec.asFloatVector();

	// create function set of nurbsCurve and store CV points
	MFnNurbsCurve fnCurve(oCurve);
	MPointArray pointArray;
	fnCurve.getCVs(pointArray, MSpace::kWorld);

	MArrayDataHandle hOutTranslate = data.outputArrayValue(aOutTranslate, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MArrayDataHandle hOutRotate = data.outputArrayValue(aOutRotate, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	MVectorArray vtangent(hOutTranslate.elementCount());
	MDoubleArray daParam(hOutTranslate.elementCount());
	double rotation[3];

	// Check initial curve data attribute for value
	MDataHandle hInitCurveData = data.inputValue(aInitCurveData, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MObject oInitCurveData = hInitCurveData.data();
	if (!oInitCurveData.hasFn(MFn::kDoubleArrayData))
	{
		for (unsigned int d=0; d<pointArray.length(); d++)
		{
			fnCurve.getParamAtPoint(pointArray[d], daParam[d], MSpace::kTransform);
		}
		// We need to populate the pointArray attribute
		MFnDoubleArrayData fnaDoubleData;
		MObject oInitDoubleData = fnaDoubleData.create(daParam);
		hInitCurveData.set(oInitDoubleData);
	}
	else
	{
		MFnDoubleArrayData fnaDoubleData(oInitCurveData);
		daParam = fnaDoubleData.array();
	}

	// Return the paralleFrameNormals
	int samples = pointArray.length();
	MVectorArray vanormals = parallelFrameNormals(samples, fvinitupvec, fnCurve, fslider);

	for (unsigned int i=0; i < samples; i++)
	{
		// Get parameter
		double param = fmod(daParam[i] + fOffset, fnCurve.numSpans()) * fslider;
		if (! islidertype)
		{
			if (fnCurve.form() == 3)
			{
				param = fmod(((fnCurve.findParamFromLength(fnCurve.length()) / samples) * i) + fOffset, fnCurve.numSpans());
			}
			if (param < 0.0)
			{
				param += fnCurve.numSpans();
			}
		}
//		else
//		{
		// float rmv = low2 + (value - low1) * (high2 - low2) / (high1 - low1)
		float rmv = 0.0 + (fslider - 0.0) * (fnCurve.length() - 0.0) / (1.0 - 0.0);
		float diff = rmv - (rmv - daParam[i]);
		cout << rmv << " " << diff << " " << daParam[daParam.length() - 1] << endl;
//		}

		fnCurve.getPointAtParam(param, pointArray[i], MSpace::kTransform);
		pointArray[i] *= mCurve;

		float fpoint[3];
		fpoint[0] = pointArray[i].x;
		fpoint[1] = pointArray[i].y;
		fpoint[2] = pointArray[i].z;

		hOutTranslate.jumpToArrayElement(i);
		hOutTranslate.outputValue().set(fpoint[0], fpoint[1], fpoint[2]);

		// Get tangent vector
		vtangent[i] = fnCurve.tangent(param, MSpace::kTransform, &status);
		vtangent[i].normalize();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		// take in curve worldMatrix into account
		vtangent[i] *= mCurve;
		vanormals[i] *= mCurve;

		calculateRotation(vanormals[i], vtangent[i], rotation);

		hOutRotate.jumpToArrayElement(i);
		hOutRotate.outputValue().set(rotation[0], rotation[1], rotation[2]);
		fnCurve.updateCurve();
	}

	//Get the closestPoint and param on the curve from each vertex
	MFnMesh fnMesh(oInputGeom);
	MPoint currentpos, position;
	MVectorArray vadelta(fnMesh.numVertices());
	MDoubleArray param(fnMesh.numVertices());

	// Check initial curve data attribute for value
	MDataHandle hInitDeltaData = data.inputValue(aInitDeltaData, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MObject oInitDeltaData = hInitDeltaData.data();
	if (!oInitDeltaData.hasFn(MFn::kVectorArrayData))
	{
		for (unsigned int m=0; m<fnMesh.numVertices(); m++)
		{
			fnMesh.getPoint(m, currentpos);
			getClosestPoint(fnCurve, currentpos * mMatrix, position, param[m]);
			double myMatrix[4][4] = {{1,0,0,0}, {0,1,0,0}, {0,0,1,0},
									 {currentpos.x, currentpos.y, currentpos.z, 1}};
			MMatrix mCurrentPos(myMatrix);
			MMatrix mValue = mMatrix * mCurrentPos;
			vadelta[m] = (position - currentpos);
			vadelta[m] *= mValue;
		}
		// We need to populate the vectorArray and doubleArray attribute
		MFnVectorArrayData fnaDeltaData;
		MObject oInitDeltaData = fnaDeltaData.create(vadelta);
		hInitDeltaData.set(oInitDeltaData);
	}
	else
	{
		MFnVectorArrayData fnaDeltaData(oInitDeltaData);
		vadelta = fnaDeltaData.array();
	}

	// Check initial curve data attribute for value
	MDataHandle hInitParamData = data.inputValue(aInitParamData, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MObject oInitParamData = hInitParamData.data();
	if (!oInitParamData.hasFn(MFn::kDoubleArrayData))
	{
		// We need to populate the vectorArray and doubleArray attribute
		MFnDoubleArrayData fnaParamData;
		MObject oInitParamData = fnaParamData.create(param);
		hInitParamData.set(oInitParamData);
	}
	else
	{
		MFnDoubleArrayData fnaParamData(oInitParamData);
		param = fnaParamData.array();
	}

	float w= 0.0;
	MVector tangent, newdelta;
	MPoint pt;
	MPointArray points(iter.count());

	for (;! iter.isDone(); iter.next())
	{
		tangent = fnCurve.tangent(param[iter.index()], MSpace::kWorld, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		newdelta = tangent ^ vadelta[iter.index()];

		// Get paintable weights
		w = weightValue(data, multiIndex, iter.index());
		status = fnCurve.getPointAtParam(param[iter.index()] * fslider, pt, MSpace::kObject);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		points[iter.index()] = ((vadelta[iter.index()] + pt) * w) * fenvelope;
		points[iter.index()] *=  mCurve;
	}
	iter.setAllPositions(points);
	return MS::kSuccess;
}


MVectorArray Curve::parallelFrameNormals(int samples, MVector upvec, MFnNurbsCurve& fnCurve, float slider)
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

		param = fmod((fnCurve.findParamFromLength(fnCurve.length()) / samples) * n, fnCurve.numSpans()) * slider;
		if (fnCurve.form() == 3)
		{
			param = fmod((fnCurve.findParamFromLength(fnCurve.length()) / samples) * n, fnCurve.numSpans());
		}

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


void Curve::calculateRotation(MVector up, MVector forward, double rotation[3])
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


void Curve::getClosestPoint(MFnNurbsCurve& fnCurve, MPoint inPosition, MPoint& position, double& paramU)
{
	position = fnCurve.closestPoint(inPosition, &paramU, 0.0, MSpace::kWorld);
}


// This is to calculate the offset
/*double paramy = fmod(param[iter.index()] + fOffset, fnCurve.numSpans()) * fslider;
/if (fnCurve.form() == 3)
{
	paramy = fmod(param[iter.index()] + fOffset, fnCurve.numSpans());
}
if (paramy < 0.0)
{
	paramy += fnCurve.numSpans();
}*/
