import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { print("AutoCAD not found"); exit(1) }
let appElement = AXUIElementCreateApplication(app.processIdentifier)

var menuBarRef: CFTypeRef?
AXUIElementCopyAttributeValue(appElement, kAXMenuBarAttribute as CFString, &menuBarRef)
guard let menuBar = menuBarRef as! AXUIElement? else { print("No menubar"); exit(1) }

var menuItemsRef: CFTypeRef?
AXUIElementCopyAttributeValue(menuBar, kAXChildrenAttribute as CFString, &menuItemsRef)
guard let menuItems = menuItemsRef as? [AXUIElement] else { print("No items"); exit(1) }

for item in menuItems {
    var titleRef: CFTypeRef?
    AXUIElementCopyAttributeValue(item, kAXTitleAttribute as CFString, &titleRef)
    let title = titleRef as? String ?? ""
    if title == "Window" {
        print("Found Window menu:")
        var subMenuRef: CFTypeRef?
        AXUIElementCopyAttributeValue(item, kAXChildrenAttribute as CFString, &subMenuRef)
        if let subMenus = subMenuRef as? [AXUIElement] {
            for sm in subMenus {
                var smChildrenRef: CFTypeRef?
                AXUIElementCopyAttributeValue(sm, kAXChildrenAttribute as CFString, &smChildrenRef)
                if let smChildren = smChildrenRef as? [AXUIElement] {
                    for child in smChildren {
                        var cTitleRef: CFTypeRef?
                        AXUIElementCopyAttributeValue(child, kAXTitleAttribute as CFString, &cTitleRef)
                        var enabledRef: CFTypeRef?
                        AXUIElementCopyAttributeValue(child, kAXEnabledAttribute as CFString, &enabledRef)
                        print("  '\(cTitleRef as? String ?? "")' (enabled=\(enabledRef as? Bool ?? false))")
                    }
                }
            }
        }
    }
}
