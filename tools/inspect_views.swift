import Cocoa

let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.autodesk.AutoCAD2027")
guard let app = apps.first else { print("AutoCAD not found"); exit(1) }

// Show palettes first
let script = "tell application \"System Events\" to tell process \"AutoCAD 2027\" to if exists (menu item \"Show Palettes\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1) then click menu item \"Show Palettes\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1"
NSAppleScript(source: script)?.executeAndReturnError(nil)
Thread.sleep(forTimeInterval: 0.5)

print("Palettes shown. Dumping view hierarchy...")
