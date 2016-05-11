#include "n_tentacleNode.h"
#include <math.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MMatrix.h>
#include <maya/MVector.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MDataHandle.h>
#include <maya/MQuaternion.h>
#include <maya/MPoint.h>
#include <maya/MEulerRotation.h>
#include <maya/MAngle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MGlobal.h>


MTypeId     n_tentacle::id( 0X00113ED6 );

MObject n_tentacle::parameter;
MObject n_tentacle::blendRot;
MObject n_tentacle::interval;
MObject n_tentacle::stretch;
MObject n_tentacle::globalScale;
MObject n_tentacle::iniLength;
MObject n_tentacle::matrix;
MObject n_tentacle::curve;
MObject n_tentacle::outTranslate;
MObject n_tentacle::outRotateX;
MObject n_tentacle::outRotateY;
MObject n_tentacle::outRotateZ;
MObject n_tentacle::outRotate;
MObject n_tentacle::tangentAxis;


n_tentacle::n_tentacle()
{
	this->init = false;
}
n_tentacle::~n_tentacle() {}




//void n_tentacle::output(const MVector &pos, const MVector &rot, int elementId, MArrayDataHandle &outTranslateArrayHnd, MArrayDataHandle &outRotateArrayHnd)
//{
//	outTranslateArrayHnd.jumpToArrayElement(elementId);
//	outRotateArrayHnd.jumpToArrayElement(elementId);

//	MDataHandle outTranslateHnd = outTranslateArrayHnd.outputValue();
//	MDataHandle outRotateHnd = outRotateArrayHnd.outputValue();

//	outTranslateHnd.set3Double(pos.x, pos.y, pos.z);

//	MDataHandle outRotateXHnd = outRotateHnd.child(n_tentacle::outRotateX);
//	MDataHandle outRotateYHnd = outRotateHnd.child(n_tentacle::outRotateY);
//	MDataHandle outRotateZHnd = outRotateHnd.child(n_tentacle::outRotateZ);

//	outRotateXHnd.setMAngle(MAngle(rot.x));
//	outRotateYHnd.setMAngle(MAngle(rot.y));
//	outRotateZHnd.setMAngle(MAngle(rot.z));

//	outTranslateHnd.setClean();
//	outRotateHnd.setClean();
//}

void n_tentacle::removeMatrixScale(MMatrix &matrix)
{
	MVector axisX = MVector(matrix(0, 0), matrix(0, 1), matrix(0, 2));
	MVector axisY = MVector(matrix(1, 0), matrix(1, 1), matrix(1, 2));
	MVector axisZ = MVector(matrix(2, 0), matrix(2, 1), matrix(2, 2));

	axisX.normalize();
	axisY.normalize();
	axisZ.normalize();

	matrix[0][0] = axisX.x;
	matrix[0][1] = axisX.y;
	matrix[0][2] = axisX.z;

	matrix[1][0] = axisY.x;
	matrix[1][1] = axisY.y;
	matrix[1][2] = axisY.z;

	matrix[2][0] = axisZ.x;
	matrix[2][1] = axisZ.y;
	matrix[2][2] = axisZ.z;
}

void* n_tentacle::creator()
{
	return new n_tentacle();
}

MStatus n_tentacle::shouldSave(const MPlug &plug, bool &isSaving)
{
	isSaving = true;
	return MStatus::kSuccess;
}

void n_tentacle::bipolarityCheck(MQuaternion &quat1, MQuaternion &quat2)
{
	// the quaternion's imaginary part can describe two rotations at the same time,
	// we make sure we always orient the two quaternions to the same direction

	double dot = (quat1.w * quat2.w) + (quat1.x * quat2.x) + (quat1.y * quat2.y) + (quat1.z * quat2.z);

	if(dot < 0.0)
	{
		quat1.negateIt();
	}
}

