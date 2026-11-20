# Changelog

All notable changes to **AutoCAD for Mac Windows Ribbon (`MacRibbon`)** are documented in this file.

## [2.0.0] - 2026-11-20

### Visual Redesign and Native Autodesk Parity
- Replaced all 236 hardcoded multi-color icons with a custom 406-SVG theme-adaptive technical CAD drafting icon set powered by CSS tokens (`--icon-ink`, `--icon-muted`, `--icon-accent`, `--icon-node`, `--icon-danger`), matching AutoCAD 2027's matte slate Inspector appearance in both Dark and Light modes.
- Removed all Apple Color Emojis from the Home Layers quick-action bar and the floating classic-mode switch button (`Windows Ribbon`), and replaced generic placeholder icons (`Trim`, `Erase`, `Match Prop`, `Offset`, `Visual Styles`, `Markup Assist`, `Options`, `Units`, `Base Point`, `Export PDF`, `Dim Style`) with recognizable CAD silhouettes.
- Added miniature technical icons to dropdown menus (`Circle`, `Arc`, `Rectangle`, `Ellipse`, `Hatch`, `Trim/Extend`, `Fillet/Chamfer`, `Array`, `Dimensions`, `Measure`, `Zoom`, `3D Views`, `Visual Styles`) and visual lineweight/linetype previews in the Properties panel.
- Styled top-right window controls (`Palettes`, `Mac Toolbar`) and popups with flat matte desktop chrome and tight elevation borders.
- Updated Dark, Live-Sampled Dark, and Light palettes so all text pairs meet WCAG AA (4.5:1+) and non-text UI graphics meet 3:1+ contrast.
- Fixed SVG text clipping (`Export PDF`, `Dim Style`, `Count`) and compacted Home tab panel layout with automatic horizontal overflow scroll buttons (`<` / `>`) for narrower displays.

### Bug Fixes and AutoCAD 2027 Command Verification
- Fixed 18 broken or unsupported commands verified live against AutoCAD for Mac 2027 (`MenuGroup.cui` and `LOGFILEON`):
  - Fixed `Blocks Palette` (`_BLOCKSPALETTE` -> `'_content`), `Image Adjust` (`_ADJUST` -> `_IMAGEADJUST`), `Xbind` (`_XBI` -> `_XBIND`), `Traces` (`_TRACEPALETTESOPEN` -> `_TRACEPALETTEOPEN`), and `Sheet Set` (`_PROJECTMANAGER` -> `_SHEETSET`).
  - Replaced unsupported macOS commands (`_LAYWALK`, `_LAYMRG`, `_LAYDEL`, `_PASTESPEC`, `_VLIDE`, `_EXPORTDWF`, `_SHAREDVIEWS`, `_DWGHISTORY`, `ARCTEXT`, `BCOUNT`, `TCASE`, `TCIRCLE`, `TCOUNT`, `TXTEXP`) with verified native AutoCAD for Mac 2027 tools (`_COUNT`, `_COUNTLIST`, `_EXPORT`, `_EXPORTLAYOUT`, `'_ACTIVITYINSIGHTSOPEN`, `_LAYULK`, `_LAYON` / `_LAYTHW` macros).
- Fixed Lineweight combo box in the Properties panel not updating its active label (`_-LWEIGHT ` prefix matching in `ui/ribbon.js`).
- Fixed `RibbonManager` detaching the Ribbon onto AutoCAD modal dialogs (`AcOCUiModalWindow`, `NSOpenPanel`, `NSPanel`) by strictly restricting attachment to `AcMainWindow`.
- Eliminated duplicate WebView reloads on every new drawing open (`kLoadDwgMsg` + `macribbon.lsp` now use `ensureRibbonVisible`).
- Expanded native AutoCAD theme synchronization in `RibbonManager.mm` to update all 15 surface, border, hover, and high-contrast text CSS tokens dynamically.
- Removed `scripts/bundle_html.py` regex HTML patching; `RibbonViewController.mm` now loads `ui/index.html` cleanly via `loadFileURL:allowingReadAccessToURL:` with direct `style.css` and `ribbon.js` links.

