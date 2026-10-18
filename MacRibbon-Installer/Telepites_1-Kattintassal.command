#!/bin/bash
TARGET_DIR="$HOME/Library/Application Support/Autodesk/ApplicationAddins"
mkdir -p "$TARGET_DIR"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "MacRibbon telepítése..."
rm -rf "$TARGET_DIR/MacRibbon.bundle"
cp -R "$SCRIPT_DIR/MacRibbon.bundle" "$TARGET_DIR/"

# Also configure acad.lsp autoload for safety
python3 -c '
import os, glob, re
HOME = os.path.expanduser("~")
autocad_support_dirs = glob.glob(f"{HOME}/Library/Application Support/Autodesk/AutoCAD */R*/roaming/*/Support")
autocad_support_dirs += glob.glob(f"{HOME}/Library/Application Support/Autodesk/AutoCAD */R*/roaming/Support")
snippet = """
;;; >>> MacRibbon Autoload >>>
(vl-catch-all-apply (quote setvar) (list "SECURELOAD" 0))
(defun macribbon_autoload (/ lsp_file bundle_dir bin_path)
  (setq lsp_file (findfile "macribbon.lsp"))
  (if lsp_file
    (load lsp_file)
    (progn
      (setq bundle_dir (strcat (getenv "HOME") "/Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle"))
      (if (findfile bundle_dir)
        (progn
          (vl-catch-all-apply (quote arxload) (list bundle_dir))
          (setq bin_path (strcat bundle_dir "/Contents/MacOS/MacRibbon"))
          (if (findfile bin_path) (vl-catch-all-apply (quote arxload) (list bin_path)))
          (setq lsp_file (strcat bundle_dir "/Contents/Resources/macribbon.lsp"))
          (if (findfile lsp_file) (load lsp_file))
        )
      )
    )
  )
)
(macribbon_autoload)
(defun-q macribbon_startup () (macribbon_autoload))
(setq S::STARTUP (append S::STARTUP (quote ((macribbon_startup)))))
;;; <<< MacRibbon Autoload <<<
"""
for sdir in autocad_support_dirs:
    if os.path.isdir(sdir):
        for fname in ["acad.lsp", "acaddoc.lsp"]:
            p = os.path.join(sdir, fname)
            c = ""
            if os.path.isfile(p):
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    c = f.read()
            c = re.sub(r";;; >>> MacRibbon Autoload >>>.*?;;; <<< MacRibbon Autoload <<<", "", c, flags=re.DOTALL)
            c = c.strip() + "\n" + snippet.strip() + "\n"
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
'

echo "========================================="
echo "✅ MacRibbon sikeresen telepítve!"
echo "Most indítsd el vagy indítsd újra az AutoCAD-et."
echo "AutoCAD parancssor parancsok:"
echo "  - RIBBON vagy MR : Ribbon megjelenítése"
echo "  - RIBBONCLOSE    : Visszaváltás Mac eszköztárra"
echo "========================================="
