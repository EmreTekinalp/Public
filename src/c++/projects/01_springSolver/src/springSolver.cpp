#include "springSolver.h"

MTypeId SpringSolver::id(0x123767);
MObject SpringSolver::envelope;
MObject SpringSolver::inputMatrix;
MObject SpringSolver::damp;
MObject SpringSolver::stiffness;
MObject SpringSolver::mass;
MObject SpringSolver::gravity;
MObject SpringSolver::friction;
MObject SpringSolver::time;

MObject SpringSolver::outTranslateX;
MObject SpringSolver::outTranslateY;
MObject SpringSolver::outTranslateZ;
MObject SpringSolver::outTranslate;
MObject SpringSolver::outRotationX;
MObject SpringSolver::outRotationY;
MObject SpringSolver::outRotationZ;
MObject SpringSolver::outRotation;


SpringSolver::SpringSolver()
{
    f_normal = 1.0;
    f_length = 10;
    q_angle.x = M_PI / 4;
    q_angle.y = M_PI / 4;

    v_initPosition = MVector(0, 0, 0);
    v_currentPosition = MVector(0, 0, 0);
    v_velocity = MVector(0, 0, 0);
    v_force = MVector(0, 0, 0);
    v_acceleration = MVector(0, 0, 0);
    v_gravity = MVector(0, 0, 0);

    /*
    q_initRotation = MQuaternion(0.0, 0.0, 0.0, 1.0);
    q_currentRotation = MQuaternion(0.0, 0.0, 0.0, 1.0);
    q_velocityRotation = MQuaternion(0.0, 0.0, 0.0, 1.0);
    q_forceRotation = MQuaternion(0.0, 0.0, 0.0, 1.0);

    v_velocityRotation = MVector(0.0, 0.0, 0.0);
    v_forceRotation = MVector(0.0, 0.0, 0.0);
    v_accelerationRotation = MVector(0.0, 0.0, 0.0);

    v_initRotation = MVector(0.0, 0.0, 0.0);
    v_currentRotation = MVector(0.0, 0.0, 0.0);
    */
}


SpringSolver::~SpringSolver()
{
}


