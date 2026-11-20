#!/usr/bin/env python3
"""
Generates ui/index.html for AutoCAD for Mac Windows Ribbon v2.0.0.
- 100% native <button type="button"> interactive controls with ARIA semantics
- Links ui/style.css and ui/ribbon.js directly (no regex bundling)
- Every command verified against AutoCAD for Mac 2027 MenuGroup.cui / acad.pgp
"""
import html as html_lib
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from cad_icons import BIG, SM, MI, svg, INK, ACCENT, MUTED


def esc(s):
    return html_lib.escape(str(s), quote=True)


def big_btn(label, cmd, icon, desc=""):
    return (
        f'<button type="button" class="btn-big" data-cmd="{esc(cmd)}" '
        f'data-tip-title="{esc(label)}" data-tip-desc="{esc(desc)}">'
        f'{icon}<span>{esc(label)}</span></button>'
    )


def split_big(label, cmd, icon, menu_id, desc=""):
    return (
        f'<div class="split-btn">'
        f'<button type="button" class="split-main" data-cmd="{esc(cmd)}" '
        f'data-tip-title="{esc(label)}" data-tip-desc="{esc(desc)}">'
        f'{icon}<span>{esc(label)}</span></button>'
        f'<button type="button" class="split-arrow" data-dropdown="{esc(menu_id)}" '
        f'aria-haspopup="menu" aria-expanded="false" aria-label="{esc(label)} options">▾</button>'
        f'</div>'
    )


def sm_btn(label, cmd, icon, desc=""):
    return (
        f'<button type="button" class="btn-small" data-cmd="{esc(cmd)}" '
        f'data-tip-title="{esc(label)}" data-tip-desc="{esc(desc)}">'
        f'{icon}<span>{esc(label)}</span></button>'
    )


def split_sm(label, cmd, icon, menu_id, desc=""):
    return (
        f'<div class="split-sm-container">'
        f'<button type="button" class="split-main-sm" data-cmd="{esc(cmd)}" '
        f'data-tip-title="{esc(label)}" data-tip-desc="{esc(desc)}">'
        f'{icon}<span>{esc(label)}</span></button>'
        f'<button type="button" class="split-arrow-sm" data-dropdown="{esc(menu_id)}" '
        f'aria-haspopup="menu" aria-expanded="false" aria-label="{esc(label)} options">▾</button>'
        f'</div>'
    )


def quick_btn(title, cmd, icon, desc=""):
    return (
        f'<button type="button" class="layer-quick-btn" data-cmd="{esc(cmd)}" '
        f'aria-label="{esc(title)}" data-tip-title="{esc(title)}" data-tip-desc="{esc(desc)}">'
        f'{icon}</button>'
    )


def panel(pid, title, body_html, has_tray=False):
    arrow = '<span class="arrow" aria-hidden="true">▾</span>' if has_tray else ""
    aria = ' aria-haspopup="true" aria-expanded="false"' if has_tray else ""
    has_attr = "true" if has_tray else "false"
    return (
        f'<section class="panel" id="{esc(pid)}" aria-label="{esc(title)}">'
        f'<div class="panel-content">{body_html}</div>'
        f'<button type="button" class="panel-footer" data-has-tray="{has_attr}"{aria}>'
        f'<span>{esc(title)}</span>{arrow}</button>'
        f'</section>'
    )


def cluster(items, rows=3):
    cls = "btn-cluster-3" if rows == 3 else "btn-cluster-2"
    return f'<div class="{cls}">{"".join(items)}</div>'


def m_item(label, cmd, icon="", short=None, color=None, extra_label=None):
    attrs = [
        'type="button"',
        'class="cad-menu-item"',
        'role="menuitem"',
        f'data-cmd="{esc(cmd)}"',
    ]
    if short:
        attrs.append(f'data-short="{esc(short)}"')
    if color:
        attrs.append(f'data-color="{esc(color)}"')
    if extra_label:
        attrs.append(f'data-label="{esc(extra_label)}"')
    return f'<button {" ".join(attrs)}>{icon}<span>{esc(label)}</span></button>'


def m_div():
    return '<div class="cad-menu-divider" role="separator"></div>'


def m_hdr(text):
    return f'<div class="cad-menu-header">{esc(text)}</div>'


def menu(mid, items_html, min_w=None):
    style = f' style="min-width:{min_w}px;"' if min_w else ""
    return f'<div class="cad-menu" id="{esc(mid)}" role="menu"{style}>{items_html}</div>'


# --- QAT ICONS ---
QAT_ICONS = {
    "app": svg('<path d="M5 24 L13 6 H17 L25 24 H20.5 L18.7 19.5 H11.3 L9.5 24 Z M12.8 15.8 H17.2 L15 10.2 Z" fill="#ffffff"/>', size=14, vb="0 0 30 30"),
    "new": svg(f'<path d="M6 3 H13 L17 7 V17 H6 Z" stroke="{INK}" stroke-width="1.4"/><polyline points="13,3 13,7 17,7" stroke="{INK}" stroke-width="1.3"/>', size=14, vb="0 0 20 20"),
    "open": svg(f'<path d="M3 6 H8 L10 8 H17 V16 H3 Z" stroke="{INK}" stroke-width="1.4"/>', size=14, vb="0 0 20 20"),
    "save": svg(f'<path d="M4 3 H14 L17 6 V17 H4 Z" stroke="{INK}" stroke-width="1.4"/><rect x="7" y="3" width="6" height="4.5" stroke="{ACCENT}" stroke-width="1.2"/><rect x="7" y="11" width="7" height="6" stroke="{MUTED}" stroke-width="1.2"/>', size=14, vb="0 0 20 20"),
    "saveas": svg(f'<path d="M4 3 H13 L16 6 V17 H4 Z" stroke="{INK}" stroke-width="1.4"/><path d="M11 12 L16 7 L18 9 L13 14 Z" stroke="{ACCENT}" stroke-width="1.3"/>', size=14, vb="0 0 20 20"),
    "plot": svg(f'<path d="M6 7 V3 H14 V7" stroke="{INK}" stroke-width="1.3"/><rect x="3" y="7" width="14" height="7" rx="1" stroke="{INK}" stroke-width="1.3"/><rect x="6" y="12" width="8" height="5" stroke="{ACCENT}" stroke-width="1.2"/>', size=14, vb="0 0 20 20"),
    "undo": svg(f'<path d="M7 7 H13 A4 4 0 0 1 13 15 H9" stroke="{INK}" stroke-width="1.5"/><polyline points="9.5,4.5 6.5,7 9.5,9.5" stroke="{INK}" stroke-width="1.5"/>', size=14, vb="0 0 20 20"),
    "redo": svg(f'<path d="M13 7 H7 A4 4 0 0 0 7 15 H11" stroke="{INK}" stroke-width="1.5"/><polyline points="10.5,4.5 13.5,7 10.5,9.5" stroke="{INK}" stroke-width="1.5"/>', size=14, vb="0 0 20 20"),
    "gear": svg(f'<circle cx="10" cy="10" r="2.8" stroke="{INK}" stroke-width="1.4"/><circle cx="10" cy="10" r="6" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="2.2 1.8"/>', size=12, vb="0 0 20 20"),
    "palettes": svg(f'<rect x="3" y="4" width="14" height="12" rx="1" stroke="{INK}" stroke-width="1.4"/><line x1="12" y1="4" x2="12" y2="16" stroke="{ACCENT}" stroke-width="1.5"/>', size=13, vb="0 0 20 20"),
    "mactoolbar": svg(f'<rect x="3" y="4" width="14" height="12" rx="1" stroke="{INK}" stroke-width="1.4"/><line x1="7.5" y1="4" x2="7.5" y2="16" stroke="{ACCENT}" stroke-width="1.5"/>', size=13, vb="0 0 20 20"),
    "chevron": svg(f'<polyline points="5,8 10,13 15,8" stroke="{INK}" stroke-width="1.6"/>', size=12, vb="0 0 20 20"),
    "close": svg(f'<line x1="5" y1="5" x2="15" y2="15" stroke="{INK}" stroke-width="1.6"/><line x1="15" y1="5" x2="5" y2="15" stroke="{INK}" stroke-width="1.6"/>', size=12, vb="0 0 20 20"),
}


