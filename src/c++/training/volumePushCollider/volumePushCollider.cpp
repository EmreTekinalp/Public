#include "volumePushCollider.h"

MTypeId VolumePushCollider::id(0x3426678);
MObject VolumePushCollider::aInCollider;
MObject VolumePushCollider::aInVolume;
MObject VolumePushCollider::aOutput;


VolumePushCollider::VolumePushCollider(){}
VolumePushCollider::~VolumePushCollider(){}

void* VolumePushCollider::creator()
{
    return new VolumePushCollider();
}

MStatus VolumePushCollider::initialize()
{
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;

    // inCollider
    aInCollider = mAttr.create("inCollider", "col");
    mAttr.setArray(true);
    CHECK_MSTATUS(addAttribute(aInCollider));

    // inVolume
    aInVolume = mAttr.create("inVolume", "vol");
    mAttr.setArray(true);
    CHECK_MSTATUS(addAttribute(aInVolume));

    // output
    aOutput = nAttr.create("output", "out", MFnNumericData::kDouble, 0.0);
    nAttr.setArray(true);
    nAttr.setReadable(true);
    nAttr.setWritable(true);
    nAttr.setHidden(true);
    CHECK_MSTATUS(addAttribute(aOutput));

    attributeAffects(aInCollider, aOutput);
    attributeAffects(aInVolume, aOutput);

    return MS::kSuccess;
}


MStatus VolumePushCollider::compute(const MPlug& plug, MDataBlock& dataBlock)
{
	MStatus status;

	if (plug == aOutput)
	{
		// inCollider
		MArrayDataHandle hInCollider = dataBlock.inputArrayValue(aInCollider);
		// inVolume
		MArrayDataHandle hInVolume = dataBlock.inputArrayValue(aInVolume);
		// output
		MArrayDataHandle hOutput = dataBlock.inputArrayValue(aOutput);
		MDoubleArray daValues(hInVolume.elementCount());

		for (unsigned int c=0; c<hInCollider.elementCount(); c++)
		{
			// Calculate the total of every collider value for each volume
			status = hInCollider.jumpToArrayElement(c);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			MMatrix mInCollider = hInCollider.inputValue().asMatrix();
			MTransformationMatrix tmInCollider(mInCollider);
			MPoint pInCollider = tmInCollider.getTranslation(MSpace::kWorld, &status);
			CHECK_MSTATUS_AND_RETURN_IT(status);

			for (unsigned int v=0; v<hInVolume.elementCount(); v++)
			{
				// pointMatrixMult
				status = hInVolume.jumpToArrayElement(v);
				CHECK_MSTATUS_AND_RETURN_IT(status);
				MMatrix mInVolume = hInVolume.inputValue().asMatrix();
				MVector vVolCollider = pInCollider * mInVolume;
				// condition
				if (vVolCollider.length() <= 1.0)
				{
					// reverse
					daValues[v] += abs(1.0 - vVolCollider.length());
				}
			}
		}
		for (unsigned int i=0; i<hInVolume.elementCount(); i++)
		{
			// set outputs
			status = hOutput.jumpToArrayElement(i);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			hOutput.outputValue().set(daValues[i]);
		}
		dataBlock.setClean(plug);
	}
	return MS::kSuccess;
}

