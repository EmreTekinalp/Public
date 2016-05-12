'''
@author:  etekinalp
@date:    Sep 18, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module generates code
'''

import os
import time


def base_build_code(file_path, data_path):
    objpath = 'goe_builds.' + data_path.replace("/", ".").split('PandorasBox.goe_builds.')[1]

    header = ("'''\n@author:  " + os.getenv("USER") +
              "\n@date:    " + time.strftime("%c") +
              "\n@mail:    ENTER YOUR EMAIL ADRESS HERE"
              "\n@brief:   add additional code inside this module"
              "\n'''")

    imports = ("\n\nfrom " + str(objpath) + " import obj"
               "\nfrom goe_functions import tools\n")

    reloads = "\nreload(obj)"

    parents = ("\n\n\ndef parent_and_child():"
               "\n    #--- this method setups the parents and children"
               "\n    pass"
               "\n#END parent_and_child()")

    constraints = ("\n\n\ndef mesh_constraints():"
                   "\n    #--- this method setups the mesh constraints"
                   "\n    pass"
                   "\n#END mesh_constraints()\n")

    limits = ("\n\ndef limit_transforms():"
              "\n    #--- this method limits the transforms"
              "\n    pass"
              "\n#END limit_transforms()\n")

    locknhide = ("\n\ndef lock_and_hide():"
                 "\n    #--- this method locks and hides attributes"
                 "\n    pass"
                 "\n#END lock_and_hide()\n")

    build = ("\n\ndef build():"
             "\n    '''this method should be used to call all the other methods'''"
             "\n    #--- parents and children"
             "\n    parent_and_child()"
             "\n\n    #--- mesh constraints"
             "\n    mesh_constraints()"
             "\n\n    #--- limit transforms"
             "\n    limit_transforms()"
             "\n\n    #--- lock and hide"
             "\n    lock_and_hide()"
             "\n#END build()"
             "\n\nbuild()\n")

    #--- create file
    with open(file_path, "w") as f:
        f.seek(0)
        f.write(header)
        f.write(imports)
        f.write(reloads)
        f.write(parents)
        f.write(constraints)
        f.write(limits)
        f.write(locknhide)
        f.write(build)
#END base_build_code()


def obj_builder(filepath=None, data=None):
    header = ("'''\n@author:  " + os.getenv("USER") +
              "\n@date:    " + time.strftime("%c") +
              "\n@mail:    e.tekinalp@icloud.com"
              "\n'''")
    imports = ("\n\nfrom goe_functions import data")
    reloads = "\nreload(data)\n"

    #--- create file
    with open(filepath, "w") as f:
        f.seek(0)
        f.write(header)
        f.write(imports)
        f.write(reloads)
    for d in data.items():
        obj_class_builder(d, filepath)
#END base_build_code()


def obj_class_builder(data=None, filepath=None):
    top = ("\n\nclass " + str(data[0]) + "(object):"
           "\n    def __init__(self):")
    with open(filepath, "a") as f:
        f.write(top)

    for num, i in enumerate(data[1][0]):
        jnt = data[1][1]
        if data[1][1]:
            jnt = "'" + str(data[1][1][num]) + "'"
        else:
            jnt = str(data[1][1])
        gmb = i.gimbal
        if i.gimbal:
            gmb = "'" + str(i.gimbal) + "'"
        else:
            gmb = str(i.gimbal)
        ctl = i.transform.split('_')[1]
        mid = ("\n        self." + str(ctl) + " = data.InfoPropCmds(grp='" + str(i.group) +
               "', trn='" + str(i.transform) + "', shp='" + str(i.shape) +
               "', gmb=" + str(gmb) + ", off=" + str(i.offsets) +
               ", jnt=" + str(jnt) + ")")
        with open(filepath, "a") as f:
            f.write(mid)
    end = ("\n    #END __init__()"
           "\n#END " + str(data[0]) + "()\n")
    with open(filepath, "a") as f:
        f.write(end)
#END obj_class_builder()