### New Windows AutoCAD Features Added (Verified in AutoCAD for Mac 2027)
- **Live Drawing State Sync (`MRSYNC`):** `macribbon.lsp` exports active drawing layers (`CLAYER`, layer table + ACI color swatches) and current properties (`CECOLOR`, `CELWEIGHT`, `CELTYPE`) to synchronize the Ribbon Layers and Properties dropdowns automatically.
- **Home Tab:** Added `Turn All Layers On`, `Thaw All`, `Unlock Layer` (`_LAYULK`), `Change Properties` (`_CHPROP`), `Change Space` (`_CHSPACE`), native `Break at Point` (`_BREAKATPOINT`), `Select Similar` (`_SELECTSIMILAR`), `Add Selected` (`_ADDSELECTED`), `Isolate Objects` (`_ISOLATEOBJECTS`), `Hide Objects` (`_HIDEOBJECTS`), `End Isolation` (`_UNISOLATEOBJECTS`), and `Count` (`_COUNT`).
- **Insert Tab:** Added `Attach DWG` (`_XATTACH`), `Attach PDF` (`_PDFATTACH`), `Attach Image` (`_IMAGEATTACH`), `PDF Recognize SHX Text` (`_PDFSHXTEXT`), and `Sync Attributes` (`_ATTSYNC`).
- **Annotate Tab:** Added `Continue Dimension` (`_DIMCONTINUE`), `Baseline Dimension` (`_DIMBASELINE`), `Dimension Space` (`_DIMSPACE`), `Dimension Break` (`_DIMBREAK`), `Jogged Line` (`_DIMJOGLINE`), `Geometric Tolerance` (`_TOLERANCE`), `Spell Check` (`_SPELL`), and `Remove Leader` (`_AIMLEADEREDITREMOVE`).
- **Parametric Tab:** Added `Infer Constraints` (`CONSTRAINTINFER`), `Show/Hide Geometric Constraints` (`_CONSTRAINTBAR`), `Show/Hide Dynamic Constraints` (`_DCDISPLAY`), and `Constraint Settings` (`_CONSTRAINTSETTINGS`).
- **3D Tools Tab:** Added `Wedge`, `Cone`, `Pyramid`, `Torus`, `Chamfer Edge` (`_CHAMFEREDGE`), `Solid Edit` (`_SOLIDEDIT`), `Interfere` (`_INTERFERE`), `Convert to Solid/Surface/Mesh`, `Materials`, and `Render`.
- **View, Output & Collaborate Tabs:** Added `ViewCube` (`_NAVVCUBE`), `UCS Icon` (`_UCSICON`), `Count Palette` (`_COUNTLIST`), `Materials Browser`, `Reset Palettes` (`_RESETPALETTES`), `Export...` (`_EXPORT`), `Export Layout to Model` (`_EXPORTLAYOUT`), and `Activity Insights` (`'_ACTIVITYINSIGHTSOPEN`).

### Keyboard Accessibility and Semantics
- Converted all 209 interactive controls to native `<button type="button">` elements with `aria-label`, `aria-expanded`, `aria-haspopup`, `role="tablist"` / `role="tab"` / `role="menuitem"`, and `aria-hidden="true"` across all 406 SVGs.
- Added full keyboard navigation: `Escape` closes open menus, panel trays, and context menus while restoring focus; `ArrowLeft` / `ArrowRight` navigates tabs; `ArrowUp` / `ArrowDown` / `Home` / `End` navigates open menus.
- Added high-contrast `:focus-visible` outlines, removed `user-scalable=no` from viewport meta, and added `@media (prefers-reduced-motion: reduce)` support.

---

## [1.0.0] - 2026-10-18

- Initial release of the native Universal Binary (`arm64` + `x86_64`) Windows Ribbon plugin for AutoCAD for Mac.
- Autoloader bundle (`PackageContents.xml`) with `RIBBON`, `MR`, and `RIBBONCLOSE` commands.
- Native `CCmdThroat::sendMenuStringToExecute` command dispatch and `ACPaneLayoutViewController` top spacer integration.
