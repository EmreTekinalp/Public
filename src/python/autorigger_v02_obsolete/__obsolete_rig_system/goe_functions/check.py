'''
@author:  etekinalp
@date:    Aug 31, 2014
@mail:    e.tekinalp@icloud.com
@brief:   This module contains checking methods
'''

import inspect


def error(obj=None, errMsg=0, target=None, addMsg=None):
    """
    @type  obj:         classObject
    @param obj:         specify the class name, in this case: obj = self

    @type  errMsg:      integer
    @param errMsg:      specify the number of the errorMessage.
                        msg = 0:
                            "Specified object does not exist!"
                        msg = 1:
                            "Specified object is not valid!"
                        msg = 2:
                            "Please specify a string!"
                        msg = 3:
                            "Please specify a list!"
                        msg = 4:
                            "Please specify a dictionary!"
                        msg = 5:
                            "Please specify an integer!"
                        msg = 6:
                            "Please specify a float!"
                        msg = 7:
                            "Please specify a double!"
                        msg = 8:
                            "Please specify a vector!"
                        msg = 9:
                            "Please specify a matrix!"
                        msg = 10:
                            "Please specify a plugin!"
                        msg = 11:
                            "Type of object is not a string!"
                        msg = 12:
                            "Type of object is not a list!"
                        msg = 13:
                            "Type of object is not an unicode!"
                        msg = 14:
                            "Type of object is not a dictionary!"
                        msg = 15:
                            "Specified object is not a mesh!"
                        msg = 16:
                            "Specified object is not a nurbsMesh!"
                        msg = 17:
                            "Specified object is not a nurbsCurve!"
                        msg = 18:
                            "Failed to load plugin!"
                        msg = 19:
                            "Failed to unload plugin!"
                        msg = 20:
                            "Specified object exists already in the scene!"
                        msg = 21:
                            "Specified index is out of range!"
                        msg = 22:
                            "Specified path does not exist!"
                        msg = 23:
                            "Specified attribute has no value!"

    @type  target:      string/list/dictionary/number
    @param target:      specify the target object which causes the error

    @type  addMsg:      srting
    @param addMsg:      add an additional message to show up in the error.
    """

    msg = None
    if not errMsg:
        msg = "Specified object does not exist!"
    elif errMsg == 1:
        msg = "Specified object is not valid!"
    elif errMsg == 2:
        msg = "Please specify a string!"
    elif errMsg == 3:
        msg = "Please specify a list!"
    elif errMsg == 4:
        msg = "Please specify a dictionary!"
    elif errMsg == 5:
        msg = "Please specify an integer!"
    elif errMsg == 6:
        msg = "Please specify a float!"
    elif errMsg == 7:
        msg = "Please specify a double!"
    elif errMsg == 8:
        msg = "Please specify a vector!"
    elif errMsg == 9:
        msg = "Please specify a matrix!"
    elif errMsg == 10:
        msg = "Please specify a plugin!"
    elif errMsg == 11:
        msg = "Type of object is not a string!"
    elif errMsg == 12:
        msg = "Type of object is not a list!"
    elif errMsg == 13:
        msg = "Type of object is not an unicode!"
    elif errMsg == 14:
        msg = "Type of object is not a dictionary!"
    elif errMsg == 15:
        msg = "Specified object is not a mesh!"
    elif errMsg == 16:
        msg = "Specified object is not a nurbsMesh!"
    elif errMsg == 17:
        msg = "Specified object is not a nurbsCurve!"
    elif errMsg == 18:
        msg = "Failed to load plugin!"
    elif errMsg == 19:
        msg = "Failed to unload plugin!"
    elif errMsg == 20:
        msg = "Specified object exists already in the scene!"
    elif errMsg == 21:
        msg = "Specified index is out of range!"
    elif errMsg == 22:
        msg = "Specified path does not exist!"
    elif errMsg == 23:
        msg = "Specified attribute has no value!"
    else:
        raise Exception("check.error: index is out of range! -> " + str(errMsg))

    #--- store the class name
    cls = obj.__class__.__name__

    #--- store the method name
    func = None
    try:
        func = inspect.stack()[1][3]
    except:
        pass

    #--- check the target
    if target:
        target = " -> " + str(target)
    else:
        target = ""

    #--- check the addMsg
    if addMsg:
        addMsg = " " + addMsg
    else:
        addMsg = ""

    #--- compose the error message and return it
    composed = str(cls) + "." + str(func) + ": " + msg + addMsg + target
    return composed
#END error()
