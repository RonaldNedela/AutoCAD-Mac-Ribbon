// AutoCAD Windows-style Native Ribbon Controller
(function () {
  const FULL_HEIGHT = 115;
  const MIN_HEIGHT = 25;
  let isMinimized = false;
  let activeMenu = null;
  let activeTray = null;
  let tooltipTimer = null;
  let tooltipEl = null;

  // --- IPC to AutoCAD ---
  function sendToAutoCAD(data) {
    if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.autocad) {
      window.webkit.messageHandlers.autocad.postMessage(data);
    } else {
      console.log('[MacRibbon IPC]:', data);
    }
  }

  function logToAutoCAD(msg) {
    sendToAutoCAD({ action: 'log', message: String(msg) });
  }

  window.onerror = function(msg, url, line, col, error) {
    logToAutoCAD('JS Error: ' + msg + ' (' + url + ':' + line + ':' + col + ')');
    return false;
  };

  function runCommand(cmd) {
    if (!cmd) return;
    logToAutoCAD('Dispatching command: ' + cmd);
    sendToAutoCAD({
      action: 'command',
      command: cmd
    });
  }

  window.setTheme = function(themeName) {
    document.body.classList.toggle('light-theme', themeName === 'light');
    logToAutoCAD('Theme switched to: ' + themeName);
  };

  // --- Tab Management ---
  function setActiveTab(tabId) {
    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
    });

    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.toggle('active', content.id === tabId);
    });

    closeAllMenus();

    if (isMinimized) {
      toggleMinimize(false);
    }
  }

  function toggleMinimize(forceState) {
    isMinimized = forceState !== undefined ? forceState : !isMinimized;
    const container = document.getElementById('ribbon');
    if (container) container.classList.toggle('minimized', isMinimized);

    const targetHeight = isMinimized ? MIN_HEIGHT : FULL_HEIGHT;
    sendToAutoCAD({
      action: 'resize',
      height: targetHeight
    });
  }

  // --- Dropdown Menu & Tray Management ---
  function closeAllMenus() {
    const ctx = document.getElementById('ctx-ribbon-menu');
    const ctxOpen = ctx && ctx.style.display !== 'none';
    const hadOpen = activeMenu !== null || activeTray !== null ||
                    document.querySelector('.cad-menu.show') !== null ||
                    document.querySelector('.panel.expanded') !== null ||
                    ctxOpen;

    document.querySelectorAll('.cad-menu.show').forEach(m => {
      m.classList.remove('show');
      m.style.display = 'none';
    });
    activeMenu = null;

    document.querySelectorAll('.panel.expanded').forEach(p => {
      p.classList.remove('expanded');
    });

    document.querySelectorAll('.panel-tray').forEach(t => {
      t.style.display = 'none';
    });
    activeTray = null;

    if (ctx) {
      ctx.style.display = 'none';
      ctx.querySelectorAll('.cad-context-item.has-sub').forEach(i => i.classList.remove('expanded'));
      ctx.querySelectorAll('.cad-sub-menu').forEach(s => s.classList.remove('show'));
    }

    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) backdrop.classList.remove('show');

    if (hadOpen) {
      const targetH = isMinimized ? MIN_HEIGHT : FULL_HEIGHT;
      logToAutoCAD('Closing all menus/trays, resetting height to: ' + targetH);
      sendToAutoCAD({
        action: 'resize',
        height: targetH
      });
    }
  }

  function toggleDropdown(triggerBtn, menuId) {
    const menu = document.getElementById(menuId);
    if (!menu) {
      logToAutoCAD('Error: menu not found for id: ' + menuId);
      return;
    }

    if (menu.classList.contains('show')) {
      closeAllMenus();
      return;
    }

    closeAllMenus();

    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) backdrop.classList.add('show');

    // Position menu directly below trigger element using viewport-fixed coordinates
    const rect = triggerBtn.getBoundingClientRect();
    menu.style.position = 'fixed';
    menu.style.top = Math.round(rect.bottom + 1) + 'px';
    
    let left = Math.round(rect.left);
    menu.style.left = left + 'px';
    menu.style.display = 'block';
    menu.classList.add('show');
    activeMenu = menu;

    // Adjust horizontal position if overflowing right edge
    const menuRect = menu.getBoundingClientRect();
    if (menuRect.right > window.innerWidth - 10) {
      left = Math.max(10, window.innerWidth - menuRect.width - 10);
      menu.style.left = left + 'px';
    }

    // Expand AutoCAD ribbon frame so the dropdown is completely visible and not clipped
    const neededH = Math.max(FULL_HEIGHT, Math.ceil(menuRect.bottom + 14));
    logToAutoCAD('Opening dropdown menu ' + menuId + ', requesting height: ' + neededH);
    sendToAutoCAD({
      action: 'resize',
      height: neededH
    });
  }

  function toggleTray(panel) {
    const tray = panel.querySelector('.panel-tray') || document.querySelector(`.panel-tray[data-for="${panel.id}"]`);
    if (!tray) return;

    const wasExpanded = panel.classList.contains('expanded');
    closeAllMenus();

    if (!wasExpanded) {
      panel.classList.add('expanded');
      const backdrop = document.getElementById('menu-backdrop');
      if (backdrop) backdrop.classList.add('show');

      const panelRect = panel.getBoundingClientRect();
      tray.style.position = 'fixed';
      tray.style.top = Math.round(panelRect.bottom) + 'px';
      tray.style.left = Math.round(panelRect.left) + 'px';
      tray.style.display = 'flex';
      activeTray = tray;

      const trayRect = tray.getBoundingClientRect();
      if (trayRect.right > window.innerWidth - 10) {
        tray.style.left = Math.max(10, window.innerWidth - trayRect.width - 10) + 'px';
      }

      const neededH = Math.max(FULL_HEIGHT, Math.ceil(trayRect.bottom + 14));
      logToAutoCAD('Panel tray opened, requesting height: ' + neededH);
      sendToAutoCAD({
        action: 'resize',
        height: neededH
      });
    }
  }

  // --- Tooltips Management ---
  function showTooltip(el) {
    if (!tooltipEl) return;
    const title = el.getAttribute('data-tip-title') || '';
    const desc = el.getAttribute('data-tip-desc') || '';
    const cmd = el.getAttribute('data-cmd') || '';

    if (!title && !desc) return;

    tooltipEl.querySelector('.tip-title').textContent = title;
    tooltipEl.querySelector('.tip-desc').textContent = desc;
    tooltipEl.querySelector('.tip-cmd').textContent = cmd ? 'Command: ' + cmd.replace('^C^C_', '').replace('^C^C', '') : '';

    tooltipEl.style.display = 'block';

    const rect = el.getBoundingClientRect();
    const tipRect = tooltipEl.getBoundingClientRect();

    let left = rect.left;
    let top = rect.bottom + 4;

    // Keep tooltip inside boundary
    if (top + tipRect.height > 112) {
      if (rect.right + tipRect.width + 10 < window.innerWidth) {
        left = rect.right + 8;
        top = Math.max(26, rect.top);
      } else {
        left = Math.max(6, rect.left - tipRect.width - 8);
        top = Math.max(26, rect.top);
      }
    }

    if (left + tipRect.width > window.innerWidth - 10) {
      left = Math.max(6, window.innerWidth - tipRect.width - 10);
    }
    if (left < 6) left = 6;

    tooltipEl.style.left = Math.round(left) + 'px';
    tooltipEl.style.top = Math.round(top) + 'px';
  }

  function hideTooltip() {
    if (!tooltipEl) return;
    tooltipEl.style.display = 'none';
  }

  // --- Initialize Events ---
  document.addEventListener('DOMContentLoaded', () => {
    tooltipEl = document.getElementById('cad-tooltip');

    // Convert any native title attributes to custom tooltip attributes so browser popups don't appear
    document.querySelectorAll('[title]').forEach(el => {
      if (!el.hasAttribute('data-tip-title')) {
        el.setAttribute('data-tip-title', el.getAttribute('title'));
      }
      el.removeAttribute('title');
    });

    // Relocate all menus and trays to document.body to prevent clipping by overflow
    document.querySelectorAll('.cad-menu, .panel-tray').forEach(el => {
      document.body.appendChild(el);
    });

    sendToAutoCAD({ action: 'resize', height: FULL_HEIGHT });

    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', (e) => {
        e.stopPropagation();
        closeAllMenus();
      });
      backdrop.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        e.stopPropagation();
        closeAllMenus();
      });
    }

    // Tab switching
    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        setActiveTab(tabId);
      });

      btn.addEventListener('dblclick', () => {
        toggleMinimize();
      });
    });

  // --- Classic Toolbar vs Ribbon Switching ---
  function switchToMacToolbar() {
    logToAutoCAD('Switching to Classic Mac Toolbar mode');
    runCommand('^C^C_TOOLSETS');
    sendToAutoCAD({ action: 'switchToMacToolbar' });
    const ribbon = document.getElementById('ribbon');
    if (ribbon) ribbon.classList.add('classic-mode');
    const pill = document.getElementById('floating-pill');
    if (pill) pill.style.display = 'flex';
    closeAllMenus();
    sendToAutoCAD({ action: 'resize', height: 25 });
  }

  function switchToWindowsRibbon() {
    logToAutoCAD('Switching to Windows Ribbon mode');
    runCommand('^C^C_TOOLSETSCLOSE');
    isMinimized = false;
    const ribbon = document.getElementById('ribbon');
    if (ribbon) {
      ribbon.classList.remove('classic-mode');
      ribbon.classList.remove('minimized');
    }
    const pill = document.getElementById('floating-pill');
    if (pill) pill.style.display = 'none';
    closeAllMenus();
    sendToAutoCAD({ action: 'resize', height: FULL_HEIGHT });
    sendToAutoCAD({ action: 'switchToWindowsRibbon' });
  }

  // --- Adaptive Submenu Orientation (Left/Right & Up/Down) ---
  function updateSubmenuOrientation(item) {
    if (!item) return;
    const sub = item.querySelector('.cad-sub-menu');
    if (!sub) return;

    const itemRect = item.getBoundingClientRect();
    const subWidth = 180;
    const winW = window.innerWidth;
    const winH = window.innerHeight;

    // Available space on right and left
    const spaceRight = winW - itemRect.right;
    const spaceLeft = itemRect.left;

    // Adaptive flyout left: if not enough space on right, or left has more room
    if (spaceRight < (subWidth + 15) && spaceLeft >= spaceRight) {
      sub.classList.add('flyout-left');
      item.classList.add('flyout-left');
    } else {
      sub.classList.remove('flyout-left');
      item.classList.remove('flyout-left');
    }

    // Adaptive vertical flyout: if near bottom, open upwards
    const subHeight = sub.offsetHeight || 220;
    const spaceBottom = winH - itemRect.top;
    const spaceTop = itemRect.bottom;

    if (spaceBottom < (subHeight + 15) && spaceTop >= spaceBottom) {
      sub.classList.add('flyout-up');
    } else {
      sub.classList.remove('flyout-up');
    }
  }

  // --- Right-click Context Menu ---
  function showContextMenu(x, y) {
    closeAllMenus();
    const ctx = document.getElementById('ctx-ribbon-menu');
    if (!ctx) return;

    // Populate panels for currently active tab
    const panelsContainer = document.getElementById('sub-menu-panels');
    if (panelsContainer) {
      panelsContainer.innerHTML = '';
      const activeTabContent = document.querySelector('.tab-content.active');
      if (activeTabContent) {
        const panels = activeTabContent.querySelectorAll('.panel');
        panels.forEach(p => {
          const footer = p.querySelector('.panel-footer');
          const title = footer ? footer.innerText.replace('▾', '').trim() : p.id;
          const isShown = p.style.display !== 'none';
          const item = document.createElement('div');
          item.className = 'cad-context-item';
          item.innerHTML = `<span class="cad-context-check">${isShown ? '✓' : ''}</span><span>${title}</span>`;
          item.addEventListener('click', (e) => {
            e.stopPropagation();
            p.style.display = isShown ? 'none' : 'flex';
            item.querySelector('.cad-context-check').innerText = isShown ? '' : '✓';
          });
          panelsContainer.appendChild(item);
        });
      }
    }

    ctx.style.display = 'block';
    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) backdrop.classList.add('show');
    const menuWidth = 210;
    const subHeight = 220;
    const winW = window.innerWidth;

    // Clamp horizontal placement inside window
    let posX = x;
    if (posX + menuWidth > winW - 10) {
      posX = Math.max(10, winW - menuWidth - 10);
    }
    ctx.style.left = posX + 'px';

    // Vertical placement
    let posY = y;
    ctx.style.top = posY + 'px';

    // Request height expansion so context menu and submenus are never clipped by the ribbon bottom!
    const neededH = Math.max(FULL_HEIGHT, Math.ceil(posY + subHeight + 35));
    logToAutoCAD('Opening context menu at (' + posX + ', ' + posY + '), requesting height: ' + neededH);
    sendToAutoCAD({
      action: 'resize',
      height: neededH
    });

    // Check orientation and attach hover/click listeners for all submenus
    ctx.querySelectorAll('.cad-context-item.has-sub').forEach(item => {
      const sub = item.querySelector('.cad-sub-menu');
      updateSubmenuOrientation(item);

      item.onmouseenter = () => {
        updateSubmenuOrientation(item);
        item.classList.add('expanded');
        if (sub) sub.classList.add('show');
      };

      item.onmouseleave = (e) => {
        if (!item.contains(e.relatedTarget)) {
          item.classList.remove('expanded');
          if (sub) sub.classList.remove('show');
        }
      };

      item.onclick = (e) => {
        if (!e.target.closest('.cad-sub-menu')) {
          e.stopPropagation();
          const isExp = item.classList.contains('expanded');
          ctx.querySelectorAll('.cad-context-item.has-sub').forEach(i => {
            i.classList.remove('expanded');
            const s = i.querySelector('.cad-sub-menu');
            if (s) s.classList.remove('show');
          });
          if (!isExp) {
            updateSubmenuOrientation(item);
            item.classList.add('expanded');
            if (sub) sub.classList.add('show');
          }
        }
      };
    });
  }

  function hideContextMenu() {
    const ctx = document.getElementById('ctx-ribbon-menu');
    if (ctx && ctx.style.display !== 'none') {
      ctx.style.display = 'none';
      const targetH = isMinimized ? MIN_HEIGHT : FULL_HEIGHT;
      sendToAutoCAD({
        action: 'resize',
        height: targetH
      });
    }
  }

    // Control buttons (switch toolbar, minimize, close, floating pill)
    const switchBtn = document.getElementById('btn-switch-toolbar');
    if (switchBtn) switchBtn.addEventListener('click', () => switchToMacToolbar());

    const floatingPill = document.getElementById('floating-pill');
    if (floatingPill) floatingPill.addEventListener('click', () => switchToWindowsRibbon());

    const minBtn = document.getElementById('btn-minimize');
    if (minBtn) minBtn.addEventListener('click', () => toggleMinimize());

    const closeBtn = document.getElementById('btn-close');
    if (closeBtn) closeBtn.addEventListener('click', () => {
      switchToMacToolbar();
    });

    // Context menu triggers: capture on document so nothing escapes or triggers browser defaults
    document.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      e.stopPropagation();
      showContextMenu(e.clientX, e.clientY);
    }, true);

    const ctxTogglePalettes = document.getElementById('ctx-toggle-palettes');
    if (ctxTogglePalettes) ctxTogglePalettes.addEventListener('click', (e) => {
      e.stopPropagation();
      logToAutoCAD('Context menu: Toggle Palettes clicked');
      sendToAutoCAD({ action: 'toggleHidePalettes' });
      hideContextMenu();
    });

    const ctxSwitch = document.getElementById('ctx-switch-toolbar');
    if (ctxSwitch) ctxSwitch.addEventListener('click', (e) => {
      e.stopPropagation();
      hideContextMenu();
      switchToMacToolbar();
    });

    const ctxMin = document.getElementById('ctx-minimize-ribbon');
    if (ctxMin) ctxMin.addEventListener('click', () => {
      hideContextMenu();
      toggleMinimize();
    });

    document.querySelectorAll('[data-toggle-tab]').forEach(item => {
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        const tabId = item.getAttribute('data-toggle-tab');
        const tabBtn = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
        if (tabBtn) {
          const isShown = tabBtn.style.display !== 'none';
          tabBtn.style.display = isShown ? 'none' : 'block';
          item.querySelector('.cad-context-check').innerText = isShown ? '' : '✓';
        }
      });
    });

    // Universal Document Click Dispatcher
    document.addEventListener('click', (e) => {
      // 1. Check if clicked a dropdown trigger (combo or split-arrow)
      const dropdownTrigger = e.target.closest('[data-dropdown]');
      if (dropdownTrigger) {
        e.stopPropagation();
        hideTooltip();
        const menuId = dropdownTrigger.getAttribute('data-dropdown');
        toggleDropdown(dropdownTrigger, menuId);
        return;
      }

      // 2. Check if clicked a panel footer (expand tray)
      const footer = e.target.closest('.panel-footer');
      if (footer) {
        e.stopPropagation();
        hideTooltip();
        const panel = footer.closest('.panel');
        if (panel) toggleTray(panel);
        return;
      }

      // 2b. Check if clicked an action button (Inspector docking, etc.)
      const actionBtn = e.target.closest('[data-action]');
      if (actionBtn) {
        e.stopPropagation();
        hideTooltip();
        const act = actionBtn.getAttribute('data-action');
        if (act === 'dockInspectorLeft') {
          sendToAutoCAD({ action: 'dockInspectorLeft', left: true });
        } else if (act === 'dockInspectorRight') {
          sendToAutoCAD({ action: 'dockInspectorLeft', left: false });
        } else if (act === 'toggleHidePalettes') {
          sendToAutoCAD({ action: 'toggleHidePalettes' });
        }
        closeAllMenus();
        return;
      }

      // 3. Check if clicked a command button
      const cmdBtn = e.target.closest('[data-cmd]');
      if (cmdBtn) {
        const cmd = cmdBtn.getAttribute('data-cmd');
        logToAutoCAD('Button clicked: cmd=' + cmd + ', text=' + (cmdBtn.innerText || '').trim());
        runCommand(cmd);

        // Click feedback
        cmdBtn.style.transform = 'scale(0.96)';
        setTimeout(() => {
          cmdBtn.style.transform = '';
        }, 100);

        closeAllMenus();
        return;
      }

      // 4. Outside click: close open menus/trays
      if (!e.target.closest('.cad-menu') && !e.target.closest('.panel-tray') && !e.target.closest('.cad-context-menu')) {
        closeAllMenus();
      }
    });

    window.toggleTabVisibility = function(tabId) {
      const tabBtn = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
      if (tabBtn) {
        const isShown = tabBtn.style.display !== 'none';
        tabBtn.style.display = isShown ? 'none' : 'block';
      }
    };

    window.togglePanelVisibility = function(panelId) {
      const panel = document.getElementById(panelId);
      if (panel) {
        const isShown = panel.style.display !== 'none';
        panel.style.display = isShown ? 'none' : 'flex';
      }
    };

    window.toggleMinimizeRibbon = function() {
      toggleMinimize();
    };

    // Tooltip event listeners
    document.addEventListener('mouseover', (e) => {
      const target = e.target.closest('[data-tip-title]');
      if (target && !activeMenu && !activeTray) {
        clearTimeout(tooltipTimer);
        tooltipTimer = setTimeout(() => {
          showTooltip(target);
        }, 300);
      }
    });

    document.addEventListener('mouseout', (e) => {
      const target = e.target.closest('[data-tip-title]');
      if (target) {
        clearTimeout(tooltipTimer);
        hideTooltip();
      }
    });
  });
})();
