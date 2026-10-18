import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { exit(1) }
let appElement = AXUIElementCreateApplication(app.processIdentifier)

var windowsRef: CFTypeRef?
AXUIElementCopyAttributeValue(appElement, kAXWindowsAttribute as CFString, &windowsRef)
guard let windows = windowsRef as? [AXUIElement], let win = windows.first else { exit(1) }

// Find AXSplitGroup containing Inspector
func findInspectorWidth(_ elem: AXUIElement) -> CGFloat {
    var childrenRef: CFTypeRef?
    AXUIElementCopyAttributeValue(elem, kAXChildrenAttribute as CFString, &childrenRef)
    guard let children = childrenRef as? [AXUIElement] else { return 0 }
    
    for c in children {
        var titleRef: CFTypeRef?
        AXUIElementCopyAttributeValue(c, kAXTitleAttribute as CFString, &titleRef)
        let title = titleRef as? String ?? ""
        if title.contains("Layers and Properties") || title.contains("Reference Manager") {
            // Found inspector child! Return size of parent or this element
            var sizeRef: CFTypeRef?
            AXUIElementCopyAttributeValue(elem, kAXSizeAttribute as CFString, &sizeRef)
            var size = CGSize.zero
            if let s = sizeRef { AXValueGetValue(s as! AXValue, .cgSize, &size) }
            return size.width
        }
        let w = findInspectorWidth(c)
        if w > 0 { return w }
    }
    return 0
}

let w = findInspectorWidth(win)
print("Inspector width via AX: \(w)")
