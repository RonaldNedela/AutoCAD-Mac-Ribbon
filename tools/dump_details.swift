import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { print("AutoCAD not found"); exit(1) }

let appElement = AXUIElementCreateApplication(app.processIdentifier)
var windowsRef: CFTypeRef?
AXUIElementCopyAttributeValue(appElement, kAXWindowsAttribute as CFString, &windowsRef)
guard let windows = windowsRef as? [AXUIElement] else { exit(1) }

func printElem(_ elem: AXUIElement, indent: String) {
    var roleRef: CFTypeRef?
    var titleRef: CFTypeRef?
    var posRef: CFTypeRef?
    var sizeRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXRoleAttribute as CFString, &roleRef)
    AXUIElementCopyAttributeValue(elem, kAXTitleAttribute as CFString, &titleRef)
    AXUIElementCopyAttributeValue(elem, kAXPositionAttribute as CFString, &posRef)
    AXUIElementCopyAttributeValue(elem, kAXSizeAttribute as CFString, &sizeRef)
    
    let role = roleRef as? String ?? ""
    let title = titleRef as? String ?? ""
    var pos = CGPoint.zero
    if let p = posRef { AXValueGetValue(p as! AXValue, .cgPoint, &pos) }
    var size = CGSize.zero
    if let s = sizeRef { AXValueGetValue(s as! AXValue, .cgSize, &size) }
    
    print("\(indent)[\(role)] '\(title)' pos=\(pos) size=\(size)")
    
    var childrenRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXChildrenAttribute as CFString, &childrenRef)
    if let children = childrenRef as? [AXUIElement] {
        for c in children {
            printElem(c, indent: indent + "  ")
        }
    }
}

for win in windows {
    printElem(win, indent: "")
}