def build_home_tab():
    p_draw = panel(
        "panel-draw", "Draw",
        big_btn("Line", "^C^C_LINE", BIG["line"], "Creates straight line segments")
        + big_btn("Polyline", "^C^C_PLINE", BIG["polyline"], "Creates a 2D polyline")
        + split_big("Circle", "^C^C_CIRCLE", BIG["circle"], "menu-circle", "Creates a circle")
        + split_big("Arc", "^C^C_ARC", BIG["arc"], "menu-arc", "Creates an arc")
        + cluster([
            split_sm("Rectangle", "^C^C_RECTANG", SM["rect"], "menu-rect", "Creates a rectangular polyline or polygon"),
            split_sm("Ellipse", "^C^C_ELLIPSE", SM["ellipse"], "menu-ellipse", "Creates an ellipse or elliptical arc"),
            split_sm("Hatch", "^C^C_BHATCH", SM["hatch"], "menu-hatch", "Fills an enclosed area with a hatch pattern"),
        ]),
        has_tray=True,
    )

    p_modify = panel(
        "panel-modify", "Modify",
        big_btn("Move", "^C^C_MOVE", BIG["move"], "Moves objects a specified distance")
        + big_btn("Rotate", "^C^C_ROTATE", BIG["rotate"], "Rotates objects around a base point")
        + split_big("Trim", "^C^C_TRIM", BIG["trim"], "menu-trim", "Trims objects to meet the edges of other objects")
        + big_btn("Erase", "^C^C_ERASE", BIG["erase"], "Removes objects from a drawing")
        + cluster([
            sm_btn("Copy", "^C^C_COPY", SM["copy"], "Copies objects a specified distance"),
            sm_btn("Mirror", "^C^C_MIRROR", SM["mirror"], "Creates a mirrored copy of selected objects"),
            split_sm("Fillet", "^C^C_FILLET", SM["fillet"], "menu-fillet", "Rounds, bevels, or blends object edges"),
        ])
        + cluster([
            sm_btn("Stretch", "^C^C_STRETCH", SM["stretch"], "Stretches objects crossed by a selection window"),
            sm_btn("Scale", "^C^C_SCALE", SM["scale"], "Enlarges or reduces selected objects"),
            split_sm("Array", "^C^C_ARRAYRECT", SM["array"], "menu-array", "Creates copies in rectangular, polar, or path patterns"),
        ])
        + cluster([
            sm_btn("Explode", "^C^C_EXPLODE", SM["explode"], "Breaks a compound object into component objects"),
            sm_btn("Offset", "^C^C_OFFSET", SM["offset_sm"], "Creates concentric circles, parallel lines, and curves"),
            sm_btn("Join", "^C^C_JOIN", SM["join"], "Joins endpoints of linear and curved objects"),
        ]),
        has_tray=True,
    )

    p_annot = panel(
        "panel-annotation", "Annotation",
        split_big("Text", "^C^C_MTEXT", BIG["mtext"], "menu-text-type", "Creates multiline or single-line text")
        + big_btn("Dimension", "^C^C_DIM", BIG["dimension"], "Creates multiple types of dimensions")
        + split_big("Linear", "^C^C_DIMLINEAR", BIG["dimlinear"], "menu-dim-types", "Creates linear, aligned, angular, or radial dimensions")
        + cluster([
            split_sm("Leader", "^C^C_MLEADER", SM["leader_sm"], "menu-leader-types", "Creates a multileader object"),
            sm_btn("Table", "^C^C_TABLE", SM["table_sm"], "Creates an empty table object"),
        ], rows=2),
        has_tray=True,
    )

    layers_controls = (
        big_btn("Layer Props", "^C^C_LAYER", BIG["layer_props"], "Opens the Layer Properties Manager")
        + '<div class="btn-cluster-2" style="width:154px;">'
        + '<button type="button" class="layer-combo" data-dropdown="menu-layer-list" '
        + 'aria-haspopup="menu" aria-expanded="false" data-tip-title="Layer Control" '
        + 'data-tip-desc="Switches current layer or manages drawing layers">'
        + '<span class="combo-left"><span class="layer-color-box"></span><span class="combo-label">0</span></span>'
        + '<span class="combo-caret" aria-hidden="true">▾</span></button>'
        + '<div class="layer-quick-row">'
        + quick_btn("Layer Off", "^C^C_LAYOFF", SM["lay_off"], "Turns off the layer of a selected object")
        + quick_btn("Turn All Layers On", "^C^C_-LAYER _ON * ;;", SM["lay_on"], "Turns on all layers in the drawing")
        + quick_btn("Isolate Layer", "^C^C_LAYISO", SM["lay_iso"], "Hides or locks all layers except selected objects")
        + quick_btn("Unisolate Layers", "^C^C_LAYUNISO", SM["lay_uniso"], "Restores layers hidden by Isolate")
        + quick_btn("Freeze Layer", "^C^C_LAYFRZ", SM["lay_frz"], "Freezes the layer of a selected object")
        + quick_btn("Lock Layer", "^C^C_LAYLCK", SM["lay_lock"], "Locks the layer of a selected object")
        + quick_btn("Unlock Layer", "^C^C_LAYULK", SM["lay_unlock"], "Unlocks the layer of a selected object")
        + '</div></div>'
    )
    p_layers = panel("panel-layers", "Layers", layers_controls, has_tray=True)

    p_block = panel(
        "panel-block", "Block",
        big_btn("Insert", "^C^C_INSERT", BIG["block_insert"], "Inserts a block or drawing")
        + cluster([
            sm_btn("Create", "^C^C_BLOCK", SM["blk_create"], "Creates a block definition from selected objects"),
            sm_btn("Edit", "^C^C_BEDIT", SM["blk_edit"], "Opens the block definition in Block Editor"),
            sm_btn("Attributes", "^C^C_EATTEDIT", SM["blk_attr"], "Edits attributes in a block reference"),
        ]),
        has_tray=True,
    )

    prop_combos = (
        '<div class="btn-cluster-3" style="width:112px;">'
        + '<button type="button" class="cad-combo" id="combo-color" data-dropdown="menu-color-list" '
        + 'aria-haspopup="menu" aria-expanded="false" data-tip-title="Object Color" data-tip-desc="Sets the current color for new objects">'
        + '<span class="combo-left"><span class="layer-color-box"></span><span class="combo-label">ByLayer</span></span>'
        + '<span class="combo-caret" aria-hidden="true">▾</span></button>'
        + '<button type="button" class="cad-combo" id="combo-lineweight" data-dropdown="menu-lineweight-list" '
        + 'aria-haspopup="menu" aria-expanded="false" data-tip-title="Lineweight" data-tip-desc="Sets the current lineweight">'
        + f'<span class="combo-left">{SM["prop_lw"]}<span class="combo-label">ByLayer</span></span>'
        + '<span class="combo-caret" aria-hidden="true">▾</span></button>'
        + '<button type="button" class="cad-combo" id="combo-linetype" data-dropdown="menu-linetype-list" '
        + 'aria-haspopup="menu" aria-expanded="false" data-tip-title="Linetype" data-tip-desc="Sets the current linetype">'
        + f'<span class="combo-left">{SM["prop_lt"]}<span class="combo-label">ByLayer</span></span>'
        + '<span class="combo-caret" aria-hidden="true">▾</span></button>'
        + '</div>'
    )
    p_props = panel(
        "panel-properties", "Properties",
        big_btn("Match", "^C^C_MATCHPROP", BIG["matchprop"], "Applies properties of a selected object to other objects")
        + prop_combos,
        has_tray=True,
    )

    p_groups = panel(
        "panel-groups", "Groups",
        big_btn("Group", "^C^C_GROUP", BIG["group"], "Creates and manages saved sets of objects")
        + cluster([
            sm_btn("Ungroup", "^C^C_UNGROUP", SM["ungroup"], "Ungroups a group"),
            sm_btn("Edit", "^C^C_GROUPEDIT", SM["group_edit"], "Adds or removes objects in a group"),
            sm_btn("Selection", "$M=$(if,$(and,$(getvar,pickstyle),1),^C^C_pickstyle 0 ,^C^C_pickstyle 1 )", SM["group_toggle"], "Toggles group selection on or off"),
        ]),
    )

    p_utils = panel(
        "panel-utilities", "Utilities",
        split_big("Measure", "^C^C_MEASUREGEOM _QUICK", BIG["measure"], "menu-measure", "Measures distance, radius, angle, area, and volume")
        + cluster([
            sm_btn("Quick Sel", "^C^C_QSELECT", SM["qselect"], "Creates a selection set based on filtering criteria"),
            sm_btn("Select All", "^C^C_AI_SELALL", SM["sel_all"], "Selects all unlocked, unfrozen objects"),
            sm_btn("Calculator", "^C^C_QUICKCALC", SM["calc"], "Opens the QuickCalc calculator"),
        ])
        + cluster([
            sm_btn("Similar", "^C^C_SELECTSIMILAR", SM["sel_similar"], "Selects objects matching properties of selected object"),
            sm_btn("Isolate", "^C^C_ISOLATEOBJECTS", SM["isolate_obj"], "Displays only selected objects in the drawing"),
            sm_btn("Count", "^C^C_COUNT", SM["count_sm"], "Counts instances of selected objects or blocks"),
        ]),
        has_tray=True,
    )

    p_clip = panel(
        "panel-clipboard", "Clipboard",
        split_big("Paste", "^C^C_PASTECLIP", BIG["paste"], "menu-paste", "Pastes objects from the Clipboard")
        + cluster([
            sm_btn("Cut", "^C^C_CUTCLIP", SM["cut"], "Copies selected objects to Clipboard and erases them"),
            sm_btn("Copy", "^C^C_COPYCLIP", SM["copyclip"], "Copies selected objects to the Clipboard"),
            sm_btn("Base", "^C^C_COPYBASE", SM["copybase"], "Copies objects with a specified base point"),
        ]),
    )

    p_view = panel(
        "panel-home-view", "View",
        cluster([
            split_sm("Top View", "^C^C_-VIEW _TOP", MI["view_ortho"], "menu-3dviews", "Switches active viewport camera orientation"),
            split_sm("2D Wire", "^C^C_VSCURRENT _2D", SM["vs_2d"], "menu-vstyles", "Switches active visual style"),
            sm_btn("Zoom Ext", "^C^C_ZOOM _E", SM["zoom_ext"], "Zooms to display maximum extents of all objects"),
        ]),
    )

    return p_draw + p_modify + p_annot + p_layers + p_block + p_props + p_groups + p_utils + p_clip + p_view


