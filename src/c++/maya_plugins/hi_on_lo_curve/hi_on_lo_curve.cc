#include "hi_on_lo_curve.h"


MTypeId HiOnLoCurve::id(0x187564);
MObject HiOnLoCurve::aInMatrix;
MObject HiOnLoCurve::aInitUpVector;
MObject HiOnLoCurve::aInitDeltaData;
MObject HiOnLoCurve::aInitParamData;
MObject HiOnLoCurve::aSlider;
MObject HiOnLoCurve::aTwist;
MObject HiOnLoCurve::aOffset;

MObject HiOnLoCurve::aOutTranslate;
MObject HiOnLoCurve::aOutRotateX;
MObject HiOnLoCurve::aOutRotateY;
MObject HiOnLoCurve::aOutRotateZ;
MObject HiOnLoCurve::aOutRotate;


HiOnLoCurve::HiOnLoCurve(){}
HiOnLoCurve::~HiOnLoCurve(){}


void* HiOnLoCurve::creator()
{
    return new HiOnLoCurve();
}


MStatus HiOnLoCurve::initialize()
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

    //inHiOnLoCurve
    aInHiOnLoCurve = tAttr.create("inHiOnLoCurve", "ic", MFnData::kNurbsHiOnLoCurve);
    nAttr.setKeyable(false);
    nAttr.setReadable(false);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInHiOnLoCurve));

    //inHiOnLoCurveMatrix
    aInHiOnLoCurveMatrix = mAttr.create("inHiOnLoCurveMatrix", "icm");
    mAttr.setKeyable(false);
    mAttr.setReadable(false);
    mAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInHiOnLoCurveMatrix));

    //initHiOnLoCurveData
    aInitHiOnLoCurveData = tAttr.create("initHiOnLoCurveData", "icd", MFnData::kDoubleArray);
    tAttr.setKeyable(false);
    tAttr.setReadable(false);
    tAttr.setStorable(true);
    tAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aInitHiOnLoCurveData));

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

    //twist
    aTwist = nAttr.create("twist", "tw", MFnNumericData::kFloat, 0.0);
    nAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aTwist));

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

    attributeAffects(aInitUpVector, aOutTranslate);
    attributeAffects(aInitUpVector, aOutRotate);
    attributeAffects(aInitUpVector, outputGeom);

    attributeAffects(aInitDeltaData, outputGeom);
    attributeAffects(aInitParamData, outputGeom);

    attributeAffects(aSlider, aOutTranslate);
    attributeAffects(aSlider, aOutRotate);
    attributeAffects(aSlider, outputGeom);

    attributeAffects(aTwist, aOutTranslate);
    attributeAffects(aTwist, aOutRotate);
    attributeAffects(aTwist, outputGeom);

    attributeAffects(aOffset, aOutTranslate);
    attributeAffects(aOffset, aOutRotate);
    attributeAffects(aOffset, outputGeom);

    MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer etcurve weights;");

    return MS::kSuccess;
}


