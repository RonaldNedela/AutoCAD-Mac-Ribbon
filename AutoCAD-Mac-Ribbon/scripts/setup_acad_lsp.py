#!/usr/bin/env python3
import os
import glob
import re

HOME = os.path.expanduser("~")
autocad_support_dirs = glob.glob(f"{HOME}/Library/Application Support/Autodesk/AutoCAD */R*/roaming/*/Support")
autocad_support_dirs += glob.glob(f"{HOME}/Library/Application Support/Autodesk/AutoCAD */R*/roaming/Support")

lsp_snippet = '''
;;; >>> MacRibbon Autoload >>>
(vl-catch-all-apply 'setvar (list "SECURELOAD" 0))

(defun macribbon_autoload (/ lsp_file bundle_dir bin_path)
  ;; 1. Check if macribbon.lsp is already in Support search path
  (setq lsp_file (findfile "macribbon.lsp"))
  (if lsp_file
    (load lsp_file)
    ;; 2. Direct fallback to ApplicationAddins
    (progn
      (setq bundle_dir (strcat (getenv "HOME") "/Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle"))
      (if (findfile bundle_dir)
        (progn
          (vl-catch-all-apply 'arxload (list bundle_dir))
          (setq bin_path (strcat bundle_dir "/Contents/MacOS/MacRibbon"))
          (if (findfile bin_path) (vl-catch-all-apply 'arxload (list bin_path)))
          (setq lsp_file (strcat bundle_dir "/Contents/Resources/macribbon.lsp"))
          (if (findfile lsp_file) (load lsp_file))
        )
      )
    )
  )
)

(macribbon_autoload)

(defun-q macribbon_startup ()
  (macribbon_autoload)
)
(setq S::STARTUP (append S::STARTUP (quote ((macribbon_startup)))))
;;; <<< MacRibbon Autoload <<<
'''

for sdir in autocad_support_dirs:
    if os.path.isdir(sdir):
        for fname in ["acad.lsp", "acaddoc.lsp"]:
            lsp_file = os.path.join(sdir, fname)
            content = ""
            if os.path.isfile(lsp_file):
                with open(lsp_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

            content = re.sub(r';;; >>> MacRibbon Autoload >>>.*?;;; <<< MacRibbon Autoload <<<', '', content, flags=re.DOTALL)
            content = content.strip() + "\n" + lsp_snippet.strip() + "\n"
            with open(lsp_file, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[MacRibbon] Configured autoload in: {lsp_file}")