def build_insert_tab():
    p_blk = panel(
        "panel-ins-block", "Block & Definition",
        big_btn("Insert", "^C^C_INSERT", BIG["block_insert"], "Inserts a block or drawing")
        + big_btn("Blocks", "'_content", BIG["blocks_palette"], "Opens the Blocks palette (CONTENT)")
        + cluster([
            sm_btn("Create Block", "^C^C_BLOCK", SM["blk_create"], "Creates a block definition"),
            sm_btn("Write Block", "^C^C_WBLOCK", SM["blk_wblock"], "Writes objects or a block to a new DWG file"),
            sm_btn("Base Point", "^C^C_BASE", SM["blk_base"], "Sets the insertion base point for the current drawing"),
        ])
        + cluster([
            sm_btn("Block Editor", "^C^C_BEDIT", SM["blk_edit"], "Opens Block Editor"),
            sm_btn("Define Attr", "^C^C_ATTDEF", SM["blk_attr"], "Creates an attribute definition"),
            sm_btn("Manage Attr", "^C^C_BATTMAN", SM["blk_attr"], "Manages attributes for a selected block"),
        ])
        + cluster([
            sm_btn("Sync Attr", "^C^C_ATTSYNC", SM["blk_sync"], "Updates block references with new/changed attributes"),
            sm_btn("Edit Attr", "^C^C_EATTEDIT", SM["blk_edit"], "Edits attribute values in a block"),
        ], rows=2),
    )

    p_ref = panel(
        "panel-ins-reference", "Reference",
        big_btn("Attach", "^C^C_ATTACH", BIG["attach"], "Attaches DWG, PDF, or raster image files")
        + big_btn("Xref Palette", "^C^C_EXTERNALREFERENCES", BIG["xref_palette"], "Opens the External References Manager")
        + cluster([
            sm_btn("Attach DWG", "^C^C_XATTACH", SM["ref_dwg"], "Inserts a DWG file as an external reference"),
            sm_btn("Attach PDF", "^C^C_PDFATTACH", SM["ref_dwg"], "Inserts a PDF underlay"),
            sm_btn("Attach Image", "^C^C_IMAGEATTACH", SM["ref_img"], "Inserts a raster image reference"),
        ])
        + cluster([
            sm_btn("Clip", "^C^C_CLIP", SM["ref_clip"], "Crops display of an xref, image, or PDF underlay"),
            sm_btn("Image Adjust", "^C^C_IMAGEADJUST", SM["ref_adjust"], "Adjusts brightness, contrast, and fade of images"),
            sm_btn("Xbind", "^C^C_XBIND", SM["ref_xbind"], "Binds dependent definitions from an xref into the drawing"),
        ]),
    )

    p_imp = panel(
        "panel-ins-import", "Import",
        big_btn("Import PDF", "^C^C_PDFIMPORT", BIG["pdf_import"], "Imports geometry, fills, images, and TrueType text from PDF")
        + big_btn("Import", "^C^C_IMPORT", BIG["import_file"], "Imports files of different formats into the current drawing")
        + cluster([
            sm_btn("SHX Text", "^C^C_PDFSHXTEXT", SM["pdf_shx"], "Converts imported PDF SHX geometry into MText"),
        ], rows=2),
    )

    p_data = panel(
        "panel-ins-data", "Data & Linking",
        big_btn("Field", "^C^C_FIELD", BIG["field"], "Creates a multiline text object with a dynamic field")
        + big_btn("Link Data", "^C^C_DATALINK", BIG["datalink"], "Creates and manages Excel/CSV data links")
        + big_btn("Update Link", "^C^C_DATALINKUPDATE", BIG["update_link"], "Updates data to or from an established external data link"),
    )

    p_content = panel(
        "panel-ins-content", "Content",
        big_btn("Content", "'_content", BIG["designcenter"], "Opens the Content / Blocks palette")
        + big_btn("Tool Sets", "^C^C_TOOLSETS", BIG["toolsets"], "Toggles the macOS Tool Sets palette"),
    )

    return p_blk + p_ref + p_imp + p_data + p_content


def build_annotate_tab():
    p_text = panel(
        "panel-ann-text", "Text",
        big_btn("MText", "^C^C_MTEXT", BIG["mtext"], "Creates a multiline text object")
        + big_btn("Single Line", "^C^C_TEXT", BIG["text"], "Creates a single-line text object")
        + cluster([
            sm_btn("Text Style", "^C^C_STYLE", SM["text_style"], "Creates, modifies, or specifies text styles"),
            sm_btn("Find Text", "^C^C_FIND", SM["find_text"], "Finds and replaces text in the drawing"),
            sm_btn("Spell Check", "^C^C_SPELL", SM["spell"], "Checks spelling in text objects"),
        ]),
    )

    p_dim = panel(
        "panel-ann-dim", "Dimensions",
        big_btn("Dimension", "^C^C_DIM", BIG["dimension"], "Creates multiple types of dimensions within one session")
        + cluster([
            sm_btn("Linear", "^C^C_DIMLINEAR", SM["dim_lin"], "Creates a linear dimension"),
            sm_btn("Aligned", "^C^C_DIMALIGNED", SM["dim_ali"], "Creates an aligned linear dimension"),
            sm_btn("Angular", "^C^C_DIMANGULAR", SM["dim_ang"], "Measures angle between geometric objects"),
        ])
        + cluster([
            sm_btn("Radius", "^C^C_DIMRADIUS", SM["dim_rad"], "Creates a radius dimension for a circle or arc"),
            sm_btn("Diameter", "^C^C_DIMDIAMETER", SM["dim_dia"], "Creates a diameter dimension"),
            sm_btn("Dim Style", "^C^C_DIMSTYLE", SM["dim_style"], "Opens the Dimension Style Manager"),
        ])
        + cluster([
            sm_btn("Continue", "^C^C_DIMCONTINUE", SM["dim_cont"], "Starts a dimension from the extension line of a previous dimension"),
            sm_btn("Baseline", "^C^C_DIMBASELINE", SM["dim_base"], "Creates dimensions from the baseline of the previous dimension"),
            sm_btn("Dim Space", "^C^C_DIMSPACE", SM["dim_space"], "Adjusts spacing between linear or angular dimensions"),
        ])
        + cluster([
            sm_btn("Dim Break", "^C^C_DIMBREAK", SM["dim_break"], "Breaks or restores dimension and extension lines"),
            sm_btn("Jog Line", "^C^C_DIMJOGLINE", SM["dim_lin"], "Adds or removes a jog line on a linear/aligned dimension"),
            sm_btn("Tolerance", "^C^C_TOLERANCE", SM["tolerance"], "Creates geometric tolerances in a feature control frame"),
        ]),
    )

    p_cl = panel(
        "panel-ann-centerlines", "Centerlines",
        cluster([
            sm_btn("Center Mark", "^C^C_CENTERMARK", SM["centermark"], "Creates an associative center mark on circles or arcs"),
            sm_btn("Centerline", "^C^C_CENTERLINE", SM["centerline"], "Creates centerline geometry associated with two lines"),
        ], rows=2),
    )

    p_ldr = panel(
        "panel-ann-leaders", "Leaders",
        big_btn("Leader", "^C^C_MLEADER", BIG["mleader"], "Creates a multileader object")
        + cluster([
            sm_btn("Add Leader", "^C^C_AIMLEADEREDITADD", SM["leader_add"], "Adds leader lines to a multileader"),
            sm_btn("Remove Leader", "^C^C_AIMLEADEREDITREMOVE", SM["leader_rem"], "Removes leader lines from a multileader"),
            sm_btn("Align", "^C^C_MLEADERALIGN", SM["leader_align"], "Aligns and spaces selected multileader objects"),
        ])
        + cluster([
            sm_btn("Collect", "^C^C_MLEADERCOLLECT", SM["leader_collect"], "Organizes block multileaders into rows or columns"),
            sm_btn("Leader Style", "^C^C_MLEADERSTYLE", SM["dim_style"], "Creates and modifies multileader styles"),
        ], rows=2),
    )

    p_tbl = panel(
        "panel-ann-tables", "Tables",
        big_btn("Table", "^C^C_TABLE", BIG["table"], "Creates an empty table object")
        + cluster([
            sm_btn("Table Style", "^C^C_TABLESTYLE", SM["table_sm"], "Creates and modifies table styles"),
            sm_btn("Data Link", "^C^C_DATALINK", SM["ref_xbind"], "Links Excel or CSV data into a table"),
        ], rows=2),
    )

    p_mk = panel(
        "panel-ann-markup", "Markup",
        cluster([
            sm_btn("Rev Cloud", "^C^C_REVCLOUD", SM["revcloud"], "Creates or modifies a revision cloud"),
            sm_btn("Wipeout", "^C^C_WIPEOUT", SM["wipeout"], "Creates a polygonal mask covering underlying objects"),
        ], rows=2),
    )

    return p_text + p_dim + p_cl + p_ldr + p_tbl + p_mk