void n_tentacle::computeSlerp(const MMatrix &matrix1, const MMatrix &matrix2, const MFnNurbsCurve &curve, double parameter, double blendRot, double iniLength, double curveLength, double stretch, double globalScale, int tangentAxis, MVector &outPos, MVector &outRot)
{
	//curveLength = curve.length()
        double lenRatio = iniLength / curveLength;

        MQuaternion quat1;
        quat1 = matrix1;

        MQuaternion quat2;
        quat2 = matrix2;

        this->bipolarityCheck(quat1, quat2);

    //need to adjust the parameter in order to maintain the length between elements, also for the stretch
		MVector tangent;
		MPoint pointAtParam;
		MPoint finaPos;
        double p = lenRatio * parameter * globalScale;
        double finalParam = p + (parameter - p) * stretch;
		
		if(curveLength * finalParam > curveLength)
		{
		  double lengthDiff = curveLength - (iniLength * parameter);

		  double param = curve.knot(curve.numKnots() - 1);
		  tangent = curve.tangent(param, MSpace::kWorld);
		  tangent.normalize();

		  curve.getPointAtParam(param, pointAtParam, MSpace::kWorld);
		  finaPos = pointAtParam;
		  pointAtParam += (- tangent) * lengthDiff;
		  //MGlobal::displayInfo("sdf");
		}
		else
		{
		  double param = curve.findParamFromLength(curveLength * finalParam);
		  tangent = curve.tangent(param, MSpace::kWorld);
		  tangent.normalize();
		  curve.getPointAtParam(param, pointAtParam, MSpace::kWorld);
		  
		}
                

        MQuaternion slerpQuat = slerp(quat1, quat2, blendRot);
        MMatrix slerpMatrix = slerpQuat.asMatrix();

        int axisId = abs(tangentAxis) - 1;
		MVector slerpMatrixYAxis = MVector(slerpMatrix(axisId, 0), slerpMatrix(axisId, 1), slerpMatrix(axisId, 2));
		slerpMatrixYAxis.normalize();
		if(tangentAxis < 0)
			slerpMatrixYAxis = - slerpMatrixYAxis;

		double angle = tangent.angle(slerpMatrixYAxis);
		MVector axis =  slerpMatrixYAxis ^ tangent;
		axis.normalize();

		MQuaternion rotationToSnapOnCurve(angle, axis);

		MQuaternion finalQuat = slerpQuat * rotationToSnapOnCurve;
		MEulerRotation finalEuler = finalQuat.asEulerRotation();

		outRot.x = finalEuler.x;
		outRot.y = finalEuler.y;
		outRot.z = finalEuler.z;
		outPos = pointAtParam;
}

