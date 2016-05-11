#include "rivetNode.h"


MTypeId RivetNode::id(0x3245657);
MObject RivetNode::aInMesh;
MObject RivetNode::aInMatrix;
MObject RivetNode::aOperator;
MObject RivetNode::aComponentIndex;

MObject RivetNode::aOutTranslate;
MObject RivetNode::aOutRotateX;
MObject RivetNode::aOutRotateY;
MObject RivetNode::aOutRotateZ;
MObject RivetNode::aOutRotate;


RivetNode::RivetNode(){}
RivetNode::~RivetNode(){}

void* RivetNode::creator()
{
    return new RivetNode();
}

MStatus RivetNode::initialize()
{
    MFnEnumAttribute eAttr;
    MFnTypedAttribute tAttr;
    MFnNumericAttribute nAttr;
    MFnUnitAttribute uAttr;
    MFnMatrixAttribute mAttr;

    //inMesh
    aInMesh = tAttr.create("inMesh", "im", MFnData::kMesh);
    CHECK_MSTATUS(addAttribute(aInMesh));

    //inMatrix
    aInMatrix = mAttr.create("inMatrix", "ima");
    CHECK_MSTATUS(addAttribute(aInMatrix));
    mAttr.setHidden(true);

    //operator
    aOperator = eAttr.create("operator", "op", 0);
    eAttr.addField("vertex", 0);
    eAttr.addField("face", 1);
    eAttr.addField("edge", 2);
    eAttr.setKeyable(true);
    CHECK_MSTATUS(addAttribute(aOperator));

    //componentIndex
    aComponentIndex = nAttr.create("componentIndex", "ci", MFnNumericData::kInt, 0);
    nAttr.setKeyable(true);
    nAttr.setMin(0);
    CHECK_MSTATUS(addAttribute(aComponentIndex));

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
    attributeAffects(aInMesh, aOutTranslate);
    attributeAffects(aInMesh, aOutRotate);

    attributeAffects(aInMatrix, aOutTranslate);
    attributeAffects(aInMatrix, aOutRotate);

    attributeAffects(aOperator, aOutTranslate);
    attributeAffects(aOperator, aOutRotate);

    attributeAffects(aComponentIndex, aOutTranslate);
    attributeAffects(aComponentIndex, aOutRotate);

    MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer rivetNode weights;");

    return MS::kSuccess;
}