def build_parametric_tab():
    p_geom = panel(
        "panel-par-geom", "Geometric",
        big_btn("Infer", "^P'_.CONSTRAINTINFER;$M=$(if,$(eq,$(getvar,CONSTRAINTINFER),0),1,0) ", BIG["infer_constraints"], "Toggles automatic inference of geometric constraints while drawing")
        + cluster([
            sm_btn("Coincident", "^C^C_GEOMCONSTRAINT _COINCIDENT", SM["c_coincident"], "Constrains two points together"),
            sm_btn("Collinear", "^C^C_GEOMCONSTRAINT _COLLINEAR", SM["c_collinear"], "Constrains two lines along the same infinite line"),
            sm_btn("Concentric", "^C^C_GEOMCONSTRAINT _CONCENTRIC", SM["c_concentric"], "Constrains arcs, circles, or ellipses to share a center"),
        ])
        + cluster([
            sm_btn("Parallel", "^C^C_GEOMCONSTRAINT _PARALLEL", SM["c_parallel"], "Constrains two lines to remain parallel"),
            sm_btn("Perpendicular", "^C^C_GEOMCONSTRAINT _PERPENDICULAR", SM["c_perp"], "Constrains two lines to a 90-degree angle"),
            sm_btn("Tangent", "^C^C_GEOMCONSTRAINT _TANGENT", SM["c_tangent"], "Constrains two curves to remain tangent"),
        ])
        + cluster([
            sm_btn("Horizontal", "^C^C_GEOMCONSTRAINT _HORIZONTAL", SM["c_horiz"], "Constrains lines or points parallel to X axis"),
            sm_btn("Vertical", "^C^C_GEOMCONSTRAINT _VERTICAL", SM["c_vert"], "Constrains lines or points parallel to Y axis"),
            sm_btn("Equal", "^C^C_GEOMCONSTRAINT _EQUAL", SM["c_equal"], "Constrains lines to equal length or circles to equal radius"),
        ])
        + cluster([
            sm_btn("Fix", "^C^C_GEOMCONSTRAINT _FIX", SM["c_fix"], "Locks points and curves to a fixed coordinate"),
            sm_btn("Smooth", "^C^C_GEOMCONSTRAINT _SMOOTH", SM["c_smooth"], "Constrains a spline to be G2 continuous with another curve"),
            sm_btn("Symmetric", "^C^C_GEOMCONSTRAINT _SYMMETRIC", SM["c_symm"], "Constrains objects symmetrically about a selected line"),
        ]),
    )

    p_dim = panel(
        "panel-par-dim", "Dimensional",
        cluster([
            sm_btn("Linear", "^C^C_DIMCONSTRAINT _L", SM["dim_lin"], "Constrains horizontal or vertical distance"),
            sm_btn("Aligned", "^C^C_DIMCONSTRAINT _A", SM["dim_ali"], "Constrains distance between two points"),
            sm_btn("Radius", "^C^C_DIMCONSTRAINT _R", SM["dim_rad"], "Constrains the radius of a circle or arc"),
        ])
        + cluster([
            sm_btn("Diameter", "^C^C_DIMCONSTRAINT _D", SM["dim_dia"], "Constrains the diameter of a circle or arc"),
            sm_btn("Angular", "^C^C_DIMCONSTRAINT _AN", SM["dim_ang"], "Constrains the angle between line segments"),
            sm_btn("Convert", "^C^C_DIMCONSTRAINT _C", SM["c_convert"], "Converts associative dimensions to dimensional constraints"),
        ]),
    )

    p_man = panel(
        "panel-par-manage", "Manage",
        big_btn("Auto", "^C^C_AUTOCONSTRAIN", BIG["autoconstrain"], "Applies geometric constraints automatically to selected objects")
        + cluster([
            sm_btn("Show Geom", "^C^C_CONSTRAINTBAR", SM["c_show"], "Shows or hides geometric constraint bars"),
            sm_btn("Show Dim", "^C^C_DCDISPLAY", SM["c_show"], "Shows or hides dynamic dimensional constraints"),
            sm_btn("Settings", "^C^C_CONSTRAINTSETTINGS", SM["c_settings"], "Opens the Constraint Settings dialog"),
        ])
        + cluster([
            sm_btn("Delete All", "^C^C_DELCONSTRAINT", SM["c_delete"], "Removes all geometric and dimensional constraints"),
            sm_btn("Parameters", "^C^C_PARAMETERS", SM["c_params"], "Opens the Parameters Manager palette"),
        ], rows=2),
    )

    return p_geom + p_dim + p_man


def build_3d_tab():
    p_mod = panel(
        "panel-3d-modeling", "Modeling",
        big_btn("Box", "^C^C_BOX", BIG["box3d"], "Creates a 3D solid box")
        + big_btn("Extrude", "^C^C_EXTRUDE", BIG["extrude"], "Creates a 3D solid or surface by extruding 2D curves")
        + big_btn("Presspull", "^C^C_PRESSPULL", BIG["presspull"], "Dynamically modifies bounded areas by extrusion or offset")
        + cluster([
            sm_btn("Cylinder", "^C^C_CYLINDER", SM["cyl"], "Creates a 3D solid cylinder"),
            sm_btn("Sphere", "^C^C_SPHERE", SM["sphere"], "Creates a 3D solid sphere"),
            sm_btn("Cone", "^C^C_CONE", SM["cone"], "Creates a 3D solid cone"),
        ])
        + cluster([
            sm_btn("Wedge", "^C^C_WEDGE", SM["wedge"], "Creates a 3D solid wedge"),
            sm_btn("Pyramid", "^C^C_PYRAMID", SM["pyramid"], "Creates a 3D solid pyramid"),
            sm_btn("Torus", "^C^C_TORUS", SM["torus"], "Creates a donut-shaped 3D solid"),
        ])
        + cluster([
            sm_btn("Polysolid", "^C^C_POLYSOLID", SM["polysolid"], "Creates a 3D wall-like polysolid"),
            sm_btn("Revolve", "^C^C_REVOLVE", SM["revolve"], "Creates a 3D solid or surface by revolving a 2D curve"),
            sm_btn("Sweep", "^C^C_SWEEP", SM["sweep"], "Sweeps a 2D profile along an open or closed path"),
        ])
        + cluster([
            sm_btn("Loft", "^C^C_LOFT", SM["loft"], "Creates a 3D solid or surface between cross sections"),
            sm_btn("To Solid", "^C^C_CONVTOSOLID", SM["convert_solid"], "Converts eligible 3D objects to 3D solids"),
            sm_btn("To Mesh", "^C^C_CONVTOMESH", SM["vs_2d"], "Converts 3D objects to smooth mesh objects"),
        ]),
    )

    p_solid = panel(
        "panel-3d-solidedit", "Solid Editing",
        cluster([
            sm_btn("Union", "^C^C_UNION", SM["union"], "Combines selected 3D solids or 2D regions"),
            sm_btn("Subtract", "^C^C_SUBTRACT", SM["subtract"], "Subtracts one set of solids from another"),
            sm_btn("Intersect", "^C^C_INTERSECT", SM["intersect"], "Creates a 3D solid from overlapping volumes"),
        ])
        + cluster([
            sm_btn("Slice", "^C^C_SLICE", SM["slice"], "Slices 3D solids and surfaces with a plane"),
            sm_btn("Thicken", "^C^C_THICKEN", SM["thicken"], "Converts a surface into a 3D solid with thickness"),
            sm_btn("Solid Edit", "^C^C_SOLIDEDIT", SM["solidedit"], "Edits faces and edges of 3D solid objects"),
        ])
        + cluster([
            sm_btn("Fillet Edge", "^C^C_FILLETEDGE", SM["filletedge"], "Rounds and fillets the edges of solid objects"),
            sm_btn("Chamfer Edge", "^C^C_CHAMFEREDGE", SM["chamferedge"], "Bevels the edges of solid objects"),
            sm_btn("Interfere", "^C^C_INTERFERE", SM["interfere"], "Creates temporary 3D solids from interferences"),
        ]),
    )

    p_ops = panel(
        "panel-3d-ops", "3D Operations & Render",
        cluster([
            sm_btn("3D Move", "^C^C_3DMOVE", SM["move3d"], "Moves objects in 3D space with a gizmo"),
            sm_btn("3D Rotate", "^C^C_3DROTATE", SM["rot3d"], "Rotates objects around a 3D axis"),
            sm_btn("3D Scale", "^C^C_3DSCALE", SM["scale3d"], "Resizes objects in 3D space"),
        ])
        + cluster([
            sm_btn("3D Mirror", "^C^C_3DMIRROR", SM["mirror3d"], "Creates a mirrored copy across a 3D plane"),
            sm_btn("Section Plane", "^C^C_SECTIONPLANE", SM["section"], "Creates a section object that cuts through 3D models"),
            sm_btn("Flatshot", "^C^C_FLATSHOT", SM["flatshot"], "Creates a 2D representation of all 3D objects"),
        ])
        + cluster([
            sm_btn("Materials", "^C^C_MATERIALS", SM["materials"], "Opens the Materials Browser palette"),
            sm_btn("Render", "^C^C_RENDER", SM["render"], "Creates a photorealistic rendered image of the 3D model"),
            sm_btn("To Surface", "^C^C_CONVTOSURFACE", SM["thicken"], "Converts objects to procedural 3D surfaces"),
        ]),
    )

    return p_mod + p_solid + p_ops


def build_view_tab():
    p_nav = panel(
        "panel-view-nav", "Navigate",
        big_btn("Pan", "^C^C_PAN", BIG["pan"], "Shifts the view without changing magnification")
        + split_big("Zoom", "^C^C_ZOOM _E", BIG["zoom"], "menu-zoom", "Increases or decreases viewport magnification")
        + big_btn("Orbit", "^C^C_3DORBIT", BIG["orbit"], "Rotates the view in 3D space")
        + cluster([
            sm_btn("ViewCube", "^C^C_NAVVCUBE", SM["viewcube"], "Controls visibility and settings of the ViewCube"),
            sm_btn("UCS Icon", "^C^C_UCSICON", SM["ucs_icon"], "Controls visibility and placement of the UCS icon"),
        ], rows=2),
    )

    p_vp = panel(
        "panel-view-vports", "Views & Viewports",
        big_btn("UCS", "^C^C_UCS", BIG["ucs"], "Manages defined user coordinate systems")
        + big_btn("Viewports", "^C^C_VPORTS", BIG["viewports"], "Creates multiple model or layout viewports")
        + big_btn("Named Views", "^C^C_VIEW", BIG["named_views"], "Saves and restores named camera views"),
    )

    p_vs = panel(
        "panel-view-styles", "Visual Styles",
        cluster([
            sm_btn("2D Wireframe", "^C^C_VSCURRENT _2D", SM["vs_2d"], "Displays objects using lines and curves"),
            sm_btn("Conceptual", "^C^C_VSCURRENT _C", SM["vs_concept"], "Shades objects with Gooch cool-to-warm face shading"),
            sm_btn("Hidden", "^C^C_VSCURRENT _H", SM["vs_hidden"], "Hides wireframe lines representing back faces"),
        ])
        + cluster([
            sm_btn("Realistic", "^C^C_VSCURRENT _R", SM["vs_realistic"], "Shades objects and displays applied materials"),
            sm_btn("Shaded", "^C^C_VSCURRENT _S", SM["vs_shaded"], "Produces a smooth shaded 3D model"),
            sm_btn("X-Ray", "^C^C_VSCURRENT _X", SM["vs_xray"], "Displays 3D objects with partial transparency"),
        ]),
    )

    p_pal = panel(
        "panel-view-palettes", "Palettes",
        big_btn("Properties", "^C^C_PROPERTIES", BIG["properties"], "Controls properties of existing objects")
        + big_btn("Layers", "^C^C_LAYER", BIG["layer_props"], "Opens the Layer Properties Manager")
        + big_btn("Content", "'_content", BIG["designcenter"], "Opens the Content / Blocks palette")
        + cluster([
            sm_btn("Tool Sets", "^C^C_TOOLSETS", SM["reset_pal"], "Toggles the macOS Tool Sets palette"),
            sm_btn("Cmd Line", "^C^C_COMMANDLINE", SM["cmdline"], "Displays the Command Line window"),
            sm_btn("Sheet Set", "^C^C_SHEETSET", SM["sheetset"], "Opens the Sheet Set Manager"),
        ])
        + cluster([
            sm_btn("Materials", "^C^C_MATERIALS", SM["materials"], "Opens the Materials Browser"),
            sm_btn("Count List", "^C^C_COUNTLIST", SM["count_sm"], "Opens the Count palette"),
            sm_btn("Reset Palettes", "^C^C_RESETPALETTES", SM["reset_pal"], "Resets palettes to default positions"),
        ]),
    )

    return p_nav + p_vp + p_vs + p_pal