MStatus n_tentacle::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus returnStatus;

	//make sure we have the curve
	MObject curveObj = data.inputValue(curve).asNurbsCurve();

	if(!curveObj.isNull())
	{
		//get the data
		MArrayDataHandle inMatrixArrayHnd = data.inputArrayValue(matrix);

		int tangentAxisI = data.inputValue(tangentAxis).asInt();
		if(tangentAxisI > 2)
			tangentAxisI = - (tangentAxisI - 2);
		else
			tangentAxisI = tangentAxisI + 1;

		double stretchF = data.inputValue(stretch).asDouble();
		double globalScaleF = data.inputValue(globalScale).asDouble();
		double iniLengthF = data.inputValue(iniLength).asDouble();

		const MFnNurbsCurve curve(curveObj);
		MArrayDataHandle parameterArrayHnd = data.inputArrayValue(parameter);
		MArrayDataHandle blendRotArrayHnd = data.inputArrayValue(blendRot);
		MArrayDataHandle intervalArrayHnd = data.inputArrayValue(interval);
		MArrayDataHandle outTranslateArrayHnd = data.outputArrayValue(outTranslate);
		MArrayDataHandle outRotateArrayHnd = data.outputArrayValue(outRotate);

		int parameterNrPlugs = parameterArrayHnd.elementCount();
		int blendRotNrPlugs = blendRotArrayHnd.elementCount();
		int outTranslateNrPlugs = outTranslateArrayHnd.elementCount();
		int outRotateNrPlugs = outRotateArrayHnd.elementCount();

		//get the current curve length
        double currCurveLen = curve.length();

        if(this->init == false)
        {
        	if(outTranslateNrPlugs == parameterNrPlugs && outRotateNrPlugs == parameterNrPlugs && parameterNrPlugs == blendRotNrPlugs)
        	{
        		this->init = true;
        	}
        }

		if( plug == outTranslate || plug == outRotate || plug == outRotateX || plug == outRotateY || plug == outRotateZ)
		{
			if(this->init)
			{
                MArrayDataBuilder tbuilder(outTranslate, parameterNrPlugs);
                MArrayDataBuilder rbuilder(outRotate, parameterNrPlugs);

				for(int i = 0; i < parameterNrPlugs; i++)
				{
					intervalArrayHnd.jumpToArrayElement(i);
					int intervalI = intervalArrayHnd.inputValue().asInt();

					inMatrixArrayHnd.jumpToArrayElement(intervalI);
					MMatrix matrix1 = inMatrixArrayHnd.inputValue().asMatrix();
					this->removeMatrixScale(matrix1);

					inMatrixArrayHnd.jumpToArrayElement(intervalI + 1);
					MMatrix matrix2 = inMatrixArrayHnd.inputValue().asMatrix();
					this->removeMatrixScale(matrix2);

					parameterArrayHnd.jumpToArrayElement(i);
					double parameterF = parameterArrayHnd.inputValue().asDouble();

					blendRotArrayHnd.jumpToArrayElement(i);
					double blendRotF = blendRotArrayHnd.inputValue().asDouble();

					MVector outPos, outRot;

					this->computeSlerp(matrix1, matrix2, curve, parameterF, blendRotF, iniLengthF, currCurveLen, stretchF, globalScaleF, tangentAxisI, outPos, outRot);

                    MDataHandle outTranslateHnd = tbuilder.addElement(i);
                    outTranslateHnd.set3Double(outPos.x, outPos.y, outPos.z);

                    MDataHandle outRotateHnd = rbuilder.addElement(i);
                    double rotation[3];
                    outRotateHnd.set( outRot.x, outRot.y, outRot.z );

                    //this->output(outPos, outRot, i, outTranslateArrayHnd, outRotateArrayHnd);

				}

                outTranslateArrayHnd.set(tbuilder);
                outTranslateArrayHnd.setAllClean();

                outRotateArrayHnd.set(rbuilder);
                outRotateArrayHnd.setAllClean();
			}
            data.setClean(plug);

		}
		else
		{
			return MS::kUnknownParameter;
		}
	}

	return MS::kSuccess;
}