MStatus SpringSolver::compute(const MPlug& plug, MDataBlock& data)
{
    MStatus status;

    MTransformationMatrix tm_transformation;
    tm_transformation = data.inputValue(inputMatrix, &status).asMatrix();
    CHECK_MSTATUS_AND_RETURN_IT(status);
    v_initPosition = tm_transformation.getTranslation(MSpace::kWorld, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);

    /* get rotation
    double d_rot[3];
    MTransformationMatrix::RotationOrder rotOrder;
    rotOrder = MTransformationMatrix::kXYZ;
    tm_transformation.getRotation(d_rot, rotOrder, MSpace::kWorld);
    v_initRotation = MVector(d_rot);

    tm_transformation.getRotationQuaternion(q_initRotation.x, q_initRotation.y, q_initRotation.z, q_initRotation.w);
    */

    if (plug == outTranslate || plug == outTranslateX ||
        plug == outTranslateY || plug == outTranslateZ ||
        plug == outRotation || plug == outRotationX ||
        plug == outRotationY || plug == outRotationZ)
    {
        // tm_transformation.getRotationQuaternion(q_currentRotation.x, q_currentRotation.y, q_currentRotation.z, q_currentRotation.w);
        // retrieve input attribute values
        f_env = data.inputValue(envelope).asFloat();
        f_damp = data.inputValue(damp).asFloat();
        f_stiffness = data.inputValue(stiffness).asFloat();
        f_mass = data.inputValue(mass).asFloat();
        f_gravity = data.inputValue(gravity).asFloat();
        f_friction = data.inputValue(friction).asFloat();
        t_time = data.inputValue(time).asTime();

        // spring algorithm based on following formula:
        // force = -kx, where k is stiffness and x the delta vector of current and init position
        // acceleration = force / m, where m is the mass
        // velocity = damp * (velocity + acceleration)
        // friction = unit_vec(velocity) * -1.0 * friction_coefficient * normal
        v_force = ((-1 * f_stiffness) * (v_currentPosition - v_initPosition));
        v_force.y += -1 * f_gravity;
        v_acceleration = v_force / f_mass;
        v_velocity = f_damp * (v_velocity + v_acceleration);
        v_velocity += v_velocity.normal() * -1.0 * f_friction * f_normal;
        v_currentPosition += v_velocity;
        v_currentPosition *= f_env;

        // set outTranslation
        MDataHandle h_outTranslation = data.outputValue(outTranslate);
        h_outTranslation.child(outTranslateX).set(static_cast<float>(v_currentPosition.x));
        h_outTranslation.child(outTranslateY).set(static_cast<float>(v_currentPosition.y));
        h_outTranslation.child(outTranslateZ).set(static_cast<float>(v_currentPosition.z));
        /*
        // angular velocity calculation
        v_accelerationRotation.x = (-1 * f_gravity / f_length) * sin(d_angle_x);
        //v_accelerationRotation.y = (-1 * f_gravity / f_length) * sin(d_angle_y);
        v_velocityRotation.x += v_accelerationRotation.x;
        //v_velocityRotation.y += v_accelerationRotation.y;
        d_angle_x += v_accelerationRotation.x;
        //d_angle_y += v_accelerationRotation.y;
        v_velocityRotation *= f_damp;
        v_currentRotation = v_initRotation + v_velocityRotation;
        q_forceRotation = ((-1 * f_stiffness) * (q_currentRotation - q_initRotation));
        q_accelerationRotation.x = q_forceRotation.x / f_mass;
        q_accelerationRotation.y = q_forceRotation.y / f_mass;
        q_accelerationRotation.z = q_forceRotation.z / f_mass;
        q_velocityRotation = f_damp * (q_velocityRotation + q_accelerationRotation);
        q_currentRotation = q_currentRotation + q_velocityRotation;
        q_currentRotation = f_env * q_currentRotation;

        double angleInDegrees;
        MVector rotationAxis;
        q_currentRotation.getAxisAngle(rotationAxis, angleInDegrees);

        MVector angularDisplacement = rotationAxis * angleInDegrees * M_PI / 180;
        MVector angularVelocity = f_damp * (angularDisplacement / t_time.value());

        // set outRotation
        MEulerRotation euler = q_currentRotation.asEulerRotation();
        v_currentRotation += angularVelocity;
        MGlobal::displayInfo(MString() + t_time.value());
        MGlobal::displayInfo(MString() + v_currentRotation.x + " " + v_currentRotation.y + " " + v_currentRotation.z);
        MDataHandle h_outRotation = data.outputValue(outRotation);
        h_outRotation.child(outRotationX).set(static_cast<double>(v_currentRotation.x));
        h_outRotation.child(outRotationY).set(static_cast<double>(v_currentRotation.y));
        h_outRotation.child(outRotationZ).set(static_cast<double>(v_currentRotation.z));

        v_forceRotation = ((-1 * f_stiffness) * (q_currentRotation - q_initRotation));
        v_accelerationRotation.x = v_forceRotation.x / f_mass;
        v_accelerationRotation.y = v_forceRotation.y / f_mass;
        v_accelerationRotation.z = v_forceRotation.z / f_mass;
        v_velocityRotation = f_damp * (v_velocityRotation + v_accelerationRotation);
        q_currentRotation = q_currentRotation + v_velocityRotation;
        q_currentRotation = f_env * q_currentRotation;

        v_forceRotation = ((-1 * f_stiffness) * (v_currentRotation - v_initRotation));
        v_accelerationRotation.x = v_forceRotation.x / f_mass;
        v_accelerationRotation.y = v_forceRotation.y / f_mass;
        v_accelerationRotation.z = v_forceRotation.z / f_mass;
        v_currentRotation += v_accelerationRotation;
        v_omega = v_currentRotation * f_damp;
        v_currentRotation.x += pow(v_omega.x, f_time) * cos(2 * M_PI * f_time);
        v_currentRotation.y += pow(v_omega.y, f_time) * cos(2 * M_PI * f_time);
        v_currentRotation.z += pow(v_omega.z, f_time) * cos(2 * M_PI * f_time);

        // set outRotation
        MDataHandle h_outRotation = data.outputValue(outRotation);
        MGlobal::displayInfo(MString() + f_time);
        h_outRotation.child(outRotationX).set(static_cast<double>(v_currentRotation.x));
        h_outRotation.child(outRotationY).set(static_cast<double>(v_currentRotation.y));
        h_outRotation.child(outRotationZ).set(static_cast<double>(v_currentRotation.z));
        data.setClean(plug);
        from maya import cmds
        import math

        damp = 1.0
        angular = math.radians(45)

        omega = angular * damp
        angular += (math.pow(omega, -i) * math.cos(2*math.pi*i))
        loc = cmds.spaceLocator()[0]
        cmds.setAttr(loc + '.rx', 45 + math.degrees(angular))
        t += 1
        print 45 + angular*/
        data.setClean(plug);
    }
    return status;
}


