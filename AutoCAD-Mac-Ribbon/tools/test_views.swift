import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { exit(1) }

// Let's use NSWorkspace or AppleScript or inspect via AXUIElement
let appElement = AXUIElementCreateApplication(app.processIdentifier)
var windowsRef: CFTypeRef?
AXUIElementCopyAttributeValue(appElement, kAXWindowsAttribute as CFString, &windowsRef)
guard let windows = windowsRef as? [AXUIElement], let win = windows.first else { exit(1) }

var childrenRef: CFTypeRef?
AXUIElementCopyAttributeValue(win, kAXChildrenAttribute as CFString, &childrenRef)
guard let children = childrenRef as? [AXUIElement] else { exit(1) }

for (i, c) in children.enumerated() {
    var roleRef: CFTypeRef?
    var sizeRef: CFTypeRef?
    var posRef: CFTypeRef?
    AXUIElementCopyAttributeValue(c, kAXRoleAttribute as CFString, &roleRef)
    AXUIElementCopyAttributeValue(c, kAXSizeAttribute as CFString, &sizeRef)
    AXUIElementCopyAttributeValue(c, kAXPositionAttribute as CFString, &posRef)
    var size = CGSize.zero
    var pos = CGPoint.zero
    if let s = sizeRef { AXValueGetValue(s as! AXValue, .cgSize, &size) }
    if let p = posRef { AXValueGetValue(p as! AXValue, .cgPoint, &pos) }
    print("Child \(i): role=\(roleRef as? String ?? "") pos=\(pos) size=\(size)")
}
