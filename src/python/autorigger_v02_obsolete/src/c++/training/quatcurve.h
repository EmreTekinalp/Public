#ifndef _n_tentacleNode
#define _n_tentacleNode

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MQuaternion.h>

class n_tentacle : public MPxNode
{
public:
						n_tentacle();
	virtual				~n_tentacle();

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();
	virtual MStatus shouldSave(const MPlug &plug, bool &isSaving);

public:
	static	MTypeId		id;
	static MObject parameter;
    static MObject blendRot;
    static MObject interval;
    static MObject stretch;
    static MObject globalScale;
    static MObject iniLength;
    static MObject matrix;
    static MObject curve;
    static MObject outTranslate;
    static MObject outRotateX;
    static MObject outRotateY;
    static MObject outRotateZ;
    static MObject outRotate;
    static MObject tangentAxis;

private:
    bool init;
	void bipolarityCheck(MQuaternion &quat1, MQuaternion &quat2);
	void computeSlerp(const MMatrix &matrix1, const MMatrix &matrix2, const MFnNurbsCurve &curve, double parameter, double blendRot, double iniLength, double curveLength, double stretch, double globalScale, int tangentAxis, MVector &outPos, MVector &outRot);
	void removeMatrixScale(MMatrix &matrix);
    //void output(const MVector &pos, const MVector &rot, int elementId, MArrayDataHandle &outTranslateArrayHnd, MArrayDataHandle &outRotateArrayHnd);
};

#endif