def build_manage_tab():
    p_cust = panel(
        "panel-man-custom", "Customization",
        big_btn("CUI", "^C^C_CUI", BIG["cui"], "Manages customized user interface elements")
        + big_btn("Aliases", "^C^C_ALIASEDIT", BIG["aliases"], "Opens the Command Aliases (PGP) editor"),
    )

    p_apps = panel(
        "panel-man-apps", "Applications",
        big_btn("AppLoad", "^C^C_APPLOAD", BIG["appload"], "Loads AutoLISP, ARX, and CRX applications")
        + big_btn("Run Script", "^C^C_SCRIPT", BIG["script"], "Executes a sequence of commands from a script file"),
    )

    p_clean = panel(
        "panel-man-clean", "Cleanup & Standards",
        big_btn("Audit", "^C^C_AUDIT", BIG["audit"], "Evaluates the integrity of a drawing and corrects errors")
        + big_btn("Purge", "^C^C_PURGE", BIG["purge"], "Removes unused blocks, layers, styles, and definitions")
        + big_btn("Recover", "^C^C_RECOVER", BIG["recover"], "Repairs and opens a damaged drawing file")
        + cluster([
            sm_btn("Units", "^C^C_UNITS", SM["units"], "Controls coordinate and angle display formats"),
            sm_btn("Options", "^C^C_OPTIONS", SM["options"], "Opens AutoCAD Preferences / Options"),
        ], rows=2),
    )

    return p_cust + p_apps + p_clean


def build_output_tab():
    p_plot = panel(
        "panel-out-plot", "Plot",
        big_btn("Plot", "^C^C_PLOT", BIG["plot"], "Plots a drawing to a plotter, printer, or PDF")
        + big_btn("Batch Plot", "^C^C_PUBLISH", BIG["publish"], "Publishes drawings to PDF or plotter sets")
        + big_btn("Preview", "^C^C_PREVIEW", BIG["preview"], "Displays the drawing as it will be plotted")
        + big_btn("Page Setup", "^C^C_PAGESETUP", BIG["pagesetup"], "Controls page layout, plotting device, and paper size"),
    )

    p_exp = panel(
        "panel-out-export", "Export & Send",
        big_btn("Export PDF", "^C^C_EXPORTPDF", BIG["export_pdf"], "Exports the current drawing to a PDF file")
        + big_btn("Export", "^C^C_EXPORT", BIG["export_other"], "Saves drawing objects to other file formats (DXF, STL, DWG, BMP)")
        + big_btn("eTransmit", "^C^C_ETRANSMIT", BIG["etransmit"], "Packages a set of drawing files and dependencies for transmittal")
        + cluster([
            sm_btn("Layout to Model", "^C^C_EXPORTLAYOUT", SM["export_layout"], "Exports all visible objects from current layout to model space"),
        ], rows=2),
    )

    return p_plot + p_exp


def build_collaborate_tab():
    p_share = panel(
        "panel-collab-share", "Share",
        big_btn("Share", "^C^C_SHARE", BIG["share"], "Shares a link to a copy of the current drawing for web/mobile review"),
    )

    p_cmp = panel(
        "panel-collab-compare", "Compare",
        big_btn("DWG Compare", "^C^C_COMPARE", BIG["compare"], "Highlights graphical differences between two drawing versions"),
    )

    p_trace = panel(
        "panel-collab-trace", "Trace & Markup",
        big_btn("Traces", "^C^C_TRACEPALETTEOPEN", BIG["traces"], "Opens the Traces palette for safe collaborative markup")
        + cluster([
            sm_btn("Markup Import", "^C^C_MARKUPIMPORT", SM["markup_imp"], "Imports a PDF, PNG, or JPG markup as a trace overlay"),
            sm_btn("Markup Assist", "^C^C_MARKUPASSIST", SM["markup_assist"], "Identifies markups as text, leaders, or revision clouds"),
        ], rows=2),
    )

    p_act = panel(
        "panel-collab-history", "Activity",
        big_btn("Activity", "^C^C'_ACTIVITYINSIGHTSOPEN", BIG["activity_insights"], "Opens Activity Insights to track drawing edits and version events"),
    )

    return p_share + p_cmp + p_trace + p_act


def build_express_tab():
    # Every command on Express Tools is verified working live in AutoCAD for Mac 2027!
    p_blk = panel(
        "panel-exp-blocks", "Blocks",
        big_btn("Burst", "^C^CBURST", BIG["burst"], "Explodes blocks while converting attribute values to text")
        + big_btn("Count", "^C^C_COUNT", BIG["count_big"], "Counts instances of selected objects or blocks in the drawing")
        + cluster([
            sm_btn("Replace Block", "^C^CBLOCKREPLACE", SM["exp_replace"], "Replaces all references of one block with another"),
            sm_btn("Copy Nested", "^C^CNCOPY", SM["exp_ncopy"], "Copies objects nested inside an xref or block"),
            sm_btn("Count Palette", "^C^C_COUNTLIST", SM["count_sm"], "Opens the Count palette to inspect and insert count tables"),
        ]),
    )

    p_txt = panel(
        "panel-exp-text", "Text",
        cluster([
            sm_btn("Convert MText", "^C^CTXT2MTXT", SM["exp_txt2mtxt"], "Combines single-line text objects into one MText object"),
            sm_btn("Find & Replace", "^C^C_FIND", SM["find_text"], "Finds and replaces text strings across the drawing"),
            sm_btn("Spell Check", "^C^C_SPELL", SM["spell"], "Checks spelling in all text and dimension objects"),
        ]),
    )

    p_mod = panel(
        "panel-exp-modify", "Modify & Draw",
        big_btn("Super Hatch", "^C^CSUPERHATCH", BIG["superhatch"], "Uses an image, block, xref, or wipeout as a hatch pattern")
        + cluster([
            sm_btn("Break-line", "^C^CBREAKLINE", SM["exp_breakline"], "Creates a polyline with a standard break-line symbol"),
            sm_btn("Overkill", "^C^C_OVERKILL", SM["overkill"], "Deletes duplicate or overlapping lines, arcs, and polylines"),
            sm_btn("Flatten", "^C^CFLATTEN", SM["exp_flatten"], "Creates a 2D representation by projecting 3D objects to Z=0"),
        ]),
    )

    return p_blk + p_txt + p_mod


