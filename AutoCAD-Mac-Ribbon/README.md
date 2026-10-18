# AutoCAD for Mac - Windows-style Ribbon Toolbar

A native plugin for **AutoCAD for Mac** that brings back the beloved, productivity-focused **Windows-style horizontal Ribbon** across the top of the screen.

Designed specifically for architects, engineers, and drafters switching from Windows to macOS who miss their muscle memory and the standard top Ribbon interface.

---

## Features

- **Top Horizontal Ribbon**: Functions are organized across the top of the canvas, just like on Windows, instead of the narrow left-hand vertical column.
- **Classic Tab Navigation**:
  - **Home**: Draw, Modify, Annotation, Layers, Block, Properties, Utilities, Clipboard.
  - **Insert**: Blocks, Xrefs, Images, PDFs, Imports.
  - **Annotate**: Text Styles, Dimension Styles, Multileader Styles, Tables.
  - **Parametric**: Constraints and parameters.
  - **View**: Zoom, Pan, Regen, Named Views, UCS.
  - **Manage**: Purge, Audit, AppLoad, Script Runner, CUI.
  - **Output**: Plot, Export PDF, Batch Plot, eTransmit.
- **Layer Quick Control**: Current layer indicator, layer manager quick launch, Off, Freeze, Lock, Isolate, Unisolate, and Match Properties.
- **Universal Binary**: Compiled natively for both **Apple Silicon (arm64)** and **Intel (x86_64)**.
- **Multi-Version Support**: Compatible with **AutoCAD for Mac 2024 (R24.3), 2025 (R25.0), 2026 (R25.1), and 2027 (R26.0)**.
- **Zero ABI Lock-in**: Uses dynamic command dispatch (`acedPostCommand`) and Cocoa/AppKit view integration, making it resilient to Autodesk internal C++ SDK changes.
- **Minimize & Collapse**: Double-click any tab or click the minimize button to cycle between full ribbon (115px) and tabs-only mode (26px).

---

## Directory Structure

```
AutoCAD-Mac-Ribbon/
├── src/
│   ├── main.mm                 # Plugin entry point (_acrxEntryPoint + constructor)
│   ├── CommandExecutor.h/.mm   # Dual-engine command execution (acedPostCommand + AppleScript)
│   ├── RibbonViewController.h/.mm # WebKit-based Ribbon view controller
│   └── RibbonManager.h/.mm     # Window detection, attachment and lifecycle manager
├── ui/
│   ├── index.html              # Ribbon layout with SVG icons
│   ├── style.css               # AutoCAD dark theme styling
│   └── ribbon.js               # Tab switching, minimize toggle, command dispatch
├── PackageContents.xml         # Autodesk Autoloader package manifest
├── Info.plist                  # macOS bundle metadata
└── Makefile                    # Universal binary compiler and deploy script
```

---

## Building and Installation

### Prerequisites
- macOS Sonoma, Sequoia or newer.
- Xcode or Command Line Tools (`clang++`).

### Quick Build & Install
Run in terminal:

```bash
cd /Users/Ronci/Desktop/AutoCAD-Mac-Ribbon
make install
```

This will:
1. Compile the Universal Binary for both `arm64` (Apple Silicon) and `x86_64` (Intel).
2. Ad-hoc sign the bundle and dylib.
3. Deploy the package into:
   `~/Library/Application Support/Autodesk/ApplicationPlugins/MacRibbon.bundle`

### Launching AutoCAD
Simply start AutoCAD for Mac (2024, 2025, 2026, or 2027). The plugin will automatically be detected and loaded upon startup.

### Uninstalling
```bash
make uninstall
```
