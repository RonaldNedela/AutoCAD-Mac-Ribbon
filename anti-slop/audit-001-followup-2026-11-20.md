# Antislop Audit #001 Follow-Up Report (2026-11-20)

**Target:** `AutoCAD-Mac-Ribbon` v2.0.0 (`/Users/Ronci/Documents/AutoCAD/AutoCAD-Mac-Ribbon`)
**Approved scope:** Findings 1 through 22 (all items)
**Design Read:** Reading this as: Native CAD Desktop Ribbon Toolbar for architects, mechanical engineers, and AutoCAD for Mac power users, in an authentic Autodesk AutoCAD 2026/2027 Windows Ribbon matte technical-drafting language, dial `ENERGY 1 / RHYTHM 2 / MOTION 1`.

---

## Resolution Summary (Items 1-22)

| # | Priority | Status | Resolution & Verification |
|---|----------|--------|---------------------------|
| 1 | HIGH | FIXED | Fixed all 18 dead/unsupported commands (`_BLOCKSPALETTE` -> `'_content`, `_ADJUST` -> `_IMAGEADJUST`, `_XBI` -> `_XBIND`, `_TRACEPALETTESOPEN` -> `_TRACEPALETTEOPEN`, `_PROJECTMANAGER` -> `_SHEETSET`, replaced unsupported macOS commands with verified AutoCAD 2027 commands). Verified live via `LOGFILEON` and `(getcname)` with 0 unknown commands. |
| 2 | HIGH | FIXED | Fixed `ui/ribbon.js` lineweight combo check (`cmd.includes('_-LWEIGHT ')`). Verified live click selecting `0.25 mm` updated `#combo-lineweight .combo-label` to `0.25 mm`. |
| 3 | HIGH | FIXED | Restricted `RibbonManager.mm` `isCandidateWindow:` strictly to `AcMainWindow` (rejects `AcOCUiModalWindow`, `NSPanel`, sheets, flyouts, splash). Added `ensureRibbonVisible` to eliminate duplicate WebView reloads on `kLoadDwgMsg`. |
| 4 | HIGH | FIXED | Rebuilt Dark, Live-Sampled Dark (`#4e5868`), and Light palettes; all 25 text/background pairings verified PASS (>= 4.5:1) via `contrast-check.py` (5.20:1 to 14.61:1) and all icon strokes >= 3.17:1. |
| 5 | HIGH | FIXED | Replaced all hardcoded neon hexes with theme-adaptive CSS custom properties (`--icon-ink`, `--icon-muted`, `--icon-accent`, `--icon-node`, `--icon-danger`). Verified live in `v2_home_light.png`. |
| 6 | HIGH | FIXED | Added full `keydown` handler in `ui/ribbon.js` (`Escape` closes dropdowns/trays/context menus and restores focus; `ArrowLeft`/`ArrowRight` navigates tabs; `ArrowUp`/`ArrowDown`/`Home`/`End` navigates menus) plus `:focus-visible` outlines in `ui/style.css`. |
| 7 | HIGH | FIXED | Converted all 209 interactive controls to native `<button type="button">` (`Non-button clickables: 0`), added `aria-label` to all icon-only controls (`0` missing), added `aria-hidden="true"` to all 406 SVGs (`0` missing), removed `user-scalable=no`, and added `@media (prefers-reduced-motion: reduce)`. |
| 8 | HIGH | FIXED | Fixed SVG text sizing (`PDF`, `Dim Style`, `Count`) and added automatic horizontal overflow scroll buttons (`<` / `>`) for narrow displays. Verified visually across all 10 tabs. |
| 9 | HIGH | FIXED | Updated `README.md` (removed em dash, documented all 10 tabs and `MRSYNC`, accurate installation steps) and added `CHANGELOG.md` for v2.0.0. |
| 10 | HIGH | FIXED | Removed `scripts/bundle_html.py` regex HTML patching; `RibbonViewController.mm` loads `ui/index.html` cleanly via `loadFileURL:allowingReadAccessToURL:` linking `style.css` and `ribbon.js` directly. |
| 11 | MEDIUM | FIXED | Removed all 7 Apple Color Emojis from Layers bar, lightning emoji from `RibbonManager.mm` floating button (`Windows Ribbon` with attributed white title), star icon from Markup Assist, and generic clipart icons. |
| 12 | MEDIUM | FIXED | Authored `scripts/cad_icons.py` with 406 crisp Autodesk CAD drafting SVGs (scissors Trim, pencil eraser Erase, paintbrush Match, concentric Offset, 3D Cube Visual Styles, dropdown miniature icons, lineweight/linetype previews). |
| 13 | MEDIUM | FIXED | Restyled `Palettes`, `Mac Toolbar`, and classic-mode `Windows Ribbon` toggle to matte native AutoCAD chrome with zero glow. |
| 14 | MEDIUM | FIXED | Tightened popup shadows to restrained `--cad-shadow-popup: 0 3px 10px rgba(0,0,0,0.36)` (0.18 in Light mode). |
| 15 | LOW | FIXED | Reduced active palette to matte slate neutral + 1 Autodesk blue accent (`#2e9df7` / `#0066b8`) + restrained amber strictly for geometric vertex/lock nodes. |
| 16 | LOW | FIXED | Expanded `RibbonManager.mm` `updateThemeFromAutoCAD` to synchronize all 15 surface, border, hover, and high-contrast text tokens. |
| 17 | LOW | FIXED | Added `macribbon-export-state` (`MRSYNC`) in `ui/macribbon.lsp` + `checkAutoCADStateSync` in `RibbonManager.mm` + `window.syncAutoCADState` in `ui/ribbon.js` to sync real active drawing layers and properties with an honest empty-state notice when no drawing is open. |
| 18-22 | FEATURE | FIXED | Added 45+ verified AutoCAD for Mac 2027 commands across Home, Insert, Annotate, Parametric, 3D Tools, View, Output, Collaborate, and Express Tools, and replaced `_SETBYLAYER` with verified `_CHPROP` after live testing. |

---

## Delivery Gate Status

- **Block 1 (Hard Gate):** PASS (0 em dashes across HTML/CSS/JS/README/CHANGELOG; 0 WCAG AA failures across Dark/Live-Sampled/Light themes via `contrast-check.py`; 0 dead buttons; 0 non-button clickables; 0 missing `aria-label` or `aria-hidden`; `Escape` + arrow keyboard navigation + `:focus-visible`; `prefers-reduced-motion`; no `user-scalable=no`; no regex patching scripts; built and click-tested live in AutoCAD 2027 across all 10 tabs and both themes).
- **Block 2 (Purpose-Gate):** PASS (matte Autodesk slate palette with single CAD blue accent for active tab/handles/focus; custom technical CAD SVGs with zero emojis or generic AI icons; system macOS font matching AutoCAD chrome; tight popup-only elevation shadows; zero glassmorphism or glow).
- **Block 3 (Liveliness):** PASS (Design Read declared; `ENERGY 1 / RHYTHM 2 / MOTION 1` held consistently; primary 28px tool focal points vs stacked 15px utility clusters; structural panel dividers and spacing; single CAD blue accent; consistent technical CAD line+node icon motif).
- **Block 4 (Craftsmanship & Quality Locks):** PASS (C-1 through C-5 satisfied; R-05, R-11, R-15, R-16, R-20, R-21, R-29, R-30, R-31 verified).