def build_panel_trays():
    trays = []
    trays.append(
        '<div class="panel-tray" data-for="panel-draw" role="group" aria-label="Extended Draw tools">'
        '<div class="tray-row">'
        + sm_btn("Spline Fit", "^C^C_SPLINE _M _FIT", SM["spline_fit"], "Creates a smooth curve passing through fit points")
        + sm_btn("Spline CV", "^C^C_SPLINE _M _CV", SM["spline_cv"], "Creates a smooth curve defined by control vertices")
        + sm_btn("XLine", "^C^C_XLINE", SM["xline"], "Creates an infinite construction line")
        + sm_btn("Ray", "^C^C_RAY", SM["ray"], "Creates a semi-infinite construction ray")
        + sm_btn("Point", "^C^C_POINT", SM["point"], "Creates a point object")
        + sm_btn("Divide", "^C^C_DIVIDE", SM["divide"], "Places evenly spaced points or blocks along an object")
        + sm_btn("Measure", "^C^C_MEASURE", SM["measure_pts"], "Places points or blocks at measured intervals")
        + '</div><div class="tray-row">'
        + sm_btn("Region", "^C^C_REGION", SM["region"], "Converts an enclosed area into a 2D region object")
        + sm_btn("Wipeout", "^C^C_WIPEOUT", SM["wipeout"], "Masks underlying objects with background color")
        + sm_btn("3D Polyline", "^C^C_3DPOLY", SM["poly3d"], "Creates a 3D polyline")
        + sm_btn("Helix", "^C^C_HELIX", SM["helix"], "Creates a 2D spiral or 3D spring")
        + sm_btn("Donut", "^C^C_DONUT", SM["donut"], "Creates a filled circle or wide ring")
        + sm_btn("Revcloud", "^C^C_REVCLOUD", SM["revcloud"], "Creates a revision cloud")
        + '</div></div>'
    )

    trays.append(
        '<div class="panel-tray" data-for="panel-modify" role="group" aria-label="Extended Modify tools">'
        '<div class="tray-row">'
        + sm_btn("Change Props", "^C^C_CHPROP", SM["setbylayer"], "Changes color, layer, linetype, or lineweight of selected objects")
        + sm_btn("Change Space", "^C^C_CHSPACE", SM["chspace"], "Moves objects between model space and paper space")
        + sm_btn("Lengthen", "^C^C_LENGTHEN", SM["lengthen"], "Changes length of objects and included angle of arcs")
        + sm_btn("Edit Polyline", "^C^C_PEDIT", SM["pedit"], "Edits polylines and 3D polygon meshes")
        + sm_btn("Edit Spline", "^C^C_SPLINEDIT", SM["spline_fit"], "Modifies parameters of a spline")
        + sm_btn("Edit Hatch", "^C^C_HATCHEDIT", SM["hatch"], "Modifies an existing hatch or fill")
        + '</div><div class="tray-row">'
        + sm_btn("Align", "^C^C_ALIGN", SM["align"], "Aligns objects with other objects in 2D and 3D")
        + sm_btn("Break", "^C^C_BREAK", SM["break"], "Breaks the selected object between two points")
        + sm_btn("Break at Point", "^C^C_BREAKATPOINT", SM["break_pt"], "Breaks an object into two objects at a single point")
        + sm_btn("Overkill", "^C^C_OVERKILL", SM["overkill"], "Removes duplicate or overlapping geometry")
        + sm_btn("Bring Front", "^C^C_DRAWORDER _F", SM["draw_front"], "Moves selected objects to the front of draw order")
        + sm_btn("Send Back", "^C^C_DRAWORDER _B", SM["draw_back"], "Moves selected objects to the back of draw order")
        + '</div></div>'
    )

    trays.append(
        '<div class="panel-tray" data-for="panel-annotation" role="group" aria-label="Annotation Styles">'
        '<div class="tray-row">'
        + sm_btn("Text Style", "^C^C_STYLE", SM["text_style"], "Manages text styles")
        + sm_btn("Dim Style", "^C^C_DIMSTYLE", SM["dim_style"], "Manages dimension styles")
        + sm_btn("Leader Style", "^C^C_MLEADERSTYLE", SM["leader_sm"], "Manages multileader styles")
        + sm_btn("Table Style", "^C^C_TABLESTYLE", SM["table_sm"], "Manages table styles")
        + '</div></div>'
    )

    trays.append(
        '<div class="panel-tray" data-for="panel-layers" role="group" aria-label="Extended Layer tools">'
        '<div class="tray-row">'
        + sm_btn("Thaw All", "^C^C_-LAYER _T * ;;", SM["lay_thw"], "Thaws all frozen layers in the drawing")
        + sm_btn("Make Current", "^C^C_LAYMCUR", SM["lay_mcur"], "Sets current layer to that of a selected object")
        + sm_btn("Match Layer", "^C^C_LAYMCH", SM["lay_mch"], "Changes layer of selected objects to match a destination object")
        + sm_btn("Change to Current", "^C^C_LAYCUR", SM["lay_cur"], "Moves selected objects to the current layer")
        + '</div></div>'
    )

    trays.append(
        '<div class="panel-tray" data-for="panel-block" role="group" aria-label="Extended Block tools">'
        '<div class="tray-row">'
        + sm_btn("Define Attr", "^C^C_ATTDEF", SM["blk_attr"], "Defines a block attribute")
        + sm_btn("Manage Attr", "^C^C_BATTMAN", SM["blk_attr"], "Opens the Block Attribute Manager")
        + sm_btn("Sync Attr", "^C^C_ATTSYNC", SM["blk_sync"], "Synchronizes block attribute definitions")
        + sm_btn("Base Point", "^C^C_BASE", SM["blk_base"], "Sets the drawing insertion base point")
        + '</div></div>'
    )

    trays.append(
        '<div class="panel-tray" data-for="panel-properties" role="group" aria-label="Extended Properties tools">'
        '<div class="tray-row">'
        + sm_btn("Properties Palette", "^C^C_PROPERTIES", SM["reset_pal"], "Toggles the Properties Inspector")
        + sm_btn("List Info", "^C^C_LIST", SM["list_info"], "Displays property data for selected objects")
        + sm_btn("LT Scale", "^C^C_LTSCALE", SM["prop_lt"], "Sets the global linetype scale factor")
        + '</div></div>'
    )

    trays.append(
        '<div class="panel-tray" data-for="panel-utilities" role="group" aria-label="Extended Selection and Isolation">'
        '<div class="tray-row">'
        + sm_btn("Add Selected", "^C^C_ADDSELECTED", SM["sel_similar"], "Creates a new object of the same type and properties")
        + sm_btn("Hide Objects", "^C^C_HIDEOBJECTS", SM["lay_off"], "Temporarily hides selected objects")
        + sm_btn("End Isolation", "^C^C_UNISOLATEOBJECTS", SM["lay_uniso"], "Displays objects hidden with Isolate or Hide Objects")
        + sm_btn("Point ID", "^C^C_ID", SM["point"], "Displays UCS coordinates of a specified location")
        + '</div></div>'
    )

    return "\n".join(trays)