void * SpringSolver::creator()
{
    return new SpringSolver();
}


MStatus SpringSolver::initialize()
{
    MStatus status;
    MFnNumericAttribute nAttr;
    MFnMatrixAttribute mAttr;
    MFnUnitAttribute uAttr;

    // envelope
    envelope = nAttr.create("envelope", "env", MFnNumericData::kFloat, 1.0, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setKeyable(true);
    nAttr.setReadable(true);
    nAttr.setHidden(false);

    // inputMatrix
    inputMatrix = mAttr.create("inputMatrix", "inm", MFnMatrixAttribute::kDouble, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    mAttr.setStorable(true);
    mAttr.setKeyable(true);
    mAttr.setReadable(true);
    mAttr.setWritable(true);
    mAttr.setCached(false);

    // damp
    damp = nAttr.create("damp", "dmp", MFnNumericData::kFloat, 0.1, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setKeyable(true);
    nAttr.setReadable(true);
    nAttr.setHidden(false);

    // stiffness
    stiffness = nAttr.create("stiffness", "stf", MFnNumericData::kFloat, 0.9, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setKeyable(true);
    nAttr.setReadable(true);
    nAttr.setHidden(false);

    // mass
    mass = nAttr.create("mass", "mas", MFnNumericData::kFloat, 1.0, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setMin(0.001);
    nAttr.setKeyable(true);
    nAttr.setReadable(true);
    nAttr.setHidden(false);

    // gravity
    gravity = nAttr.create("gravity", "gra", MFnNumericData::kFloat, 9.8, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setKeyable(true);
    nAttr.setReadable(true);
    nAttr.setHidden(false);

    // friction
    friction = nAttr.create("friction", "fri", MFnNumericData::kFloat, 0.1, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setKeyable(true);
    nAttr.setReadable(true);
    nAttr.setHidden(false);

    // time
    time = uAttr.create("time", "tim", MFnUnitAttribute::kTime, 0.0, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    uAttr.setKeyable(true);
    uAttr.setReadable(true);

    // outTranslateX
    outTranslateX = nAttr.create("outTranslateX", "otx", MFnNumericData::kFloat, 0.0, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setKeyable(false);
    nAttr.setReadable(true);

    // outTranslateY
    outTranslateY = nAttr.create("outTranslateY", "oty", MFnNumericData::kFloat, 0.0, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setKeyable(false);
    nAttr.setReadable(true);

    // outTranslateZ
    outTranslateZ = nAttr.create("outTranslateZ", "otz", MFnNumericData::kFloat, 0.0, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setKeyable(false);
    nAttr.setReadable(true);

    // outTranslate
    outTranslate = nAttr.create("outTranslate", "ot", outTranslateX, outTranslateY, outTranslateZ, &status);
    CHECK_MSTATUS_AND_RETURN_IT(status);
    nAttr.setKeyable(false);
    nAttr.setReadable(true);

//    // outRotationX
//    outRotationX = uAttr.create("outRotationX", "orx", MFnUnitAttribute::kAngle, 0.0, &status);
//    CHECK_MSTATUS_AND_RETURN_IT(status);
//    uAttr.setKeyable(false);
//    uAttr.setReadable(true);
//
//    // outRotationY
//    outRotationY = uAttr.create("outRotationY", "ory", MFnUnitAttribute::kAngle, 0.0, &status);
//    CHECK_MSTATUS_AND_RETURN_IT(status);
//    uAttr.setKeyable(false);
//    uAttr.setReadable(true);
//
//    // outRotationZ
//    outRotationZ = uAttr.create("outRotationZ", "orz", MFnUnitAttribute::kAngle, 0.0, &status);
//    CHECK_MSTATUS_AND_RETURN_IT(status);
//    uAttr.setKeyable(false);
//    uAttr.setReadable(true);
//
//    // outRotation
//    outRotation = nAttr.create("outRotation", "or", outRotationX, outRotationY, outRotationZ, &status);
//    CHECK_MSTATUS_AND_RETURN_IT(status);
//    nAttr.setKeyable(false);
//    nAttr.setReadable(true);

    // add attributes
    CHECK_MSTATUS(addAttribute(envelope));
    CHECK_MSTATUS(addAttribute(inputMatrix));
    CHECK_MSTATUS(addAttribute(damp));
    CHECK_MSTATUS(addAttribute(stiffness));
    CHECK_MSTATUS(addAttribute(mass));
    CHECK_MSTATUS(addAttribute(gravity));
    CHECK_MSTATUS(addAttribute(friction));
    CHECK_MSTATUS(addAttribute(time));
    CHECK_MSTATUS(addAttribute(outTranslate));
    // CHECK_MSTATUS(addAttribute(outRotation));

    // attribute affects
    CHECK_MSTATUS(attributeAffects(envelope, outTranslate));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outTranslate));
    CHECK_MSTATUS(attributeAffects(damp, outTranslate));
    CHECK_MSTATUS(attributeAffects(stiffness, outTranslate));
    CHECK_MSTATUS(attributeAffects(mass, outTranslate));
    CHECK_MSTATUS(attributeAffects(gravity, outTranslate));
    CHECK_MSTATUS(attributeAffects(friction, outTranslate));
    CHECK_MSTATUS(attributeAffects(time, outTranslate));

    CHECK_MSTATUS(attributeAffects(envelope, outTranslateX));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outTranslateX));
    CHECK_MSTATUS(attributeAffects(damp, outTranslateX));
    CHECK_MSTATUS(attributeAffects(stiffness, outTranslateX));
    CHECK_MSTATUS(attributeAffects(mass, outTranslateX));
    CHECK_MSTATUS(attributeAffects(gravity, outTranslateX));
    CHECK_MSTATUS(attributeAffects(friction, outTranslateX));
    CHECK_MSTATUS(attributeAffects(time, outTranslateX));

    CHECK_MSTATUS(attributeAffects(envelope, outTranslateY));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outTranslateY));
    CHECK_MSTATUS(attributeAffects(damp, outTranslateY));
    CHECK_MSTATUS(attributeAffects(stiffness, outTranslateY));
    CHECK_MSTATUS(attributeAffects(mass, outTranslateY));
    CHECK_MSTATUS(attributeAffects(gravity, outTranslateY));
    CHECK_MSTATUS(attributeAffects(friction, outTranslateY));
    CHECK_MSTATUS(attributeAffects(time, outTranslateY));

    CHECK_MSTATUS(attributeAffects(envelope, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(damp, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(stiffness, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(mass, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(gravity, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(friction, outTranslateZ));
    CHECK_MSTATUS(attributeAffects(time, outTranslateZ));

    /*
    CHECK_MSTATUS(attributeAffects(envelope, outRotation));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outRotation));
    CHECK_MSTATUS(attributeAffects(damp, outRotation));
    CHECK_MSTATUS(attributeAffects(stiffness, outRotation));
    CHECK_MSTATUS(attributeAffects(mass, outRotation));
    CHECK_MSTATUS(attributeAffects(gravity, outRotation));
    CHECK_MSTATUS(attributeAffects(friction, outRotation));
    CHECK_MSTATUS(attributeAffects(time, outRotation));

    CHECK_MSTATUS(attributeAffects(envelope, outRotationX));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outRotationX));
    CHECK_MSTATUS(attributeAffects(damp, outRotationX));
    CHECK_MSTATUS(attributeAffects(stiffness, outRotationX));
    CHECK_MSTATUS(attributeAffects(mass, outRotationX));
    CHECK_MSTATUS(attributeAffects(gravity, outRotationX));
    CHECK_MSTATUS(attributeAffects(friction, outRotationX));
    CHECK_MSTATUS(attributeAffects(time, outRotationX));

    CHECK_MSTATUS(attributeAffects(envelope, outRotationY));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outRotationY));
    CHECK_MSTATUS(attributeAffects(damp, outRotationY));
    CHECK_MSTATUS(attributeAffects(stiffness, outRotationY));
    CHECK_MSTATUS(attributeAffects(mass, outRotationY));
    CHECK_MSTATUS(attributeAffects(gravity, outRotationY));
    CHECK_MSTATUS(attributeAffects(friction, outRotationY));
    CHECK_MSTATUS(attributeAffects(time, outRotationY));

    CHECK_MSTATUS(attributeAffects(envelope, outRotationZ));
    CHECK_MSTATUS(attributeAffects(inputMatrix, outRotationZ));
    CHECK_MSTATUS(attributeAffects(damp, outRotationZ));
    CHECK_MSTATUS(attributeAffects(stiffness, outRotationZ));
    CHECK_MSTATUS(attributeAffects(mass, outRotationZ));
    */

    return status;
}