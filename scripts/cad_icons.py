#!/usr/bin/env python3
"""
Theme-adaptive Autodesk CAD technical drafting SVG icon library.
All icons use CSS custom properties (--icon-ink, --icon-muted, --icon-accent,
--icon-node, --icon-danger, --icon-fill-soft) so they render crisply in both
Dark and Light AutoCAD themes with zero emojis and zero hardcoded neon colors.
"""

INK = "var(--icon-ink)"
MUTED = "var(--icon-muted)"
ACCENT = "var(--icon-accent)"
NODE = "var(--icon-node)"
DANGER = "var(--icon-danger)"
SOFT = "var(--icon-fill-soft)"
SURF = "var(--icon-surface)"


def svg(body, size=28, vb="0 0 32 32"):
    return (
        f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="{vb}" '
        f'fill="none" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )


def sm(body, size=15, vb="0 0 20 20"):
    return svg(body, size=size, vb=vb)


def mi(body, size=14, vb="0 0 20 20"):
    return svg(body, size=size, vb=vb)


def _node(cx, cy, r=2.1):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{NODE}" stroke="{SURF}" stroke-width="0.9"/>'


def _node_sm(cx, cy, r=1.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{NODE}"/>'


# =============================================================================
# LARGE RIBBON ICONS (28x28, viewBox 0 0 32 32)
# =============================================================================
BIG = {
    # --- DRAW ---
    "line": svg(
        f'<line x1="6" y1="26" x2="26" y2="6" stroke="{INK}" stroke-width="2"/>'
        + _node(6, 26) + _node(26, 6)
    ),
    "polyline": svg(
        f'<polyline points="5,25 11,9 21,19 27,7" stroke="{INK}" stroke-width="2"/>'
        + _node(5, 25) + _node(11, 9) + _node(21, 19) + _node(27, 7)
    ),
    "circle": svg(
        f'<circle cx="16" cy="16" r="10.5" stroke="{INK}" stroke-width="1.9"/>'
        f'<line x1="16" y1="16" x2="26.2" y2="16" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="2.5 1.8"/>'
        + _node(16, 16) + _node(26.2, 16, 1.8)
    ),
    "arc": svg(
        f'<path d="M6 24 A16 16 0 0 1 26 9" stroke="{INK}" stroke-width="2"/>'
        + _node(6, 24) + _node(14.5, 11.5) + _node(26, 9)
    ),

    # --- MODIFY ---
    "move": svg(
        f'<rect x="5" y="13" width="9" height="9" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="2 1.5"/>'
        f'<rect x="17" y="6" width="9" height="9" stroke="{INK}" stroke-width="1.8" fill="{SOFT}"/>'
        f'<line x1="10" y1="17" x2="21" y2="11" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<polyline points="17.5,10 21.5,10.8 19.5,14.5" stroke="{ACCENT}" stroke-width="1.6"/>'
    ),
    "rotate": svg(
        f'<rect x="7" y="15" width="9" height="9" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="2 1.5"/>'
        f'<rect x="13" y="8" width="9" height="9" transform="rotate(-24 17 12)" stroke="{INK}" stroke-width="1.8" fill="{SOFT}"/>'
        f'<path d="M25 22 A11 11 0 0 0 18 5.5" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<polyline points="20.5,3.5 17.5,5.5 20,8" stroke="{ACCENT}" stroke-width="1.5"/>'
        + _node(11.5, 22, 1.8)
    ),
    "trim": svg(
        # Authentic AutoCAD scissors cutting a line
        f'<line x1="4" y1="16" x2="17" y2="16" stroke="{INK}" stroke-width="2"/>'
        f'<line x1="17" y1="16" x2="28" y2="16" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="2.5 2"/>'
        f'<line x1="17" y1="5" x2="17" y2="27" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="20" y1="13" x2="27" y2="6" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="20" y1="13" x2="27" y2="20" stroke="{INK}" stroke-width="1.7"/>'
        f'<circle cx="26.5" cy="6.5" r="2.1" stroke="{INK}" stroke-width="1.4"/>'
        f'<circle cx="26.5" cy="19.5" r="2.1" stroke="{INK}" stroke-width="1.4"/>'
    ),
    "erase": svg(
        # Tilted drafting pencil eraser
        f'<path d="M8 24 L17 15 L24 22 L15 28 H10 Z" fill="{SOFT}" stroke="{INK}" stroke-width="1.7"/>'
        f'<path d="M17 15 L22 10 L28 16 L24 22 Z" fill="{DANGER}" fill-opacity="0.32" stroke="{DANGER}" stroke-width="1.7"/>'
        f'<line x1="5" y1="28" x2="26" y2="28" stroke="{MUTED}" stroke-width="1.5"/>'
    ),
    "offset": svg(
        # Concentric parallel offset geometry (not Wi-Fi)
        f'<path d="M6 25 V14 A8 8 0 0 1 14 6 H25" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="2.5 1.8"/>'
        f'<path d="M12 25 V16 A4 4 0 0 1 16 12 H25" stroke="{INK}" stroke-width="2"/>'
        f'<line x1="9" y1="9" x2="14" y2="14" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<polyline points="11.5,14 14.3,14.3 14,11.5" stroke="{ACCENT}" stroke-width="1.4"/>'
    ),

    # --- ANNOTATION ---
    "mtext": svg(
        f'<path d="M7 25 L14.5 7 L22 25" stroke="{INK}" stroke-width="2.1"/>'
        f'<line x1="9.8" y1="19" x2="19.2" y2="19" stroke="{INK}" stroke-width="1.8"/>'
        f'<line x1="23" y1="11" x2="28" y2="11" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="23" y1="15" x2="28" y2="15" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<line x1="23" y1="19" x2="27" y2="19" stroke="{MUTED}" stroke-width="1.4"/>'
    ),
    "text": svg(
        f'<path d="M7 24 L14 7 L21 24" stroke="{INK}" stroke-width="2"/>'
        f'<line x1="9.5" y1="18.5" x2="18.5" y2="18.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="5" y1="26.5" x2="27" y2="26.5" stroke="{ACCENT}" stroke-width="1.5"/>'
    ),
    "dimension": svg(
        f'<line x1="6" y1="25" x2="6" y2="9" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="26" y1="25" x2="26" y2="9" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="6" y1="14" x2="26" y2="14" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<polyline points="10,11.5 6.5,14 10,16.5" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<polyline points="22,11.5 25.5,14 22,16.5" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="12" y1="9" x2="20" y2="9" stroke="{INK}" stroke-width="2"/>'
    ),
    "dimlinear": svg(
        f'<line x1="6" y1="25" x2="6" y2="10" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<line x1="26" y1="25" x2="26" y2="10" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<line x1="6" y1="13" x2="26" y2="13" stroke="{INK}" stroke-width="1.8"/>'
        f'<polyline points="9.5,11 6.5,13 9.5,15" stroke="{INK}" stroke-width="1.4"/>'
        f'<polyline points="22.5,11 25.5,13 22.5,15" stroke="{INK}" stroke-width="1.4"/>'
        f'<line x1="6" y1="24" x2="26" y2="24" stroke="{ACCENT}" stroke-width="1.8"/>'
    ),

    # --- LAYERS ---
    "layer_props": svg(
        # Authentic isometric stacked CAD sheets + properties list badge
        f'<polygon points="16,4 28,10 16,16 4,10" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<polyline points="4,15.5 16,21.5 28,15.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<polyline points="4,21 16,27 28,21" stroke="{MUTED}" stroke-width="1.6"/>'
    ),

    # --- BLOCK & PROPERTIES & GROUPS & UTILITIES & CLIPBOARD ---
    "block_insert": svg(
        f'<rect x="7" y="9" width="16" height="16" stroke="{INK}" stroke-width="1.8" fill="{SOFT}"/>'
        f'<circle cx="15" cy="17" r="4" stroke="{ACCENT}" stroke-width="1.5"/>'
        + _node(7, 9, 2.2)
    ),
    "blocks_palette": svg(
        f'<rect x="5" y="5" width="9" height="9" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<rect x="18" y="5" width="9" height="9" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<rect x="5" y="18" width="9" height="9" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<rect x="18" y="18" width="9" height="9" stroke="{ACCENT}" stroke-width="1.7"/>'
    ),
    "matchprop": svg(
        # Authentic paintbrush icon
        f'<path d="M23 5 L27 9 L16 20 L12 16 Z" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<path d="M12 16 L7 21 C5.5 22.5 5.5 25.5 8 26.5 C10.5 27.5 13 25.5 13.5 23 L16 20 Z" fill="{NODE}" fill-opacity="0.35" stroke="{NODE}" stroke-width="1.6"/>'
    ),
    "group": svg(
        f'<rect x="5" y="5" width="22" height="22" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="3 2"/>'
        f'<circle cx="12" cy="12" r="3" stroke="{INK}" stroke-width="1.7"/>'
        f'<rect x="17" y="17" width="6" height="6" stroke="{INK}" stroke-width="1.7"/>'
    ),
    "measure": svg(
        f'<rect x="5" y="11" width="22" height="10" transform="rotate(-32 16 16)" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<line x1="11" y1="16" x2="13" y2="19" stroke="{ACCENT}" stroke-width="1.4"/>'
        f'<line x1="15" y1="13.5" x2="17" y2="16.5" stroke="{ACCENT}" stroke-width="1.4"/>'
        f'<line x1="19" y1="11" x2="21" y2="14" stroke="{ACCENT}" stroke-width="1.4"/>'
    ),
    "paste": svg(
        f'<rect x="7" y="7" width="16" height="20" rx="1.5" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<rect x="11" y="4" width="8" height="4" rx="1" stroke="{ACCENT}" stroke-width="1.5" fill="{SURF}"/>'
        f'<line x1="11" y1="14" x2="19" y2="14" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="11" y1="18" x2="19" y2="18" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="11" y1="22" x2="16" y2="22" stroke="{MUTED}" stroke-width="1.5"/>'
    ),

    # --- INSERT ---
    "attach": svg(
        f'<path d="M21.5 11.5 L12.5 20.5 A3.5 3.5 0 0 0 17.5 25.5 L26 17 A5.5 5.5 0 0 0 18.2 9.2 L9 18.4 A7.5 7.5 0 0 0 19.6 29" stroke="{INK}" stroke-width="1.8"/>'
        f'<circle cx="10" cy="10" r="3" stroke="{ACCENT}" stroke-width="1.6"/>'
    ),
    "xref_palette": svg(
        f'<rect x="5" y="6" width="15" height="19" stroke="{INK}" stroke-width="1.7"/>'
        f'<rect x="13" y="10" width="14" height="16" fill="{SURF}" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="16" y1="15" x2="24" y2="15" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<line x1="16" y1="19" x2="24" y2="19" stroke="{MUTED}" stroke-width="1.4"/>'
    ),
    "pdf_import": svg(
        f'<path d="M7 4 H19 L25 10 V27 H7 Z" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<polyline points="19,4 19,10 25,10" stroke="{INK}" stroke-width="1.5"/>'
        f'<rect x="8.5" y="15" width="15" height="7" rx="1" fill="{DANGER}" fill-opacity="0.25" stroke="{DANGER}" stroke-width="1.2"/>'
        f'<text x="16" y="20.6" text-anchor="middle" fill="{INK}" font-size="6.2" font-weight="700" font-family="sans-serif">PDF</text>'
    ),
    "import_file": svg(
        f'<path d="M7 21 V26 H25 V21" stroke="{INK}" stroke-width="1.8"/>'
        f'<line x1="16" y1="5" x2="16" y2="20" stroke="{ACCENT}" stroke-width="2"/>'
        f'<polyline points="11,15 16,20.5 21,15" stroke="{ACCENT}" stroke-width="2"/>'
    ),
    "field": svg(
        f'<rect x="5" y="7" width="22" height="18" rx="1.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<rect x="8.5" y="11" width="15" height="10" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.3"/>'
        f'<line x1="11" y1="16" x2="21" y2="16" stroke="{INK}" stroke-width="1.6"/>'
    ),
    "datalink": svg(
        f'<rect x="5" y="6" width="14" height="12" stroke="{INK}" stroke-width="1.6"/>'
        f'<line x1="5" y1="11" x2="19" y2="11" stroke="{MUTED}" stroke-width="1.2"/>'
        f'<line x1="11" y1="6" x2="11" y2="18" stroke="{MUTED}" stroke-width="1.2"/>'
        f'<path d="M16 23 A4 4 0 0 1 16 17 H21 A4 4 0 0 1 21 25 H19" stroke="{ACCENT}" stroke-width="1.7"/>'
    ),
    "update_link": svg(
        f'<path d="M24 14 A8.5 8.5 0 1 0 22.5 21.5" stroke="{INK}" stroke-width="1.8"/>'
        f'<polyline points="20,10 24.5,14 27,9.5" stroke="{ACCENT}" stroke-width="1.8"/>'
    ),
    "designcenter": svg(
        f'<rect x="5" y="5" width="22" height="22" rx="1.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="13" y1="5" x2="13" y2="27" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<rect x="16" y="9" width="8" height="6" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4"/>'
        f'<rect x="16" y="18" width="8" height="5" stroke="{MUTED}" stroke-width="1.3"/>'
    ),
    "toolsets": svg(
        f'<rect x="5" y="5" width="9" height="22" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<rect x="14" y="5" width="13" height="22" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="7.5" y1="10" x2="11.5" y2="10" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="7.5" y1="14" x2="11.5" y2="14" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="7.5" y1="18" x2="11.5" y2="18" stroke="{INK}" stroke-width="1.5"/>'
    ),

    # --- ANNOTATE ---
    "mleader": svg(
        f'<polyline points="6,24 14,12 24,12" stroke="{INK}" stroke-width="1.9"/>'
        f'<polygon points="6,24 10.5,21.5 8,18.5" fill="{ACCENT}"/>'
        f'<line x1="25" y1="10" x2="29" y2="10" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="25" y1="14" x2="29" y2="14" stroke="{MUTED}" stroke-width="1.5"/>'
    ),
    "table": svg(
        f'<rect x="5" y="6" width="22" height="20" stroke="{INK}" stroke-width="1.7"/>'
        f'<rect x="5" y="6" width="22" height="5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.3"/>'
        f'<line x1="5" y1="16" x2="27" y2="16" stroke="{MUTED}" stroke-width="1.3"/>'
        f'<line x1="5" y1="21" x2="27" y2="21" stroke="{MUTED}" stroke-width="1.3"/>'
        f'<line x1="13" y1="11" x2="13" y2="26" stroke="{MUTED}" stroke-width="1.3"/>'
        f'<line x1="20" y1="11" x2="20" y2="26" stroke="{MUTED}" stroke-width="1.3"/>'
    ),

    # --- PARAMETRIC ---
    "autoconstrain": svg(
        f'<rect x="6" y="7" width="16" height="16" stroke="{INK}" stroke-width="1.8"/>'
        f'<line x1="10" y1="12" x2="18" y2="12" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="10" y1="16" x2="18" y2="16" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<circle cx="23" cy="23" r="5" fill="{SURF}" stroke="{NODE}" stroke-width="1.6"/>'
        f'<path d="M21 25 L23 20.5 L25 25" stroke="{NODE}" stroke-width="1.3"/>'
    ),
    "infer_constraints": svg(
        f'<line x1="6" y1="24" x2="22" y2="8" stroke="{INK}" stroke-width="1.8"/>'
        f'<line x1="10" y1="26" x2="26" y2="10" stroke="{ACCENT}" stroke-width="1.8"/>'
        f'<rect x="5" y="6" width="8" height="8" stroke="{NODE}" stroke-width="1.5" fill="{SOFT}"/>'
    ),

    # --- 3D TOOLS ---
    "box3d": svg(
        f'<polygon points="16,5 27,11 16,17 5,11" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<polygon points="5,11 16,17 16,28 5,22" stroke="{INK}" stroke-width="1.6"/>'
        f'<polygon points="27,11 16,17 16,28 27,22" stroke="{INK}" stroke-width="1.6"/>'
    ),
    "extrude": svg(
        f'<polygon points="16,16 25,21 16,26 7,21" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="2 1.5"/>'
        f'<polygon points="16,7 25,12 16,17 7,12" fill="{SOFT}" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="7" y1="12" x2="7" y2="21" stroke="{INK}" stroke-width="1.6"/>'
        f'<line x1="25" y1="12" x2="25" y2="21" stroke="{INK}" stroke-width="1.6"/>'
        f'<line x1="16" y1="17" x2="16" y2="26" stroke="{INK}" stroke-width="1.6"/>'
        f'<line x1="16" y1="12" x2="16" y2="3.5" stroke="{ACCENT}" stroke-width="1.8"/>'
        f'<polyline points="13.5,6 16,3.5 18.5,6" stroke="{ACCENT}" stroke-width="1.6"/>'
    ),
    "presspull": svg(
        f'<rect x="7" y="15" width="18" height="11" fill="{SOFT}" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="16" y1="15" x2="16" y2="5" stroke="{ACCENT}" stroke-width="2"/>'
        f'<polyline points="12,9 16,4.5 20,9" stroke="{ACCENT}" stroke-width="1.8"/>'
    ),

    # --- VIEW ---
    "pan": svg(
        f'<path d="M12 17 V9.5 A1.5 1.5 0 0 1 15 9.5 V15 M15 14 V8 A1.5 1.5 0 0 1 18 8 V15 M18 14 V9.5 A1.5 1.5 0 0 1 21 9.5 V15 M21 13 V11.5 A1.5 1.5 0 0 1 24 11.5 V19 C24 23.5 20.8 26.5 16.5 26.5 C12.5 26.5 10 24 8.5 20.5 L6.5 16.5 A1.5 1.5 0 0 1 9.2 15 L12 18" stroke="{INK}" stroke-width="1.6"/>'
    ),
    "zoom": svg(
        f'<circle cx="14" cy="14" r="8" stroke="{INK}" stroke-width="1.9" fill="{SOFT}"/>'
        f'<line x1="20" y1="20" x2="27" y2="27" stroke="{INK}" stroke-width="2.3"/>'
        f'<line x1="11" y1="14" x2="17" y2="14" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<line x1="14" y1="11" x2="14" y2="17" stroke="{ACCENT}" stroke-width="1.6"/>'
    ),
    "orbit": svg(
        f'<circle cx="16" cy="16" r="9.5" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<ellipse cx="16" cy="16" rx="9.5" ry="4" stroke="{INK}" stroke-width="1.4"/>'
        f'<ellipse cx="16" cy="16" rx="4" ry="9.5" stroke="{MUTED}" stroke-width="1.3"/>'
    ),
    "ucs": svg(
        f'<line x1="8" y1="24" x2="8" y2="6" stroke="{ACCENT}" stroke-width="1.9"/>'
        f'<polyline points="5.5,9.5 8,6 10.5,9.5" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<line x1="8" y1="24" x2="26" y2="24" stroke="{INK}" stroke-width="1.9"/>'
        f'<polyline points="22.5,21.5 26,24 22.5,26.5" stroke="{INK}" stroke-width="1.6"/>'
        f'<rect x="6" y="22" width="4" height="4" fill="{NODE}"/>'
    ),
    "viewports": svg(
        f'<rect x="5" y="6" width="22" height="20" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="16" y1="6" x2="16" y2="26" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<line x1="16" y1="16" x2="27" y2="16" stroke="{MUTED}" stroke-width="1.4"/>'
    ),
    "named_views": svg(
        f'<rect x="5" y="7" width="22" height="18" rx="1.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<circle cx="16" cy="16" r="4.5" stroke="{ACCENT}" stroke-width="1.6" fill="{SOFT}"/>'
        f'<circle cx="16" cy="16" r="1.5" fill="{INK}"/>'
    ),
    "properties": svg(
        f'<rect x="6" y="5" width="20" height="22" rx="1.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<rect x="6" y="5" width="20" height="5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.3"/>'
        f'<line x1="10" y1="14" x2="15" y2="14" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="17" y1="14" x2="22" y2="14" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="10" y1="18.5" x2="15" y2="18.5" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="17" y1="18.5" x2="22" y2="18.5" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="10" y1="23" x2="15" y2="23" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="17" y1="23" x2="22" y2="23" stroke="{INK}" stroke-width="1.5"/>'
    ),

    # --- MANAGE ---
    "cui": svg(
        f'<rect x="5" y="6" width="22" height="20" rx="1.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="5" y1="11" x2="27" y2="11" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<rect x="8" y="14" width="6" height="9" fill="{SOFT}" stroke="{MUTED}" stroke-width="1.3"/>'
        f'<line x1="17" y1="16" x2="24" y2="16" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="17" y1="20" x2="24" y2="20" stroke="{MUTED}" stroke-width="1.5"/>'
    ),
    "aliases": svg(
        f'<rect x="5" y="7" width="22" height="18" rx="1.5" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<text x="16" y="19" text-anchor="middle" fill="{ACCENT}" font-size="8.5" font-weight="700" font-family="sans-serif">PGP</text>'
    ),
    "appload": svg(
        f'<rect x="5" y="7" width="22" height="18" rx="1.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="16" y1="21" x2="16" y2="11" stroke="{ACCENT}" stroke-width="1.9"/>'
        f'<polyline points="12,14.5 16,10.5 20,14.5" stroke="{ACCENT}" stroke-width="1.8"/>'
    ),
    "script": svg(
        f'<path d="M8 5 H20 L25 10 V27 H8 Z" stroke="{INK}" stroke-width="1.7"/>'
        f'<polyline points="20,5 20,10 25,10" stroke="{INK}" stroke-width="1.4"/>'
        f'<polygon points="13,14 21,18.5 13,23" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'
    ),
    "audit": svg(
        f'<path d="M16 4 L26 8 V16 C26 22 21.5 26.2 16 28 C10.5 26.2 6 22 6 16 V8 Z" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<polyline points="11.5,16.5 15,20 21.5,12.5" stroke="{ACCENT}" stroke-width="2"/>'
    ),
    "purge": svg(
        f'<polyline points="7,9 25,9" stroke="{INK}" stroke-width="1.8"/>'
        f'<path d="M12 9 V6 H20 V9" stroke="{INK}" stroke-width="1.6"/>'
        f'<path d="M9 9 L10.5 26 H21.5 L23 9" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<line x1="13.5" y1="13" x2="14" y2="22" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<line x1="18.5" y1="13" x2="18" y2="22" stroke="{MUTED}" stroke-width="1.4"/>'
    ),
    "recover": svg(
        f'<path d="M8 5 H20 L25 10 V27 H8 Z" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="16.5" y1="14" x2="16.5" y2="22" stroke="{ACCENT}" stroke-width="2"/>'
        f'<line x1="12.5" y1="18" x2="20.5" y2="18" stroke="{ACCENT}" stroke-width="2"/>'
    ),

    # --- OUTPUT ---
    "plot": svg(
        f'<path d="M9 11 V5 H23 V11" stroke="{INK}" stroke-width="1.6"/>'
        f'<rect x="5" y="11" width="22" height="11" rx="1.5" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<rect x="9" y="18" width="14" height="9" fill="{SURF}" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<line x1="12" y1="22" x2="20" y2="22" stroke="{MUTED}" stroke-width="1.3"/>'
    ),
    "publish": svg(
        f'<rect x="5" y="9" width="14" height="17" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<rect x="11" y="5" width="16" height="19" fill="{SURF}" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="15" y1="11" x2="23" y2="11" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="15" y1="15" x2="23" y2="15" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<line x1="15" y1="19" x2="20" y2="19" stroke="{MUTED}" stroke-width="1.4"/>'
    ),
    "preview": svg(
        f'<path d="M8 5 H19 L24 10 V26 H8 Z" stroke="{INK}" stroke-width="1.6"/>'
        f'<circle cx="19" cy="19" r="5" fill="{SURF}" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="22.8" y1="22.8" x2="27" y2="27" stroke="{ACCENT}" stroke-width="2"/>'
    ),
    "pagesetup": svg(
        f'<rect x="6" y="5" width="20" height="22" stroke="{INK}" stroke-width="1.7"/>'
        f'<rect x="9.5" y="8.5" width="13" height="15" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="2.5 1.5"/>'
    ),
    "export_pdf": svg(
        f'<path d="M7 4 H19 L25 10 V27 H7 Z" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<polyline points="19,4 19,10 25,10" stroke="{INK}" stroke-width="1.5"/>'
        f'<rect x="8.5" y="15" width="15" height="7" rx="1" fill="{DANGER}" fill-opacity="0.25" stroke="{DANGER}" stroke-width="1.2"/>'
        f'<text x="16" y="20.6" text-anchor="middle" fill="{INK}" font-size="6.2" font-weight="700" font-family="sans-serif">PDF</text>'
    ),
    "export_other": svg(
        f'<path d="M7 21 V26 H25 V21" stroke="{INK}" stroke-width="1.8"/>'
        f'<line x1="16" y1="20" x2="16" y2="6" stroke="{ACCENT}" stroke-width="2"/>'
        f'<polyline points="11,11 16,5.5 21,11" stroke="{ACCENT}" stroke-width="2"/>'
    ),
    "etransmit": svg(
        f'<rect x="5" y="8" width="22" height="16" rx="1.5" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<polyline points="5,9 16,17 27,9" stroke="{ACCENT}" stroke-width="1.7"/>'
    ),

    # --- COLLABORATE ---
    "share": svg(
        f'<circle cx="23" cy="8" r="3" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<circle cx="9" cy="16" r="3" stroke="{INK}" stroke-width="1.7"/>'
        f'<circle cx="23" cy="24" r="3" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="11.8" y1="14.6" x2="20.2" y2="9.4" stroke="{INK}" stroke-width="1.6"/>'
        f'<line x1="11.8" y1="17.4" x2="20.2" y2="22.6" stroke="{INK}" stroke-width="1.6"/>'
    ),
    "compare": svg(
        f'<rect x="5" y="7" width="14" height="17" stroke="{INK}" stroke-width="1.6"/>'
        f'<rect x="13" y="9" width="14" height="17" stroke="{ACCENT}" stroke-width="1.6" fill="{SOFT}"/>'
    ),
    "traces": svg(
        f'<path d="M6 25 H26" stroke="{MUTED}" stroke-width="1.4"/>'
        f'<path d="M10 21 L22 9 L26 13 L14 25 L9 26 Z" fill="{SOFT}" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="19" y1="12" x2="23" y2="16" stroke="{ACCENT}" stroke-width="1.6"/>'
    ),
    "activity_insights": svg(
        f'<circle cx="16" cy="16" r="10.5" stroke="{INK}" stroke-width="1.7"/>'
        f'<polyline points="16,10 16,16 21,19" stroke="{ACCENT}" stroke-width="1.9"/>'
        f'<polyline points="5,10 5,15 10,15" stroke="{MUTED}" stroke-width="1.5"/>'
    ),

    # --- EXPRESS TOOLS ---
    "burst": svg(
        f'<rect x="10" y="10" width="12" height="12" stroke="{INK}" stroke-width="1.7" stroke-dasharray="3 2"/>'
        f'<line x1="6" y1="6" x2="10" y2="10" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="26" y1="6" x2="22" y2="10" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="6" y1="26" x2="10" y2="22" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="26" y1="26" x2="22" y2="22" stroke="{ACCENT}" stroke-width="1.7"/>'
    ),
    "superhatch": svg(
        f'<rect x="6" y="6" width="20" height="20" stroke="{INK}" stroke-width="1.7"/>'
        f'<line x1="6" y1="16" x2="16" y2="6" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="6" y1="26" x2="26" y2="6" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="16" y1="26" x2="26" y2="16" stroke="{ACCENT}" stroke-width="1.5"/>'
    ),
    "count_big": svg(
        f'<rect x="5" y="6" width="22" height="20" rx="1.5" stroke="{INK}" stroke-width="1.7" fill="{SOFT}"/>'
        f'<line x1="10" y1="12" x2="22" y2="12" stroke="{ACCENT}" stroke-width="1.7"/>'
        f'<line x1="10" y1="17" x2="22" y2="17" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="10" y1="22" x2="18" y2="22" stroke="{MUTED}" stroke-width="1.5"/>'
    ),
}


# =============================================================================
# SMALL RIBBON & TRAY ICONS (15x15, viewBox 0 0 20 20)
# =============================================================================
SM = {
    # --- DRAW SMALL ---
    "rect": sm(f'<rect x="3" y="4.5" width="14" height="11" stroke="{INK}" stroke-width="1.6"/>' + _node_sm(3, 4.5) + _node_sm(17, 15.5)),
    "ellipse": sm(f'<ellipse cx="10" cy="10" rx="7.5" ry="4.8" stroke="{INK}" stroke-width="1.6"/>' + _node_sm(10, 10)),
    "hatch": sm(
        f'<rect x="3" y="3.5" width="14" height="13" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="3" y1="10" x2="10" y2="3.5" stroke="{ACCENT}" stroke-width="1.3"/>'
        f'<line x1="3" y1="16.5" x2="16.5" y2="3.5" stroke="{ACCENT}" stroke-width="1.3"/>'
        f'<line x1="10" y1="16.5" x2="17" y2="9.5" stroke="{ACCENT}" stroke-width="1.3"/>'
    ),
    "spline_fit": sm(f'<path d="M3 15 C6 4, 14 16, 17 5" stroke="{INK}" stroke-width="1.6"/>' + _node_sm(3, 15) + _node_sm(10, 10) + _node_sm(17, 5)),
    "spline_cv": sm(f'<polyline points="3,15 7,4 13,16 17,5" stroke="{MUTED}" stroke-width="1.1" stroke-dasharray="2 1.5"/><path d="M3 15 C6 6, 14 14, 17 5" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "xline": sm(f'<line x1="3" y1="17" x2="17" y2="3" stroke="{INK}" stroke-width="1.5"/><polyline points="13,3 17,3 17,7" stroke="{ACCENT}" stroke-width="1.3"/><polyline points="7,17 3,17 3,13" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "ray": sm(f'<line x1="4" y1="16" x2="17" y2="3" stroke="{INK}" stroke-width="1.5"/><polyline points="13,3 17,3 17,7" stroke="{ACCENT}" stroke-width="1.3"/>' + _node_sm(4, 16)),
    "point": sm(f'<line x1="10" y1="4" x2="10" y2="16" stroke="{MUTED}" stroke-width="1.2"/><line x1="4" y1="10" x2="16" y2="10" stroke="{MUTED}" stroke-width="1.2"/>' + _node_sm(10, 10, 2.2)),
    "divide": sm(f'<line x1="2.5" y1="10" x2="17.5" y2="10" stroke="{INK}" stroke-width="1.5"/>' + _node_sm(6.5, 10) + _node_sm(10, 10) + _node_sm(13.5, 10)),
    "measure_pts": sm(f'<line x1="2.5" y1="10" x2="17.5" y2="10" stroke="{INK}" stroke-width="1.5"/><line x1="7" y1="7" x2="7" y2="13" stroke="{ACCENT}" stroke-width="1.5"/><line x1="13" y1="7" x2="13" y2="13" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "region": sm(f'<rect x="3.5" y="4" width="13" height="12" fill="{SOFT}" stroke="{INK}" stroke-width="1.6"/>'),
    "wipeout": sm(f'<polygon points="4,6 15,4 17,15 5,16" fill="{INK}" fill-opacity="0.25" stroke="{INK}" stroke-width="1.5"/>'),
    "poly3d": sm(f'<polyline points="3,15 8,6 13,12 17,4" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "helix": sm(f'<path d="M5 15 C5 12, 15 12, 15 10 C15 8, 5 8, 5 6 C5 4, 15 4, 15 3" stroke="{INK}" stroke-width="1.5"/>'),
    "donut": sm(f'<circle cx="10" cy="10" r="6" stroke="{INK}" stroke-width="3.2"/>'),
    "revcloud": sm(f'<path d="M5.5 14 H14.5 A3 3 0 0 0 15 8.2 A4.2 4.2 0 0 0 7 7.5 A3 3 0 0 0 5.5 14 Z" stroke="{INK}" stroke-width="1.5"/>'),

    # --- MODIFY SMALL ---
    "copy": sm(f'<circle cx="7.5" cy="12" r="4.2" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="2 1.2"/><circle cx="12.5" cy="8" r="4.2" stroke="{INK}" stroke-width="1.6" fill="{SOFT}"/>'),
    "mirror": sm(f'<polygon points="3,15 8,5 8,15" stroke="{MUTED}" stroke-width="1.4"/><line x1="10" y1="2.5" x2="10" y2="17.5" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="2 1.5"/><polygon points="17,15 12,5 12,15" stroke="{INK}" stroke-width="1.5" fill="{SOFT}"/>'),
    "fillet": sm(f'<path d="M4 16 V10 A6 6 0 0 1 10 4 H16" stroke="{INK}" stroke-width="1.7"/><path d="M4 10 A6 6 0 0 1 10 4" stroke="{ACCENT}" stroke-width="2"/>'),
    "stretch": sm(f'<rect x="3" y="6" width="7" height="8" stroke="{MUTED}" stroke-width="1.4"/><line x1="10" y1="10" x2="16.5" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><polyline points="14,7.5 17,10 14,12.5" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "scale": sm(f'<rect x="3" y="10" width="6" height="6" stroke="{MUTED}" stroke-width="1.4"/><rect x="3" y="4" width="13" height="12" stroke="{INK}" stroke-width="1.6"/>'),
    "array": sm(
        f'<rect x="3" y="3" width="4" height="4" fill="{ACCENT}"/>'
        f'<rect x="8.5" y="3" width="4" height="4" fill="{INK}"/>'
        f'<rect x="14" y="3" width="4" height="4" fill="{INK}"/>'
        f'<rect x="3" y="8.5" width="4" height="4" fill="{INK}"/>'
        f'<rect x="8.5" y="8.5" width="4" height="4" fill="{INK}"/>'
        f'<rect x="14" y="8.5" width="4" height="4" fill="{INK}"/>'
        f'<rect x="3" y="14" width="4" height="4" fill="{INK}"/>'
        f'<rect x="8.5" y="14" width="4" height="4" fill="{INK}"/>'
        f'<rect x="14" y="14" width="4" height="4" fill="{INK}"/>'
    ),
    "explode": sm(
        f'<line x1="4" y1="4" x2="7.5" y2="7.5" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<line x1="16" y1="4" x2="12.5" y2="7.5" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<line x1="4" y1="16" x2="7.5" y2="12.5" stroke="{INK}" stroke-width="1.6"/>'
        f'<line x1="16" y1="16" x2="12.5" y2="12.5" stroke="{INK}" stroke-width="1.6"/>'
    ),
    "offset_sm": sm(f'<path d="M4 16 V9 A5 5 0 0 1 9 4 H16" stroke="{MUTED}" stroke-width="1.4"/><path d="M8 16 V11 A3 3 0 0 1 11 8 H16" stroke="{INK}" stroke-width="1.6"/>'),
    "join": sm(f'<line x1="3" y1="10" x2="8.5" y2="10" stroke="{INK}" stroke-width="1.7"/><line x1="11.5" y1="10" x2="17" y2="10" stroke="{INK}" stroke-width="1.7"/><line x1="8.5" y1="10" x2="11.5" y2="10" stroke="{ACCENT}" stroke-width="2"/>'),
    "break": sm(f'<line x1="3" y1="10" x2="7.5" y2="10" stroke="{INK}" stroke-width="1.7"/><line x1="12.5" y1="10" x2="17" y2="10" stroke="{INK}" stroke-width="1.7"/><line x1="8" y1="7" x2="12" y2="13" stroke="{DANGER}" stroke-width="1.4"/>'),
    "break_pt": sm(f'<line x1="3" y1="10" x2="17" y2="10" stroke="{INK}" stroke-width="1.6"/><line x1="10" y1="5" x2="10" y2="15" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "align": sm(f'<line x1="3" y1="16" x2="17" y2="16" stroke="{ACCENT}" stroke-width="1.6"/><rect x="5" y="6" width="10" height="7" stroke="{INK}" stroke-width="1.5"/>'),
    "overkill": sm(f'<line x1="3" y1="8" x2="17" y2="8" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="2 1.5"/><line x1="3" y1="12" x2="17" y2="12" stroke="{INK}" stroke-width="1.8"/>'),
    "pedit": sm(f'<polyline points="3,15 8,5 13,13 17,6" stroke="{INK}" stroke-width="1.6"/>' + _node_sm(8, 5) + _node_sm(13, 13)),
    "lengthen": sm(f'<line x1="3" y1="10" x2="12" y2="10" stroke="{INK}" stroke-width="1.7"/><line x1="12" y1="10" x2="17" y2="10" stroke="{ACCENT}" stroke-width="1.7" stroke-dasharray="2 1.2"/>'),
    "draw_front": sm(f'<rect x="7" y="7" width="10" height="10" stroke="{MUTED}" stroke-width="1.3"/><rect x="3" y="3" width="10" height="10" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "draw_back": sm(f'<rect x="3" y="3" width="10" height="10" stroke="{MUTED}" stroke-width="1.3"/><rect x="7" y="7" width="10" height="10" fill="{SOFT}" stroke="{INK}" stroke-width="1.6"/>'),
    "setbylayer": sm(f'<polygon points="10,3 17,7 10,11 3,7" stroke="{ACCENT}" stroke-width="1.4" fill="{SOFT}"/><polyline points="3,11.5 10,15.5 17,11.5" stroke="{INK}" stroke-width="1.5"/>'),
    "chspace": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.5"/><line x1="7" y1="10" x2="13" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><polyline points="11,8 13.5,10 11,12" stroke="{ACCENT}" stroke-width="1.4"/>'),

    # --- LAYERS QUICK BAR (Authentic CAD SVG Icons replacing ALL emojis!) ---
    "lay_off": sm(
        f'<path d="M10 3.5 A4.2 4.2 0 0 0 7.3 11 V13 H12.7 V11 A4.2 4.2 0 0 0 10 3.5 Z" stroke="{INK}" stroke-width="1.5"/>'
        f'<line x1="8" y1="15.5" x2="12" y2="15.5" stroke="{MUTED}" stroke-width="1.5"/>'
        f'<line x1="4" y1="4" x2="16" y2="16" stroke="{DANGER}" stroke-width="1.5"/>'
    ),
    "lay_on": sm(
        f'<path d="M10 4 A4 4 0 0 0 7.5 11.2 V13 H12.5 V11.2 A4 4 0 0 0 10 4 Z" fill="{NODE}" fill-opacity="0.32" stroke="{NODE}" stroke-width="1.5"/>'
        f'<line x1="8" y1="15.5" x2="12" y2="15.5" stroke="{INK}" stroke-width="1.5"/>'
    ),
    "lay_iso": sm(
        f'<polygon points="10,3 17,6.5 10,10 3,6.5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<polyline points="3,13.5 10,17 17,13.5" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="2 1.5"/>'
    ),
    "lay_uniso": sm(
        f'<polygon points="10,3 17,6.5 10,10 3,6.5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4"/>'
        f'<polyline points="3,10.5 10,14 17,10.5" stroke="{INK}" stroke-width="1.4"/>'
        f'<polyline points="3,14 10,17.5 17,14" stroke="{INK}" stroke-width="1.4"/>'
    ),
    "lay_frz": sm(
        f'<line x1="10" y1="3" x2="10" y2="17" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="4" y1="6.5" x2="16" y2="13.5" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="16" y1="6.5" x2="4" y2="13.5" stroke="{ACCENT}" stroke-width="1.5"/>'
    ),
    "lay_thw": sm(
        f'<circle cx="10" cy="10" r="3.5" fill="{NODE}" fill-opacity="0.3" stroke="{NODE}" stroke-width="1.5"/>'
        f'<line x1="10" y1="2.5" x2="10" y2="4.5" stroke="{NODE}" stroke-width="1.4"/>'
        f'<line x1="10" y1="15.5" x2="10" y2="17.5" stroke="{NODE}" stroke-width="1.4"/>'
        f'<line x1="2.5" y1="10" x2="4.5" y2="10" stroke="{NODE}" stroke-width="1.4"/>'
        f'<line x1="15.5" y1="10" x2="17.5" y2="10" stroke="{NODE}" stroke-width="1.4"/>'
    ),
    "lay_lock": sm(
        f'<rect x="5" y="9" width="10" height="8" rx="1.2" fill="{NODE}" fill-opacity="0.28" stroke="{NODE}" stroke-width="1.5"/>'
        f'<path d="M7.5 9 V6.5 A2.5 2.5 0 0 1 12.5 6.5 V9" stroke="{INK}" stroke-width="1.5"/>'
    ),
    "lay_unlock": sm(
        f'<rect x="5" y="9.5" width="10" height="7.5" rx="1.2" stroke="{INK}" stroke-width="1.5"/>'
        f'<path d="M7.5 9.5 V6.5 A2.5 2.5 0 0 1 12.5 6.5" stroke="{ACCENT}" stroke-width="1.5"/>'
    ),
    "lay_mcur": sm(
        f'<polygon points="10,4 17,7.5 10,11 3,7.5" stroke="{INK}" stroke-width="1.4"/>'
        f'<polyline points="6,14.5 9,17 15,11.5" stroke="{ACCENT}" stroke-width="1.8"/>'
    ),
    "lay_mch": sm(
        f'<polygon points="10,3 17,6.5 10,10 3,6.5" stroke="{MUTED}" stroke-width="1.3"/>'
        f'<polygon points="10,10 17,13.5 10,17 3,13.5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'
    ),
    "lay_cur": sm(
        f'<polygon points="10,10 17,13.5 10,17 3,13.5" stroke="{INK}" stroke-width="1.4"/>'
        f'<line x1="10" y1="3" x2="10" y2="10" stroke="{ACCENT}" stroke-width="1.6"/>'
        f'<polyline points="7.5,7.5 10,10.5 12.5,7.5" stroke="{ACCENT}" stroke-width="1.4"/>'
    ),

    # --- PROPERTIES COMBO INDICATORS ---
    "prop_lw": sm(
        f'<line x1="2" y1="5" x2="18" y2="5" stroke="{MUTED}" stroke-width="1"/>'
        f'<line x1="2" y1="10" x2="18" y2="10" stroke="{INK}" stroke-width="2"/>'
        f'<line x1="2" y1="15.5" x2="18" y2="15.5" stroke="{ACCENT}" stroke-width="3"/>'
    ),
    "prop_lt": sm(
        f'<line x1="2" y1="5" x2="18" y2="5" stroke="{INK}" stroke-width="1.4"/>'
        f'<line x1="2" y1="10" x2="18" y2="10" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="4 2"/>'
        f'<line x1="2" y1="15" x2="18" y2="15" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="1.5 2"/>'
    ),

    # --- BLOCKS, GROUPS, UTILITIES, CLIPBOARD SMALL ---
    "blk_create": sm(f'<rect x="3.5" y="4.5" width="11" height="11" stroke="{INK}" stroke-width="1.5"/><line x1="15" y1="3" x2="15" y2="9" stroke="{ACCENT}" stroke-width="1.6"/><line x1="12" y1="6" x2="18" y2="6" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "blk_edit": sm(f'<rect x="3" y="5" width="11" height="11" stroke="{MUTED}" stroke-width="1.4"/><path d="M10 14 L16 8 L18 10 L12 16 Z" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "blk_attr": sm(f'<path d="M3 10 L9 4 H16 V11 L10 17 Z" stroke="{INK}" stroke-width="1.5"/>' + _node_sm(13, 7)),
    "blk_wblock": sm(f'<rect x="3" y="6" width="11" height="11" stroke="{INK}" stroke-width="1.5"/><line x1="11" y1="9" x2="17" y2="3" stroke="{ACCENT}" stroke-width="1.6"/><polyline points="13,3 17,3 17,7" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "blk_base": sm(f'<circle cx="10" cy="10" r="4" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="2.5" x2="10" y2="17.5" stroke="{ACCENT}" stroke-width="1.3"/><line x1="2.5" y1="10" x2="17.5" y2="10" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "blk_sync": sm(f'<path d="M16 9 A6 6 0 1 0 14.5 14" stroke="{INK}" stroke-width="1.5"/><polyline points="13,6 16.5,9 18,5.5" stroke="{ACCENT}" stroke-width="1.4"/>'),

    "ungroup": sm(f'<rect x="3" y="3" width="6" height="6" stroke="{INK}" stroke-width="1.5"/><rect x="11" y="11" width="6" height="6" stroke="{ACCENT}" stroke-width="1.5"/><line x1="4" y1="16" x2="16" y2="4" stroke="{DANGER}" stroke-width="1.3"/>'),
    "group_edit": sm(f'<rect x="3" y="3" width="14" height="14" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="2 1.5"/><circle cx="10" cy="10" r="3" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "group_toggle": sm(f'<rect x="3.5" y="3.5" width="13" height="13" stroke="{INK}" stroke-width="1.5"/><polyline points="6.5,10 9,12.5 14,7" stroke="{ACCENT}" stroke-width="1.7"/>'),

    "qselect": sm(f'<polygon points="3,4 17,4 12,10 12,16 8,14 8,10" stroke="{INK}" stroke-width="1.5" fill="{SOFT}"/>'),
    "sel_all": sm(f'<rect x="3" y="3" width="14" height="14" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="2.5 1.5"/><rect x="6.5" y="6.5" width="7" height="7" fill="{SOFT}" stroke="{INK}" stroke-width="1.4"/>'),
    "sel_similar": sm(f'<rect x="3" y="4" width="6" height="6" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/><rect x="11" y="10" width="6" height="6" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "calc": sm(f'<rect x="4" y="2.5" width="12" height="15" rx="1.2" stroke="{INK}" stroke-width="1.5"/><rect x="6.5" y="5" width="7" height="3" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.1"/><circle cx="7.5" cy="11.5" r="0.9" fill="{INK}"/><circle cx="10" cy="11.5" r="0.9" fill="{INK}"/><circle cx="12.5" cy="11.5" r="0.9" fill="{INK}"/><circle cx="7.5" cy="14.5" r="0.9" fill="{INK}"/><circle cx="10" cy="14.5" r="0.9" fill="{INK}"/><circle cx="12.5" cy="14.5" r="0.9" fill="{ACCENT}"/>'),
    "isolate_obj": sm(f'<circle cx="10" cy="10" r="4" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.6"/><circle cx="10" cy="10" r="7.5" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="2 2"/>'),
    "count_sm": sm(f'<rect x="3.5" y="3.5" width="13" height="13" rx="1" stroke="{INK}" stroke-width="1.5"/><line x1="6.5" y1="8" x2="13.5" y2="8" stroke="{ACCENT}" stroke-width="1.5"/><line x1="6.5" y1="12" x2="11.5" y2="12" stroke="{INK}" stroke-width="1.5"/>'),

    "cut": sm(f'<circle cx="6" cy="14.5" r="2.2" stroke="{INK}" stroke-width="1.4"/><circle cx="14" cy="14.5" r="2.2" stroke="{INK}" stroke-width="1.4"/><line x1="7.5" y1="12.8" x2="14" y2="4" stroke="{INK}" stroke-width="1.5"/><line x1="12.5" y1="12.8" x2="6" y2="4" stroke="{INK}" stroke-width="1.5"/>'),
    "copyclip": sm(f'<rect x="7" y="6" width="9" height="11" stroke="{INK}" stroke-width="1.5" fill="{SOFT}"/><path d="M13 6 V3.5 H4 V14 H7" stroke="{MUTED}" stroke-width="1.4"/>'),
    "copybase": sm(f'<rect x="6" y="6" width="10" height="10" stroke="{INK}" stroke-width="1.5"/>' + _node_sm(6, 16, 2)),

    # --- ANNOTATE SMALL ---
    "dim_lin": sm(f'<line x1="3" y1="5" x2="3" y2="15" stroke="{MUTED}" stroke-width="1.3"/><line x1="17" y1="5" x2="17" y2="15" stroke="{MUTED}" stroke-width="1.3"/><line x1="3" y1="10" x2="17" y2="10" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "dim_ali": sm(f'<line x1="4" y1="15" x2="16" y2="5" stroke="{ACCENT}" stroke-width="1.7"/>' + _node_sm(4, 15) + _node_sm(16, 5)),
    "dim_ang": sm(f'<line x1="4" y1="15" x2="16" y2="15" stroke="{INK}" stroke-width="1.4"/><line x1="4" y1="15" x2="14" y2="4" stroke="{INK}" stroke-width="1.4"/><path d="M11.5 15 A7.5 7.5 0 0 0 9.5 9" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "dim_rad": sm(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="10" x2="15.5" y2="6.5" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "dim_dia": sm(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/><line x1="5" y1="15" x2="15" y2="5" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "dim_cont": sm(f'<line x1="2" y1="10" x2="18" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><line x1="3" y1="6" x2="3" y2="14" stroke="{INK}" stroke-width="1.4"/><line x1="10" y1="6" x2="10" y2="14" stroke="{INK}" stroke-width="1.4"/><line x1="17" y1="6" x2="17" y2="14" stroke="{INK}" stroke-width="1.4"/>'),
    "dim_base": sm(f'<line x1="3" y1="4" x2="3" y2="16" stroke="{INK}" stroke-width="1.5"/><line x1="3" y1="7" x2="11" y2="7" stroke="{ACCENT}" stroke-width="1.5"/><line x1="3" y1="13" x2="17" y2="13" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "dim_style": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.5"/><line x1="6" y1="10" x2="14" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><line x1="6" y1="7" x2="6" y2="13" stroke="{MUTED}" stroke-width="1.3"/><line x1="14" y1="7" x2="14" y2="13" stroke="{MUTED}" stroke-width="1.3"/>'),
    "dim_break": sm(f'<line x1="3" y1="10" x2="8" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><line x1="12" y1="10" x2="17" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><line x1="10" y1="3" x2="10" y2="17" stroke="{INK}" stroke-width="1.5"/>'),
    "dim_space": sm(f'<line x1="3" y1="6" x2="17" y2="6" stroke="{INK}" stroke-width="1.5"/><line x1="3" y1="14" x2="17" y2="14" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="6" x2="10" y2="14" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "tolerance": sm(f'<rect x="2.5" y="6" width="15" height="8" stroke="{INK}" stroke-width="1.4"/><line x1="8" y1="6" x2="8" y2="14" stroke="{INK}" stroke-width="1.3"/><line x1="13" y1="6" x2="13" y2="14" stroke="{INK}" stroke-width="1.3"/><circle cx="5.2" cy="10" r="1.4" stroke="{ACCENT}" stroke-width="1.2"/>'),
    "centermark": sm(f'<circle cx="10" cy="10" r="6" stroke="{INK}" stroke-width="1.4"/><line x1="10" y1="2.5" x2="10" y2="17.5" stroke="{ACCENT}" stroke-width="1.4"/><line x1="2.5" y1="10" x2="17.5" y2="10" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "centerline": sm(f'<line x1="4" y1="4" x2="4" y2="16" stroke="{INK}" stroke-width="1.5"/><line x1="16" y1="4" x2="16" y2="16" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="3" x2="10" y2="17" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="3.5 1.8"/>'),
    "leader_sm": sm(f'<polyline points="3,16 9,7 17,7" stroke="{INK}" stroke-width="1.6"/><polygon points="3,16 7,13.5 4.8,11.5" fill="{ACCENT}"/>'),
    "leader_add": sm(f'<polyline points="3,15 9,8 16,8" stroke="{INK}" stroke-width="1.5"/><line x1="14" y1="11.5" x2="14" y2="17.5" stroke="{ACCENT}" stroke-width="1.6"/><line x1="11" y1="14.5" x2="17" y2="14.5" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "leader_rem": sm(f'<polyline points="3,15 9,8 16,8" stroke="{INK}" stroke-width="1.5"/><line x1="11" y1="14.5" x2="17" y2="14.5" stroke="{DANGER}" stroke-width="1.7"/>'),
    "leader_align": sm(f'<line x1="14" y1="3" x2="14" y2="17" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="2 1.5"/><line x1="4" y1="6" x2="14" y2="6" stroke="{INK}" stroke-width="1.5"/><line x1="4" y1="10" x2="14" y2="10" stroke="{INK}" stroke-width="1.5"/><line x1="4" y1="14" x2="14" y2="14" stroke="{INK}" stroke-width="1.5"/>'),
    "leader_collect": sm(f'<rect x="3" y="4" width="5" height="5" stroke="{INK}" stroke-width="1.4"/><rect x="12" y="4" width="5" height="5" stroke="{INK}" stroke-width="1.4"/><rect x="7.5" y="12" width="5" height="5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "table_sm": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.5"/><line x1="3" y1="8" x2="17" y2="8" stroke="{ACCENT}" stroke-width="1.4"/><line x1="3" y1="12" x2="17" y2="12" stroke="{MUTED}" stroke-width="1.2"/><line x1="10" y1="8" x2="10" y2="16" stroke="{MUTED}" stroke-width="1.2"/>'),
    "text_style": sm(f'<path d="M4 15 L8.5 5 L13 15" stroke="{INK}" stroke-width="1.6"/><line x1="5.8" y1="11.5" x2="11.2" y2="11.5" stroke="{INK}" stroke-width="1.4"/><line x1="14" y1="15" x2="18" y2="15" stroke="{ACCENT}" stroke-width="1.8"/>'),
    "find_text": sm(f'<circle cx="8.5" cy="8.5" r="5" stroke="{INK}" stroke-width="1.6"/><line x1="12.5" y1="12.5" x2="17" y2="17" stroke="{ACCENT}" stroke-width="2"/>'),
    "spell": sm(f'<path d="M4 11 L7 4 L10 11" stroke="{INK}" stroke-width="1.5"/><polyline points="10,14.5 12.5,17 17,11.5" stroke="{ACCENT}" stroke-width="1.7"/>'),

    # --- PARAMETRIC CONSTRAINTS ---
    "c_coincident": sm(f'<circle cx="10" cy="10" r="5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.6"/>' + _node_sm(10, 10, 2)),
    "c_collinear": sm(f'<line x1="3" y1="14" x2="8.5" y2="10.5" stroke="{INK}" stroke-width="1.8"/><line x1="11.5" y1="8.5" x2="17" y2="5" stroke="{ACCENT}" stroke-width="1.8"/>'),
    "c_concentric": sm(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/><circle cx="10" cy="10" r="3" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "c_parallel": sm(f'<line x1="6" y1="16" x2="11" y2="4" stroke="{INK}" stroke-width="1.8"/><line x1="11" y1="16" x2="16" y2="4" stroke="{ACCENT}" stroke-width="1.8"/>'),
    "c_perp": sm(f'<line x1="3" y1="15.5" x2="17" y2="15.5" stroke="{INK}" stroke-width="1.8"/><line x1="10" y1="4" x2="10" y2="15.5" stroke="{ACCENT}" stroke-width="1.8"/><rect x="10" y="12" width="3.5" height="3.5" stroke="{MUTED}" stroke-width="1.1"/>'),
    "c_tangent": sm(f'<circle cx="8" cy="11" r="5" stroke="{INK}" stroke-width="1.6"/><line x1="13" y1="3.5" x2="13" y2="17" stroke="{ACCENT}" stroke-width="1.7"/>'),
    "c_horiz": sm(f'<line x1="3" y1="10" x2="17" y2="10" stroke="{ACCENT}" stroke-width="2"/>'),
    "c_vert": sm(f'<line x1="10" y1="3" x2="10" y2="17" stroke="{ACCENT}" stroke-width="2"/>'),
    "c_equal": sm(f'<line x1="4" y1="7.5" x2="16" y2="7.5" stroke="{INK}" stroke-width="1.9"/><line x1="4" y1="12.5" x2="16" y2="12.5" stroke="{ACCENT}" stroke-width="1.9"/>'),
    "c_fix": sm(f'<rect x="5" y="9" width="10" height="8" rx="1" fill="{SOFT}" stroke="{NODE}" stroke-width="1.5"/><path d="M7.5 9 V6.5 A2.5 2.5 0 0 1 12.5 6.5 V9" stroke="{INK}" stroke-width="1.5"/>'),
    "c_smooth": sm(f'<path d="M3 15 C7 15, 7 5, 11 5 C14 5, 14 10, 17 10" stroke="{ACCENT}" stroke-width="1.7"/>'),
    "c_symm": sm(f'<line x1="10" y1="3" x2="10" y2="17" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="2 1.5"/><rect x="3.5" y="7" width="4" height="6" stroke="{INK}" stroke-width="1.5"/><rect x="12.5" y="7" width="4" height="6" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "c_convert": sm(f'<line x1="3" y1="10" x2="13" y2="10" stroke="{INK}" stroke-width="1.6"/><polyline points="10,7 13.5,10 10,13" stroke="{ACCENT}" stroke-width="1.6"/><rect x="14.5" y="7" width="3" height="6" fill="{ACCENT}"/>'),
    "c_delete": sm(f'<line x1="5" y1="5" x2="15" y2="15" stroke="{DANGER}" stroke-width="1.8"/><line x1="15" y1="5" x2="5" y2="15" stroke="{DANGER}" stroke-width="1.8"/>'),
    "c_params": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.5"/><text x="10" y="13.2" text-anchor="middle" fill="{ACCENT}" font-size="8.5" font-weight="700" font-style="italic" font-family="serif">fx</text>'),
    "c_show": sm(f'<path d="M2.5 10 C4.5 6, 15.5 6, 17.5 10 C15.5 14, 4.5 14, 2.5 10 Z" stroke="{INK}" stroke-width="1.5"/><circle cx="10" cy="10" r="2.3" fill="{ACCENT}"/>'),
    "c_settings": sm(f'<circle cx="10" cy="10" r="3" stroke="{ACCENT}" stroke-width="1.6"/><circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.4" stroke-dasharray="2.5 2"/>'),

    # --- 3D SMALL ---
    "cyl": sm(f'<ellipse cx="10" cy="5.5" rx="5.5" ry="2.5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4"/><path d="M4.5 5.5 V14.5 A5.5 2.5 0 0 0 15.5 14.5 V5.5" stroke="{INK}" stroke-width="1.5"/>'),
    "sphere": sm(f'<circle cx="10" cy="10" r="6.5" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/><ellipse cx="10" cy="10" rx="6.5" ry="2.5" stroke="{ACCENT}" stroke-width="1.2"/>'),
    "cone": sm(f'<ellipse cx="10" cy="15" rx="5.5" ry="2.2" stroke="{INK}" stroke-width="1.4"/><line x1="4.5" y1="15" x2="10" y2="3.5" stroke="{INK}" stroke-width="1.5"/><line x1="15.5" y1="15" x2="10" y2="3.5" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "wedge": sm(f'<polygon points="4,15 16,15 16,5" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/><polyline points="4,15 7,12 16,5" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "pyramid": sm(f'<polygon points="10,3.5 3.5,14 10,16.5 16.5,14" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="3.5" x2="10" y2="16.5" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "torus": sm(f'<ellipse cx="10" cy="10" rx="7" ry="4.5" stroke="{INK}" stroke-width="1.6"/><ellipse cx="10" cy="10" rx="3" ry="1.6" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "polysolid": sm(f'<path d="M3 14 L8 6 L14 11 L17 6" stroke="{INK}" stroke-width="2.2"/>'),
    "revolve": sm(f'<line x1="6" y1="3" x2="6" y2="17" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="2 1.5"/><path d="M9 5 C15 5, 15 15, 9 15" stroke="{ACCENT}" stroke-width="1.6" fill="{SOFT}"/>'),
    "sweep": sm(f'<path d="M4 16 C4 9, 16 11, 16 4" stroke="{ACCENT}" stroke-width="1.7"/><circle cx="4" cy="16" r="2" stroke="{INK}" stroke-width="1.3"/>'),
    "loft": sm(f'<ellipse cx="10" cy="5" rx="3.5" ry="1.6" stroke="{ACCENT}" stroke-width="1.4"/><ellipse cx="10" cy="15" rx="6" ry="2.2" stroke="{INK}" stroke-width="1.4"/><line x1="6.5" y1="5" x2="4" y2="15" stroke="{INK}" stroke-width="1.4"/><line x1="13.5" y1="5" x2="16" y2="15" stroke="{INK}" stroke-width="1.4"/>'),
    "union": sm(f'<circle cx="7.5" cy="10" r="4.5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/><circle cx="12.5" cy="10" r="4.5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "subtract": sm(f'<circle cx="7.5" cy="10" r="4.5" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/><circle cx="12.5" cy="10" r="4.5" stroke="{DANGER}" stroke-width="1.4" stroke-dasharray="2 1.5"/>'),
    "intersect": sm(f'<circle cx="7.5" cy="10" r="4.5" stroke="{MUTED}" stroke-width="1.4"/><circle cx="12.5" cy="10" r="4.5" stroke="{MUTED}" stroke-width="1.4"/><path d="M10 6.2 A4.5 4.5 0 0 1 10 13.8 A4.5 4.5 0 0 1 10 6.2 Z" fill="{ACCENT}"/>'),
    "slice": sm(f'<rect x="4" y="4" width="12" height="12" stroke="{INK}" stroke-width="1.5"/><line x1="3" y1="17" x2="17" y2="3" stroke="{ACCENT}" stroke-width="1.7"/>'),
    "thicken": sm(f'<path d="M4 11 Q10 6 16 11" stroke="{INK}" stroke-width="1.6"/><path d="M4 14.5 Q10 9.5 16 14.5" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "filletedge": sm(f'<path d="M4 16 V9 A5 5 0 0 1 9 4 H16" stroke="{INK}" stroke-width="1.6"/><path d="M4 9 A5 5 0 0 1 9 4" stroke="{ACCENT}" stroke-width="2.2"/>'),
    "chamferedge": sm(f'<polyline points="4,16 4,9 9,4 16,4" stroke="{INK}" stroke-width="1.6"/><line x1="4" y1="9" x2="9" y2="4" stroke="{ACCENT}" stroke-width="2.2"/>'),
    "solidedit": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4"/><polyline points="3,7 3,14 10,17.5 17,14 17,7" stroke="{INK}" stroke-width="1.4"/>'),
    "interfere": sm(f'<rect x="3" y="4" width="9" height="9" stroke="{INK}" stroke-width="1.4"/><rect x="8" y="7" width="9" height="9" stroke="{ACCENT}" stroke-width="1.4"/><rect x="8" y="7" width="4" height="6" fill="{DANGER}" fill-opacity="0.4"/>'),
    "move3d": sm(f'<line x1="10" y1="3" x2="10" y2="17" stroke="{ACCENT}" stroke-width="1.6"/><line x1="3" y1="10" x2="17" y2="10" stroke="{INK}" stroke-width="1.6"/>'),
    "rot3d": sm(f'<circle cx="10" cy="10" r="6" stroke="{ACCENT}" stroke-width="1.5"/><ellipse cx="10" cy="10" rx="6" ry="2.5" stroke="{INK}" stroke-width="1.3"/>'),
    "scale3d": sm(f'<polygon points="10,4 16,7.5 10,11 4,7.5" stroke="{ACCENT}" stroke-width="1.4"/><rect x="6" y="11" width="8" height="6" stroke="{INK}" stroke-width="1.4"/>'),
    "mirror3d": sm(f'<line x1="10" y1="2.5" x2="10" y2="17.5" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="2 1.5"/><polygon points="3,15 8,6 8,15" stroke="{MUTED}" stroke-width="1.4"/><polygon points="17,15 12,6 12,15" stroke="{INK}" stroke-width="1.5"/>'),
    "section": sm(f'<polygon points="3,15 16,15 16,5" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/><line x1="3" y1="15" x2="16" y2="5" stroke="{INK}" stroke-width="1.6"/>'),
    "flatshot": sm(f'<rect x="3" y="11" width="14" height="5" stroke="{ACCENT}" stroke-width="1.5"/><polygon points="10,3 15,6 10,9 5,6" stroke="{INK}" stroke-width="1.3"/>'),
    "materials": sm(f'<circle cx="10" cy="10" r="6.5" fill="{SOFT}" stroke="{INK}" stroke-width="1.5"/><path d="M10 3.5 A6.5 6.5 0 0 1 16.5 10 H10 Z" fill="{ACCENT}"/>'),
    "render": sm(f'<rect x="3" y="4" width="14" height="12" rx="1" stroke="{INK}" stroke-width="1.5"/><circle cx="10" cy="10" r="3" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "convert_solid": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{ACCENT}" fill-opacity="0.3" stroke="{ACCENT}" stroke-width="1.4"/><polygon points="3,7 10,11 10,17 3,13" stroke="{INK}" stroke-width="1.4"/><polygon points="17,7 10,11 10,17 17,13" stroke="{INK}" stroke-width="1.4"/>'),

    # --- VISUAL STYLES (Authentic 3D Cubes instead of generic triangles!) ---
    "vs_2d": sm(f'<polygon points="10,3 17,7 10,11 3,7" stroke="{INK}" stroke-width="1.3"/><polyline points="3,7 3,13.5 10,17 17,13.5 17,7" stroke="{INK}" stroke-width="1.3"/><line x1="10" y1="11" x2="10" y2="17" stroke="{MUTED}" stroke-width="1.1"/>'),
    "vs_concept": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{ACCENT}" fill-opacity="0.45" stroke="{ACCENT}" stroke-width="1.3"/><polygon points="3,7 10,11 10,17 3,13.5" fill="{SOFT}" stroke="{INK}" stroke-width="1.3"/><polygon points="17,7 10,11 10,17 17,13.5" fill="{INK}" fill-opacity="0.2" stroke="{INK}" stroke-width="1.3"/>'),
    "vs_hidden": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{SURF}" stroke="{INK}" stroke-width="1.4"/><polygon points="3,7 10,11 10,17 3,13.5" fill="{SURF}" stroke="{INK}" stroke-width="1.4"/><polygon points="17,7 10,11 10,17 17,13.5" fill="{SURF}" stroke="{INK}" stroke-width="1.4"/>'),
    "vs_realistic": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{INK}" fill-opacity="0.45" stroke="{INK}" stroke-width="1.2"/><polygon points="3,7 10,11 10,17 3,13.5" fill="{INK}" fill-opacity="0.25" stroke="{INK}" stroke-width="1.2"/><polygon points="17,7 10,11 10,17 17,13.5" fill="{ACCENT}" fill-opacity="0.35" stroke="{INK}" stroke-width="1.2"/>'),
    "vs_shaded": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{ACCENT}" fill-opacity="0.55"/><polygon points="3,7 10,11 10,17 3,13.5" fill="{ACCENT}" fill-opacity="0.28"/><polygon points="17,7 10,11 10,17 17,13.5" fill="{ACCENT}" fill-opacity="0.4"/>'),
    "vs_xray": sm(f'<polygon points="10,3 17,7 10,11 3,7" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.2"/><polyline points="3,7 3,13.5 10,17 17,13.5 17,7" stroke="{ACCENT}" stroke-width="1.2" stroke-dasharray="2 1.2"/><line x1="10" y1="3" x2="10" y2="17" stroke="{MUTED}" stroke-width="1" stroke-dasharray="1.5 1.5"/>'),

    # --- VIEW / MANAGE / INSERT / COLLABORATE / EXPRESS SMALL ---
    "viewcube": sm(f'<polygon points="10,3 16.5,6.8 10,10.5 3.5,6.8" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4"/><polygon points="3.5,6.8 10,10.5 10,17 3.5,13.2" stroke="{INK}" stroke-width="1.4"/><polygon points="16.5,6.8 10,10.5 10,17 16.5,13.2" stroke="{INK}" stroke-width="1.4"/>'),
    "ucs_icon": sm(f'<line x1="5" y1="15" x2="5" y2="4" stroke="{ACCENT}" stroke-width="1.6"/><line x1="5" y1="15" x2="16" y2="15" stroke="{INK}" stroke-width="1.6"/>'),
    "cmdline": sm(f'<rect x="3" y="5" width="14" height="10" rx="1" stroke="{INK}" stroke-width="1.5"/><line x1="6" y1="10" x2="14" y2="10" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "sheetset": sm(f'<rect x="5" y="3" width="11" height="14" stroke="{INK}" stroke-width="1.4"/><path d="M5 6 H3.5 V17 H13 V15.5" stroke="{MUTED}" stroke-width="1.3"/><line x1="8" y1="7" x2="13" y2="7" stroke="{ACCENT}" stroke-width="1.4"/><line x1="8" y1="10.5" x2="13" y2="10.5" stroke="{MUTED}" stroke-width="1.3"/>'),
    "reset_pal": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.4"/><line x1="12" y1="4" x2="12" y2="16" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "units": sm(f'<rect x="3" y="6" width="14" height="8" stroke="{INK}" stroke-width="1.5"/><line x1="6.5" y1="6" x2="6.5" y2="10" stroke="{ACCENT}" stroke-width="1.4"/><line x1="10" y1="6" x2="10" y2="11" stroke="{ACCENT}" stroke-width="1.4"/><line x1="13.5" y1="6" x2="13.5" y2="10" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "options": sm(f'<line x1="3" y1="6" x2="17" y2="6" stroke="{MUTED}" stroke-width="1.4"/><circle cx="7" cy="6" r="2" fill="{SURF}" stroke="{ACCENT}" stroke-width="1.5"/><line x1="3" y1="14" x2="17" y2="14" stroke="{MUTED}" stroke-width="1.4"/><circle cx="13" cy="14" r="2" fill="{SURF}" stroke="{INK}" stroke-width="1.5"/>'),
    "ref_clip": sm(f'<rect x="4" y="4" width="12" height="12" stroke="{INK}" stroke-width="1.5"/><rect x="7" y="7" width="9" height="9" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="2 1.5"/>'),
    "ref_adjust": sm(f'<circle cx="10" cy="10" r="6" stroke="{INK}" stroke-width="1.5"/><path d="M10 4 A6 6 0 0 1 10 16 Z" fill="{ACCENT}"/>'),
    "ref_xbind": sm(f'<rect x="3" y="6" width="7" height="8" stroke="{INK}" stroke-width="1.5"/><rect x="10" y="6" width="7" height="8" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "ref_dwg": sm(f'<path d="M5 3 H12 L16 7 V17 H5 Z" stroke="{INK}" stroke-width="1.4"/><rect x="7" y="10" width="6" height="4" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "ref_img": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.5"/><polyline points="4,14 8,9.5 11.5,12.5 14,10 16,13" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "pdf_shx": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.4"/><path d="M7 13 L10 7 L13 13" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "markup_imp": sm(f'<path d="M4 14 V17 H16 V14" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="4" x2="10" y2="13" stroke="{ACCENT}" stroke-width="1.6"/><polyline points="7,10 10,13.5 13,10" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "markup_assist": sm(
        # Technical markup review check icon (NO generic AI star!)
        f'<rect x="3" y="4" width="14" height="12" rx="1.2" stroke="{INK}" stroke-width="1.5"/>'
        f'<polyline points="6.5,10 9,12.5 14,7.5" stroke="{ACCENT}" stroke-width="1.7"/>'
    ),
    "zoom_ext": sm(f'<rect x="4" y="4" width="12" height="12" stroke="{INK}" stroke-width="1.5"/><polyline points="4,8 4,4 8,4" stroke="{ACCENT}" stroke-width="2"/><polyline points="12,16 16,16 16,12" stroke="{ACCENT}" stroke-width="2"/>'),
    "list_info": sm(f'<rect x="4" y="3" width="12" height="14" stroke="{INK}" stroke-width="1.5"/><line x1="7" y1="7" x2="13" y2="7" stroke="{ACCENT}" stroke-width="1.5"/><line x1="7" y1="10.5" x2="13" y2="10.5" stroke="{INK}" stroke-width="1.4"/><line x1="7" y1="14" x2="11" y2="14" stroke="{MUTED}" stroke-width="1.4"/>'),
    "export_layout": sm(f'<rect x="3" y="4" width="14" height="12" stroke="{INK}" stroke-width="1.5"/><line x1="9" y1="10" x2="15" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><polyline points="12.5,7.5 15.5,10 12.5,12.5" stroke="{ACCENT}" stroke-width="1.4"/>'),

    # --- EXPRESS TOOLS SMALL ---
    "exp_replace": sm(f'<rect x="3" y="4" width="6" height="6" stroke="{MUTED}" stroke-width="1.4"/><rect x="11" y="10" width="6" height="6" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/><polyline points="11,6 15,6 15,9" stroke="{INK}" stroke-width="1.3"/>'),
    "exp_ncopy": sm(f'<rect x="3" y="3" width="10" height="10" stroke="{MUTED}" stroke-width="1.3"/><rect x="7" y="7" width="10" height="10" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "exp_txt2mtxt": sm(f'<line x1="3" y1="7" x2="9" y2="7" stroke="{INK}" stroke-width="1.6"/><line x1="3" y1="13" x2="9" y2="13" stroke="{INK}" stroke-width="1.6"/><rect x="11" y="5" width="6.5" height="10" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "exp_breakline": sm(f'<polyline points="2,10 7,10 8.5,5.5 11.5,14.5 13,10 18,10" stroke="{ACCENT}" stroke-width="1.6"/>'),
    "exp_flatten": sm(f'<line x1="3" y1="15" x2="17" y2="15" stroke="{INK}" stroke-width="1.8"/><line x1="10" y1="4" x2="10" y2="12" stroke="{ACCENT}" stroke-width="1.7"/><polyline points="7,9.5 10,12.5 13,9.5" stroke="{ACCENT}" stroke-width="1.5"/>'),
}


# =============================================================================
# MINIATURE MENU ICONS (14x14, viewBox 0 0 20 20)
# =============================================================================
MI = {
    "cir_cr": mi(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/><line x1="10" y1="10" x2="16.5" y2="10" stroke="{ACCENT}" stroke-width="1.4"/>' + _node_sm(10, 10)),
    "cir_cd": mi(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/><line x1="3.5" y1="10" x2="16.5" y2="10" stroke="{ACCENT}" stroke-width="1.4"/>'),
    "cir_2p": mi(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/>' + _node_sm(3.5, 10) + _node_sm(16.5, 10)),
    "cir_3p": mi(f'<circle cx="10" cy="10" r="6.5" stroke="{INK}" stroke-width="1.5"/>' + _node_sm(10, 3.5) + _node_sm(4.5, 13.5) + _node_sm(15.5, 13.5)),
    "cir_ttr": mi(f'<circle cx="10" cy="11" r="5" stroke="{INK}" stroke-width="1.5"/><line x1="3" y1="16" x2="17" y2="16" stroke="{ACCENT}" stroke-width="1.3"/><line x1="15" y1="4" x2="15" y2="17" stroke="{ACCENT}" stroke-width="1.3"/>'),
    "arc_std": mi(f'<path d="M4 15 A10 10 0 0 1 16 5" stroke="{INK}" stroke-width="1.6"/>' + _node_sm(4, 15) + _node_sm(9, 7.5) + _node_sm(16, 5)),
    "poly": mi(f'<polygon points="10,3 16.5,7.8 14,16 6,16 3.5,7.8" stroke="{INK}" stroke-width="1.5"/>'),
    "gradient": mi(f'<rect x="3.5" y="4" width="13" height="12" fill="{ACCENT}" fill-opacity="0.35" stroke="{INK}" stroke-width="1.5"/>'),
    "boundary": mi(f'<rect x="3.5" y="4" width="13" height="12" stroke="{ACCENT}" stroke-width="1.6" stroke-dasharray="3 1.5"/>'),
    "extend": mi(f'<line x1="3" y1="10" x2="11" y2="10" stroke="{INK}" stroke-width="1.6"/><line x1="11" y1="10" x2="16" y2="10" stroke="{ACCENT}" stroke-width="1.5" stroke-dasharray="2 1.2"/><line x1="16" y1="4" x2="16" y2="16" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "chamfer": mi(f'<polyline points="4,16 4,9 9,4 16,4" stroke="{INK}" stroke-width="1.6"/><line x1="4" y1="9" x2="9" y2="4" stroke="{ACCENT}" stroke-width="1.8"/>'),
    "blend": mi(f'<line x1="3" y1="15" x2="7" y2="15" stroke="{INK}" stroke-width="1.6"/><path d="M7 15 C11 15, 9 5, 13 5" stroke="{ACCENT}" stroke-width="1.6"/><line x1="13" y1="5" x2="17" y2="5" stroke="{INK}" stroke-width="1.6"/>'),
    "arr_polar": mi(f'<circle cx="10" cy="10" r="5.5" stroke="{MUTED}" stroke-width="1.1" stroke-dasharray="2 1.5"/>' + _node_sm(10, 4.5) + _node_sm(15.5, 10) + _node_sm(10, 15.5) + _node_sm(4.5, 10)),
    "arr_path": mi(f'<path d="M3 15 Q10 4 17 12" stroke="{MUTED}" stroke-width="1.2"/>' + _node_sm(4, 13.5) + _node_sm(10, 8.2) + _node_sm(16, 11.2)),
    "view_ortho": mi(f'<rect x="4" y="4" width="12" height="12" stroke="{INK}" stroke-width="1.5"/><rect x="4" y="4" width="12" height="4" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.2"/>'),
    "view_iso": mi(f'<polygon points="10,3 16.5,6.8 10,10.5 3.5,6.8" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.3"/><polyline points="3.5,6.8 3.5,13.5 10,17 16.5,13.5 16.5,6.8" stroke="{INK}" stroke-width="1.3"/>'),
    "dist": mi(f'<line x1="3" y1="10" x2="17" y2="10" stroke="{ACCENT}" stroke-width="1.6"/><line x1="3" y1="6.5" x2="3" y2="13.5" stroke="{INK}" stroke-width="1.4"/><line x1="17" y1="6.5" x2="17" y2="13.5" stroke="{INK}" stroke-width="1.4"/>'),
    "area": mi(f'<polygon points="4,15 6,5 16,7 14,15" fill="{SOFT}" stroke="{ACCENT}" stroke-width="1.5"/>'),
    "zoom_sm": mi(f'<circle cx="8.5" cy="8.5" r="4.8" stroke="{INK}" stroke-width="1.5"/><line x1="12" y1="12" x2="16.5" y2="16.5" stroke="{ACCENT}" stroke-width="1.8"/>'),
}
