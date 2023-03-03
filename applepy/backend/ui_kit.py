from rubicon.objc import (
    ObjCClass, ObjCProtocol, ObjCInstance, NSObject, objc_method, objc_classmethod
)
from rubicon.objc.runtime import load_library, Foundation, objc_id
from ctypes import c_int, c_char_p, POINTER

uilib = load_library('UIKit')


UIApplication = ObjCClass('UIApplication')
UITabBarController = ObjCClass('UITabBarController ')
UIPageViewController = ObjCClass('UIPageViewController')

UIApplicationMain = uilib.UIApplicationMain
UIApplicationMain.restype = c_int
UIApplicationMain.argtypes = [c_int, c_char_p, objc_id, objc_id]

NSStringFromClass = Foundation.NSStringFromClass
NSStringFromClass.restype = objc_id
NSStringFromClass.argtypes = [objc_id]