MStatus n_tentacle::initialize()
{

	MFnNumericAttribute numericAttr;
	MFnMatrixAttribute matrixAttr;
	MFnTypedAttribute typedAttr;
	MFnUnitAttribute unitAttribute;
	MFnEnumAttribute enumAttr;
	MStatus				stat;


	stretch = numericAttr.create("stretch", "st", MFnNumericData::kDouble, 0.0);
	numericAttr.setMin(0.0);
	numericAttr.setMax(1.0);

	globalScale = numericAttr.create("globalScale", "gs", MFnNumericData::kDouble, 1.0);
	numericAttr.setMin(0.00001);
	numericAttr.setMax(10.0);

	iniLength = numericAttr.create("iniLength", "iln", MFnNumericData::kDouble, 0.01);

	parameter = numericAttr.create("parameter", "prm", MFnNumericData::kDouble, 0.0);
	numericAttr.setArray(true);

	blendRot = numericAttr.create("blendRot", "blr", MFnNumericData::kDouble, 0.0);
	numericAttr.setArray(true);

	interval = numericAttr.create("interval", "itv", MFnNumericData::kInt, 0);
	numericAttr.setArray(true);

	matrix = matrixAttr.create("matrix", "mtx");
	matrixAttr.setArray(true);
	matrixAttr.setHidden(true);

	curve = typedAttr.create("curve", "crv", MFnData::kNurbsCurve);

	outTranslate = numericAttr.create("outTranslate", "ot", MFnNumericData::k3Double);
	numericAttr.setArray(true);
	numericAttr.setHidden(true);
    numericAttr.setUsesArrayDataBuilder(true);
    numericAttr.setHidden(true);

	outRotateX = unitAttribute.create("outRotateX", "orx", MFnUnitAttribute::kAngle);
	outRotateY = unitAttribute.create("outRotateY", "ory", MFnUnitAttribute::kAngle);
	outRotateZ = unitAttribute.create("outRotateZ", "orz", MFnUnitAttribute::kAngle);
	outRotate = numericAttr.create("outRotate", "or",outRotateX, outRotateY, outRotateZ);
	numericAttr.setArray(true);
	numericAttr.setHidden(true);
    numericAttr.setUsesArrayDataBuilder(true);
    numericAttr.setHidden(true);

	tangentAxis = enumAttr.create("tangentAxis", "tga", 1);
	enumAttr.addField("X", 0);
	enumAttr.addField("Y", 1);
	enumAttr.addField("Z", 2);
	enumAttr.addField("negativeX", 3);
	enumAttr.addField("negativeY", 4);
	enumAttr.addField("negativeZ", 5);


	// Add the attributes we have created to the node
	//
	stat = addAttribute( parameter );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( blendRot );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( interval );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( stretch );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( globalScale );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( iniLength );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( matrix );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( curve );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outTranslate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( outRotate );
		if (!stat) { stat.perror("addAttribute"); return stat;}
	stat = addAttribute( tangentAxis );
		if (!stat) { stat.perror("addAttribute"); return stat;}

	attributeAffects( parameter, outTranslate );
	attributeAffects( blendRot, outTranslate );
	attributeAffects( interval, outTranslate );
	attributeAffects( stretch, outTranslate );
	attributeAffects( globalScale, outTranslate );
	attributeAffects( iniLength, outTranslate );
	attributeAffects( matrix, outTranslate );
	attributeAffects( curve, outTranslate );
	attributeAffects( tangentAxis, outTranslate );

	attributeAffects( parameter, outRotate );
	attributeAffects( blendRot, outRotate );
	attributeAffects( interval, outRotate );
	attributeAffects( stretch, outRotate );
	attributeAffects( globalScale, outRotate );
	attributeAffects( iniLength, outRotate );
	attributeAffects( matrix, outRotate );
	attributeAffects( curve, outRotate );
	attributeAffects( tangentAxis, outRotate );

	attributeAffects( parameter, outRotateX );
	attributeAffects( blendRot, outRotateX );
	attributeAffects( interval, outRotateX );
	attributeAffects( stretch, outRotateX );
	attributeAffects( globalScale, outRotateX );
	attributeAffects( iniLength, outRotateX );
	attributeAffects( matrix, outRotateX );
	attributeAffects( curve, outRotateX );
	attributeAffects( tangentAxis, outRotateX );

	attributeAffects( parameter, outRotateY );
	attributeAffects( blendRot, outRotateY );
	attributeAffects( interval, outRotateY );
	attributeAffects( stretch, outRotateY );
	attributeAffects( globalScale, outRotateY );
	attributeAffects( iniLength, outRotateY );
	attributeAffects( matrix, outRotateY );
	attributeAffects( curve, outRotateY );
	attributeAffects( tangentAxis, outRotateY );

	attributeAffects( parameter, outRotateZ );
	attributeAffects( blendRot, outRotateZ );
	attributeAffects( interval, outRotateZ );
	attributeAffects( stretch, outRotateZ );
	attributeAffects( globalScale, outRotateZ );
	attributeAffects( iniLength, outRotateZ );
	attributeAffects( matrix, outRotateZ );
	attributeAffects( curve, outRotateZ );
	attributeAffects( tangentAxis, outRotateZ );


	return MS::kSuccess;

}

