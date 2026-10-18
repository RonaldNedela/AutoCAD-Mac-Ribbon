import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { print("AutoCAD not found"); exit(1) }
let appElement = AXUIElementCreateApplication(app.processIdentifier)

var windowsRef: CFTypeRef?
AXUIElementCopyAttributeValue(appElement, kAXWindowsAttribute as CFString, &windowsRef)
guard let windows = windowsRef as? [AXUIElement] else { print("No windows"); exit(1) }

func dumpUI(_ elem: AXUIElement, depth: Int) {
    if depth > 4 { return }
    var roleRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXRoleAttribute as CFString, &roleRef)
    var titleRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXTitleAttribute as CFString, &titleRef)
    var posRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXPositionAttribute as CFString, &posRef)
    var sizeRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXSizeAttribute as CFString, &sizeRef)
    
    let role = roleRef as? String ?? ""
    let t = titleRef as? String ?? ""
    var pos = CGPoint.zero
    if let p = posRef { AXValueGetValue(p as! AXValue, .cgPoint, &pos) }
    var size = CGSize.zero
    if let s = sizeRef { AXValueGetValue(s as! AXValue, .cgSize, &size) }
    
    if (role.contains("Button") || role.contains("Tab") || role.contains("Radio") || role.contains("Group")) && size.width > 0 && pos.y < 200 {
        print(String(repeating: "  ", count: depth) + "[\(role)] '\(t)' pos=(\(pos.x), \(pos.y)) size=(\(size.width), \(size.height))")
    }
    
    var childrenRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXChildrenAttribute as CFString, &childrenRef)
    if let children = childrenRef as? [AXUIElement] {
        for child in children {
            dumpUI(child, depth: depth + 1)
        }
    }
}

for win in windows {
    dumpUI(win, depth: 1)
}
