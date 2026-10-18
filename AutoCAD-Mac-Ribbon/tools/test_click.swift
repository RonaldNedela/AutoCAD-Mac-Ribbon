import Cocoa
import CoreGraphics

let args = CommandLine.arguments
let x = Double(args[1])!
let y = Double(args[2])!
let pt = CGPoint(x: x, y: y)

let src = CGEventSource(stateID: .hidSystemState)
let down = CGEvent(mouseEventSource: src, mouseType: .leftMouseDown, mouseCursorPosition: pt, mouseButton: .left)
down?.setIntegerValueField(.mouseEventClickState, value: 1)
let up = CGEvent(mouseEventSource: src, mouseType: .leftMouseUp, mouseCursorPosition: pt, mouseButton: .left)
up?.setIntegerValueField(.mouseEventClickState, value: 1)

down?.post(tap: .cghidEventTap)
usleep(40000)
up?.post(tap: .cghidEventTap)
