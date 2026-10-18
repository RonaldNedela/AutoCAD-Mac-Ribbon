import Cocoa
import CoreGraphics

let options = CGWindowListOption(arrayLiteral: .excludeDesktopElements, .optionOnScreenOnly)
guard let windowListInfo = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
    exit(1)
}

for info in windowListInfo {
    let owner = info[kCGWindowOwnerName as String] as? String ?? ""
    let name = info[kCGWindowName as String] as? String ?? ""
    let wid = info[kCGWindowNumber as String] as? Int ?? 0
    if owner.contains("AutoCAD") && name.contains("Drawing") {
        print("\(wid)")
        exit(0)
    }
}
exit(1)
