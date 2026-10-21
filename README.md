# AutoCAD for Mac — Windows Ribbon Toolbar

[![macOS](https://img.shields.io/badge/macOS-Sonoma%20%7C%20Sequoia-black?logo=apple)](https://www.apple.com/macos/)
[![AutoCAD](https://img.shields.io/badge/AutoCAD-2024%20--%202027+-red?logo=autodesk)](https://www.autodesk.com/products/autocad)
[![Architecture](https://img.shields.io/badge/Architecture-Universal%20(arm64%20+%20x86__64)-blue)](#system-and-software-compatibility)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A native, high-performance plugin for **AutoCAD for Mac** that restores the standardized **Windows-style horizontal Ribbon** across the top of the drawing canvas.

Designed for architects, mechanical engineers, and CAD professionals transitioning from Windows to macOS who require muscle-memory consistency, top-docked toolsets, and full-width canvas workspace optimization.

---

## Interface Preview

![AutoCAD Windows Ribbon on macOS](docs/images/preview.png)

*Windows Ribbon operating natively inside AutoCAD on macOS with dynamic theme synchronization and automatic canvas resizing.*

---

## Core Features

- **Standardized Windows Layout**: Toolsets organized horizontally across the top perimeter into standardized panels (Draw, Modify, Annotation, Layers, Block, Properties, Utilities, Clipboard).
- **Comprehensive 7-Tab Navigation**:
  - **Home**: Draw (Line, Polyline, Circle, Arc, Rectangle, Ellipse, Hatch), Modify (Move, Rotate, Trim, Erase, Copy, Mirror, Fillet, Stretch, Scale, Array, Explode, Offset), Annotations, Layers, Blocks, Properties.
  - **Insert**: Block insertion, Xref external reference management, raster images, DWF/PDF underlays, point clouds.
  - **Annotate**: Multiline text, Linear/Aligned dimensions, Multileaders, Tables, markup utilities.
  - **Parametric**: Geometric constraints (Coincident, Parallel, Perpendicular, Tangent) and Dimensional constraints.
  - **View**: Real-time Pan, Zoom window/extents, UCS manager, Named views, Viewport configurations.
  - **Manage**: Purge, Audit, AppLoad, Script runner, CUI editor.
  - **Output**: Plot, Page Setup, Batch Plot, Export to PDF, eTransmit.
  - **Collaborate**: Shared Views, DWG Compare, Activity Insights.
- **Dynamic Theme Synchronization**: Samples AutoCAD’s active palette in real time, automatically adhering to dark and light interface modes.
- **Screen Boundary-Aware Menus**: Flyout submenus monitor display boundaries and automatically invert orientation to eliminate edge clipping.
- **Command-Line and Single-Click Toggling**:
  - Execute `RIBBON` or `MR` in the AutoCAD command line to engage the Windows Ribbon layout.
  - Execute `RIBBONCLOSE` or click **"Mac Toolbar"** in the top navigation strip to restore the classic vertical Mac palette.
- **Zero-Dependency Bundle Deployment**: Drop `MacRibbon.bundle` into the Autodesk ApplicationAddins directory for immediate recognition on launch.
- **Universal Binary**: Compiled natively for **Apple Silicon (arm64, M1 through M4)** and **Intel (x86_64)**.

---

## Registered AutoCAD Commands

| Command | Description |
| :--- | :--- |
| `RIBBON` | Activates the Windows Ribbon toolbar, docks palette frames, and hides the vertical Mac toolset. |
| `MR` | Shortened command alias for `RIBBON`. |
| `RIBBONCLOSE` | Restores the standard macOS floating/docked Tool Sets palette and displays the quick-switch bar. |

---

## Installation

### Method 1: ApplicationAddins Directory Deployment (Recommended)
1. Locate or download `MacRibbon.bundle` from the [Releases](../../releases) section or the `build/` directory.
2. Move `MacRibbon.bundle` into your user ApplicationAddins directory:
   ```text
   ~/Library/Application Support/Autodesk/ApplicationAddins/
   ```
   *(Create the directory if it does not yet exist).*
3. Launch AutoCAD for Mac. The plugin will initialize automatically.

### Method 2: Package Installer
Run the standalone pre-packaged binary installer:
```bash
./MacRibbon-Installer
```

### Method 3: Compilation from Source
Prerequisites: Xcode Command Line Tools.

```bash
git clone git@github.com:RonaldNedela/AutoCAD-Mac-Ribbon.git
cd AutoCAD-Mac-Ribbon
make bundle
make install
```

---

## Dual Workspace Operation

The plugin supports dynamic, non-destructive switching between macOS and Windows interface configurations without restarting AutoCAD:

```
[ Default Mac Layout ]  <=== (Type 'MR' or 'RIBBON') ===>  [ Windows Ribbon Layout ]
```

1. **Windows Ribbon Mode (`RIBBON` / `MR`)**:
   - The top Ribbon toolbar mounts immediately beneath the macOS document title bar.
   - The vertical Tool Sets side palette collapses automatically.
   - The active drawing canvas expands to the full display width.
2. **Classic Mac Tool Sets Mode (`RIBBONCLOSE`)**:
   - The top Ribbon toolbar unmounts cleanly.
   - Classic macOS floating toolsets, Properties inspector, and Layer manager restore to their previous coordinate positions.
   - A minimalist, non-intrusive "Windows Ribbon" activation button remains in the upper-right corner.

---

## Architecture and Technical Implementation

```
AutoCAD-Mac-Ribbon/
├── PackageContents.xml         # Autodesk Package Autoloader Specification
├── Info.plist                  # Bundle Metadata & Class Mapping
├── Makefile                    # Multi-target Clang Universal Compiler
└── src/
    ├── MacRibbonPlugin.m       # AutoCAD Entry Point, Extension Registration & Command Map
    ├── MRRibbonBar.m           # AppKit Top-Docked NSView, Tab Strip & Dynamic Layout
    ├── MRRibbonTheme.m         # Theme Extraction Engine (Dark / Light Dynamic Adaptation)
    ├── MRMenuEngine.m          # Screen-Edge Aware Flyout Menu & Submenu Matrix
    └── MRCanvasManager.m       # NSWindow Hierarchy Frame Resizing & Split-View Adjustment
```

### Technical Highlights
- **Direct AppKit Layer Integration**: Directly injects custom `NSView` hierarchies into AutoCAD's primary document windows rather than wrapping web views, ensuring instantaneous click-to-execute response times.
- **Command Dispatch via AutoCAD Runtime**: Button activations dispatch commands through AutoCAD's native `sendStringToExecute` / `acDocManager` pipeline.
- **Thread Safety**: UI mutations are bound to the AppKit main dispatch queue with automatic transaction coalescing.

---

## System and Software Compatibility

- **Host Software**: Autodesk AutoCAD for Mac 2024, 2025, 2026, and 2027+.
- **Operating Systems**: macOS 14 Sonoma, macOS 15 Sequoia, and newer.
- **Hardware Architecture**: Apple Silicon (arm64, M1 through M4) and Intel (x86_64).

---

## Removal and Uninstallation

To completely remove the plugin:
```bash
rm -rf ~/Library/Application\ Support/Autodesk/ApplicationAddins/MacRibbon.bundle
```
Upon the subsequent launch, AutoCAD will revert entirely to its default factory interface layout.

---

## Author

- **Developer**: Ronald Nedela ([@RonaldNedela](https://github.com/RonaldNedela))

---

## License

This project is licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for complete terms.
