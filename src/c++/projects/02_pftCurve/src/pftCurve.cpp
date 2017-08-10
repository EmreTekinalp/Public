#include "pftCurve.h"

MTypeId PftCurve::id(0x987321);
MObject PftCurve::upMatrix;
MObject PftCurve::outTranslate;
MObject PftCurve::outRotateX;
MObject PftCurve::outRotateY;
MObject PftCurve::outRotateZ;
MObject PftCurve::outRotate;

PftCurve::PftCurve()
{
}

PftCurve::~PftCurve()
{
}

MStatus PftCurve::deform(MDataBlock& data, MItGeometry& iterator,
                         const MMatrix& matrix, unsigned int multiIndex)
{
    MStatus status;
    // get the inputGeom, note we are using outputArrayValue and outputValue
    // because the compute method gets us already the inputGeom data and calls
    // the deform method. If we would use inputValue we would let maya recalculate
    // the node and propagate it as dirty.
    MArrayDataHandle hInput = data.outputArrayValue(input, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status)
    status = hInput.jumpToElement(multiIndex);
    CHECK_MSTATUS_AND_RETURN_IT(status)
    MObject oInputGeom = hInput.outputValue().child(inputGeom).asNurbsCurve();
    if (!oInputGeom.hasFn(MFn::kNurbsCurve))
    {
        MGlobal::displayWarning("Invalid geometry, please select a nurbsCurve!");
        return MS::kUnknownParameter;
    }
    MFnNurbsCurve fnInputCurve(oInputGeom);
    double dLength = fnInputCurve.length();
    unsigned int uiNumCvs = fnInputCurve.numCVs();
    unsigned int uiNumSpans = fnInputCurve.numSpans();

    // get worldMatrix of geometry
    MTransformationMatrix tmInputGeom(matrix);
    MVector vTranslation = tmInputGeom.getTranslation(MSpace::kWorld, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    MGlobal::displayInfo(MString() + dLength + ", " + uiNumCvs);

    // get the envelope
    float fEnvelope = data.outputValue(envelope).asFloat();

    // set initial up vector
    MVector vInitUp(0, 1, 0);

    MArrayDataHandle hOutTranslate = data.outputArrayValue(outTranslate, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    MArrayDataHandle hOutRotate = data.outputArrayValue(outRotate, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    for (unsigned int i = 0; i < uiNumSpans; i++)
    {
        double dParam = fnInputCurve.findParamFromLength((dLength * i) / uiNumCvs);
        MVector vTangent = fnInputCurve.tangent(dParam, MSpace::kWorld, &status);
        CHECK_MSTATUS_AND_RETURN_IT(status);
        MVector vNormal = pftAlgorithm(vInitUp, vTangent);
        vInitUp = vNormal;

        // set outTranslation
        MPoint pPosition;
        fnInputCurve.getPointAtParam(dParam, pPosition, MSpace::kTransform);
        pPosition *= matrix;

        hOutTranslate.jumpToArrayElement(i);
        hOutTranslate.outputValue().set(static_cast<float>(pPosition.x),
                                        static_cast<float>(pPosition.y),
                                        static_cast<float>(pPosition.z));

        // Calculate the rotation required to align the y-axis with the up
        // vector
        //
        MTransformationMatrix firstRot;
        MVector rotAxis = MVector::yAxis ^ vNormal;
        rotAxis.normalize();
        firstRot.setToRotationAxis(rotAxis, MVector::yAxis.angle(vNormal));

        // Calculate the second rotation required to align the forward vector
        //
        MTransformationMatrix secondRot;
        MVector transformedForward = firstRot.asMatrix() * vTangent;
        transformedForward.normalize();
        double angle = transformedForward.angle(MVector::zAxis);
        if (transformedForward.x < 0.0) {
            // Compensate for the fact that the angle method returns
            // the absolute value
            //
            angle *= -1.0;
        }
        secondRot.setToRotationAxis(vNormal, angle);
        MTransformationMatrix result = firstRot.asMatrix() * secondRot.asMatrix();
        MTransformationMatrix::RotationOrder rotOrder;
        rotOrder = MTransformationMatrix::kXYZ;
        result.reorderRotation(rotOrder);

        double rotation[3];
        result.getRotation(rotation, rotOrder, MSpace::kTransform);
        MDataHandle outputRot = data.outputValue(outRotate);
        outputRot.set(rotation[0], rotation[1], rotation[2]);
        outputRot.setClean();
    }
    return status;
}

MVector PftCurve::pftAlgorithm(MVector up, MVector tangent)
{
    // reorient normals based on parallelFrameTransportation algorithm.
    MVector orthogonal = tangent ^ up;
    MVector orthonormal = orthogonal ^ tangent;
    return orthonormal;
}

void * PftCurve::creator()
{
    return new PftCurve();
}

MStatus PftCurve::initialize()
{
    MStatus status;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;
    MFnUnitAttribute uAttr;

    // inputMatrix
    upMatrix = mAttr.create("upMatrix", "upm", MFnMatrixAttribute::kDouble, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    mAttr.setStorable(true);
    mAttr.setKeyable(false);
    mAttr.setReadable(true);
    mAttr.setWritable(true);
    mAttr.setCached(false);

    //outTranslate
    outTranslate = nAttr.createPoint("outTranslate", "ot");
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setHidden(true);
    nAttr.setArray(true);
    CHECK_MSTATUS(addAttribute(outTranslate));

    // Set up rotate outputs
    outRotateX = uAttr.create("outRotateX", "orx", MFnUnitAttribute::kAngle, 0.0);
    nAttr.setWritable(false);
    uAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(outRotateX));

    outRotateY = uAttr.create("outRotateY", "ory", MFnUnitAttribute::kAngle, 0.0);
    nAttr.setWritable(false);
    uAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(outRotateY));

    outRotateZ = uAttr.create("outRotateZ", "orz", MFnUnitAttribute::kAngle, 0.0);
    nAttr.setWritable(false);
    uAttr.setStorable(false);
    uAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(outRotateZ));

    outRotate = nAttr.create("outRotate", "or", outRotateX, outRotateY, outRotateZ);
    nAttr.setWritable(false);
    nAttr.setStorable(false);
    nAttr.setHidden(true);
    nAttr.setArray(true);
    CHECK_MSTATUS(addAttribute(outRotate));

    // add attribute
    CHECK_MSTATUS(addAttribute(upMatrix));
    CHECK_MSTATUS(addAttribute(outTranslate));
    CHECK_MSTATUS(addAttribute(outRotate));

    // attribute affects
    CHECK_MSTATUS(attributeAffects(upMatrix, outputGeom));
    CHECK_MSTATUS(attributeAffects(upMatrix, outTranslate));
    CHECK_MSTATUS(attributeAffects(upMatrix, outRotateX));
    CHECK_MSTATUS(attributeAffects(upMatrix, outRotateY));
    CHECK_MSTATUS(attributeAffects(upMatrix, outRotateZ));
    CHECK_MSTATUS(attributeAffects(upMatrix, outRotate));
    return status;
}