#ifndef _LOCATOR_H
#define _LOCATOR_H

//-
// ==========================================================================
// Copyright 1995,2006,2008 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+

//
// Description:
//  A simple locator node that demonstrates the transparency flag on
//  locator nodes. Transparent objects must be drawn in a special draw
//  pass by Maya because the rendered output is dependent on the draw
//  order of objects.  The isTransparent() method tells the API that
//  this locator should be placed in this special transparency queue
//  for rendering.
//
//  API programmers can see the effects of this draw operation by
//  toggling the 'transparencySort' attribute on this node.  When the
//  attribute is set to true the locator will be drawn in sorted order
//  with all transparent objects in the scene.  When it is set to
//  false it will be drawn with all opaque objects in the scene.
//
//  This also demonstrates the related drawLast() flag.  This flag allows
//  a locator to be specified as the last object to be drawn in a given
//  refresh pass.  This flag a very specialized purpose, but it can be
//  important when using the isTransparent flag in crucial situations.
//

#include <maya/MPxLocatorNode.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MColor.h>
#include <maya/M3dView.h>
#include <maya/MFnPlugin.h>
#include <maya/MFnNumericAttribute.h>



class curvedArrows : public MPxLocatorNode
{
public:
        curvedArrows();
        virtual ~curvedArrows();

        virtual void                    postConstructor();

    virtual MStatus             compute( const MPlug& plug, MDataBlock& data );

        virtual void            draw( M3dView & view, const MDagPath & path,
                                                                  M3dView::DisplayStyle style,
                                                                  M3dView::DisplayStatus status );

        virtual void                    drawEdgeLoop( M3dView &, M3dView::DisplayStatus );

        virtual bool            isBounded() const;
        virtual MBoundingBox    boundingBox() const;
        virtual bool                    isTransparent() const;
        virtual bool                    drawLast() const;

        static  void *          creator();
        static  MStatus         initialize();

        static  MObject                 aEnableTransparencySort;
        static  MObject                 aEnableDrawLast;
        static  MObject                 aTheColor;
        static  MObject                 aTransparency;

public:
        static  MTypeId         id;
        static unsigned int fsVertexListSize;
        double3 fsVertexList[];
        double3 fsNormalList[];
        typedef unsigned int uint3[3];
        uint3 fsFaceList[];
        static unsigned int fsFaceListSize;
        static unsigned int fsEdgeLoopSize;
};

#endif