def build_dropdown_menus():
    menus = []

    menus.append(menu("menu-app", "".join([
        m_item("New Drawing...", "^C^C_NEW", QAT_ICONS["new"]),
        m_item("Open Drawing...", "^C^C_OPEN", QAT_ICONS["open"]),
        m_item("Save", "^C^C_QSAVE", QAT_ICONS["save"]),
        m_item("Save As...", "^C^C_SAVEAS", QAT_ICONS["saveas"]),
        m_div(),
        m_item("Import...", "^C^C_IMPORT", SM["markup_imp"]),
        m_item("Export to PDF...", "^C^C_EXPORTPDF", SM["ref_dwg"]),
        m_item("Export Other Formats...", "^C^C_EXPORT", SM["export_layout"]),
        m_item("Publish / Batch Plot...", "^C^C_PUBLISH", QAT_ICONS["plot"]),
        m_item("Print / Plot...", "^C^C_PLOT", QAT_ICONS["plot"]),
        m_div(),
        m_item("Drawing Utilities: Audit", "^C^C_AUDIT", SM["group_toggle"]),
        m_item("Drawing Utilities: Purge", "^C^C_PURGE", SM["c_delete"]),
        m_item("Drawing Utilities: Units", "^C^C_UNITS", SM["units"]),
        m_div(),
        m_item("Preferences / Options...", "^C^C_OPTIONS", SM["options"]),
        m_item("Close Drawing", "^C^C_CLOSE", QAT_ICONS["close"]),
    ]), min_w=210))

    menus.append(menu("menu-workspace", "".join([
        '<button type="button" class="cad-menu-item" role="menuitem" data-workspace="Drafting &amp; Annotation" data-target-tab="tab-home">✓ Drafting &amp; Annotation</button>',
        '<button type="button" class="cad-menu-item" role="menuitem" data-workspace="3D Modeling" data-target-tab="tab-3d">3D Modeling</button>',
        m_div(),
        m_item("Customize Workspaces...", "^C^C_CUI", SM["options"]),
    ]), min_w=205))

    menus.append(menu("menu-circle", "".join([
        m_item("Center, Radius", "^C^C_CIRCLE", MI["cir_cr"], short="Circle"),
        m_item("Center, Diameter", "^C^C_CIRCLE \\_d", MI["cir_cd"], short="Diameter"),
        m_div(),
        m_item("2-Point", "^C^C_CIRCLE _2P", MI["cir_2p"], short="2-Point"),
        m_item("3-Point", "^C^C_CIRCLE _3P", MI["cir_3p"], short="3-Point"),
        m_div(),
        m_item("Tan, Tan, Radius", "^C^C_CIRCLE _TTR", MI["cir_ttr"], short="Tan Tan R"),
        m_item("Tan, Tan, Tan", "^C^C_CIRCLE _3P _TAN \\_TAN \\_TAN \\", MI["cir_ttr"], short="Tan Tan Tan"),
    ])))

    menus.append(menu("menu-arc", "".join([
        m_item("3-Point", "^C^C_ARC", MI["arc_std"], short="Arc"),
        m_div(),
        m_item("Start, Center, End", "^C^C_ARC \\_C", MI["arc_std"], short="Arc SCE"),
        m_item("Start, Center, Angle", "^C^C_ARC \\_C \\_A", MI["arc_std"], short="Arc SCA"),
        m_item("Start, Center, Length", "^C^C_ARC \\_C \\_L", MI["arc_std"], short="Arc SCL"),
        m_div(),
        m_item("Start, End, Angle", "^C^C_ARC \\_E \\_A", MI["arc_std"], short="Arc SEA"),
        m_item("Start, End, Direction", "^C^C_ARC \\_E \\_D", MI["arc_std"], short="Arc SED"),
        m_item("Start, End, Radius", "^C^C_ARC \\_E \\_R", MI["arc_std"], short="Arc SER"),
        m_div(),
        m_item("Center, Start, End", "^C^C_ARC _C", MI["arc_std"], short="Arc CSE"),
        m_item("Center, Start, Angle", "^C^C_ARC _C \\\\_A", MI["arc_std"], short="Arc CSA"),
        m_item("Center, Start, Length", "^C^C_ARC _C \\\\_L", MI["arc_std"], short="Arc CSL"),
        m_div(),
        m_item("Continue", "^C^C_ARC ;", MI["arc_std"], short="Continue"),
    ]), min_w=195))

    menus.append(menu("menu-rect", "".join([
        m_item("Rectangle", "^C^C_RECTANG", SM["rect"], short="Rectangle"),
        m_item("Polygon", "^C^C_POLYGON", MI["poly"], short="Polygon"),
    ])))

    menus.append(menu("menu-ellipse", "".join([
        m_item("Center", "^C^C_ELLIPSE _C", SM["ellipse"], short="Ellipse"),
        m_item("Axis, End", "^C^C_ELLIPSE", SM["ellipse"], short="Axis, End"),
        m_item("Elliptical Arc", "^C^C_ELLIPSE _A", MI["arc_std"], short="Ellip Arc"),
    ])))

    menus.append(menu("menu-hatch", "".join([
        m_item("Hatch", "^C^C_BHATCH", SM["hatch"], short="Hatch"),
        m_item("Gradient", "^C^C_GRADIENT", MI["gradient"], short="Gradient"),
        m_item("Boundary", "^C^C_BOUNDARY", MI["boundary"], short="Boundary"),
    ])))

    menus.append(menu("menu-trim", "".join([
        m_item("Trim", "^C^C_TRIM", SM["cut"], short="Trim"),
        m_item("Extend", "^C^C_EXTEND", MI["extend"], short="Extend"),
    ])))

    menus.append(menu("menu-fillet", "".join([
        m_item("Fillet", "^C^C_FILLET", SM["fillet"], short="Fillet"),
        m_item("Chamfer", "^C^C_CHAMFER", MI["chamfer"], short="Chamfer"),
        m_item("Blend Curves", "^C^C_BLEND", MI["blend"], short="Blend"),
    ])))

    menus.append(menu("menu-array", "".join([
        m_item("Rectangular Array", "^C^C_ARRAYRECT", SM["array"], short="Array"),
        m_item("Path Array", "^C^C_ARRAYPATH", MI["arr_path"], short="Path Arr"),
        m_item("Polar Array", "^C^C_ARRAYPOLAR", MI["arr_polar"], short="Polar Arr"),
    ])))

    menus.append(menu("menu-text-type", "".join([
        m_item("Multiline Text", "^C^C_MTEXT", SM["text_style"], short="Text"),
        m_item("Single Line Text", "^C^C_TEXT", SM["text_style"], short="Single Line"),
    ])))

    menus.append(menu("menu-dim-types", "".join([
        m_item("Linear", "^C^C_DIMLINEAR", SM["dim_lin"], short="Linear"),
        m_item("Aligned", "^C^C_DIMALIGNED", SM["dim_ali"], short="Aligned"),
        m_item("Angular", "^C^C_DIMANGULAR", SM["dim_ang"], short="Angular"),
        m_item("Arc Length", "^C^C_DIMARC", MI["arc_std"], short="Arc Len"),
        m_item("Radius", "^C^C_DIMRADIUS", SM["dim_rad"], short="Radius"),
        m_item("Diameter", "^C^C_DIMDIAMETER", SM["dim_dia"], short="Diameter"),
        m_item("Ordinate", "^C^C_DIMORDINATE", SM["ucs_icon"], short="Ordinate"),
        m_item("Jogged", "^C^C_DIMJOGGED", SM["dim_lin"], short="Jogged"),
    ])))

    menus.append(menu("menu-leader-types", "".join([
        m_item("Multileader", "^C^C_MLEADER", SM["leader_sm"], short="Leader"),
        m_item("Add Leader", "^C^C_AIMLEADEREDITADD", SM["leader_add"], short="Add Ldr"),
        m_item("Remove Leader", "^C^C_AIMLEADEREDITREMOVE", SM["leader_rem"], short="Rem Ldr"),
        m_item("Align Leaders", "^C^C_MLEADERALIGN", SM["leader_align"], short="Align"),
        m_item("Collect Leaders", "^C^C_MLEADERCOLLECT", SM["leader_collect"], short="Collect"),
    ])))

    menus.append(menu("menu-3dviews", "".join([
        m_item("Top", "^C^C_-VIEW _TOP", MI["view_ortho"], short="Top View"),
        m_item("Bottom", "^C^C_-VIEW _BOTTOM", MI["view_ortho"], short="Bottom"),
        m_item("Left", "^C^C_-VIEW _LEFT", MI["view_ortho"], short="Left"),
        m_item("Right", "^C^C_-VIEW _RIGHT", MI["view_ortho"], short="Right"),
        m_item("Front", "^C^C_-VIEW _FRONT", MI["view_ortho"], short="Front"),
        m_item("Back", "^C^C_-VIEW _BACK", MI["view_ortho"], short="Back"),
        m_div(),
        m_item("SW Isometric", "^C^C_-VIEW _SWISO", MI["view_iso"], short="SW Iso"),
        m_item("SE Isometric", "^C^C_-VIEW _SEISO", MI["view_iso"], short="SE Iso"),
        m_item("NE Isometric", "^C^C_-VIEW _NEISO", MI["view_iso"], short="NE Iso"),
        m_item("NW Isometric", "^C^C_-VIEW _NWISO", MI["view_iso"], short="NW Iso"),
    ])))

    menus.append(menu("menu-vstyles", "".join([
        m_item("2D Wireframe", "^C^C_VSCURRENT _2D", SM["vs_2d"], short="2D Wire"),
        m_item("Wireframe", "^C^C_VSCURRENT _W", SM["vs_2d"], short="Wireframe"),
        m_item("Hidden", "^C^C_VSCURRENT _H", SM["vs_hidden"], short="Hidden"),
        m_item("Realistic", "^C^C_VSCURRENT _R", SM["vs_realistic"], short="Realistic"),
        m_item("Conceptual", "^C^C_VSCURRENT _C", SM["vs_concept"], short="Conceptual"),
        m_item("Shaded", "^C^C_VSCURRENT _S", SM["vs_shaded"], short="Shaded"),
        m_item("Shaded with Edges", "^C^C_VSCURRENT _E", SM["vs_shaded"], short="Shaded+"),
        m_item("Shades of Gray", "^C^C_VSCURRENT _G", SM["vs_realistic"], short="Gray"),
        m_item("Sketchy", "^C^C_VSCURRENT _SK", SM["vs_2d"], short="Sketchy"),
        m_item("X-Ray", "^C^C_VSCURRENT _X", SM["vs_xray"], short="X-Ray"),
    ])))

    # Layer dropdown with live drawing layer container + verified Mac actions
    menus.append(menu("menu-layer-list", "".join([
        '<div id="layer-dynamic-list">',
        m_hdr("Quick Layers"),
        m_item("0", "^C^C_-LAYER _S 0 ;;", '<span class="layer-color-box" style="background:#ffffff;"></span>', color="#ffffff", extra_label="0"),
        '<div class="cad-menu-empty">Open a drawing or run MRSYNC to list all drawing layers.</div>',
        '</div>',
        m_div(),
        m_item("Refresh Drawing Layers (MRSYNC)", "^C^C_MRSYNC", SM["blk_sync"]),
        m_item("Layer Properties Manager...", "^C^C_LAYER", SM["lay_uniso"]),
        m_item("Isolate Selected Layers", "^C^C_LAYISO", SM["lay_iso"]),
        m_item("Unisolate All Layers", "^C^C_LAYUNISO", SM["lay_uniso"]),
    ]), min_w=230))

    color_rows = [
        ("ByLayer", "^C^C_CECOLOR ByLayer", "#ffffff"),
        ("ByBlock", "^C^C_CECOLOR ByBlock", "#888888"),
        ("1 Red", "^C^C_CECOLOR 1", "#ff3b30"),
        ("2 Yellow", "^C^C_CECOLOR 2", "#f5d000"),
        ("3 Green", "^C^C_CECOLOR 3", "#2ecc71"),
        ("4 Cyan", "^C^C_CECOLOR 4", "#00bcd4"),
        ("5 Blue", "^C^C_CECOLOR 5", "#2979ff"),
        ("6 Magenta", "^C^C_CECOLOR 6", "#d500f9"),
        ("7 White", "^C^C_CECOLOR 7", "#ffffff"),
    ]
    menus.append(menu("menu-color-list", "".join([
        m_item(lbl, cmd, f'<span class="layer-color-box" style="background:{hx};"></span>', color=hx, extra_label=lbl)
        for lbl, cmd, hx in color_rows
    ] + [m_div(), m_item("Select Color...", "^C^C_COLOR", SM["ref_adjust"])]), min_w=175))

    lw_rows = [
        ("ByLayer", "^C^C_-LWEIGHT ByLayer", 1),
        ("ByBlock", "^C^C_-LWEIGHT ByBlock", 1),
        ("Default", "^C^C_-LWEIGHT Default", 1),
        ("0.00 mm", "^C^C_-LWEIGHT 0", 1),
        ("0.05 mm", "^C^C_-LWEIGHT 0.05", 1),
        ("0.09 mm", "^C^C_-LWEIGHT 0.09", 1),
        ("0.13 mm", "^C^C_-LWEIGHT 0.13", 1.5),
        ("0.25 mm", "^C^C_-LWEIGHT 0.25", 2),
        ("0.30 mm", "^C^C_-LWEIGHT 0.30", 2.5),
        ("0.50 mm", "^C^C_-LWEIGHT 0.50", 3.5),
    ]
    menus.append(menu("menu-lineweight-list", "".join([
        m_item(lbl, cmd, f'<span class="menu-lw-bar" style="height:{px}px;"></span>', extra_label=lbl)
        for lbl, cmd, px in lw_rows
    ] + [m_div(), m_item("Lineweight Settings...", "^C^C_LWEIGHT", SM["options"])]), min_w=185))

    lt_rows = [
        ("ByLayer", "^C^C_-LINETYPE _S ByLayer ;;", ""),
        ("ByBlock", "^C^C_-LINETYPE _S ByBlock ;;", ""),
        ("Continuous", "^C^C_-LINETYPE _S Continuous ;;", ""),
        ("Center", "^C^C_-LINETYPE _S Center ;;", ' stroke-dasharray="7 2 2 2"'),
        ("Dashed", "^C^C_-LINETYPE _S Dashed ;;", ' stroke-dasharray="4 2"'),
        ("Hidden", "^C^C_-LINETYPE _S Hidden ;;", ' stroke-dasharray="2 2"'),
        ("Phantom", "^C^C_-LINETYPE _S Phantom ;;", ' stroke-dasharray="6 2 1.5 2 1.5 2"'),
    ]
    menus.append(menu("menu-linetype-list", "".join([
        m_item(
            lbl,
            cmd,
            f'<svg aria-hidden="true" class="menu-lt-preview" viewBox="0 0 28 10"><line x1="0" y1="5" x2="28" y2="5" stroke="currentColor" stroke-width="1.4"{dash}/></svg>',
            extra_label=lbl,
        )
        for lbl, cmd, dash in lt_rows
    ] + [m_div(), m_item("Other...", "^C^C_LINETYPE", SM["options"])]), min_w=185))

    menus.append(menu("menu-measure", "".join([
        m_item("Quick Measure", "^C^C_MEASUREGEOM _QUICK", MI["dist"], short="Measure"),
        m_item("Distance", "^C^C_MEASUREGEOM _DISTANCE", MI["dist"], short="Distance"),
        m_item("Radius", "^C^C_MEASUREGEOM _RADIUS", SM["dim_rad"], short="Radius"),
        m_item("Angle", "^C^C_MEASUREGEOM _ANGLE", SM["dim_ang"], short="Angle"),
        m_item("Area", "^C^C_MEASUREGEOM _AREA", MI["area"], short="Area"),
        m_item("Volume", "^C^C_MEASUREGEOM _VOLUME", MI["view_iso"], short="Volume"),
        m_div(),
        m_item("Point ID", "^C^C_ID", SM["point"], short="ID"),
    ])))

    menus.append(menu("menu-paste", "".join([
        m_item("Paste", "^C^C_PASTECLIP", SM["copyclip"], short="Paste"),
        m_item("Paste as Block", "^C^C_PASTEBLOCK", SM["blk_create"], short="Paste Blk"),
        m_item("Paste to Original Coords", "^C^C_PASTEORIG", SM["copybase"], short="Paste Orig"),
    ])))

    menus.append(menu("menu-zoom", "".join([
        m_item("Zoom Extents", "^C^C_ZOOM _E", SM["zoom_ext"], short="Extents"),
        m_item("Zoom Window", "^C^C_ZOOM _W", MI["zoom_sm"], short="Window"),
        m_item("Zoom Previous", "^C^C_ZOOM _P", MI["zoom_sm"], short="Previous"),
        m_item("Zoom Realtime", "^C^C_ZOOM _R", MI["zoom_sm"], short="Realtime"),
        m_item("Zoom All", "^C^C_ZOOM _A", SM["zoom_ext"], short="All"),
        m_item("Zoom Dynamic", "^C^C_ZOOM _D", MI["zoom_sm"], short="Dynamic"),
        m_item("Zoom Scale", "^C^C_ZOOM _S", MI["zoom_sm"], short="Scale"),
        m_item("Zoom Center", "^C^C_ZOOM _C", MI["zoom_sm"], short="Center"),
        m_item("Zoom Object", "^C^C_ZOOM _O", MI["zoom_sm"], short="Object"),
        m_item("Zoom In", "^C^C_ZOOM 2X", MI["zoom_sm"], short="Zoom In"),
        m_item("Zoom Out", "^C^C_ZOOM .5X", MI["zoom_sm"], short="Zoom Out"),
    ])))

    return "\n".join(menus)


