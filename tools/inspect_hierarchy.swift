import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { print("AutoCAD not found"); exit(1) }

// We can read via NSWorkspace or LLDB or inspect logs
