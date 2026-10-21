#!/usr/bin/env python3
import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>AutoCAD Windows-style Ribbon</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="ribbon-container" id="ribbon">
    <!-- Floating Switcher Pill (displayed when switched to Classic Mac Toolbar) -->
    <div class="floating-ribbon-pill" id="floating-pill" style="display:none;" title="Click to activate Windows Ribbon">
      <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,1 11,1 7,7 13,7 5,15 7,9 3,9" fill="#00b4d8"/></svg>
      <span>Windows Ribbon</span>
    </div>

    <!-- Top Tabs Bar -->
    <div class="ribbon-tabs-bar" id="ribbon-tabs-bar">
      <!-- Quick Access Toolbar (QAT) & Application Logo -->
      <div class="qat-bar">
        <div class="cad-app-logo" data-cmd="^C^C_ABOUT" title="AutoCAD 2027">
          <svg viewBox="0 0 32 32" width="18" height="18"><polygon points="16,2 3,28 10,28 16,14 22,28 29,28" fill="#d90429"/><polygon points="16,14 10,28 16,23 22,28" fill="#a0001e"/></svg>
        </div>
        <button class="qat-btn" data-cmd="^C^C_NEW" title="New (QNEW)"><svg viewBox="0 0 16 16" width="11" height="11"><path d="M3 2h7l3 3v9H3z" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M10 2v3h3" fill="none" stroke="currentColor" stroke-width="1.3"/></svg></button>
        <button class="qat-btn" data-cmd="^C^C_OPEN" title="Open (OPEN)"><svg viewBox="0 0 16 16" width="11" height="11"><path d="M2 4h4l2 2h6v8H2z" fill="none" stroke="currentColor" stroke-width="1.3"/></svg></button>
        <button class="qat-btn" data-cmd="^C^C_QSAVE" title="Save (QSAVE)"><svg viewBox="0 0 16 16" width="11" height="11"><path d="M3 2h8l2 2v10H3z" fill="none" stroke="currentColor" stroke-width="1.3"/><rect x="5" y="2" width="6" height="4" fill="currentColor"/><rect x="5" y="8" width="6" height="5" fill="none" stroke="currentColor" stroke-width="1"/></svg></button>
        <button class="qat-btn" data-cmd="^C^C_SAVEAS" title="Save As (SAVEAS)"><svg viewBox="0 0 16 16" width="11" height="11"><path d="M2 2h8l2 2v10H2z" fill="none" stroke="currentColor" stroke-width="1.3"/><polygon points="10,8 14,8 12,12" fill="#ffd166"/></svg></button>
        <button class="qat-btn" data-cmd="^C^C_PLOT" title="Plot (PLOT)"><svg viewBox="0 0 16 16" width="11" height="11"><rect x="4" y="2" width="8" height="3" fill="none" stroke="currentColor" stroke-width="1.2"/><rect x="3" y="5" width="10" height="6" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/><rect x="5" y="9" width="6" height="5" fill="none" stroke="currentColor" stroke-width="1.2"/></svg></button>
        <button class="qat-btn" data-cmd="^C^C_U" title="Undo (U)"><svg viewBox="0 0 16 16" width="11" height="11"><path d="M5 6 L2 9 L5 12" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M3 9 h7 a4 4 0 0 1 4 4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
        <button class="qat-btn" data-cmd="^C^C_REDO" title="Redo (REDO)"><svg viewBox="0 0 16 16" width="11" height="11"><path d="M11 6 L14 9 L11 12" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M13 9 h-7 a4 4 0 0 0 -4 4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button>
        <div class="workspace-selector" title="Workspace: Drafting & Annotation">
          <svg viewBox="0 0 16 16" width="11" height="11"><path fill="currentColor" d="M8 5a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm5.3 1.8l-1-.6c-.1-.3-.2-.5-.3-.7l.5-1.1c.2-.4.1-.9-.3-1.2l-.7-.7c-.3-.3-.8-.4-1.2-.2l-1.1.5c-.2-.1-.5-.2-.7-.3l-.6-1c-.2-.4-.6-.7-1.1-.7h-1c-.5 0-.9.3-1.1.7l-.6 1c-.3.1-.5.2-.7.3l-1.1-.5c-.4-.2-.9-.1-1.2.2l-.7.7c-.3.3-.4.8-.2 1.2l.5 1.1c-.1.2-.2.5-.3.7l-1 .6c-.4.2-.7.6-.7 1.1v1c0 .5.3.9.7 1.1l1 .6c.1.3.2.5.3.7l-.5 1.1c-.2.4-.1.9.2 1.2l.7.7c.3.3.8.4 1.2.2l1.1-.5c.2.1.5.2.7.3l.6 1c.2.4.6.7 1.1.7h1c.5 0 .9-.3 1.1-.7l.6-1c.3-.1.5-.2.7-.3l1.1.5c.4.2.9.1 1.2-.2l.7-.7c.3-.3.4-.8.2-1.2l-.5-1.1c.1-.2.2-.5.3-.7l1-.6c.4-.2.7-.6.7-1.1v-1c0-.5-.3-.9-.7-1.1z"/></svg>
          <span>Drafting & Annotation</span>
          <span class="arrow">▾</span>
        </div>
      </div>

      <!-- Ribbon Tabs -->
      <div class="ribbon-tabs">
        <button class="tab-button active" data-tab="tab-home">Home</button>
        <button class="tab-button" data-tab="tab-insert">Insert</button>
        <button class="tab-button" data-tab="tab-annotate">Annotate</button>
        <button class="tab-button" data-tab="tab-parametric">Parametric</button>
        <button class="tab-button" data-tab="tab-view">View</button>
        <button class="tab-button" data-tab="tab-manage">Manage</button>
        <button class="tab-button" data-tab="tab-output">Output</button>
        <button class="tab-button" data-tab="tab-collaborate">Collaborate</button>
      </div>

      <!-- Right-side Ribbon Controls -->
      <div class="ribbon-controls">
        <button class="ctrl-btn-toolbar" id="btn-switch-toolbar" title="Switch to Mac Toolbar (Classic Tool Sets)">
          <svg viewBox="0 0 16 16" width="12" height="12"><path fill="currentColor" d="M1 2.5h14v2H1zM1 6.5h4v7H1zM7 6.5h8v7H7z"/></svg>
          <span>Mac Toolbar</span>
        </button>
        <button class="ctrl-btn" id="btn-minimize" title="Minimize / Expand Ribbon (or double-click any tab)">
          <svg viewBox="0 0 16 16" width="11" height="11"><path fill="currentColor" d="M3 6l5 5 5-5z"/></svg>
        </button>
        <button class="ctrl-btn" id="btn-close" title="Hide Ribbon (Switch to Mac Toolbar)">
          <svg viewBox="0 0 16 16" width="11" height="11"><path fill="currentColor" d="M4 4l8 8m0-8l-8 8" stroke="currentColor" stroke-width="1.6"/></svg>
        </button>
      </div>
    </div>

    <!-- Ribbon Body -->
    <div class="ribbon-body" id="ribbon-body">

      <!-- ================= 1. HOME TAB ================= -->
      <div class="tab-content active" id="tab-home">

        <!-- 1.1 DRAW PANEL -->
        <div class="panel" id="panel-draw">
          <div class="panel-content">
            <!-- Line -->
            <button class="btn-big" data-cmd="^C^C_LINE" data-tip-title="Line" data-tip-desc="Creates straight line segments. With LINE, you can create a series of contiguous line segments.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="5" y1="27" x2="27" y2="5" stroke="#00b4d8" stroke-width="3" stroke-linecap="round"/>
                <circle cx="5" cy="27" r="3" fill="#ffffff" stroke="#0077b6" stroke-width="1.5"/>
                <circle cx="27" cy="5" r="3" fill="#ffffff" stroke="#0077b6" stroke-width="1.5"/>
              </svg>
              <span>Line</span>
            </button>

            <!-- Polyline -->
            <button class="btn-big" data-cmd="^C^C_PLINE" data-tip-title="Polyline" data-tip-desc="Creates a 2D polyline, a single object composed of line and arc segments.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <polyline points="4,26 13,9 28,19" fill="none" stroke="#00b4d8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <rect x="2.5" y="24.5" width="4" height="4" fill="#ffffff" stroke="#0077b6"/>
                <rect x="11" y="7" width="4" height="4" fill="#ffffff" stroke="#0077b6"/>
                <rect x="26" y="17" width="4" height="4" fill="#ffffff" stroke="#0077b6"/>
              </svg>
              <span>Polyline</span>
            </button>

            <!-- Circle Split Button -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_CIRCLE" data-tip-title="Circle (Center, Radius)" data-tip-desc="Creates a circle using a center point and a radius value.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <circle cx="16" cy="15" r="11" fill="none" stroke="#ef476f" stroke-width="2.5"/>
                  <circle cx="16" cy="15" r="2.5" fill="#ffffff" stroke="#d90429"/>
                  <line x1="16" y1="15" x2="27" y2="15" stroke="#00b4d8" stroke-width="1.5" stroke-dasharray="2,2"/>
                </svg>
                <span>Circle</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-circle">▾</button>
            </div>

            <!-- Arc Split Button -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_ARC" data-tip-title="Arc (3-Point)" data-tip-desc="Creates an arc using three specified points on the circumference.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <path d="M 5,25 A 16,16 0 0,1 27,9" fill="none" stroke="#06d6a0" stroke-width="2.5"/>
                  <circle cx="5" cy="25" r="2.5" fill="#ffffff" stroke="#0077b6"/>
                  <circle cx="13" cy="11" r="2.5" fill="#ffffff" stroke="#0077b6"/>
                  <circle cx="27" cy="9" r="2.5" fill="#ffffff" stroke="#0077b6"/>
                </svg>
                <span>Arc</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-arc">▾</button>
            </div>

            <!-- Small 3-row cluster: Rect, Ellipse, Hatch -->
            <div class="btn-cluster-3">
              <!-- Rectangle Split -->
              <div class="split-sm-container">
                <button class="split-main-sm" data-cmd="^C^C_RECTANG" data-tip-title="Rectangle" data-tip-desc="Creates a rectangular polyline from two corner points.">
                  <svg viewBox="0 0 16 16" width="13" height="13"><rect x="2" y="3" width="12" height="10" fill="none" stroke="#00b4d8" stroke-width="1.6"/><circle cx="2" cy="3" r="1.5" fill="#fff"/></svg>
                  <span>Rectangle</span>
                </button>
                <button class="split-arrow-sm" data-dropdown="menu-rect">▾</button>
              </div>

              <!-- Ellipse Split -->
              <div class="split-sm-container">
                <button class="split-main-sm" data-cmd="^C^C_ELLIPSE" data-tip-title="Ellipse (Center)" data-tip-desc="Creates an ellipse using a center point, end point of first axis, and length of second axis.">
                  <svg viewBox="0 0 16 16" width="13" height="13"><ellipse cx="8" cy="8" rx="6.5" ry="4" fill="none" stroke="#ffd166" stroke-width="1.6"/></svg>
                  <span>Ellipse</span>
                </button>
                <button class="split-arrow-sm" data-dropdown="menu-ellipse">▾</button>
              </div>

              <!-- Hatch Split -->
              <div class="split-sm-container">
                <button class="split-main-sm" data-cmd="^C^C_BHATCH" data-tip-title="Hatch" data-tip-desc="Fills an enclosed area or selected objects with a hatch pattern, solid fill, or gradient fill.">
                  <svg viewBox="0 0 16 16" width="13" height="13">
                    <rect x="2" y="2" width="12" height="12" fill="none" stroke="#888" stroke-width="1"/>
                    <line x1="2" y1="10" x2="10" y2="2" stroke="#ef476f" stroke-width="1.5"/>
                    <line x1="4" y1="14" x2="14" y2="4" stroke="#ef476f" stroke-width="1.5"/>
                    <line x1="8" y1="14" x2="14" y2="8" stroke="#ef476f" stroke-width="1.5"/>
                  </svg>
                  <span>Hatch</span>
                </button>
                <button class="split-arrow-sm" data-dropdown="menu-hatch">▾</button>
              </div>
            </div>
          </div>
          <div class="panel-footer">Draw <span class="arrow">▾</span></div>
        </div>

        <!-- 1.2 MODIFY PANEL -->
        <div class="panel" id="panel-modify">
          <div class="panel-content">
            <!-- Move -->
            <button class="btn-big" data-cmd="^C^C_MOVE" data-tip-title="Move" data-tip-desc="Moves objects a specified distance in a specified direction.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M16 4 L16 28 M4 16 L28 16" stroke="#00b4d8" stroke-width="2.5" stroke-linecap="round"/>
                <polygon points="16,2 13,6 19,6" fill="#00b4d8"/>
                <polygon points="16,30 13,26 19,26" fill="#00b4d8"/>
                <polygon points="2,16 6,13 6,19" fill="#00b4d8"/>
                <polygon points="30,16 26,13 26,19" fill="#00b4d8"/>
              </svg>
              <span>Move</span>
            </button>

            <!-- Rotate -->
            <button class="btn-big" data-cmd="^C^C_ROTATE" data-tip-title="Rotate" data-tip-desc="Rotates objects around a base point.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M24 16 A9 9 0 1 1 16 7" fill="none" stroke="#ffd166" stroke-width="2.5" stroke-linecap="round"/>
                <polygon points="16,3 16,11 21,7" fill="#ffd166"/>
              </svg>
              <span>Rotate</span>
            </button>

            <!-- Trim Split Button -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_TRIM" data-tip-title="Trim" data-tip-desc="Trims objects to meet the edges of other objects.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <line x1="7" y1="7" x2="25" y2="25" stroke="#ef476f" stroke-width="2.5"/>
                  <line x1="7" y1="25" x2="25" y2="7" stroke="#ef476f" stroke-width="2.5"/>
                  <circle cx="16" cy="16" r="3" fill="#ffffff" stroke="#d90429"/>
                </svg>
                <span>Trim</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-trim">▾</button>
            </div>

            <!-- Erase -->
            <button class="btn-big" data-cmd="^C^C_ERASE" data-tip-title="Erase" data-tip-desc="Removes objects from a drawing.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="8" y1="8" x2="24" y2="24" stroke="#ef476f" stroke-width="3" stroke-linecap="round"/>
                <line x1="24" y1="8" x2="8" y2="24" stroke="#ef476f" stroke-width="3" stroke-linecap="round"/>
              </svg>
              <span>Erase</span>
            </button>

            <!-- Small 3-row cluster 1: Copy, Mirror, Fillet -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_COPY" data-tip-title="Copy" data-tip-desc="Copies objects a specified distance in a specified direction.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="6" cy="10" r="4" fill="none" stroke="#00b4d8" stroke-width="1.5"/><circle cx="10" cy="6" r="4" fill="none" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Copy</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_MIRROR" data-tip-title="Mirror" data-tip-desc="Creates a mirrored copy of selected objects.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="8" y1="2" x2="8" y2="14" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="2,2"/><polygon points="3,4 7,8 3,12" fill="#00b4d8"/><polygon points="13,4 9,8 13,12" fill="none" stroke="#00b4d8"/></svg>
                <span>Mirror</span>
              </button>
              <div class="split-sm-container">
                <button class="split-main-sm" data-cmd="^C^C_FILLET" data-tip-title="Fillet" data-tip-desc="Rounds and fillets the edges of objects.">
                  <svg viewBox="0 0 16 16" width="13" height="13"><path d="M3 13 L3 8 A 5 5 0 0 1 8 3 L13 3" fill="none" stroke="#06d6a0" stroke-width="1.6"/></svg>
                  <span>Fillet</span>
                </button>
                <button class="split-arrow-sm" data-dropdown="menu-fillet">▾</button>
              </div>
            </div>

            <!-- Small 3-row cluster 2: Stretch, Scale, Array -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_STRETCH" data-tip-title="Stretch" data-tip-desc="Stretches objects crossed by a selection window or polygon.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="7" height="10" fill="none" stroke="#ffd166" stroke-width="1.5"/><line x1="10" y1="8" x2="14" y2="8" stroke="#ffd166" stroke-width="1.5"/><polygon points="14,6 16,8 14,10" fill="#ffd166"/></svg>
                <span>Stretch</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_SCALE" data-tip-title="Scale" data-tip-desc="Enlarges or reduces selected objects, keeping the same proportions.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="7" width="5" height="5" fill="#00b4d8"/><rect x="3" y="3" width="10" height="9" fill="none" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Scale</span>
              </button>
              <div class="split-sm-container">
                <button class="split-main-sm" data-cmd="^C^C_ARRAYRECT" data-tip-title="Rectangular Array" data-tip-desc="Distributes copies of selected objects into any combination of rows and columns.">
                  <svg viewBox="0 0 16 16" width="13" height="13"><rect x="2" y="2" width="3" height="3" fill="#00b4d8"/><rect x="7" y="2" width="3" height="3" fill="#00b4d8"/><rect x="12" y="2" width="3" height="3" fill="#00b4d8"/><rect x="2" y="7" width="3" height="3" fill="#00b4d8"/><rect x="7" y="7" width="3" height="3" fill="#00b4d8"/><rect x="12" y="7" width="3" height="3" fill="#00b4d8"/></svg>
                  <span>Array</span>
                </button>
                <button class="split-arrow-sm" data-dropdown="menu-array">▾</button>
              </div>
            </div>

            <!-- Small 2-row cluster: Explode, Offset -->
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_EXPLODE" data-tip-title="Explode" data-tip-desc="Breaks a compound object into its component objects.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="3" x2="6" y2="6" stroke="#ef476f" stroke-width="1.6"/><line x1="13" y1="3" x2="10" y2="6" stroke="#ef476f" stroke-width="1.6"/><line x1="3" y1="13" x2="6" y2="10" stroke="#ef476f" stroke-width="1.6"/><line x1="13" y1="13" x2="10" y2="10" stroke="#ef476f" stroke-width="1.6"/></svg>
                <span>Explode</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_OFFSET" data-tip-title="Offset" data-tip-desc="Creates concentric circles, parallel lines, and parallel curves.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M2 13 A 10 10 0 0 1 13 2" fill="none" stroke="#00b4d8" stroke-width="1.6"/><path d="M6 13 A 6 6 0 0 1 13 6" fill="none" stroke="#00b4d8" stroke-width="1.6"/></svg>
                <span>Offset</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Modify <span class="arrow">▾</span></div>
        </div>

        <!-- 1.3 ANNOTATION PANEL -->
        <div class="panel" id="panel-annotation">
          <div class="panel-content">
            <!-- Text Split -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_MTEXT" data-tip-title="Multiline Text" data-tip-desc="Creates a multiline text object.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <text x="6" y="24" fill="#00b4d8" font-size="24" font-weight="bold">A</text>
                </svg>
                <span>Text</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-text-type">▾</button>
            </div>

            <!-- Smart Dimension -->
            <button class="btn-big" data-cmd="^C^C_DIM" data-tip-title="Dimension" data-tip-desc="Creates multiple types of dimensions within a single command session.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="4" y1="18" x2="28" y2="18" stroke="#ffd166" stroke-width="2"/>
                <line x1="4" y1="12" x2="4" y2="24" stroke="#ffd166" stroke-width="1.5"/>
                <line x1="28" y1="12" x2="28" y2="24" stroke="#ffd166" stroke-width="1.5"/>
                <polygon points="4,18 8,15 8,21" fill="#ffd166"/>
                <polygon points="28,18 24,15 24,21" fill="#ffd166"/>
                <text x="13" y="15" fill="#ffd166" font-size="9" font-weight="bold">150</text>
              </svg>
              <span>Dimension</span>
            </button>

            <!-- Linear Dimension Split -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_DIMLINEAR" data-tip-title="Linear Dimension" data-tip-desc="Creates a horizontal or vertical dimension line.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <line x1="6" y1="10" x2="26" y2="10" stroke="#00b4d8" stroke-width="1.8"/>
                  <polygon points="6,10 10,8 10,12" fill="#00b4d8"/>
                  <polygon points="26,10 22,8 22,12" fill="#00b4d8"/>
                  <line x1="6" y1="10" x2="6" y2="24" stroke="#00b4d8" stroke-width="1" stroke-dasharray="2,2"/>
                  <line x1="26" y1="10" x2="26" y2="24" stroke="#00b4d8" stroke-width="1" stroke-dasharray="2,2"/>
                </svg>
                <span>Linear</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-dim-types">▾</button>
            </div>

            <!-- Leader & Table cluster -->
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_MLEADER" data-tip-title="Multileader" data-tip-desc="Creates a multileader object.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="8" y2="6" stroke="#00b4d8" stroke-width="1.5"/><line x1="8" y1="6" x2="13" y2="6" stroke="#00b4d8" stroke-width="1.5"/><polygon points="3,13 6,10 7,12" fill="#00b4d8"/></svg>
                <span>Leader</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_TABLE" data-tip-title="Table" data-tip-desc="Creates an empty table object.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="2" y="2" width="12" height="11" fill="none" stroke="#06d6a0" stroke-width="1.5"/><line x1="2" y1="6" x2="14" y2="6" stroke="#06d6a0" stroke-width="1.2"/><line x1="8" y1="2" x2="8" y2="13" stroke="#06d6a0" stroke-width="1.2"/></svg>
                <span>Table</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Annotation</div>
        </div>

        <!-- 1.4 LAYERS PANEL -->
        <div class="panel" id="panel-layers">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_LAYER" data-tip-title="Layer Properties" data-tip-desc="Manages layers and layer properties.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <polygon points="16,4 27,10 16,16 5,10" fill="#ef476f"/>
                <polygon points="16,11 27,17 16,23 5,17" fill="#ffd166"/>
                <polygon points="16,18 27,24 16,30 5,24" fill="#00b4d8"/>
              </svg>
              <span>Layer Props</span>
            </button>

            <div style="display:flex; flex-direction:column; gap:4px; min-width:145px;">
              <!-- Current Layer Dropdown -->
              <div class="layer-combo" data-dropdown="menu-layer-list">
                <span class="layer-color-box"></span>
                <span style="flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-weight:600; font-size:10px; padding:0 4px;">0 (Default)</span>
                <span style="font-size:8px; color:var(--cad-text-muted);">▾</span>
              </div>

              <!-- Layer Quick Controls -->
              <div style="display:flex; gap:6px; font-size:10px; color:var(--cad-text-muted); align-items:center;">
                <span style="cursor:pointer; display:inline-flex;" title="Turn Off / On" data-cmd="^C^C_LAYOFF"><svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 2.38 1.19 4.47 3 5.74V17a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 0 0-7-7zM9 21a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-1H9v1z"/></svg></span>
                <span style="cursor:pointer; display:inline-flex;" title="Freeze / Thaw" data-cmd="^C^C_LAYFRZ"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="5" y1="5" x2="19" y2="19"/><line x1="5" y1="19" x2="19" y2="5"/></svg></span>
                <span style="cursor:pointer; display:inline-flex;" title="Lock / Unlock" data-cmd="^C^C_LAYLCK"><svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor"><rect x="4" y="10" width="16" height="12" rx="2"/><path d="M8 10V7a4 4 0 1 1 8 0v3" fill="none" stroke="currentColor" stroke-width="2"/></svg></span>
                <span style="cursor:pointer; display:inline-flex;" title="Make Current" data-cmd="^C^C_LAYMCUR"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg></span>
                <span style="cursor:pointer; display:inline-flex;" title="Match Layer" data-cmd="^C^C_LAYMCH"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 0 0-10 10c0 5.5 4.5 10 10 10 1.5 0 3-1.5 3-3 0-.8-.3-1.5-.8-2-.5-.5-.7-1.2-.7-2 0-1.7 1.3-3 3-3h2c2.8 0 5-2.2 5-5 0-5.5-5.4-7-11.5-7z"/></svg></span>
                <span style="cursor:pointer; display:inline-flex;" title="Isolate Layer" data-cmd="^C^C_LAYISO"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></span>
              </div>
            </div>
          </div>
          <div class="panel-footer">Layers</div>
        </div>

        <!-- 1.5 BLOCK PANEL -->
        <div class="panel" id="panel-block">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_INSERT" data-tip-title="Insert Block" data-tip-desc="Inserts a block or drawing into current drawing.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="7" y="7" width="18" height="18" fill="none" stroke="#00b4d8" stroke-width="2.5"/>
                <circle cx="7" cy="7" r="2.5" fill="#06d6a0"/>
              </svg>
              <span>Insert</span>
            </button>

            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_BLOCK" data-tip-title="Create Block" data-tip-desc="Creates a block definition from selected objects.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#ffd166" stroke-width="1.5"/></svg>
                <span>Create</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_BEDIT" data-tip-title="Edit Block" data-tip-desc="Opens block definition in Block Editor.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="11" y2="5" stroke="#06d6a0" stroke-width="1.8"/><polygon points="11,5 14,2 14,5" fill="#06d6a0"/></svg>
                <span>Edit</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_ATTDEF" data-tip-title="Define Attributes" data-tip-desc="Creates a block attribute definition.">
                <svg viewBox="0 0 16 16" width="13" height="13"><text x="2" y="12" fill="#00b4d8" font-size="10" font-weight="bold">A=</text></svg>
                <span>Attrib</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Block</div>
        </div>

        <!-- 1.6 PROPERTIES PANEL -->
        <div class="panel" id="panel-properties">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_MATCHPROP" data-tip-title="Match Properties" data-tip-desc="Applies the properties of a selected object to other objects.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="8" y1="24" x2="22" y2="10" stroke="#ffd166" stroke-width="2.5"/>
                <polygon points="22,10 26,6 26,14" fill="#ffd166"/>
              </svg>
              <span>Match Prop</span>
            </button>

            <!-- Color / Lineweight / Linetype combos -->
            <div style="display:flex; flex-direction:column; gap:3px; min-width:125px;">
              <!-- Color Combo -->
              <div class="cad-combo" data-dropdown="menu-color-list">
                <span class="layer-color-box" style="background-color:#ffffff; width:10px; height:10px; border:1px solid #888;"></span>
                <span style="flex:1; padding:0 4px;">ByLayer</span>
                <span style="font-size:8px; color:var(--cad-text-muted);">▾</span>
              </div>

              <!-- Lineweight Combo -->
              <div class="cad-combo" data-dropdown="menu-lineweight-list">
                <span style="flex:1;">ByLayer</span>
                <span style="font-size:8px; color:var(--cad-text-muted);">▾</span>
              </div>

              <!-- Linetype Combo -->
              <div class="cad-combo" data-dropdown="menu-linetype-list">
                <span style="flex:1; font-family:monospace; letter-spacing:-1px;">--- ByLayer</span>
                <span style="font-size:8px; color:var(--cad-text-muted);">▾</span>
              </div>
            </div>
          </div>
          <div class="panel-footer">Properties</div>
        </div>

        <!-- 1.7 GROUPS PANEL -->
        <div class="panel" id="panel-groups">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_GROUP" data-tip-title="Group" data-tip-desc="Creates a saved set of objects called a group.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="6" width="20" height="20" fill="none" stroke="#00b4d8" stroke-width="2" stroke-dasharray="3,2"/>
                <circle cx="11" cy="11" r="3" fill="#00b4d8"/>
                <circle cx="21" cy="11" r="3" fill="#00b4d8"/>
                <circle cx="16" cy="21" r="3" fill="#00b4d8"/>
              </svg>
              <span>Group</span>
            </button>

            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_UNGROUP" data-tip-title="Ungroup" data-tip-desc="Disassociates objects that are part of a group.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="5" cy="5" r="2.5" fill="#ef476f"/><circle cx="11" cy="11" r="2.5" fill="#ef476f"/></svg>
                <span>Ungroup</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GROUPEDIT" data-tip-title="Group Edit" data-tip-desc="Adds and removes objects from the selected group.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M3 13 L11 5 L14 8 Z" fill="#ffd166"/></svg>
                <span>Edit Group</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_PICKSTYLE 1" data-tip-title="Group Selection" data-tip-desc="Turns group selection on or off.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#06d6a0" stroke-width="1.5"/></svg>
                <span>Select On/Off</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Groups</div>
        </div>

        <!-- 1.8 UTILITIES PANEL -->
        <div class="panel" id="panel-utilities">
          <div class="panel-content">
            <!-- Measure Split Button -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_MEASUREGEOM _QUICK" data-tip-title="Quick Measure" data-tip-desc="Measures distances and angles across a drawing in real time.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <path d="M4 14 L4 20 L28 20 L28 14 Z" fill="#ffd166"/>
                  <line x1="8" y1="14" x2="8" y2="18" stroke="#333" stroke-width="1.5"/>
                  <line x1="12" y1="14" x2="12" y2="16" stroke="#333" stroke-width="1.5"/>
                  <line x1="16" y1="14" x2="16" y2="18" stroke="#333" stroke-width="1.5"/>
                  <line x1="20" y1="14" x2="20" y2="16" stroke="#333" stroke-width="1.5"/>
                  <line x1="24" y1="14" x2="24" y2="18" stroke="#333" stroke-width="1.5"/>
                </svg>
                <span>Measure</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-measure">▾</button>
            </div>

            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_QSELECT" data-tip-title="Quick Select" data-tip-desc="Creates a selection set based on filtering criteria.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,3 13,8 8,10 6,14" fill="#00b4d8"/></svg>
                <span>Quick Sel</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_QUICKCALC" data-tip-title="Quick Calculator" data-tip-desc="Opens the QuickCalc calculator palette.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="2" width="10" height="12" fill="none" stroke="#fff" stroke-width="1.2"/><rect x="5" y="4" width="6" height="3" fill="#00b4d8"/></svg>
                <span>Calc</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_PURGE" data-tip-title="Purge" data-tip-desc="Removes unused items such as block definitions and layers from drawing.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M3 4 L13 4 M5 4 L5 13 L11 13 L11 4" fill="none" stroke="#ef476f" stroke-width="1.2"/></svg>
                <span>Purge</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Utilities</div>
        </div>

        <!-- 1.9 CLIPBOARD PANEL -->
        <div class="panel" id="panel-clipboard">
          <div class="panel-content">
            <!-- Paste Split Button -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_PASTECLIP" data-tip-title="Paste" data-tip-desc="Pastes objects from the Clipboard into the current drawing.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <rect x="8" y="8" width="16" height="20" fill="none" stroke="#ffd166" stroke-width="2"/>
                  <rect x="11" y="4" width="10" height="6" fill="#ffd166" rx="1"/>
                </svg>
                <span>Paste</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-paste">▾</button>
            </div>

            <div class="btn-cluster-2">
              <button class="btn-icon-only" data-cmd="^C^C_CUTCLIP" data-tip-title="Cut" data-tip-desc="Copies objects to Clipboard and removes them from drawing.">
                <svg viewBox="0 0 16 16" width="14" height="14"><circle cx="5" cy="11" r="2.5" fill="none" stroke="#ef476f"/><circle cx="11" cy="11" r="2.5" fill="none" stroke="#ef476f"/><line x1="6.5" y1="9" x2="13" y2="3" stroke="#ef476f" stroke-width="1.5"/><line x1="9.5" y1="9" x2="3" y2="3" stroke="#ef476f" stroke-width="1.5"/></svg>
              </button>
              <button class="btn-icon-only" data-cmd="^C^C_COPYCLIP" data-tip-title="Copy" data-tip-desc="Copies objects to the Clipboard.">
                <svg viewBox="0 0 16 16" width="14" height="14"><rect x="3" y="5" width="8" height="9" fill="none" stroke="#00b4d8" stroke-width="1.4"/><rect x="6" y="2" width="8" height="9" fill="none" stroke="#00b4d8" stroke-width="1.4"/></svg>
              </button>
            </div>
          </div>
          <div class="panel-footer">Clipboard</div>
        </div>

      </div><!-- /tab-home -->

      <!-- ================= 2. INSERT TAB ================= -->
      <div class="tab-content" id="tab-insert">

        <!-- 2.1 BLOCK PANEL -->
        <div class="panel" id="panel-ins-block">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_INSERT" data-tip-title="Insert Block" data-tip-desc="Inserts a block or drawing into current drawing.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="6" width="20" height="20" fill="none" stroke="#00b4d8" stroke-width="2.5"/>
                <circle cx="6" cy="6" r="3" fill="#06d6a0"/>
              </svg>
              <span>Insert</span>
            </button>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_BLOCK" data-tip-title="Create Block" data-tip-desc="Creates a block definition.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#ffd166" stroke-width="1.5"/></svg>
                <span>Create Block</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_WBLOCK" data-tip-title="Write Block" data-tip-desc="Writes objects or a block to a new drawing file.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M3 3 L13 3 L13 13 L3 13 Z" fill="none" stroke="#06d6a0" stroke-width="1.5"/></svg>
                <span>Write Block</span>
              </button>
            </div>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_BEDIT" data-tip-title="Block Editor" data-tip-desc="Opens block definition in Block Editor.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="11" y2="5" stroke="#06d6a0" stroke-width="1.8"/><polygon points="11,5 14,2 14,5" fill="#06d6a0"/></svg>
                <span>Block Editor</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_BATTMAN" data-tip-title="Manage Attributes" data-tip-desc="Manages attribute definitions for blocks.">
                <svg viewBox="0 0 16 16" width="13" height="13"><text x="2" y="12" fill="#00b4d8" font-size="10" font-weight="bold">AT</text></svg>
                <span>Manage Attr</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Block Definition</div>
        </div>

        <!-- 2.2 REFERENCE PANEL -->
        <div class="panel" id="panel-ins-reference">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_ATTACH" data-tip-title="Attach Reference" data-tip-desc="Inserts DWG, raster images, point clouds, or PDF underlays as external references.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M12 20 L22 10 A 4 4 0 0 0 16 4 L6 14 A 6 6 0 0 0 14 22 L20 16" fill="none" stroke="#ffd166" stroke-width="2.5"/>
              </svg>
              <span>Attach</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_XREF" data-tip-title="External References" data-tip-desc="Opens External References palette.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="5" y="5" width="22" height="22" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <line x1="5" y1="12" x2="27" y2="12" stroke="#00b4d8" stroke-width="1.5"/>
                <line x1="12" y1="12" x2="12" y2="27" stroke="#00b4d8" stroke-width="1.5"/>
              </svg>
              <span>Xref Palette</span>
            </button>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_CLIP" data-tip-title="Clip" data-tip-desc="Clips an xref, image, or underlay.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#ef476f" stroke-width="1.5"/></svg>
                <span>Clip</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_ADJUST" data-tip-title="Adjust" data-tip-desc="Adjusts brightness, contrast, and fade of images or underlays.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="5" fill="none" stroke="#ffd166" stroke-width="1.5"/></svg>
                <span>Adjust</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Reference</div>
        </div>

        <!-- 2.3 IMPORT PANEL -->
        <div class="panel" id="panel-ins-import">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_PDFIMPORT" data-tip-title="PDF Import" data-tip-desc="Imports geometry, fills, raster images, and TrueType text from a PDF file.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="7" y="5" width="18" height="22" fill="#ef476f" rx="2"/>
                <text x="8" y="20" fill="#fff" font-size="10" font-weight="bold">PDF</text>
              </svg>
              <span>Import PDF</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_IMPORT" data-tip-title="Import File" data-tip-desc="Imports files of various formats (3DM, SAT, DGN, STEP, IGES, WMF) into the current drawing.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M16 6 L16 22 M10 16 L16 22 L22 16" fill="none" stroke="#06d6a0" stroke-width="2.5"/>
                <line x1="6" y1="26" x2="26" y2="26" stroke="#fff" stroke-width="2"/>
              </svg>
              <span>Import</span>
            </button>
          </div>
          <div class="panel-footer">Import</div>
        </div>

        <!-- 2.4 DATA & LINKING PANEL -->
        <div class="panel" id="panel-ins-data">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_FIELD" data-tip-title="Insert Field" data-tip-desc="Creates a text object with a field that updates automatically as data changes.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="8" width="20" height="16" fill="none" stroke="#06d6a0" stroke-width="2"/>
                <line x1="10" y1="16" x2="22" y2="16" stroke="#06d6a0" stroke-width="2"/>
              </svg>
              <span>Field</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_DATALINK" data-tip-title="Data Link" data-tip-desc="Links a table with an external Microsoft Excel spreadsheet.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M10 16 A 6 6 0 0 1 20 10 L24 14" fill="none" stroke="#00b4d8" stroke-width="2.5"/>
                <path d="M22 16 A 6 6 0 0 1 12 22 L8 18" fill="none" stroke="#00b4d8" stroke-width="2.5"/>
              </svg>
              <span>Link Data</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_DATAEXTRACTION" data-tip-title="Extract Data" data-tip-desc="Extracts drawing information and block attributes to a table or external file.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="6" width="20" height="20" fill="none" stroke="#ffd166" stroke-width="2"/>
                <line x1="6" y1="13" x2="26" y2="13" stroke="#ffd166" stroke-width="1.5"/>
                <line x1="14" y1="13" x2="14" y2="26" stroke="#ffd166" stroke-width="1.5"/>
              </svg>
              <span>Extract Data</span>
            </button>
          </div>
          <div class="panel-footer">Data & Linking</div>
        </div>

        <!-- 2.5 CONTENT & TOOLS PANEL -->
        <div class="panel" id="panel-ins-content">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_ADCENTER" data-tip-title="DesignCenter" data-tip-desc="Manages and inserts content such as drawings, blocks, and hatches.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="5" y="6" width="22" height="20" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <circle cx="16" cy="16" r="4" fill="#00b4d8"/>
              </svg>
              <span>DesignCenter</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_TOOLPALETTES" data-tip-title="Tool Palettes" data-tip-desc="Displays the Tool Palettes window.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="5" width="6" height="22" fill="#00b4d8"/>
                <rect x="15" y="5" width="11" height="22" fill="none" stroke="#888" stroke-width="1.2"/>
              </svg>
              <span>Tool Palettes</span>
            </button>
          </div>
          <div class="panel-footer">Content</div>
        </div>

      </div><!-- /tab-insert -->

      <!-- ================= 3. ANNOTATE TAB ================= -->
      <div class="tab-content" id="tab-annotate">

        <!-- 3.1 TEXT PANEL -->
        <div class="panel" id="panel-ann-text">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_MTEXT" data-tip-title="Multiline Text" data-tip-desc="Creates a multiline text object.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <text x="6" y="24" fill="#00b4d8" font-size="24" font-weight="bold">A</text>
              </svg>
              <span>MText</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_TEXT" data-tip-title="Single Line Text" data-tip-desc="Creates a single-line text object.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <text x="6" y="24" fill="#ffd166" font-size="20">A_</text>
              </svg>
              <span>Single Line</span>
            </button>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_STYLE" data-tip-title="Text Style" data-tip-desc="Manages text styles.">
                <svg viewBox="0 0 16 16" width="13" height="13"><text x="3" y="12" fill="#fff" font-size="10" font-weight="bold">S</text></svg>
                <span>Style</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_FIND" data-tip-title="Find & Replace" data-tip-desc="Finds, replaces, and selects text in drawing.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="6" cy="6" r="4" fill="none" stroke="#ffd166" stroke-width="1.5"/><line x1="9" y1="9" x2="13" y2="13" stroke="#ffd166" stroke-width="1.8"/></svg>
                <span>Find</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Text</div>
        </div>

        <!-- 3.2 DIMENSIONS PANEL -->
        <div class="panel" id="panel-ann-dim">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_DIM" data-tip-title="Dimension" data-tip-desc="Creates multiple types of dimensions.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="5" y1="18" x2="27" y2="18" stroke="#ffd166" stroke-width="2"/>
                <polygon points="5,18 9,15 9,21" fill="#ffd166"/>
                <polygon points="27,18 23,15 23,21" fill="#ffd166"/>
              </svg>
              <span>Dimension</span>
            </button>

            <!-- Dim Cluster 1 -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_DIMLINEAR" data-tip-title="Linear Dimension" data-tip-desc="Creates a horizontal or vertical dimension line.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="2" y1="8" x2="14" y2="8" stroke="#00b4d8" stroke-width="1.5"/><line x1="2" y1="4" x2="2" y2="12" stroke="#00b4d8" stroke-width="1.2"/><line x1="14" y1="4" x2="14" y2="12" stroke="#00b4d8" stroke-width="1.2"/></svg>
                <span>Linear</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMALIGNED" data-tip-title="Aligned Dimension" data-tip-desc="Creates an aligned linear dimension line.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="13" y2="3" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Aligned</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMANGULAR" data-tip-title="Angular Dimension" data-tip-desc="Creates an angular dimension.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M 3,13 A 10,10 0 0,1 13,3" fill="none" stroke="#ffd166" stroke-width="1.5"/></svg>
                <span>Angular</span>
              </button>
            </div>

            <!-- Dim Cluster 2 -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_DIMRADIUS" data-tip-title="Radius Dimension" data-tip-desc="Creates a radial dimension for circles or arcs.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="5" fill="none" stroke="#06d6a0" stroke-width="1.2"/><line x1="8" y1="8" x2="13" y2="5" stroke="#06d6a0" stroke-width="1.5"/></svg>
                <span>Radius</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMDIAMETER" data-tip-title="Diameter Dimension" data-tip-desc="Creates a diameter dimension for circles or arcs.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="5" fill="none" stroke="#06d6a0" stroke-width="1.2"/><line x1="4" y1="12" x2="12" y2="4" stroke="#06d6a0" stroke-width="1.5"/></svg>
                <span>Diameter</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMSTYLE" data-tip-title="Dimension Style Manager" data-tip-desc="Creates and modifies dimension styles.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#fff" stroke-width="1.2"/><text x="4" y="11" fill="#fff" font-size="8">ISO</text></svg>
                <span>Dim Style</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Dimensions</div>
        </div>

        <!-- 3.3 CENTERLINES PANEL -->
        <div class="panel" id="panel-ann-centerlines">
          <div class="panel-content">
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_CENTERMARK" data-tip-title="Center Mark" data-tip-desc="Creates an associative cross mark at center of a circle or arc.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="5" fill="none" stroke="#00b4d8" stroke-width="1"/><line x1="8" y1="1" x2="8" y2="15" stroke="#00b4d8" stroke-width="1.5"/><line x1="1" y1="8" x2="15" y2="8" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Center Mark</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_CENTERLINE" data-tip-title="Centerline" data-tip-desc="Creates centerline geometry associated with selected lines.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="4" y1="2" x2="4" y2="14" stroke="#888" stroke-width="1.2"/><line x1="12" y1="2" x2="12" y2="14" stroke="#888" stroke-width="1.2"/><line x1="8" y1="1" x2="8" y2="15" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="2,2"/></svg>
                <span>Centerline</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Centerlines</div>
        </div>

        <!-- 3.4 LEADERS PANEL -->
        <div class="panel" id="panel-ann-leaders">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_MLEADER" data-tip-title="Multileader" data-tip-desc="Creates multileader object.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="4" y1="24" x2="16" y2="12" stroke="#00b4d8" stroke-width="2"/>
                <line x1="16" y1="12" x2="28" y2="12" stroke="#00b4d8" stroke-width="2"/>
                <polygon points="4,24 8,20 10,22" fill="#00b4d8"/>
              </svg>
              <span>Leader</span>
            </button>
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_AIMLEADEREDITADD" data-tip-title="Add Leader" data-tip-desc="Adds leader lines to an existing multileader.">
                <svg viewBox="0 0 16 16" width="13" height="13"><text x="2" y="12" fill="#06d6a0" font-size="11" font-weight="bold">+</text></svg>
                <span>Add Leader</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_MLEADERALIGN" data-tip-title="Align Leaders" data-tip-desc="Aligns selected multileaders.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="4" x2="13" y2="4" stroke="#00b4d8" stroke-width="1.2"/><line x1="3" y1="8" x2="13" y2="8" stroke="#00b4d8" stroke-width="1.2"/><line x1="3" y1="12" x2="13" y2="12" stroke="#00b4d8" stroke-width="1.2"/></svg>
                <span>Align</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_MLEADERCOLLECT" data-tip-title="Collect Leaders" data-tip-desc="Organizes selected multileaders that contain blocks.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="4" height="4" fill="#ffd166"/><rect x="9" y="3" width="4" height="4" fill="#ffd166"/><rect x="6" y="9" width="4" height="4" fill="#ffd166"/></svg>
                <span>Collect</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Leaders</div>
        </div>

        <!-- 3.5 TABLES PANEL -->
        <div class="panel" id="panel-ann-tables">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_TABLE" data-tip-title="Table" data-tip-desc="Creates an empty table object.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="5" y="6" width="22" height="20" fill="none" stroke="#06d6a0" stroke-width="1.8"/>
                <line x1="5" y1="13" x2="27" y2="13" stroke="#06d6a0" stroke-width="1.5"/>
                <line x1="5" y1="19" x2="27" y2="19" stroke="#06d6a0" stroke-width="1.5"/>
                <line x1="16" y1="6" x2="16" y2="26" stroke="#06d6a0" stroke-width="1.5"/>
              </svg>
              <span>Table</span>
            </button>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_TABLESTYLE" data-tip-title="Table Style" data-tip-desc="Creates, modifies, or manages table styles.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#fff" stroke-width="1.2"/></svg>
                <span>Table Style</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DATALINK" data-tip-title="Data Link" data-tip-desc="Links drawing table to Excel spreadsheet.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="4" fill="none" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Excel Link</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Tables</div>
        </div>

        <!-- 3.6 MARKUP & REVCLOUD PANEL -->
        <div class="panel" id="panel-ann-markup">
          <div class="panel-content">
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_REVCLOUD" data-tip-title="Revision Cloud" data-tip-desc="Creates revision clouds using polylines.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M4 11 A 3 3 0 0 1 6 5 A 4 4 0 0 1 12 5 A 3 3 0 0 1 14 11 Z" fill="none" stroke="#ef476f" stroke-width="1.5"/></svg>
                <span>Rev Cloud</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_WIPEOUT" data-tip-title="Wipeout" data-tip-desc="Creates a polygonal area that masks underlying objects.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,3 13,3 10,13 3,10" fill="#fff" stroke="#888" stroke-width="1"/></svg>
                <span>Wipeout</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Markup</div>
        </div>

      </div><!-- /tab-annotate -->

      <!-- ================= 4. PARAMETRIC TAB ================= -->
      <div class="tab-content" id="tab-parametric">

        <!-- 4.1 GEOMETRIC CONSTRAINTS PANEL -->
        <div class="panel" id="panel-par-geom">
          <div class="panel-content">
            <!-- Row 1: Coincident, Collinear, Concentric -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _COINCIDENT" data-tip-title="Coincident" data-tip-desc="Constrains two points together or a point to a curve.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="4" fill="#00b4d8"/><circle cx="8" cy="8" r="2" fill="#fff"/></svg>
                <span>Coincident</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _COLLINEAR" data-tip-title="Collinear" data-tip-desc="Constrains two or more lines to lie along the same infinite line.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="2" y1="8" x2="6" y2="8" stroke="#00b4d8" stroke-width="2"/><line x1="10" y1="8" x2="14" y2="8" stroke="#00b4d8" stroke-width="2"/></svg>
                <span>Collinear</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _CONCENTRIC" data-tip-title="Concentric" data-tip-desc="Constrains circles or arcs to share the same center point.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="6" fill="none" stroke="#ffd166" stroke-width="1.2"/><circle cx="8" cy="8" r="3" fill="none" stroke="#ffd166" stroke-width="1.2"/></svg>
                <span>Concentric</span>
              </button>
            </div>

            <!-- Row 2: Parallel, Perpendicular, Tangent -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _PARALLEL" data-tip-title="Parallel" data-tip-desc="Constrains two lines to remain parallel.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="4" y1="3" x2="4" y2="13" stroke="#06d6a0" stroke-width="2"/><line x1="10" y1="3" x2="10" y2="13" stroke="#06d6a0" stroke-width="2"/></svg>
                <span>Parallel</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _PERPENDICULAR" data-tip-title="Perpendicular" data-tip-desc="Constrains two lines to maintain a 90-degree angle.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="13" y2="13" stroke="#ef476f" stroke-width="2"/><line x1="8" y1="3" x2="8" y2="13" stroke="#ef476f" stroke-width="2"/></svg>
                <span>Perpendicular</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _TANGENT" data-tip-title="Tangent" data-tip-desc="Constrains two curves to remain tangent to each other.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="7" cy="8" r="4.5" fill="none" stroke="#ffd166" stroke-width="1.5"/><line x1="12" y1="2" x2="12" y2="14" stroke="#ffd166" stroke-width="1.8"/></svg>
                <span>Tangent</span>
              </button>
            </div>

            <!-- Row 3: Horizontal, Vertical, Equal -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _HORIZONTAL" data-tip-title="Horizontal" data-tip-desc="Constrains lines or pairs of points to lie parallel to X axis.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="2" y1="8" x2="14" y2="8" stroke="#00b4d8" stroke-width="2.2"/></svg>
                <span>Horizontal</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _VERTICAL" data-tip-title="Vertical" data-tip-desc="Constrains lines or pairs of points to lie parallel to Y axis.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="8" y1="2" x2="8" y2="14" stroke="#00b4d8" stroke-width="2.2"/></svg>
                <span>Vertical</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _EQUAL" data-tip-title="Equal" data-tip-desc="Resizes arcs/circles to equal radius or lines to equal length.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="4" y1="6" x2="12" y2="6" stroke="#ffd166" stroke-width="1.8"/><line x1="4" y1="10" x2="12" y2="10" stroke="#ffd166" stroke-width="1.8"/></svg>
                <span>Equal</span>
              </button>
            </div>

            <!-- Row 4: Fix, Smooth, Symmetric -->
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _FIX" data-tip-title="Fix" data-tip-desc="Locks points and curves in position and orientation.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="4" y="8" width="8" height="6" rx="1" fill="#ef476f"/><path d="M5 8V5a3 3 0 0 1 6 0v3" fill="none" stroke="#ef476f" stroke-width="1.4"/></svg>
                <span>Fix</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _SMOOTH" data-tip-title="Smooth" data-tip-desc="Constrains a spline to be fluid and maintain G2 continuity with another curve.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M2 13 C 6 13, 8 3, 14 3" fill="none" stroke="#06d6a0" stroke-width="2"/></svg>
                <span>Smooth</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_GEOMCONSTRAINT _SYMMETRIC" data-tip-title="Symmetric" data-tip-desc="Constrains two curves or points to maintain symmetry about a selected line.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="8" y1="2" x2="8" y2="14" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="2,2"/><circle cx="4" cy="8" r="2" fill="#00b4d8"/><circle cx="12" cy="8" r="2" fill="#00b4d8"/></svg>
                <span>Symmetric</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Geometric Constraints</div>
        </div>

        <!-- 4.2 DIMENSIONAL CONSTRAINTS PANEL -->
        <div class="panel" id="panel-par-dim">
          <div class="panel-content">
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_DIMCONSTRAINT _L" data-tip-title="Linear Constraint" data-tip-desc="Constrains the horizontal or vertical distance between points.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="2" y1="8" x2="14" y2="8" stroke="#ffd166" stroke-width="1.5"/><line x1="2" y1="4" x2="2" y2="12" stroke="#ffd166" stroke-width="1.2"/><line x1="14" y1="4" x2="14" y2="12" stroke="#ffd166" stroke-width="1.2"/></svg>
                <span>Linear</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMCONSTRAINT _A" data-tip-title="Aligned Constraint" data-tip-desc="Constrains the distance between two points.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="13" y2="3" stroke="#ffd166" stroke-width="1.5"/></svg>
                <span>Aligned</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMCONSTRAINT _R" data-tip-title="Radius Constraint" data-tip-desc="Constrains radius of a circle or arc.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="5" fill="none" stroke="#00b4d8" stroke-width="1.2"/><line x1="8" y1="8" x2="13" y2="5" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Radius</span>
              </button>
            </div>
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_DIMCONSTRAINT _D" data-tip-title="Diameter Constraint" data-tip-desc="Constrains diameter of a circle or arc.">
                <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="5" fill="none" stroke="#00b4d8" stroke-width="1.2"/><line x1="4" y1="12" x2="12" y2="4" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>Diameter</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMCONSTRAINT _AN" data-tip-title="Angular Constraint" data-tip-desc="Constrains angle between two lines.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M 3,13 A 10,10 0 0,1 13,3" fill="none" stroke="#06d6a0" stroke-width="1.5"/></svg>
                <span>Angular</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_DIMCONSTRAINT _C" data-tip-title="Convert Constraint" data-tip-desc="Converts associative dimensions to dimensional constraints.">
                <svg viewBox="0 0 16 16" width="13" height="13"><path d="M 4,8 L 12,8 M 9,5 L 12,8 L 9,11" fill="none" stroke="#ef476f" stroke-width="1.5"/></svg>
                <span>Convert</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Dimensional</div>
        </div>

        <!-- 4.3 MANAGE CONSTRAINTS PANEL -->
        <div class="panel" id="panel-par-manage">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_AUTOCONSTRAIN" data-tip-title="Auto Constrain" data-tip-desc="Applies geometric constraints automatically based on geometry relationships.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="10" fill="none" stroke="#ffd166" stroke-width="2"/>
                <text x="11" y="21" fill="#ffd166" font-size="14" font-weight="bold">A</text>
              </svg>
              <span>Auto</span>
            </button>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_DELCONSTRAINT" data-tip-title="Delete Constraints" data-tip-desc="Removes all geometric and dimensional constraints from selected objects.">
                <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="3" x2="13" y2="13" stroke="#ef476f" stroke-width="1.8"/><line x1="13" y1="3" x2="3" y2="13" stroke="#ef476f" stroke-width="1.8"/></svg>
                <span>Delete All</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_PARAMETERS" data-tip-title="Parameters Manager" data-tip-desc="Opens the Parameters Manager palette.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="none" stroke="#00b4d8" stroke-width="1.2"/><text x="4" y="11" fill="#00b4d8" font-size="8">fx</text></svg>
                <span>Parameters</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Manage</div>
        </div>

      </div><!-- /tab-parametric -->

      <!-- ================= 5. VIEW TAB ================= -->
      <div class="tab-content" id="tab-view">

        <!-- 5.1 NAVIGATE 2D PANEL -->
        <div class="panel" id="panel-view-nav">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_PAN" data-tip-title="Pan" data-tip-desc="Shifts the display without changing the magnification.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="9" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <path d="M12 16 L20 16 M16 12 L16 20" stroke="#00b4d8" stroke-width="2"/>
              </svg>
              <span>Pan</span>
            </button>

            <!-- Zoom Split Button -->
            <div class="split-btn">
              <button class="split-main" data-cmd="^C^C_ZOOM _E" data-tip-title="Zoom Extents" data-tip-desc="Zooms to display the maximum extents of all objects.">
                <svg viewBox="0 0 32 32" width="28" height="28">
                  <circle cx="14" cy="14" r="8" fill="none" stroke="#ffd166" stroke-width="2"/>
                  <line x1="20" y1="20" x2="27" y2="27" stroke="#ffd166" stroke-width="2.5" stroke-linecap="round"/>
                  <polygon points="14,9 11,13 17,13" fill="#ffd166"/>
                  <polygon points="14,19 11,15 17,15" fill="#ffd166"/>
                </svg>
                <span>Zoom</span>
              </button>
              <button class="split-arrow" data-dropdown="menu-zoom">▾</button>
            </div>

            <button class="btn-big" data-cmd="^C^C_3DORBIT" data-tip-title="3D Orbit" data-tip-desc="Rotates the view in 3D space.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="10" fill="none" stroke="#06d6a0" stroke-width="2" stroke-dasharray="3,3"/>
                <polygon points="16,3 13,8 19,8" fill="#06d6a0"/>
              </svg>
              <span>Orbit</span>
            </button>
          </div>
          <div class="panel-footer">Navigate 2D</div>
        </div>

        <!-- 5.2 VIEWS & VIEWPORTS PANEL -->
        <div class="panel" id="panel-view-vports">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_UCS" data-tip-title="User Coordinate System" data-tip-desc="Manages user coordinate systems.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <line x1="6" y1="26" x2="26" y2="26" stroke="#ef476f" stroke-width="2.5"/>
                <line x1="6" y1="26" x2="6" y2="6" stroke="#06d6a0" stroke-width="2.5"/>
                <text x="23" y="22" fill="#ef476f" font-size="10">X</text><text x="9" y="13" fill="#06d6a0" font-size="10">Y</text>
              </svg>
              <span>UCS</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_VPORTS" data-tip-title="Viewports" data-tip-desc="Creates multiple viewports in model space or layout.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="5" y="5" width="22" height="22" fill="none" stroke="#00b4d8" stroke-width="1.8"/>
                <line x1="16" y1="5" x2="16" y2="27" stroke="#00b4d8" stroke-width="1.5"/>
              </svg>
              <span>Viewports</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_VIEW" data-tip-title="View Manager" data-tip-desc="Saves and restores named views.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="8" width="20" height="16" fill="none" stroke="#ffd166" stroke-width="2"/>
                <circle cx="16" cy="16" r="4" fill="#ffd166"/>
              </svg>
              <span>Named Views</span>
            </button>
          </div>
          <div class="panel-footer">Views & Viewports</div>
        </div>

        <!-- 5.3 VISUAL STYLES PANEL -->
        <div class="panel" id="panel-view-styles">
          <div class="panel-content">
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_VSCURRENT _2D" data-tip-title="2D Wireframe" data-tip-desc="Displays objects using lines and curves.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,13 8,3 13,13" fill="none" stroke="#00b4d8" stroke-width="1.5"/></svg>
                <span>2D Wire</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_VSCURRENT _C" data-tip-title="Conceptual" data-tip-desc="Displays objects with smooth shading and Gooch face style.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,13 8,3 13,13" fill="#ffd166"/></svg>
                <span>Conceptual</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_VSCURRENT _H" data-tip-title="Hidden" data-tip-desc="Displays objects using 3D wireframe representation and hides back lines.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,13 8,3 13,13" fill="#222" stroke="#888"/></svg>
                <span>Hidden</span>
              </button>
            </div>
            <div class="btn-cluster-3">
              <button class="btn-small" data-cmd="^C^C_VSCURRENT _R" data-tip-title="Realistic" data-tip-desc="Displays objects with smooth shading and materials.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,13 8,3 13,13" fill="#06d6a0"/></svg>
                <span>Realistic</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_VSCURRENT _S" data-tip-title="Shaded" data-tip-desc="Displays objects with smooth shading.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,13 8,3 13,13" fill="#00b4d8"/></svg>
                <span>Shaded</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_VSCURRENT _X" data-tip-title="X-Ray" data-tip-desc="Displays objects with partial transparency.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,13 8,3 13,13" fill="rgba(0,180,216,0.3)" stroke="#00b4d8"/></svg>
                <span>X-Ray</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Visual Styles</div>
        </div>

        <!-- 5.4 PALETTES PANEL -->
        <div class="panel" id="panel-view-palettes">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_PROPERTIES" data-tip-title="Properties Palette" data-tip-desc="Opens Properties palette.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="5" width="20" height="22" fill="none" stroke="#fff" stroke-width="1.5"/>
                <line x1="10" y1="11" x2="22" y2="11" stroke="#ffd166" stroke-width="1.5"/>
                <line x1="10" y1="17" x2="18" y2="17" stroke="#ffd166" stroke-width="1.5"/>
              </svg>
              <span>Properties</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_LAYER" data-tip-title="Layer Properties" data-tip-desc="Opens Layer Properties Manager.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <polygon points="16,6 26,11 16,16 6,11" fill="#00b4d8"/>
                <polygon points="16,12 26,17 16,22 6,17" fill="#ffd166"/>
                <polygon points="16,18 26,23 16,28 6,23" fill="#ff4d4f"/>
              </svg>
              <span>Layer Props</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_TOOLPALETTES" data-tip-title="Tool Palettes" data-tip-desc="Opens Tool Palettes window.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="5" width="6" height="22" fill="#00b4d8"/>
                <rect x="15" y="5" width="11" height="22" fill="none" stroke="#888" stroke-width="1.2"/>
              </svg>
              <span>Tool Palettes</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_COMMANDLINE" data-tip-title="Command Line" data-tip-desc="Displays Command Line window.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="4" y="10" width="24" height="12" fill="#111" stroke="#888"/>
                <text x="7" y="19" fill="#00b4d8" font-size="10">>_</text>
              </svg>
              <span>Command Line</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_SHEETSET" data-tip-title="Sheet Set Manager" data-tip-desc="Opens Sheet Set Manager.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="6" width="16" height="20" fill="none" stroke="#fff" stroke-width="1.5"/>
                <rect x="10" y="10" width="16" height="20" fill="#00b4d8" opacity="0.7"/>
              </svg>
              <span>Sheet Set</span>
            </button>
          </div>
          <div class="panel-footer">Palettes</div>
        </div>

      </div><!-- /tab-view -->

      <!-- ================= 6. MANAGE TAB ================= -->
      <div class="tab-content" id="tab-manage">

        <!-- 6.1 CUSTOMIZATION PANEL -->
        <div class="panel" id="panel-man-custom">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_CUI" data-tip-title="Customize User Interface" data-tip-desc="Manages customized user interface elements.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="10" fill="none" stroke="#ffd166" stroke-width="2"/>
                <path d="M16 11 L16 13 M16 19 L16 21 M11 16 L13 16 M19 16 L21 16" stroke="#ffd166" stroke-width="2"/>
              </svg>
              <span>CUI</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_ALIASEDIT" data-tip-title="Edit Aliases" data-tip-desc="Edits command aliases in the acad.pgp file.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="6" width="20" height="20" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <text x="9" y="20" fill="#00b4d8" font-size="12" font-weight="bold">PGP</text>
              </svg>
              <span>Aliases</span>
            </button>
          </div>
          <div class="panel-footer">Customization</div>
        </div>

        <!-- 6.2 APPLICATIONS PANEL -->
        <div class="panel" id="panel-man-apps">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_APPLOAD" data-tip-title="Load Application" data-tip-desc="Loads ObjectARX, LISP, and bundle plug-ins.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M7 6 L25 6 L25 26 L7 26 Z" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <polygon points="16,11 21,17 11,17" fill="#06d6a0"/>
              </svg>
              <span>AppLoad</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_SCRIPT" data-tip-title="Run Script" data-tip-desc="Executes a sequence of commands from a script file (.scr).">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="7" y="5" width="18" height="22" fill="none" stroke="#06d6a0" stroke-width="2"/>
                <line x1="11" y1="11" x2="21" y2="11" stroke="#06d6a0" stroke-width="1.5"/>
                <line x1="11" y1="16" x2="21" y2="16" stroke="#06d6a0" stroke-width="1.5"/>
              </svg>
              <span>Script</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_VLIDE" data-tip-title="Visual LISP" data-tip-desc="Opens Visual LISP environment.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="6" y="6" width="20" height="20" fill="none" stroke="#ef476f" stroke-width="2"/>
                <text x="9" y="20" fill="#ef476f" font-size="11" font-weight="bold">(L)</text>
              </svg>
              <span>VLISP</span>
            </button>
          </div>
          <div class="panel-footer">Applications</div>
        </div>

        <!-- 6.3 CLEANUP & STANDARDS PANEL -->
        <div class="panel" id="panel-man-clean">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_AUDIT" data-tip-title="Audit" data-tip-desc="Evaluates integrity of drawing and corrects errors.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M8 16 L14 22 L24 10" fill="none" stroke="#06d6a0" stroke-width="3"/>
              </svg>
              <span>Audit</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_PURGE" data-tip-title="Purge" data-tip-desc="Removes unused named objects such as layers and blocks.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M6 8 L26 8 M10 8 L10 24 L22 24 L22 8" fill="none" stroke="#ef476f" stroke-width="2"/>
              </svg>
              <span>Purge</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_RECOVER" data-tip-title="Recover" data-tip-desc="Repairs a damaged drawing file.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="10" fill="none" stroke="#ffd166" stroke-width="2"/>
                <path d="M12 16 L20 16 M16 12 L16 20" stroke="#ffd166" stroke-width="2.5"/>
              </svg>
              <span>Recover</span>
            </button>
          </div>
          <div class="panel-footer">Cleanup & Standards</div>
        </div>

      </div><!-- /tab-manage -->

      <!-- ================= 7. OUTPUT TAB ================= -->
      <div class="tab-content" id="tab-output">

        <!-- 7.1 PLOT PANEL -->
        <div class="panel" id="panel-out-plot">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_PLOT" data-tip-title="Plot" data-tip-desc="Plots a drawing to a plotter, printer, or PDF file.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="8" y="5" width="16" height="8" fill="none" stroke="#fff" stroke-width="1.5"/>
                <rect x="5" y="13" width="22" height="10" fill="#00b4d8"/>
                <rect x="8" y="18" width="16" height="9" fill="#fff"/>
              </svg>
              <span>Plot</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_PUBLISH" data-tip-title="Batch Plot" data-tip-desc="Publishes drawings to DWF, DWFx, and PDF files, or to plotters.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="5" y="8" width="18" height="18" fill="none" stroke="#ffd166" stroke-width="1.8"/>
                <rect x="9" y="4" width="18" height="18" fill="none" stroke="#ffd166" stroke-width="1.8"/>
              </svg>
              <span>Batch Plot</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_PREVIEW" data-tip-title="Plot Preview" data-tip-desc="Displays the drawing as it will be plotted.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="9" fill="none" stroke="#06d6a0" stroke-width="2"/>
                <circle cx="16" cy="16" r="3" fill="#06d6a0"/>
              </svg>
              <span>Preview</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_PAGESETUP" data-tip-title="Page Setup Manager" data-tip-desc="Controls page layout, device, paper size, and plot settings.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="7" y="5" width="18" height="22" fill="none" stroke="#fff" stroke-width="2"/>
                <circle cx="16" cy="16" r="4" fill="#00b4d8"/>
              </svg>
              <span>Page Setup</span>
            </button>
          </div>
          <div class="panel-footer">Plot</div>
        </div>

        <!-- 7.2 EXPORT & SEND PANEL -->
        <div class="panel" id="panel-out-export">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_EXPORTPDF" data-tip-title="Export to PDF" data-tip-desc="Creates a PDF file from current layout or drawing.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="7" y="5" width="18" height="22" fill="#ef476f" rx="2"/>
                <text x="8" y="19" fill="#fff" font-size="9" font-weight="bold">EXPORT</text>
              </svg>
              <span>Export PDF</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_EXPORTDWF" data-tip-title="Export to DWF" data-tip-desc="Creates a DWF file from current layout.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="7" y="5" width="18" height="22" fill="#00b4d8" rx="2"/>
                <text x="8" y="19" fill="#fff" font-size="9" font-weight="bold">DWF</text>
              </svg>
              <span>Export DWF</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_ETRANSMIT" data-tip-title="eTransmit" data-tip-desc="Packages a set of files for transmission over Internet or email.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M6 10 L16 18 L26 10" fill="none" stroke="#ffd166" stroke-width="2.5"/>
                <rect x="6" y="8" width="20" height="16" fill="none" stroke="#ffd166" stroke-width="1.8"/>
              </svg>
              <span>eTransmit</span>
            </button>
          </div>
          <div class="panel-footer">Export & Send</div>
        </div>

      </div><!-- /tab-output -->

      <!-- ================= 8. COLLABORATE TAB ================= -->
      <div class="tab-content" id="tab-collaborate">

        <!-- 8.1 SHARE PANEL -->
        <div class="panel" id="panel-collab-share">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_SHARE" data-tip-title="Share Drawing" data-tip-desc="Shares a link to a copy of the current drawing to view or edit in AutoCAD on the web or mobile.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="23" cy="8" r="4" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <circle cx="9" cy="16" r="4" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <circle cx="23" cy="24" r="4" fill="none" stroke="#00b4d8" stroke-width="2"/>
                <line x1="12.5" y1="14" x2="19.5" y2="10" stroke="#00b4d8" stroke-width="1.8"/>
                <line x1="12.5" y1="18" x2="19.5" y2="22" stroke="#00b4d8" stroke-width="1.8"/>
              </svg>
              <span>Share</span>
            </button>
            <button class="btn-big" data-cmd="^C^C_SHAREDVIEWS" data-tip-title="Shared Views" data-tip-desc="Opens the Shared Views palette to publish 2D and 3D views of your design for online review.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M4 16 C 9 8, 23 8, 28 16 C 23 24, 9 24, 4 16 Z" fill="none" stroke="#06d6a0" stroke-width="2"/>
                <circle cx="16" cy="16" r="4" fill="#06d6a0"/>
              </svg>
              <span>Shared Views</span>
            </button>
          </div>
          <div class="panel-footer">Share</div>
        </div>

        <!-- 8.2 COMPARE PANEL -->
        <div class="panel" id="panel-collab-compare">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_COMPARE" data-tip-title="DWG Compare" data-tip-desc="Compares a specified drawing file with the current drawing file, highlighting differences in color.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <rect x="5" y="8" width="14" height="18" rx="1" fill="none" stroke="#00b4d8" stroke-width="1.8"/>
                <rect x="13" y="4" width="14" height="18" rx="1" fill="rgba(255,209,102,0.2)" stroke="#ffd166" stroke-width="1.8"/>
                <line x1="9" y1="14" x2="15" y2="14" stroke="#00b4d8" stroke-width="1.5"/>
                <line x1="17" y1="10" x2="23" y2="10" stroke="#ffd166" stroke-width="1.5"/>
              </svg>
              <span>DWG Compare</span>
            </button>
          </div>
          <div class="panel-footer">Compare</div>
        </div>

        <!-- 8.3 TRACE & REVIEW PANEL -->
        <div class="panel" id="panel-collab-trace">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_TRACE" data-tip-title="Trace" data-tip-desc="Opens the Trace palette to provide feedback, markups, and design revisions without altering drawing geometry.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <path d="M6 26 L10 26 L24 12 L20 8 L6 22 Z" fill="none" stroke="#ffd166" stroke-width="1.8"/>
                <line x1="18" y1="10" x2="22" y2="14" stroke="#ffd166" stroke-width="1.8"/>
                <path d="M4 28 C 10 28, 14 30, 28 28" stroke="#00b4d8" stroke-width="1.8" stroke-linecap="round"/>
              </svg>
              <span>Trace</span>
            </button>
            <div class="btn-cluster-2">
              <button class="btn-small" data-cmd="^C^C_MARKUPIMPORT" data-tip-title="Markup Import" data-tip-desc="Imports a marked-up drawing file (PDF, PNG, JPG) to overlay on your drawing.">
                <svg viewBox="0 0 16 16" width="13" height="13"><rect x="2" y="2" width="12" height="12" rx="1" fill="none" stroke="#00b4d8" stroke-width="1.2"/><polygon points="8,4 12,8 9,8 9,12 7,12 7,8 4,8" fill="#00b4d8"/></svg>
                <span>Import</span>
              </button>
              <button class="btn-small" data-cmd="^C^C_MARKUPASSIST" data-tip-title="Markup Assist" data-tip-desc="Automatically identifies markups in imported files as text and revision clouds.">
                <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="8,1 10,6 15,6 11,9 13,14 8,11 3,14 5,9 1,6 6,6" fill="#ffd166"/></svg>
                <span>Assist</span>
              </button>
            </div>
          </div>
          <div class="panel-footer">Trace & Markup</div>
        </div>

        <!-- 8.4 HISTORY PANEL -->
        <div class="panel" id="panel-collab-history">
          <div class="panel-content">
            <button class="btn-big" data-cmd="^C^C_DWGHISTORY" data-tip-title="Drawing History" data-tip-desc="Opens the Drawing History palette to view and compare previous versions saved in cloud storage.">
              <svg viewBox="0 0 32 32" width="28" height="28">
                <circle cx="16" cy="16" r="11" fill="none" stroke="#ef476f" stroke-width="2"/>
                <polyline points="16,9 16,16 21,19" fill="none" stroke="#ef476f" stroke-width="2" stroke-linecap="round"/>
                <path d="M16 5 A 11 11 0 0 0 6 12 L 4 8" fill="none" stroke="#ef476f" stroke-width="1.8"/>
              </svg>
              <span>History</span>
            </button>
          </div>
          <div class="panel-footer">History</div>
        </div>

      </div><!-- /tab-collaborate -->

    </div><!-- /ribbon-body -->
  </div><!-- /ribbon-container -->

  <!-- ================= FLOATING DROPDOWN MENUS (BODY LEVEL) ================= -->
  <!-- Circle Dropdown -->
  <div class="cad-menu" id="menu-circle">
    <div class="cad-menu-item" data-cmd="^C^C_CIRCLE">Center, Radius</div>
    <div class="cad-menu-item" data-cmd="^C^C_CIRCLE _D">Center, Diameter</div>
    <div class="cad-menu-item" data-cmd="^C^C_CIRCLE _2P">2-Point</div>
    <div class="cad-menu-item" data-cmd="^C^C_CIRCLE _3P">3-Point</div>
    <div class="cad-menu-item" data-cmd="^C^C_CIRCLE _TTR">Tan, Tan, Radius</div>
    <div class="cad-menu-item" data-cmd="^C^C_CIRCLE _3P _TAN \_TAN \_TAN \">Tan, Tan, Tan</div>
  </div>

  <!-- Arc Dropdown -->
  <div class="cad-menu" id="menu-arc">
    <div class="cad-menu-item" data-cmd="^C^C_ARC">3-Point</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC _C">Start, Center, End</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC _C \_A">Start, Center, Angle</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC _C \_L">Start, Center, Length</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC _E \_A">Start, End, Angle</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC _E \_D">Start, End, Direction</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC _E \_R">Start, End, Radius</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARC ;">Continue</div>
  </div>

  <!-- Rect Dropdown -->
  <div class="cad-menu" id="menu-rect">
    <div class="cad-menu-item" data-cmd="^C^C_RECTANG">Rectangle</div>
    <div class="cad-menu-item" data-cmd="^C^C_POLYGON">Polygon</div>
  </div>

  <!-- Ellipse Dropdown -->
  <div class="cad-menu" id="menu-ellipse">
    <div class="cad-menu-item" data-cmd="^C^C_ELLIPSE _C">Center</div>
    <div class="cad-menu-item" data-cmd="^C^C_ELLIPSE">Axis, End</div>
    <div class="cad-menu-item" data-cmd="^C^C_ELLIPSE _A">Elliptical Arc</div>
  </div>

  <!-- Hatch Dropdown -->
  <div class="cad-menu" id="menu-hatch">
    <div class="cad-menu-item" data-cmd="^C^C_BHATCH">Hatch</div>
    <div class="cad-menu-item" data-cmd="^C^C_GRADIENT">Gradient</div>
    <div class="cad-menu-item" data-cmd="^C^C_BOUNDARY">Boundary</div>
  </div>

  <!-- Trim Dropdown -->
  <div class="cad-menu" id="menu-trim">
    <div class="cad-menu-item" data-cmd="^C^C_TRIM">Trim</div>
    <div class="cad-menu-item" data-cmd="^C^C_EXTEND">Extend</div>
  </div>

  <!-- Fillet Dropdown -->
  <div class="cad-menu" id="menu-fillet">
    <div class="cad-menu-item" data-cmd="^C^C_FILLET">Fillet</div>
    <div class="cad-menu-item" data-cmd="^C^C_CHAMFER">Chamfer</div>
    <div class="cad-menu-item" data-cmd="^C^C_BLEND">Blend Curves</div>
  </div>

  <!-- Array Dropdown -->
  <div class="cad-menu" id="menu-array">
    <div class="cad-menu-item" data-cmd="^C^C_ARRAYRECT">Rectangular Array</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARRAYPATH">Path Array</div>
    <div class="cad-menu-item" data-cmd="^C^C_ARRAYPOLAR">Polar Array</div>
  </div>

  <!-- Text Type Dropdown -->
  <div class="cad-menu" id="menu-text-type">
    <div class="cad-menu-item" data-cmd="^C^C_MTEXT">Multiline Text</div>
    <div class="cad-menu-item" data-cmd="^C^C_TEXT">Single Line Text</div>
  </div>

  <!-- Dimension Types Dropdown -->
  <div class="cad-menu" id="menu-dim-types">
    <div class="cad-menu-item" data-cmd="^C^C_DIMLINEAR">Linear</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMALIGNED">Aligned</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMANGULAR">Angular</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMARC">Arc Length</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMRADIUS">Radius</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMDIAMETER">Diameter</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMJOGGED">Jogged</div>
    <div class="cad-menu-item" data-cmd="^C^C_DIMORDINATE">Ordinate</div>
  </div>

  <!-- Layer List Dropdown -->
  <div class="cad-menu" id="menu-layer-list" style="min-width: 220px;">
    <div class="cad-menu-item" data-cmd="^C^C_-LAYER _S 0 \"><span style="width:12px;height:12px;background:#ffffff;display:inline-block;border:1px solid #888;border-radius:1px;"></span> 0</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LAYER _S Defpoints \"><span style="width:12px;height:12px;background:#888888;display:inline-block;border:1px solid #888;border-radius:1px;"></span> Defpoints</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_LAYER">Layer Properties Manager...</div>
    <div class="cad-menu-item" data-cmd="^C^C_LAYWALK">Layer Walk...</div>
    <div class="cad-menu-item" data-cmd="^C^C_LAYISO">Isolate Selected Layers</div>
    <div class="cad-menu-item" data-cmd="^C^C_LAYUNISO">Unisolate All Layers</div>
  </div>

  <!-- Properties Color Dropdown -->
  <div class="cad-menu" id="menu-color-list" style="min-width: 170px;">
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR ByLayer"><span style="width:10px;height:10px;background:none;border:1px dashed #888;display:inline-block;"></span> ByLayer</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR ByBlock"><span style="width:10px;height:10px;background:none;border:1px solid #fff;display:inline-block;"></span> ByBlock</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 1"><span style="width:10px;height:10px;background:#ff0000;display:inline-block;"></span> 1 Red</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 2"><span style="width:10px;height:10px;background:#ffff00;display:inline-block;"></span> 2 Yellow</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 3"><span style="width:10px;height:10px;background:#00ff00;display:inline-block;"></span> 3 Green</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 4"><span style="width:10px;height:10px;background:#00ffff;display:inline-block;"></span> 4 Cyan</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 5"><span style="width:10px;height:10px;background:#0000ff;display:inline-block;"></span> 5 Blue</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 6"><span style="width:10px;height:10px;background:#ff00ff;display:inline-block;"></span> 6 Magenta</div>
    <div class="cad-menu-item" data-cmd="^C^C_-COLOR 7"><span style="width:10px;height:10px;background:#ffffff;display:inline-block;"></span> 7 White</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_COLOR">Select Color...</div>
  </div>

  <!-- Properties Lineweight Dropdown -->
  <div class="cad-menu" id="menu-lineweight-list" style="min-width: 170px;">
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT ByLayer">ByLayer</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT ByBlock">ByBlock</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT Default">Default</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT 0">0.00 mm</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT 5">0.05 mm</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT 9">0.09 mm</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT 13">0.13 mm</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT 25">0.25 mm</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LWEIGHT 50">0.50 mm</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_LWEIGHT">Lineweight Settings...</div>
  </div>

  <!-- Properties Linetype Dropdown -->
  <div class="cad-menu" id="menu-linetype-list" style="min-width: 170px;">
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S ByLayer ;">ByLayer</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S ByBlock ;">ByBlock</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S Continuous ;">Continuous</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S Center ;">Center</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S Dashed ;">Dashed</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S Hidden ;">Hidden</div>
    <div class="cad-menu-item" data-cmd="^C^C_-LINETYPE _S Phantom ;">Phantom</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_LINETYPE">Other...</div>
  </div>

  <!-- Measure Dropdown -->
  <div class="cad-menu" id="menu-measure">
    <div class="cad-menu-item" data-cmd="^C^C_MEASUREGEOM _QUICK">Quick Measure</div>
    <div class="cad-menu-item" data-cmd="^C^C_MEASUREGEOM _DISTANCE">Distance</div>
    <div class="cad-menu-item" data-cmd="^C^C_MEASUREGEOM _RADIUS">Radius</div>
    <div class="cad-menu-item" data-cmd="^C^C_MEASUREGEOM _ANGLE">Angle</div>
    <div class="cad-menu-item" data-cmd="^C^C_MEASUREGEOM _AREA">Area</div>
    <div class="cad-menu-item" data-cmd="^C^C_MEASUREGEOM _VOLUME">Volume</div>
    <div class="cad-menu-divider"></div>
    <div class="cad-menu-item" data-cmd="^C^C_ID">Point ID</div>
  </div>

  <!-- Paste Dropdown -->
  <div class="cad-menu" id="menu-paste">
    <div class="cad-menu-item" data-cmd="^C^C_PASTECLIP">Paste</div>
    <div class="cad-menu-item" data-cmd="^C^C_PASTEBLOCK">Paste as Block</div>
    <div class="cad-menu-item" data-cmd="^C^C_PASTEORIG">Paste to Original Coords</div>
    <div class="cad-menu-item" data-cmd="^C^C_PASTESPEC">Paste Special...</div>
  </div>

  <!-- Zoom Dropdown (View Tab) -->
  <div class="cad-menu" id="menu-zoom">
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _E">Zoom Extents</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _W">Zoom Window</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _P">Zoom Previous</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _R">Zoom Realtime</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _A">Zoom All</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _D">Zoom Dynamic</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _S">Zoom Scale</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _C">Zoom Center</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM _O">Zoom Object</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM 2X">Zoom In</div>
    <div class="cad-menu-item" data-cmd="^C^C_ZOOM .5X">Zoom Out</div>
  </div>

  <!-- ================= FLOATING EXTENDED TRAYS (BODY LEVEL) ================= -->
  <!-- Extended Draw Tray -->
  <div class="panel-tray" data-for="panel-draw">
    <div style="display:flex; gap:6px;">
      <button class="btn-small" data-cmd="^C^C_SPLINE" data-tip-title="Spline Fit" data-tip-desc="Creates a smooth curve that passes through or near specified points.">
        <svg viewBox="0 0 16 16" width="13" height="13"><path d="M2 13 Q 6 3 10 13 T 14 3" fill="none" stroke="#00b4d8" stroke-width="1.6"/></svg>
        <span>Spline Fit</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_CVSHOW" data-tip-title="Spline CV" data-tip-desc="Creates a spline with control vertices.">
        <svg viewBox="0 0 16 16" width="13" height="13"><path d="M2 13 Q 8 2 14 13" fill="none" stroke="#00b4d8" stroke-width="1.5"/><rect x="7" y="2" width="2" height="2" fill="#fff"/></svg>
        <span>Spline CV</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_CENTERLINE" data-tip-title="Centerline" data-tip-desc="Creates centerline geometry.">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="8" y1="1" x2="8" y2="15" stroke="#ffd166" stroke-width="1.5" stroke-dasharray="2,2"/></svg>
        <span>Centerline</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_CENTERMARK" data-tip-title="Center Mark" data-tip-desc="Creates center mark on circle or arc.">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="8" y1="2" x2="8" y2="14" stroke="#00b4d8" stroke-width="1.5"/><line x1="2" y1="8" x2="14" y2="8" stroke="#00b4d8" stroke-width="1.5"/></svg>
        <span>Center Mark</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_REVCLOUD" data-tip-title="Revision Cloud" data-tip-desc="Creates revision cloud.">
        <svg viewBox="0 0 16 16" width="13" height="13"><path d="M4 11 A 3 3 0 0 1 6 5 A 4 4 0 0 1 12 5 A 3 3 0 0 1 14 11 Z" fill="none" stroke="#ef476f" stroke-width="1.5"/></svg>
        <span>Revcloud</span>
      </button>
    </div>
    <div style="display:flex; gap:6px; margin-top:4px;">
      <button class="btn-small" data-cmd="^C^C_XLINE" data-tip-title="Construction Line" data-tip-desc="Creates a line of infinite length (XLINE).">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="1" y1="15" x2="15" y2="1" stroke="#00b4d8" stroke-width="1.5"/><circle cx="8" cy="8" r="1.5" fill="#fff"/></svg>
        <span>Construction Line</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_RAY" data-tip-title="Ray" data-tip-desc="Creates a line that starts at a point and continues to infinity.">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="13" x2="14" y2="2" stroke="#06d6a0" stroke-width="1.5"/><circle cx="3" cy="13" r="1.5" fill="#fff"/></svg>
        <span>Ray</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_POINT" data-tip-title="Point" data-tip-desc="Creates a point object (POINT).">
        <svg viewBox="0 0 16 16" width="13" height="13"><circle cx="8" cy="8" r="2.5" fill="#ffd166"/></svg>
        <span>Point</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_DIVIDE" data-tip-title="Divide" data-tip-desc="Creates evenly spaced point objects along object.">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="2" y1="8" x2="14" y2="8" stroke="#888" stroke-width="1.5"/><circle cx="5" cy="8" r="1.5" fill="#00b4d8"/><circle cx="11" cy="8" r="1.5" fill="#00b4d8"/></svg>
        <span>Divide</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_REGION" data-tip-title="Region" data-tip-desc="Converts an enclosed shape into a 2D region object.">
        <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="10" height="10" fill="rgba(0,180,216,0.3)" stroke="#00b4d8" stroke-width="1.2"/></svg>
        <span>Region</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_WIPEOUT" data-tip-title="Wipeout" data-tip-desc="Creates a polygonal area that masks underlying objects.">
        <svg viewBox="0 0 16 16" width="13" height="13"><polygon points="3,3 13,3 10,13 3,10" fill="#fff" stroke="#888" stroke-width="1"/></svg>
        <span>Wipeout</span>
      </button>
    </div>
  </div>

  <!-- Extended Modify Tray -->
  <div class="panel-tray" data-for="panel-modify">
    <div style="display:flex; gap:6px;">
      <button class="btn-small" data-cmd="^C^C_JOIN" data-tip-title="Join" data-tip-desc="Joins similar objects to form a single object.">
        <svg viewBox="0 0 16 16" width="13" height="13"><path d="M3 8 L6 8 M10 8 L13 8 M6 5 L10 11" stroke="#00b4d8" stroke-width="1.5"/></svg>
        <span>Join</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_ALIGN" data-tip-title="Align" data-tip-desc="Aligns objects with other objects in 2D or 3D.">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="3" x2="13" y2="13" stroke="#ffd166" stroke-width="1.5"/></svg>
        <span>Align</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_BREAK" data-tip-title="Break" data-tip-desc="Breaks selected object between two points.">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="2" y1="8" x2="6" y2="8" stroke="#ef476f" stroke-width="1.5"/><line x1="10" y1="8" x2="14" y2="8" stroke="#ef476f" stroke-width="1.5"/></svg>
        <span>Break</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_OVERKILL" data-tip-title="Delete Duplicate Objects" data-tip-desc="Removes duplicate or overlapping lines, arcs, and polylines (OVERKILL).">
        <svg viewBox="0 0 16 16" width="13" height="13"><line x1="3" y1="6" x2="13" y2="6" stroke="#06d6a0" stroke-width="1.8"/><line x1="3" y1="10" x2="13" y2="10" stroke="#ef476f" stroke-width="1.2"/></svg>
        <span>Overkill</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_DRAWORDER _F" data-tip-title="Bring to Front" data-tip-desc="Changes the draw order of objects (Bring to Front).">
        <svg viewBox="0 0 16 16" width="13" height="13"><rect x="3" y="3" width="7" height="7" fill="#555"/><rect x="6" y="6" width="7" height="7" fill="#00b4d8"/></svg>
        <span>Bring to Front</span>
      </button>
      <button class="btn-small" data-cmd="^C^C_DRAWORDER _B" data-tip-title="Send to Back" data-tip-desc="Changes the draw order of objects (Send to Back).">
        <svg viewBox="0 0 16 16" width="13" height="13"><rect x="6" y="6" width="7" height="7" fill="#00b4d8"/><rect x="3" y="3" width="7" height="7" fill="#555"/></svg>
        <span>Send to Back</span>
      </button>
    </div>
  </div>

  <!-- Native AutoCAD Rich Tooltip Element -->
  <div id="cad-tooltip">
    <div class="tip-title"></div>
    <div class="tip-desc"></div>
    <div class="tip-cmd"></div>
  </div>

  <!-- Menu Backdrop for robust outside-click handling -->
  <div id="menu-backdrop" class="menu-backdrop"></div>

  <!-- Right-Click Context Menu -->
  <div class="cad-context-menu" id="ctx-ribbon-menu">
    <div class="cad-context-item" data-cmd="^C^C_CUSTOMIZE">
      <span>Add to Quick Access Toolbar</span>
    </div>
    <div class="cad-context-item has-sub" id="ctx-item-tabs">
      <span>Show Tabs</span>
      <div class="cad-sub-menu" id="sub-menu-tabs">
        <div class="cad-context-item" data-toggle-tab="tab-home"><span class="cad-context-check">✓</span><span>Home</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-insert"><span class="cad-context-check">✓</span><span>Insert</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-annotate"><span class="cad-context-check">✓</span><span>Annotate</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-parametric"><span class="cad-context-check">✓</span><span>Parametric</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-view"><span class="cad-context-check">✓</span><span>View</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-manage"><span class="cad-context-check">✓</span><span>Manage</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-output"><span class="cad-context-check">✓</span><span>Output</span></div>
        <div class="cad-context-item" data-toggle-tab="tab-collaborate"><span class="cad-context-check">✓</span><span>Collaborate</span></div>
      </div>
    </div>
    <div class="cad-context-item has-sub" id="ctx-item-panels">
      <span>Show Panels</span>
      <div class="cad-sub-menu" id="sub-menu-panels">
        <!-- Populated dynamically based on active tab -->
      </div>
    </div>
    <div class="cad-menu-divider"></div>
    <div class="cad-context-item" id="ctx-switch-toolbar">
      <span style="color:#00a2ff; font-weight:600;">Switch to Mac Toolbar</span>
    </div>
    <div class="cad-context-item" id="ctx-minimize-ribbon">
      <span>Minimize the Ribbon</span>
    </div>
  </div>

  <script src="ribbon.js"></script>
</body>
</html>
"""

with open("ui/index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated comprehensive ui/index.html successfully!")