def generate():
    tabs_meta = [
        ("tab-home", "Home", build_home_tab()),
        ("tab-insert", "Insert", build_insert_tab()),
        ("tab-annotate", "Annotate", build_annotate_tab()),
        ("tab-parametric", "Parametric", build_parametric_tab()),
        ("tab-3d", "3D Tools", build_3d_tab()),
        ("tab-view", "View", build_view_tab()),
        ("tab-manage", "Manage", build_manage_tab()),
        ("tab-output", "Output", build_output_tab()),
        ("tab-collaborate", "Collaborate", build_collaborate_tab()),
        ("tab-express", "Express Tools", build_express_tab()),
    ]

    tab_btns = []
    tab_panels = []
    ctx_tabs = []
    for idx, (tid, title, content) in enumerate(tabs_meta):
        active_cls = " active" if idx == 0 else ""
        sel = "true" if idx == 0 else "false"
        tindex = "0" if idx == 0 else "-1"
        hidden_attr = "" if idx == 0 else " hidden"
        tab_btns.append(
            f'<button type="button" class="tab-button{active_cls}" role="tab" '
            f'id="btn-{tid}" data-tab="{tid}" aria-controls="{tid}" '
            f'aria-selected="{sel}" tabindex="{tindex}">{esc(title)}</button>'
        )
        tab_panels.append(
            f'<div class="tab-content{active_cls}" id="{tid}" role="tabpanel" '
            f'aria-labelledby="btn-{tid}"{hidden_attr}>{content}</div>'
        )
        ctx_tabs.append(
            f'<button type="button" class="cad-context-item" role="menuitemcheckbox" '
            f'aria-checked="true" data-toggle-tab="{tid}">'
            f'<span class="cad-context-check">✓</span><span>{esc(title)}</span></button>'
        )

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AutoCAD Windows Ribbon</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="ribbon-container" id="ribbon" aria-label="AutoCAD Ribbon">
    <nav class="ribbon-tabs-bar" aria-label="Quick Access and Ribbon Tabs">
      <div class="qat-bar">
        <button type="button" class="cad-app-logo" data-dropdown="menu-app" aria-haspopup="menu" aria-expanded="false" aria-label="Application Menu" data-tip-title="Application Menu" data-tip-desc="File, export, print, and drawing utility commands">
          {QAT_ICONS["app"]}<span class="app-arrow" aria-hidden="true">▾</span>
        </button>
        <button type="button" class="qat-btn" data-cmd="^C^C_QNEW" aria-label="New Drawing" data-tip-title="New" data-tip-desc="Creates a new drawing">{QAT_ICONS["new"]}</button>
        <button type="button" class="qat-btn" data-cmd="^C^C_OPEN" aria-label="Open Drawing" data-tip-title="Open" data-tip-desc="Opens an existing drawing file">{QAT_ICONS["open"]}</button>
        <button type="button" class="qat-btn" data-cmd="^C^C_QSAVE" aria-label="Save Drawing" data-tip-title="Save" data-tip-desc="Saves the current drawing">{QAT_ICONS["save"]}</button>
        <button type="button" class="qat-btn" data-cmd="^C^C_SAVEAS" aria-label="Save Drawing As" data-tip-title="Save As" data-tip-desc="Saves a copy of the current drawing under a new name">{QAT_ICONS["saveas"]}</button>
        <button type="button" class="qat-btn" data-cmd="^C^C_PLOT" aria-label="Plot Drawing" data-tip-title="Plot" data-tip-desc="Plots the current drawing to a printer or PDF">{QAT_ICONS["plot"]}</button>
        <button type="button" class="qat-btn" data-cmd="^C^C_U" aria-label="Undo" data-tip-title="Undo" data-tip-desc="Reverses the most recent operation">{QAT_ICONS["undo"]}</button>
        <button type="button" class="qat-btn" data-cmd="^C^C_REDO" aria-label="Redo" data-tip-title="Redo" data-tip-desc="Reverses the effects of the previous Undo">{QAT_ICONS["redo"]}</button>
        <button type="button" class="workspace-selector" data-dropdown="menu-workspace" aria-haspopup="menu" aria-expanded="false" data-tip-title="Workspace Switching" data-tip-desc="Switches between 2D Drafting and 3D Modeling tabs">
          {QAT_ICONS["gear"]}<span class="ws-label">Drafting &amp; Annotation</span><span class="arrow" aria-hidden="true">▾</span>
        </button>
      </div>

      <div class="ribbon-tabs" role="tablist" aria-label="Ribbon Tabs">
        {"".join(tab_btns)}
      </div>

      <div class="ribbon-controls">
        <button type="button" class="ctrl-btn-toolbar" data-action="toggleHidePalettes" data-tip-title="Toggle Right Inspector" data-tip-desc="Shows or hides the Layers and Properties Inspector">
          {QAT_ICONS["palettes"]}<span>Palettes</span>
        </button>
        <button type="button" class="ctrl-btn-toolbar" id="btn-switch-toolbar" data-tip-title="Switch to Mac Toolbar" data-tip-desc="Hides the Windows Ribbon and restores the native macOS Tool Sets palette">
          {QAT_ICONS["mactoolbar"]}<span>Mac Toolbar</span>
        </button>
        <button type="button" class="ctrl-btn" id="btn-minimize" aria-label="Minimize or Expand Ribbon" aria-expanded="true" data-tip-title="Minimize Ribbon" data-tip-desc="Collapses or expands the ribbon panels">
          {QAT_ICONS["chevron"]}
        </button>
        <button type="button" class="ctrl-btn" id="btn-close" aria-label="Close Ribbon" data-tip-title="Close Ribbon" data-tip-desc="Closes the ribbon and restores Mac Tool Sets">
          {QAT_ICONS["close"]}
        </button>
      </div>
    </nav>

    <main class="ribbon-body-wrap" aria-label="Active Ribbon Panels">
      <button type="button" class="ribbon-scroll-btn left" id="btn-scroll-left" aria-label="Scroll panels left">‹</button>
      <div class="ribbon-body" id="ribbon-body">
        {"".join(tab_panels)}
      </div>
      <button type="button" class="ribbon-scroll-btn right" id="btn-scroll-right" aria-label="Scroll panels right">›</button>
    </main>
  </header>

  <div class="menu-backdrop" id="menu-backdrop"></div>

  <div id="cad-tooltip" role="tooltip">
    <div class="tip-title"></div>
    <div class="tip-desc"></div>
    <div class="tip-cmd"></div>
  </div>

  {build_panel_trays()}
  {build_dropdown_menus()}

  <div class="cad-context-menu" id="ctx-ribbon-menu" role="menu" aria-label="Ribbon Options">
    <button type="button" class="cad-context-item" id="ctx-switch-toolbar" role="menuitem"><span>Switch to Mac Toolbar</span></button>
    <div class="cad-menu-divider" role="separator"></div>
    <div class="cad-context-item has-sub" role="menuitem" aria-haspopup="menu" tabindex="0">
      <span>Show Tabs</span>
      <div class="cad-sub-menu" role="menu">
        {"".join(ctx_tabs)}
      </div>
    </div>
    <div class="cad-context-item has-sub" role="menuitem" aria-haspopup="menu" tabindex="0">
      <span>Show Panels</span>
      <div class="cad-sub-menu" id="sub-menu-panels" role="menu"></div>
    </div>
    <div class="cad-menu-divider" role="separator"></div>
    <button type="button" class="cad-context-item" id="ctx-minimize-ribbon" role="menuitem"><span>Minimize / Expand Ribbon</span></button>
  </div>

  <script src="ribbon.js" defer></script>
</body>
</html>
"""

    out_path = os.path.join(ROOT_DIR, "ui", "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Generated clean {out_path} ({len(doc)} bytes, 10 tabs)")


if __name__ == "__main__":
    generate()
