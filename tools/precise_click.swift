import Cocoa
import CoreGraphics

let args = CommandLine.arguments
if args.count < 3 {
    print("Usage: precise_click <x> <y>")
    exit(1)
}

let x = Double(args[1])!
let y = Double(args[2])!
let pt = CGPoint(x: x, y: y)

let move = CGEvent(mouseEventSource: nil, mouseType: .mouseMoved, mouseCursorPosition: pt, mouseButton: .left)
move?.post(tap: .cghidEventTap)
usleep(20000)

let down = CGEvent(mouseEventSource: nil, mouseType: .leftMouseDown, mouseCursorPosition: pt, mouseButton: .left)
down?.setIntegerValueField(.mouseEventClickState, value: 1)
down?.post(tap: .cghidEventTap)
usleep(50000)

let up = CGEvent(mouseEventSource: nil, mouseType: .leftMouseUp, mouseCursorPosition: pt, mouseButton: .left)
up?.setIntegerValueField(.mouseEventClickState, value: 1)
up?.post(tap: .cghidEventTap)
