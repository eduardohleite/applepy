from rubicon.objc import (
    ObjCClass, ObjCProtocol, ObjCInstance, NSObject, objc_method, objc_classmethod
)
from rubicon.objc.runtime import load_library, SEL, objc_id
from rubicon.objc.types import NSRect, NSPoint, NSSize
from enum import Enum


load_library('AppKit')
load_library('Cocoa')


NSApplication = ObjCClass('NSApplication')
NSWindow = ObjCClass('NSWindow')
NSNotification = ObjCClass('NSNotification')
NSMenu = ObjCClass('NSMenu')
NSMenuItem = ObjCClass('NSMenuItem')
NSStackView = ObjCClass('NSStackView')
NSView = ObjCClass('NSView')
NSTextField = ObjCClass('NSTextField')
NSButton = ObjCClass('NSButton')
NSColor = ObjCClass('NSColor')
NSControl = ObjCClass('NSControl')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
NSStatusBar = ObjCClass('NSStatusBar')
NSStatusItem = ObjCClass('NSStatusItem')
NSImage = ObjCClass('NSImage')
NSAlert = ObjCClass('NSAlert')
NSOpenPanel = ObjCClass('NSOpenPanel')
NSSavePanel = ObjCClass('NSSavePanel')
NSDate = ObjCClass('NSDate')
NSDateComponents = ObjCClass('NSDateComponents')
NSCalendar = ObjCClass('NSCalendar')
NSDatePicker = ObjCClass('NSDatePicker')
NSURL = ObjCClass('NSURL')
NSDatePickerCell = ObjCClass('NSDatePickerCell')
NSProgressIndicator = ObjCClass('NSProgressIndicator')

NSApp = NSApplication.sharedApplication

UTType = ObjCClass('UTType')


class NSWindowStyleMask(Enum):
    NSWindowStyleMaskBorderless = 0
    NSWindowStyleMaskTitled = 1 << 0
    NSWindowStyleMaskClosable = 1 << 1
    NSWindowStyleMaskMiniaturizable = 1 << 2
    NSWindowStyleMaskResizable = 1 << 3
    NSWindowStyleMaskUtilityWindow = 1 << 4
    NSWindowStyleMaskDocModalWindow = 1 << 6
    NSWindowStyleMaskNonactivatingPanel = 1 << 7
    NSWindowStyleMaskUnifiedTitleAndToolbar = 1 << 12
    NSWindowStyleMaskHUDWindow = 1 << 13
    NSWindowStyleMaskFullScreen = 1 << 14
    NSWindowStyleMaskFullSizeContentView = 1 << 15


class NSBackingStoreType(Enum):
    NSBackingStoreBuffered = 2


class NSUserInterfaceLayoutDirection(Enum):
    NSUserInterfaceLayoutDirectionLeftToRight = 0
    NSUserInterfaceLayoutDirectionRightToLeft = 1


class NSUserInterfaceLayoutOrientation(Enum):
    NSUserInterfaceLayoutOrientationHorizontal = 0
    NSUserInterfaceLayoutOrientationVertical = 1


class NSStackViewGravity(Enum):
    NSStackViewGravityTop = 1
    NSStackViewGravityLeading = 1
    NSStackViewGravityCenter = 2
    NSStackViewGravityBottom = 3
    NSStackViewGravityTrailing = 3


class NSDatePickerElementFlags(Enum):
    NSDatePickerElementFlagEra = 0x0100
    NSDatePickerElementFlagHourMinute = 0x000c
    NSDatePickerElementFlagHourMinuteSecond = 0x000e
    NSDatePickerElementFlagTimeZone = 0x0010
    NSDatePickerElementFlagYearMonth = 0x00c0
    NSDatePickerElementFlagYearMonthDay = 0x00e0
