import Cocoa

let sys = AXUIElementCreateSystemWide()
var elem: AXUIElement?
let pt = CGPoint(x: 70, y: 268)
let err = AXUIElementCopyElementAtPosition(sys, Float(pt.x), Float(pt.y), &elem)

if let el = elem {
    var roleRef: CFTypeRef?
    AXUIElementCopyAttributeValue(el, kAXRoleAttribute as CFString, &roleRef)
    var titleRef: CFTypeRef?
    AXUIElementCopyAttributeValue(el, kAXTitleAttribute as CFString, &titleRef)
    print("Role: \(roleRef as? String ?? "") Title: \(titleRef as? String ?? "")")
    
    let pressErr = AXUIElementPerformAction(el, kAXPressAction as CFString)
    print("Press result: \(pressErr.rawValue)")
} else {
    print("Error code: \(err.rawValue)")
}
