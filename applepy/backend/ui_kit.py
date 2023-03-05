from typing import Any
from enum import Enum
from rubicon.objc import (
    ObjCClass,
    ObjCProtocol,
    ObjCInstance,
    NSObject,
    objc_method,
    objc_classmethod,
    objc_property
)
from rubicon.objc.eventloop import EventLoopPolicy, CocoaLifecycle, iOSLifecycle
from rubicon.objc.runtime import (
    Foundation,
    SEL,
    load_library,
    send_super,
    objc_id,
    objc_super
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
NSAlert = Any
NSOpenPanel = Any
NSSavePanel = Any

NSDate = ObjCClass('NSDate')
NSURL = ObjCClass('NSURL')
NSDictionary = ObjCClass('NSDictionary')

UTType = ObjCClass('UTType')

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
UITextField = ObjCClass('UITextField')
UIButton = ObjCClass('UIButton')
UIButtonConfiguration = ObjCClass('UIButtonConfiguration')
UIAlertController = ObjCClass('UIAlertController')
UIAlertAction = ObjCClass('UIAlertAction')

UIApplicationMain = uilib.UIApplicationMain
UIApplicationMain.restype = c_int
UIApplicationMain.argtypes = [c_int, c_char_p, objc_id, objc_id]

NSStringFromClass = Foundation.NSStringFromClass
NSStringFromClass.restype = objc_id
NSStringFromClass.argtypes = [objc_id]


class UIButtonType(Enum):
    UIButtonTypeCustom = 0
    UIButtonTypeSystem = 1
    UIButtonTypeDetailDisclosure = 2
    UIButtonTypeInfoLight = 3
    UIButtonTypeInfoDark = 4
    UIButtonTypeContactAdd = 5
    UIButtonTypePlain = 6
    UIButtonTypeClose = 7


class UIControlState(Enum):
    UIControlStateNormal = 0
    UIControlStateHighlighted = 1 << 0
    UIControlStateDisabled = 1 << 1
    UIControlStateSelected = 1 << 2
    UIControlStateFocused = 1 << 3
    UIControlStateApplication = 0x00FF0000
    UIControlStateReserved = 0xFF000000


class UIControlEvents(Enum):
    UIControlEventTouchDown = 1 <<  0
    UIControlEventTouchDownRepeat = 1 <<  1
    UIControlEventTouchDragInside = 1 <<  2
    UIControlEventTouchDragOutside = 1 <<  3
    UIControlEventTouchDragEnter = 1 <<  4
    UIControlEventTouchDragExit = 1 <<  5
    UIControlEventTouchUpInside = 1 <<  6
    UIControlEventTouchUpOutside = 1 <<  7
    UIControlEventTouchCancel = 1 <<  8
    UIControlEventValueChanged = 1 << 12
    UIControlEventMenuActionTriggered = 1 << 14
    UIControlEventPrimaryActionTriggered = 1 << 13
    UIControlEventEditingDidBegin = 1 << 16
    UIControlEventEditingChanged = 1 << 17
    UIControlEventEditingDidEnd = 1 << 18
    UIControlEventEditingDidEndOnExit = 1 << 19
    UIControlEventAllTouchEvents = 0x00000FFF
    UIControlEventAllEditingEvents = 0x000F0000
    UIControlEventApplicationReserved = 0x0F000000
    UIControlEventSystemReserved = 0xF0000000
    UIControlEventAllEvents = 0xFFFFFFFF


class UIAlertControllerStyle(Enum):
    UIAlertControllerStyleActionSheet = 0
    UIAlertControllerStyleAlert = 1
