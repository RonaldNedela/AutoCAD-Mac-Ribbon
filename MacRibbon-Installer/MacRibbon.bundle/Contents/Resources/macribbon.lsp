;;; =========================================================================
;;; MacRibbon for AutoCAD for Mac v2.0.0
;;; Universal AutoLISP Companion, Dynamic Bundle Loader & Drawing State Sync
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

(defun macribbon-json-escape (s / i ch out len)
  (if (not s) ""
    (progn
      (setq out "" i 1 len (strlen s))
      (while (<= i len)
        (setq ch (substr s i 1))
        (cond
          ((= ch "\\") (setq out (strcat out "\\\\")))
          ((= ch "\"") (setq out (strcat out "\\\"")))
          (T (setq out (strcat out ch)))
        )
        (setq i (1+ i))
      )
      out
    )
  )
)

(defun macribbon-export-state (/ f tbl name col first clayer cecolor celtype celweight dwg)
  (vl-catch-all-apply
    '(lambda ()
       (setq clayer (getvar "CLAYER"))
       (setq cecolor (getvar "CECOLOR"))
       (setq celtype (getvar "CELTYPE"))
       (setq celweight (getvar "CELWEIGHT"))
       (setq dwg (getvar "DWGNAME"))
       (setq f (open "/tmp/macribbon_state.json" "w"))
       (if f
         (progn
           (write-line "{" f)
           (write-line (strcat "  \"drawing\": \"" (macribbon-json-escape (if dwg dwg "")) "\",") f)
           (write-line (strcat "  \"clayer\": \"" (macribbon-json-escape (if clayer clayer "0")) "\",") f)
           (write-line (strcat "  \"cecolor\": \"" (macribbon-json-escape (if cecolor cecolor "BYLAYER")) "\",") f)
           (write-line (strcat "  \"celtype\": \"" (macribbon-json-escape (if celtype celtype "ByLayer")) "\",") f)
           (write-line (strcat "  \"celweight\": " (itoa (if celweight celweight -1)) ",") f)
           (write-line "  \"layers\": [" f)
           (setq tbl (tblnext "LAYER" T))
           (setq first T)
           (while tbl
             (setq name (cdr (assoc 2 tbl)))
             (setq col (cdr (assoc 62 tbl)))
             (if (not col) (setq col 7))
             (if (not first) (write-line "," f))
             (setq first nil)
             (write-line
               (strcat "    {\"name\":\"" (macribbon-json-escape name) "\",\"color\":" (itoa col) "}")
               f
             )
             (setq tbl (tblnext "LAYER"))
           )
           (write-line "  ]" f)
           (write-line "}" f)
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
    "/Users/Ronci/Documents/AutoCAD/AutoCAD-Mac-Ribbon/build/MacRibbon.bundle"
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
  (macribbon-export-state)
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

;; Command: MRSYNC (manually refresh drawing layers/properties in Ribbon)
(defun c:mrsync ()
  (macribbon-export-state)
  (princ "\n[MacRibbon] Drawing layer and property state synchronized.")
  (princ)
)

;; Auto-start Ribbon and sync drawing layers on load
(macribbon-ensure-loaded)
(macribbon-export-state)
(macribbon-write-cmd "ensureRibbonVisible")
(princ "\n[MacRibbon] Windows Ribbon v2.0.0 ready. Commands: RIBBON, MR, RIBBONCLOSE, MRSYNC.")
(princ)
