import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { exit(1) }

// We can check via AppleScript or inspect
print("Checking AutoCAD...")
