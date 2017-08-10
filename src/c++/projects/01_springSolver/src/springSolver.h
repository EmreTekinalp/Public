#pragma once
#define _USE_MATH_DEFINES
// Converts degrees to radians.
#define degreesToRadians(angleDegrees) (angleDegrees * M_PI / 180.0)

// Converts radians to degrees.
#define radiansToDegrees(angleRadians) (angleRadians * 180.0 / M_PI)

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MVector.h>
#include <maya/MQuaternion.h>
#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MEulerRotation.h>
#include <maya/MTime.h>
#include <iostream>
#include <math.h>

using std::cerr;
using std::cout;
using std::endl;

class SpringSolver : public MPxNode
{
public:
    SpringSolver();
    virtual ~SpringSolver();

    virtual MStatus compute(const MPlug& plug, MDataBlock& data);
    static void* creator();
    static MStatus initialize();

    static MTypeId id;

    // input parameters
    static MObject envelope;
    static MObject inputMatrix;
    static MObject damp;
    static MObject stiffness;
    static MObject mass;
    static MObject gravity;
    static MObject friction;
    static MObject time;

    // output parameters
    static MObject outTranslateX;
    static MObject outTranslateY;
    static MObject outTranslateZ;
    static MObject outTranslate;
    static MObject outRotationX;
    static MObject outRotationY;
    static MObject outRotationZ;
    static MObject outRotation;
private:
    float f_env;
    float f_damp;
    float f_stiffness;
    float f_mass;
    float f_gravity;
    float f_friction;
    float f_normal;
    float f_time;
    float f_length;
    double d_angle_x;
    double d_angle_y;
    MTime t_time;

    MVector v_initPosition;
    MVector v_currentPosition;
    MVector v_velocity;
    MVector v_force;
    MVector v_acceleration;
    MVector v_gravity;
    MVector v_friction;

    MQuaternion q_initRotation;
    MQuaternion q_currentRotation;
    MQuaternion q_velocityRotation;
    MQuaternion q_forceRotation;

    MVector v_velocityRotation;
    MVector v_forceRotation;
    MVector v_accelerationRotation;
    MQuaternion q_accelerationRotation;
    MQuaternion q_angle;

    MVector v_initRotation;
    MVector v_currentRotation;
    MQuaternion q_omega;
};