MStatus HiOnLoCurve::deform(MDataBlock& data, MItGeometry& iter, const MMatrix& mat, unsigned int multiIndex)
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
	MMatrix mInvMatrix = mMatrix.inverse();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// inHiOnLoCurve
	MObject oHiOnLoCurve = data.inputValue(aInHiOnLoCurve, &status).asNurbsHiOnLoCurve();
	if (oHiOnLoCurve.isNull())
	{
		return MS::kUnknownParameter;
	}

	// inHiOnLoCurveMatrix
	MMatrix mHiOnLoCurve = data.inputValue(aInHiOnLoCurveMatrix, &status).asMatrix();
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
	float fTwist = data.inputValue(aTwist, &status).asFloat();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// initUpVector
	MDataHandle hInitUpVec = data.inputValue(aInitUpVector, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MFloatVector fvinitupvec = hInitUpVec.asFloatVector();

	// create function set of nurbsHiOnLoCurve and store CV points
	MFnNurbsHiOnLoCurve fnHiOnLoCurve(oHiOnLoCurve);
	MPointArray pointArray;
	fnHiOnLoCurve.getCVs(pointArray, MSpace::kWorld);

	MArrayDataHandle hOutTranslate = data.outputArrayValue(aOutTranslate, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MArrayDataHandle hOutRotate = data.outputArrayValue(aOutRotate, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	MVectorArray vtangent(hOutTranslate.elementCount());
	MDoubleArray daParam(hOutTranslate.elementCount());
	double rotation[3];

	// Check initial curve data attribute for value
	MDataHandle hInitHiOnLoCurveData = data.inputValue(aInitHiOnLoCurveData, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MObject oInitHiOnLoCurveData = hInitHiOnLoCurveData.data();
	if (!oInitHiOnLoCurveData.hasFn(MFn::kDoubleArrayData))
	{
		for (unsigned int d=0; d<pointArray.length(); d++)
		{
			fnHiOnLoCurve.getParamAtPoint(pointArray[d], daParam[d], MSpace::kTransform);
		}
		// We need to populate the pointArray attribute
		MFnDoubleArrayData fnaDoubleData;
		MObject oInitDoubleData = fnaDoubleData.create(daParam);
		hInitHiOnLoCurveData.set(oInitDoubleData);
	}
	else
	{
		MFnDoubleArrayData fnaDoubleData(oInitHiOnLoCurveData);
		daParam = fnaDoubleData.array();
	}

	// Return the paralleFrameNormals
	int samples = pointArray.length();
	MVectorArray vanormals = parallelFrameNormals(samples, fvinitupvec, fnHiOnLoCurve, fslider);

	for (unsigned int i=0; i < samples; i++)
	{
		// Calculate Translation with modulus on
		double param = fmod(daParam[i] + fOffset, fnHiOnLoCurve.numSpans()) * fslider;
		if (fnHiOnLoCurve.form() == 3)
		{
			param = fmod(((fnHiOnLoCurve.findParamFromLength(fnHiOnLoCurve.length()) / samples) * i) + fOffset, fnHiOnLoCurve.numSpans());
		}
		if (param < 0.0)
		{
			param += fnHiOnLoCurve.numSpans();
		}

		fnHiOnLoCurve.getPointAtParam(param, pointArray[i], MSpace::kTransform);
		pointArray[i] *= mHiOnLoCurve;

		float fpoint[3];
		fpoint[0] = pointArray[i].x;
		fpoint[1] = pointArray[i].y;
		fpoint[2] = pointArray[i].z;

		hOutTranslate.jumpToArrayElement(i);
		hOutTranslate.outputValue().set(fpoint[0], fpoint[1], fpoint[2]);

		// Get tangent vector
		vtangent[i] = fnHiOnLoCurve.tangent(param, MSpace::kTransform, &status);
		vtangent[i].normalize();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		// take in curve worldMatrix into account
		vtangent[i] *= mHiOnLoCurve;
		vanormals[i] *= mHiOnLoCurve;

		calculateRotation(vanormals[i], vtangent[i], rotation, fTwist);

		hOutRotate.jumpToArrayElement(i);
		hOutRotate.outputValue().set(rotation[0], rotation[1], rotation[2]);
		fnHiOnLoCurve.updateHiOnLoCurve();
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
			getClosestPoint(fnHiOnLoCurve, currentpos * mMatrix, position, param[m]);
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
		tangent = fnHiOnLoCurve.tangent(param[iter.index()], MSpace::kWorld, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		newdelta = tangent ^ vadelta[iter.index()];

		// Get paintable weights
		w = weightValue(data, multiIndex, iter.index());
		status = fnHiOnLoCurve.getPointAtParam(param[iter.index()] * fslider, pt, MSpace::kObject);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		points[iter.index()] = ((newdelta + pt) * w) * fenvelope;
		points[iter.index()] *=  mHiOnLoCurve;
	}
	iter.setAllPositions(points);
	return MS::kSuccess;
}


void HiOnLoCurve::getClosestPoint(MFnNurbsCurve& fnHiOnLoCurve, MPoint inPosition, MPoint& position, double& paramU)
{
	position = fnHiOnLoCurve.closestPoint(inPosition, &paramU, 0.0, MSpace::kWorld);
}
