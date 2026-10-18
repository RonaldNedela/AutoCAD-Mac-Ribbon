;;; =========================================================================
;;; MacRibbon for AutoCAD for Mac
;;; Universal AutoLISP Companion & Dynamic Bundle Loader
;;; =========================================================================

(vl-catch-all-apply 'setvar (list "SECURELOAD" 0))

(defun macribbon-write-cmd (cmd / f)
  (vl-catch-all-apply
    '(lambda ()
       (setq f (open "/tmp/ribbon_cmd.txt" "w"))
       (if f
         (progn
           (write-line cmd f)
           (close f)
         )
       )
     )
  )
)

(defun macribbon-locate-bundle (/ lsp candidates found c)
  (setq lsp (findfile "macribbon.lsp"))
  (setq candidates (list
    (if lsp
      (vl-filename-directory (vl-filename-directory (vl-filename-directory lsp)))
      nil
    )
    (strcat (getenv "HOME") "/Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle")
    (strcat (getenv "HOME") "/Library/Application Support/Autodesk/ApplicationPlugins/MacRibbon.bundle")
    "/Applications/Autodesk/ApplicationAddins/MacRibbon.bundle"
    "/Applications/Autodesk/ApplicationPlugins/MacRibbon.bundle"
    "/Users/Ronci/Desktop/AutoCAD-Mac-Ribbon/build/MacRibbon.bundle"
  ))
  (setq found nil)
  (while (and candidates (not found))
    (setq c (car candidates))
    (if (and c (findfile c))
      (setq found c)
    )
    (setq candidates (cdr candidates))
  )
  found
)

(defun macribbon-ensure-loaded (/ bpath binpath)
  (setq bpath (macribbon-locate-bundle))
  (if bpath
    (progn
      (vl-catch-all-apply 'arxload (list bpath))
      (setq binpath (strcat bpath "/Contents/MacOS/MacRibbon"))
      (if (findfile binpath)
        (vl-catch-all-apply 'arxload (list binpath))
      )
    )
  )
)

;; Command: RIBBON
(defun c:ribbon ()
  (vl-catch-all-apply 'setvar (list "SECURELOAD" 0))
  (macribbon-ensure-loaded)
  (macribbon-write-cmd "switchToWindowsRibbon")
  (vl-catch-all-apply 'command (list "_TOOLSETSCLOSE"))
  (princ "\n[MacRibbon] Windows Ribbon enabled.")
  (princ)
)

;; Command: MR (MacRibbon shortcut)
(defun c:mr ()
  (c:ribbon)
  (princ)
)

;; Command: RIBBONCLOSE
(defun c:ribbonclose ()
  (macribbon-write-cmd "switchToMacToolbar")
  (vl-catch-all-apply 'command (list "_TOOLSETS"))
  (princ "\n[MacRibbon] Classic Mac Toolbar enabled. Type 'RIBBON' or 'MR' to re-open.")
  (princ)
)

;; Auto-start Ribbon on load
(macribbon-ensure-loaded)
(macribbon-write-cmd "switchToWindowsRibbon")
(princ "\n[MacRibbon] Windows Ribbon loaded. Type 'RIBBON' or 'MR' to toggle.")
(princ)
