from typing import Any
from rubicon.objc import (
    ObjCClass,
    ObjCProtocol,
    ObjCInstance,
    NSObject,
    objc_method,
    objc_classmethod,
    objc_property
)
from rubicon.objc.runtime import (
    Foundation,
    SEL,
    load_library,
    objc_id
)
from ctypes import c_int, c_char_p

uilib = load_library('UIKit')

NSMenuItem = Any
NSButton = Any
NSView = Any
NSImage = Any
NSStackView = Any
NSTextField = Any
NSColor = Any

NSDate = ObjCClass('NSDate')
NSURL = ObjCClass('NSURL')

UIApplication = ObjCClass('UIApplication')
UIWindow = ObjCClass('UIWindow')
UIScreen = ObjCClass('UIScreen')
UIView = ObjCClass('UIView')
UIViewController = ObjCClass('UIViewController')
UITabBarController = ObjCClass('UITabBarController')
UIPageViewController = ObjCClass('UIPageViewController')
UIStackView = ObjCClass('UIStackView')
UILabel = ObjCClass('UILabel')
UIColor = ObjCClass('UIColor')

UIApplicationMain = uilib.UIApplicationMain
UIApplicationMain.restype = c_int
UIApplicationMain.argtypes = [c_int, c_char_p, objc_id, objc_id]

NSStringFromClass = Foundation.NSStringFromClass
NSStringFromClass.restype = objc_id
NSStringFromClass.argtypes = [objc_id]