MStatus RivetNode::compute(const MPlug& plug, MDataBlock& data)
{
	MStatus status;
	//Check the output for dirt
	if (plug == aOutTranslate || plug == aOutRotate)
    {
		//Check the inMesh value
		MObject oInMesh = data.inputValue(aInMesh).asMesh();
		if (oInMesh.isNull())
		{
			return MS::kSuccess;
		}
		//Check the inMatrix value
		MMatrix mInMatrix = data.inputValue(aInMatrix).asMatrix();
		//Get the Operator value
		unsigned int iOperator = data.inputValue(aOperator).asInt();
		//Get the ComponentIndex value
		unsigned int iComponentIndex = data.inputValue(aComponentIndex).asInt();

		//Get DataHandles for the outputs
		MDataHandle hOutTranslate = data.outputValue(aOutTranslate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		MDataHandle hOutRotate = data.outputValue(aOutRotate, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);

		if (oInMesh.hasFn(MFn::kMesh))
		{
			MFnMesh fnInMesh(oInMesh);
				//Check the operator value: 0=Vertices, 1=Faces, 2=Edges
			if (iOperator == 0)
			{
				//Define arrays points and vectors
				MItMeshVertex itVertices(oInMesh);
				MIntArray iaAdjacentVtxIndex;
				MPoint pVertexPosition, pVertexAdjacent;
				MVector vUp, vForward;

				//Set max value for the componentIndex
				MFnNumericAttribute nAttr;
				nAttr.setObject(aComponentIndex);
				nAttr.setMax(fnInMesh.numVertices() - 1);

				//Set current index and get the adjacent vertex point
				int iPreviousVertex;
				itVertices.setIndex(iComponentIndex, iPreviousVertex);
				itVertices.getConnectedVertices(iaAdjacentVtxIndex);
				if (iaAdjacentVtxIndex.length() < 2)
				{
					return MS::kSuccess;
				}
				fnInMesh.getPoint(iaAdjacentVtxIndex[0], pVertexAdjacent, MSpace::kWorld);

				//Get the mesh points and get the normalized vertex normal
				fnInMesh.getPoint(iComponentIndex, pVertexPosition, MSpace::kWorld);
				fnInMesh.getVertexNormal(iComponentIndex, false, vUp, MSpace::kTransform);
				vUp.normalize();
				vUp *= mInMatrix;
				vForward = pVertexAdjacent - pVertexPosition;

				//Calculate the rotation axis and set outRotate
				double dRotation[3];
				calculateRotation(vUp, vForward, dRotation);
				hOutRotate.set(dRotation[0], dRotation[1], dRotation[2]);

				//Set outTranslate
				float fOutTranslate[3];
				fOutTranslate[0] = pVertexPosition.x;
				fOutTranslate[1] = pVertexPosition.y;
				fOutTranslate[2] = pVertexPosition.z;
				hOutTranslate.set(fOutTranslate[0], fOutTranslate[1], fOutTranslate[2]);

				data.setClean(plug);
			}
			else if (iOperator == 1)
			{
				//Define arrays vectors and points
				MIntArray iaVertexList;
				MPoint pVtx0, pVtx1, pVtx2, pVtx3, pMid0, pTangent1, pTangent2;
				MVector vUp, vForward;

				//Set max value for the componentIndex
				MFnNumericAttribute nAttr;
				nAttr.setObject(aComponentIndex);
				nAttr.setMax(fnInMesh.numPolygons() - 1);

				//Get the vertices and vertex positions of the face
				fnInMesh.getPolygonVertices(iComponentIndex, iaVertexList);
				fnInMesh.getPoint(iaVertexList[0], pVtx0, MSpace::kWorld);
				fnInMesh.getPoint(iaVertexList[1], pVtx1, MSpace::kWorld);
				fnInMesh.getPoint(iaVertexList[2], pVtx2, MSpace::kWorld);
				if (iaVertexList.length() > 3)
				{
					//Get the mid positions and calculate the tangents
					fnInMesh.getPoint(iaVertexList[3], pVtx3, MSpace::kWorld);
					pMid0 = (pVtx0 + pVtx1 + pVtx2 + pVtx3) / iaVertexList.length();
					pTangent1 = (pVtx1 + pVtx2) / 2;
					pTangent2 = (pVtx3 + pVtx0) / 2;
				}
				else
				{
					//Get the mid positions and calculate the tangents
					pMid0 = (pVtx0 + pVtx1 + pVtx2) / iaVertexList.length();
					pTangent1 = pVtx0;
					pTangent2 = (pVtx1 + pVtx2) / 2;
				}

				//Get polygonNormal and Tangent
				fnInMesh.getPolygonNormal(iComponentIndex, vUp, MSpace::kTransform);
				vUp.normalize();
				vUp *= mInMatrix;

				//Get the forward vector/ tangent vector
				vForward = pTangent2 - pTangent1;
				vForward.normalize();

				//Calculate the rotation axis and set outRotate
				double dRotation[3];
				calculateRotation(vUp, vForward, dRotation);
				hOutRotate.set(dRotation[0], dRotation[1], dRotation[2]);

				//Set outTranslate
				float fOutTranslate[3];
				fOutTranslate[0] = pMid0.x;
				fOutTranslate[1] = pMid0.y;
				fOutTranslate[2] = pMid0.z;
				hOutTranslate.set(fOutTranslate[0], fOutTranslate[1], fOutTranslate[2]);

				data.setClean(plug);
			}
			else if (iOperator == 2)
			{
				//Define arrays vectors and points
				int iVertexList[2];
				MPoint pVtx0, pVtx1, pVtx2, pVtx3, pMid0;
				MVector vNormal0, vNormal1, vUp, vForward, vTangent0, vTangent1;

				//Set max value for the componentIndex
				MFnNumericAttribute nAttr;
				nAttr.setObject(aComponentIndex);
				nAttr.setMax(fnInMesh.numEdges() - 1);

				//Set the edge and get its connected vertices
				fnInMesh.getEdgeVertices(iComponentIndex, iVertexList);
				//Get both vertex positions and normals
				fnInMesh.getPoint(iVertexList[0], pVtx0, MSpace::kWorld);
				fnInMesh.getPoint(iVertexList[1], pVtx1, MSpace::kWorld);
				pMid0 = (pVtx0 + pVtx1) / 2;
				//Calculate the average of both normals
				fnInMesh.getVertexNormal(iVertexList[0], vNormal0, MSpace::kTransform);
				fnInMesh.getVertexNormal(iVertexList[1], vNormal1, MSpace::kTransform);
				vUp = (vNormal0 + vNormal1) / 2;
				vUp.normalize();
				vUp *= mInMatrix;
				//Calculate the tangent vector
				vTangent0 = pMid0 - pVtx0;
				vTangent1 = pVtx1 - pMid0;
				vForward = (vTangent0 + vTangent1) / 2;
				vForward.normalize();

				//Calculate the rotation axis and set outRotate
				double dRotation[3];
				calculateRotation(vUp, vForward, dRotation);
				hOutRotate.set(dRotation[0], dRotation[1], dRotation[2]);

				//Set outTranslate
				float fOutTranslate[3];
				fOutTranslate[0] = pMid0.x;
				fOutTranslate[1] = pMid0.y;
				fOutTranslate[2] = pMid0.z;
				hOutTranslate.set(fOutTranslate[0], fOutTranslate[1], fOutTranslate[2]);
			}
		}
    }
	return MS::kSuccess;
}

void RivetNode::calculateRotation(MVector up, MVector forward, double rotation[3])
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
