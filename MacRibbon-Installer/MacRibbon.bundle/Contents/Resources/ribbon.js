// AutoCAD Windows Ribbon Controller v2.0.0
(function () {
  const FULL_HEIGHT = 115;
  const MIN_HEIGHT = 25;
  let isMinimized = false;
  let activeMenu = null;
  let activeTrigger = null;
  let activeTray = null;
  let lastFocusTrigger = null;
  let tooltipTimer = null;
  let tooltipEl = null;

  // Standard AutoCAD Color Index (ACI 1-9 + common) map for real layer swatches
  const ACI_COLORS = {
    1: '#ff3b30',
    2: '#f5d000',
    3: '#2ecc71',
    4: '#00bcd4',
    5: '#2979ff',
    6: '#d500f9',
    7: '#ffffff',
    8: '#808080',
    9: '#b8b8b8',
    10: '#ff0000',
    30: '#ff7f00',
    40: '#ffbf00',
    50: '#ffff00',
    90: '#00ff00',
    130: '#00ffff',
    170: '#0000ff',
    210: '#ff00ff',
    250: '#333333',
    251: '#505050',
    252: '#696969',
    253: '#828282',
    254: '#bebebe',
    255: '#ffffff'
  };

  function aciToHex(aci) {
    const n = Math.abs(parseInt(aci, 10));
    if (ACI_COLORS[n]) return ACI_COLORS[n];
    return '#cfd8e3';
  }

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

  window.onerror = function (msg, url, line, col) {
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

  window.setTheme = function (themeName) {
    document.body.classList.toggle('light-theme', themeName === 'light');
    logToAutoCAD('Theme switched to: ' + themeName);
  };

  // --- Horizontal Overflow Scroll Controls ---
  function updateScrollButtons() {
    const body = document.getElementById('ribbon-body');
    const leftBtn = document.getElementById('btn-scroll-left');
    const rightBtn = document.getElementById('btn-scroll-right');
    if (!body || !leftBtn || !rightBtn) return;

    const maxScroll = body.scrollWidth - body.clientWidth;
    if (maxScroll <= 4) {
      leftBtn.classList.remove('visible');
      rightBtn.classList.remove('visible');
      return;
    }
    leftBtn.classList.toggle('visible', body.scrollLeft > 4);
    rightBtn.classList.toggle('visible', body.scrollLeft < maxScroll - 4);
  }

  // --- Live Drawing Layer & Property State Sync ---
  window.syncAutoCADState = function (state) {
    if (!state || typeof state !== 'object') return;

    const layerCombo = document.querySelector('.layer-combo');
    const dynamicHost = document.getElementById('layer-dynamic-list');
    const layers = Array.isArray(state.layers) ? state.layers : [];

    if (dynamicHost) {
      dynamicHost.innerHTML = '';
      if (layers.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'cad-menu-empty';
        empty.textContent = 'No active drawing layers loaded. Open a drawing or run MRSYNC.';
        dynamicHost.appendChild(empty);
      } else {
        const header = document.createElement('div');
        header.className = 'cad-menu-header';
        header.textContent = state.drawing ? 'Drawing Layers (' + state.drawing + ')' : 'Drawing Layers';
        dynamicHost.appendChild(header);

        layers.forEach(layer => {
          const name = String(layer.name || '0');
          const hex = aciToHex(layer.color);
          const isCurrent = name.toLowerCase() === String(state.clayer || '0').toLowerCase();
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'cad-menu-item';
          btn.setAttribute('role', 'menuitem');
          btn.setAttribute('data-cmd', '^C^C_-LAYER _S "' + name.replace(/"/g, '') + '" ;;');
          btn.setAttribute('data-color', hex);
          btn.setAttribute('data-label', name);
          btn.innerHTML =
            '<span class="layer-color-box" style="background:' + hex + ';"></span>' +
            '<span>' + (isCurrent ? '✓ ' : '') + name.replace(/</g, '&lt;') + '</span>';
          dynamicHost.appendChild(btn);

          if (isCurrent && layerCombo) {
            const sw = layerCombo.querySelector('.layer-color-box');
            const lbl = layerCombo.querySelector('.combo-label');
            if (sw) sw.style.backgroundColor = hex;
            if (lbl) lbl.textContent = name;
          }
        });
      }
    }

    if (state.cecolor) {
      const colorCombo = document.getElementById('combo-color');
      if (colorCombo) {
        const lbl = colorCombo.querySelector('.combo-label');
        const sw = colorCombo.querySelector('.layer-color-box');
        const val = String(state.cecolor);
        if (lbl) lbl.textContent = val.toUpperCase() === 'BYLAYER' ? 'ByLayer' : (val.toUpperCase() === 'BYBLOCK' ? 'ByBlock' : val);
        if (sw) sw.style.backgroundColor = /^\d+$/.test(val) ? aciToHex(val) : '#ffffff';
      }
    }

    if (typeof state.celweight === 'number') {
      const lwCombo = document.getElementById('combo-lineweight');
      if (lwCombo) {
        const lbl = lwCombo.querySelector('.combo-label');
        if (lbl) {
          if (state.celweight === -1) lbl.textContent = 'ByLayer';
          else if (state.celweight === -2) lbl.textContent = 'ByBlock';
          else if (state.celweight === -3) lbl.textContent = 'Default';
          else lbl.textContent = (state.celweight / 100).toFixed(2) + ' mm';
        }
      }
    }

    if (state.celtype) {
      const ltCombo = document.getElementById('combo-linetype');
      if (ltCombo) {
        const lbl = ltCombo.querySelector('.combo-label');
        if (lbl) lbl.textContent = String(state.celtype);
      }
    }
  };

  // --- Tab Management ---
  function setActiveTab(tabId) {
    document.querySelectorAll('.tab-button').forEach(btn => {
      const isMatch = btn.getAttribute('data-tab') === tabId;
      btn.classList.toggle('active', isMatch);
      btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
      btn.setAttribute('tabindex', isMatch ? '0' : '-1');
    });

    document.querySelectorAll('.tab-content').forEach(content => {
      const isMatch = content.id === tabId;
      content.classList.toggle('active', isMatch);
      content.hidden = !isMatch;
    });

    closeAllMenus(false);

    if (isMinimized) {
      toggleMinimize(false);
    }

    const body = document.getElementById('ribbon-body');
    if (body) body.scrollLeft = 0;
    requestAnimationFrame(updateScrollButtons);
  }

  function toggleMinimize(forceState) {
    isMinimized = forceState !== undefined ? forceState : !isMinimized;
    const container = document.getElementById('ribbon');
    if (container) container.classList.toggle('minimized', isMinimized);

    const minBtn = document.getElementById('btn-minimize');
    if (minBtn) {
      minBtn.style.transform = isMinimized ? 'rotate(180deg)' : '';
      minBtn.setAttribute('aria-expanded', isMinimized ? 'false' : 'true');
    }

    const targetHeight = isMinimized ? MIN_HEIGHT : FULL_HEIGHT;
    sendToAutoCAD({
      action: 'resize',
      height: targetHeight
    });
  }

  // --- Dropdown Menu & Tray Management ---
  function closeAllMenus(restoreFocus) {
    const ctx = document.getElementById('ctx-ribbon-menu');
    const ctxOpen = ctx && ctx.style.display !== 'none' && ctx.style.display !== '';
    const hadOpen = activeMenu !== null || activeTray !== null ||
                    document.querySelector('.cad-menu.show') !== null ||
                    document.querySelector('.panel.expanded') !== null ||
                    ctxOpen;

    document.querySelectorAll('.cad-menu.show').forEach(m => {
      m.classList.remove('show');
      m.style.display = 'none';
    });

    document.querySelectorAll('[aria-expanded="true"][data-dropdown]').forEach(el => {
      el.setAttribute('aria-expanded', 'false');
    });

    document.querySelectorAll('.panel.expanded').forEach(p => {
      p.classList.remove('expanded');
      const footer = p.querySelector('.panel-footer');
      if (footer) footer.setAttribute('aria-expanded', 'false');
    });

    document.querySelectorAll('.panel-tray').forEach(t => {
      t.classList.remove('show');
      t.style.display = 'none';
    });

    if (ctx) {
      ctx.style.display = 'none';
      ctx.querySelectorAll('.cad-context-item.has-sub').forEach(i => i.classList.remove('expanded'));
      ctx.querySelectorAll('.cad-sub-menu').forEach(s => s.classList.remove('show'));
    }

    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) backdrop.classList.remove('show');

    activeMenu = null;
    activeTrigger = null;
    activeTray = null;

    if (restoreFocus && lastFocusTrigger && typeof lastFocusTrigger.focus === 'function') {
      lastFocusTrigger.focus();
      lastFocusTrigger = null;
    }

    if (hadOpen) {
      const targetH = isMinimized ? MIN_HEIGHT : FULL_HEIGHT;
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
      closeAllMenus(true);
      return;
    }

    closeAllMenus(false);
    lastFocusTrigger = triggerBtn;

    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) backdrop.classList.add('show');

    const anchorEl = triggerBtn.closest('.split-btn, .split-sm-container, .layer-combo, .cad-combo, .workspace-selector, .cad-app-logo') || triggerBtn;
    const rect = anchorEl.getBoundingClientRect();
    menu.style.position = 'fixed';
    menu.style.top = Math.round(rect.bottom + 1) + 'px';

    let left = Math.round(rect.left);
    menu.style.left = left + 'px';
    menu.style.display = 'block';
    menu.classList.add('show');
    triggerBtn.setAttribute('aria-expanded', 'true');
    activeMenu = menu;
    activeTrigger = anchorEl;

    const menuRect = menu.getBoundingClientRect();
    if (menuRect.right > window.innerWidth - 10) {
      left = Math.max(8, window.innerWidth - menuRect.width - 10);
      menu.style.left = left + 'px';
    }

    const neededH = Math.max(FULL_HEIGHT, Math.ceil(menuRect.bottom + 14));
    sendToAutoCAD({
      action: 'resize',
      height: neededH
    });
  }

  function toggleTray(panel, footerBtn) {
    const tray = panel.querySelector('.panel-tray') || document.querySelector(`.panel-tray[data-for="${panel.id}"]`);
    if (!tray) return;

    const wasExpanded = panel.classList.contains('expanded');
    closeAllMenus(false);

    if (!wasExpanded) {
      lastFocusTrigger = footerBtn || null;
      panel.classList.add('expanded');
      if (footerBtn) footerBtn.setAttribute('aria-expanded', 'true');

      const backdrop = document.getElementById('menu-backdrop');
      if (backdrop) backdrop.classList.add('show');

      const panelRect = panel.getBoundingClientRect();
      tray.style.position = 'fixed';
      tray.style.top = Math.round(panelRect.bottom) + 'px';
      tray.style.left = Math.round(panelRect.left) + 'px';
      tray.style.display = 'flex';
      tray.classList.add('show');
      activeTray = tray;

      const trayRect = tray.getBoundingClientRect();
      if (trayRect.right > window.innerWidth - 10) {
        tray.style.left = Math.max(8, window.innerWidth - trayRect.width - 10) + 'px';
      }

      const neededH = Math.max(FULL_HEIGHT, Math.ceil(trayRect.bottom + 14));
      sendToAutoCAD({
        action: 'resize',
        height: neededH
      });
    }
  }

  // --- Dynamic UI State Updates for Combos & Split Buttons ---
  function updateComboOrSplitState(menuItem) {
    const menu = menuItem.closest('.cad-menu');
    if (!menu) return;
    const menuId = menu.id;
    const itemText = (menuItem.getAttribute('data-label') || menuItem.textContent || '').replace(/^✓\s*/, '').trim();
    const itemColor = menuItem.getAttribute('data-color');
    const cmd = menuItem.getAttribute('data-cmd') || '';

    if (menuId === 'menu-layer-list' && itemColor) {
      const combo = document.querySelector('.layer-combo');
      if (combo) {
        const swatch = combo.querySelector('.layer-color-box');
        const label = combo.querySelector('.combo-label');
        if (swatch) swatch.style.backgroundColor = itemColor;
        if (label) label.textContent = itemText;
      }
    } else if (menuId === 'menu-color-list' && itemColor) {
      const combo = document.getElementById('combo-color');
      if (combo) {
        const swatch = combo.querySelector('.layer-color-box');
        const label = combo.querySelector('.combo-label');
        if (swatch) swatch.style.backgroundColor = itemColor;
        if (label) label.textContent = itemText;
      }
    } else if (menuId === 'menu-lineweight-list' && cmd.includes('_-LWEIGHT ')) {
      const combo = document.getElementById('combo-lineweight');
      if (combo) {
        const label = combo.querySelector('.combo-label');
        if (label && itemText) label.textContent = itemText;
      }
    } else if (menuId === 'menu-linetype-list' && cmd.includes('_-LINETYPE ')) {
      const combo = document.getElementById('combo-linetype');
      if (combo) {
        const label = combo.querySelector('.combo-label');
        if (label && itemText) label.textContent = itemText;
      }
    } else if (activeTrigger && (activeTrigger.classList.contains('split-btn') || activeTrigger.classList.contains('split-sm-container'))) {
      const mainBtn = activeTrigger.querySelector('.split-main, .split-main-sm');
      if (mainBtn && cmd) {
        mainBtn.setAttribute('data-cmd', cmd);
        mainBtn.setAttribute('data-tip-title', itemText);
        const shortLabel = menuItem.getAttribute('data-short');
        const spanEl = mainBtn.querySelector('span');
        if (shortLabel && spanEl) {
          spanEl.textContent = shortLabel;
        }
      }
    }
  }

  // --- Tooltips Management ---
  function formatCommandForTooltip(cmd) {
    if (!cmd) return '';
    return cmd
      .replace(/^\*?(\^C)+/i, '')
      .replace(/^'_/, '')
      .replace(/^_/, '')
      .replace(/[\\;]+/g, ' ')
      .trim()
      .toUpperCase();
  }

  function showTooltip(el) {
    if (!tooltipEl) return;
    const title = el.getAttribute('data-tip-title') || '';
    const desc = el.getAttribute('data-tip-desc') || '';
    const cmd = el.getAttribute('data-cmd') || '';

    if (!title && !desc) return;

    tooltipEl.querySelector('.tip-title').textContent = title;
    tooltipEl.querySelector('.tip-desc').textContent = desc;
    const cleanCmd = formatCommandForTooltip(cmd);
    const tipCmd = tooltipEl.querySelector('.tip-cmd');
    tipCmd.textContent = cleanCmd ? 'Command: ' + cleanCmd : '';
    tipCmd.style.display = cleanCmd ? 'block' : 'none';

    tooltipEl.style.display = 'block';

    const rect = el.getBoundingClientRect();
    const tipRect = tooltipEl.getBoundingClientRect();

    let left = rect.left;
    const top = rect.bottom + 6;

    if (left + tipRect.width > window.innerWidth - 10) {
      left = Math.max(6, window.innerWidth - tipRect.width - 10);
    }
    if (left < 6) left = 6;

    tooltipEl.style.left = Math.round(left) + 'px';
    tooltipEl.style.top = Math.round(top) + 'px';

    if (!activeMenu && !activeTray && !isMinimized) {
      const neededH = Math.max(FULL_HEIGHT, Math.ceil(top + tipRect.height + 10));
      if (neededH > FULL_HEIGHT) {
        sendToAutoCAD({ action: 'resize', height: neededH });
      }
    }
  }

  function hideTooltip() {
    if (!tooltipEl || tooltipEl.style.display === 'none') return;
    tooltipEl.style.display = 'none';
    if (!activeMenu && !activeTray) {
      const targetH = isMinimized ? MIN_HEIGHT : FULL_HEIGHT;
      sendToAutoCAD({ action: 'resize', height: targetH });
    }
  }

  // --- Classic Toolbar vs Ribbon Switching ---
  function switchToMacToolbar() {
    logToAutoCAD('Switching to Classic Mac Toolbar mode');
    closeAllMenus(false);
    sendToAutoCAD({ action: 'switchToMacToolbar' });
  }

  function switchToWindowsRibbon() {
    logToAutoCAD('Switching to Windows Ribbon mode');
    isMinimized = false;
    const ribbon = document.getElementById('ribbon');
    if (ribbon) ribbon.classList.remove('minimized');
    closeAllMenus(false);
    sendToAutoCAD({ action: 'resize', height: FULL_HEIGHT });
    sendToAutoCAD({ action: 'switchToWindowsRibbon' });
  }

  // --- Adaptive Submenu Orientation ---
  function updateSubmenuOrientation(item) {
    if (!item) return;
    const sub = item.querySelector('.cad-sub-menu');
    if (!sub) return;

    const itemRect = item.getBoundingClientRect();
    const subWidth = 185;
    const winW = window.innerWidth;
    const winH = window.innerHeight;

    const spaceRight = winW - itemRect.right;
    const spaceLeft = itemRect.left;

    if (spaceRight < (subWidth + 15) && spaceLeft >= spaceRight) {
      sub.classList.add('flyout-left');
      item.classList.add('flyout-left');
    } else {
      sub.classList.remove('flyout-left');
      item.classList.remove('flyout-left');
    }

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
    closeAllMenus(false);
    hideTooltip();
    const ctx = document.getElementById('ctx-ribbon-menu');
    if (!ctx) return;

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
          const item = document.createElement('button');
          item.type = 'button';
          item.className = 'cad-context-item';
          item.setAttribute('role', 'menuitemcheckbox');
          item.setAttribute('aria-checked', isShown ? 'true' : 'false');
          item.innerHTML = '<span class="cad-context-check">' + (isShown ? '✓' : '') + '</span><span>' + title + '</span>';
          item.addEventListener('click', (e) => {
            e.stopPropagation();
            const nowShown = p.style.display === 'none';
            p.style.display = nowShown ? 'flex' : 'none';
            item.setAttribute('aria-checked', nowShown ? 'true' : 'false');
            item.querySelector('.cad-context-check').innerText = nowShown ? '✓' : '';
            requestAnimationFrame(updateScrollButtons);
          });
          panelsContainer.appendChild(item);
        });
      }
    }

    ctx.style.display = 'block';
    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) backdrop.classList.add('show');
    const menuWidth = 215;
    const subHeight = 260;
    const winW = window.innerWidth;

    let posX = x;
    if (posX + menuWidth > winW - 10) {
      posX = Math.max(10, winW - menuWidth - 10);
    }
    ctx.style.left = posX + 'px';
    ctx.style.top = y + 'px';

    const neededH = Math.max(FULL_HEIGHT, Math.ceil(y + subHeight + 40));
    sendToAutoCAD({
      action: 'resize',
      height: neededH
    });

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
    });
  }

  // --- Initialize Events ---
  document.addEventListener('DOMContentLoaded', () => {
    tooltipEl = document.getElementById('cad-tooltip');

    document.querySelectorAll('[title]').forEach(el => {
      if (!el.hasAttribute('data-tip-title')) {
        el.setAttribute('data-tip-title', el.getAttribute('title'));
      }
      el.removeAttribute('title');
    });

    document.querySelectorAll('.cad-menu, .panel-tray').forEach(el => {
      document.body.appendChild(el);
    });

    sendToAutoCAD({ action: 'resize', height: FULL_HEIGHT });

    const bodyEl = document.getElementById('ribbon-body');
    const scrollLeftBtn = document.getElementById('btn-scroll-left');
    const scrollRightBtn = document.getElementById('btn-scroll-right');
    if (bodyEl) {
      bodyEl.addEventListener('scroll', updateScrollButtons);
      window.addEventListener('resize', updateScrollButtons);
      requestAnimationFrame(updateScrollButtons);
    }
    if (scrollLeftBtn && bodyEl) {
      scrollLeftBtn.addEventListener('click', () => {
        bodyEl.scrollBy({ left: -240, behavior: 'smooth' });
      });
    }
    if (scrollRightBtn && bodyEl) {
      scrollRightBtn.addEventListener('click', () => {
        bodyEl.scrollBy({ left: 240, behavior: 'smooth' });
      });
    }

    const backdrop = document.getElementById('menu-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', (e) => {
        e.stopPropagation();
        closeAllMenus(false);
      });
      backdrop.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        e.stopPropagation();
        closeAllMenus(false);
      });
    }

    const tabButtons = Array.from(document.querySelectorAll('.tab-button'));
    tabButtons.forEach((btn, idx) => {
      btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        setActiveTab(tabId);
      });

      btn.addEventListener('dblclick', () => {
        toggleMinimize();
      });

      btn.addEventListener('keydown', (e) => {
        const visibleTabs = tabButtons.filter(t => t.style.display !== 'none');
        const curIdx = visibleTabs.indexOf(btn);
        if (e.key === 'ArrowRight') {
          e.preventDefault();
          const next = visibleTabs[(curIdx + 1) % visibleTabs.length];
          if (next) {
            setActiveTab(next.getAttribute('data-tab'));
            next.focus();
          }
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          const prev = visibleTabs[(curIdx - 1 + visibleTabs.length) % visibleTabs.length];
          if (prev) {
            setActiveTab(prev.getAttribute('data-tab'));
            prev.focus();
          }
        }
      });
    });

    const switchBtn = document.getElementById('btn-switch-toolbar');
    if (switchBtn) switchBtn.addEventListener('click', () => switchToMacToolbar());

    const minBtn = document.getElementById('btn-minimize');
    if (minBtn) minBtn.addEventListener('click', () => toggleMinimize());

    const closeBtn = document.getElementById('btn-close');
    if (closeBtn) closeBtn.addEventListener('click', () => switchToMacToolbar());

    document.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      e.stopPropagation();
      showContextMenu(e.clientX, e.clientY);
    }, true);

    const ctxSwitch = document.getElementById('ctx-switch-toolbar');
    if (ctxSwitch) ctxSwitch.addEventListener('click', (e) => {
      e.stopPropagation();
      closeAllMenus(false);
      switchToMacToolbar();
    });

    const ctxMin = document.getElementById('ctx-minimize-ribbon');
    if (ctxMin) ctxMin.addEventListener('click', (e) => {
      e.stopPropagation();
      closeAllMenus(false);
      toggleMinimize();
    });

    document.querySelectorAll('[data-toggle-tab]').forEach(item => {
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        const tabId = item.getAttribute('data-toggle-tab');
        const tabBtn = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
        if (tabBtn) {
          const nowShown = tabBtn.style.display === 'none';
          tabBtn.style.display = nowShown ? 'block' : 'none';
          item.setAttribute('aria-checked', nowShown ? 'true' : 'false');
          item.querySelector('.cad-context-check').innerText = nowShown ? '✓' : '';
        }
      });
    });

    // Global Keyboard Accessibility (Escape closes menus/trays/context, Arrow keys navigate menus)
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        hideTooltip();
        closeAllMenus(true);
        return;
      }

      if (activeMenu && (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Home' || e.key === 'End')) {
        const items = Array.from(activeMenu.querySelectorAll('button.cad-menu-item:not(:disabled)'));
        if (items.length === 0) return;
        e.preventDefault();
        const cur = items.indexOf(document.activeElement);
        let nextIdx = 0;
        if (e.key === 'ArrowDown') nextIdx = cur < 0 ? 0 : (cur + 1) % items.length;
        else if (e.key === 'ArrowUp') nextIdx = cur <= 0 ? items.length - 1 : cur - 1;
        else if (e.key === 'Home') nextIdx = 0;
        else if (e.key === 'End') nextIdx = items.length - 1;
        items[nextIdx].focus();
      }
    });

    // Universal Document Click Dispatcher
    document.addEventListener('click', (e) => {
      // 1. Workspace switching items
      const wsItem = e.target.closest('[data-workspace]');
      if (wsItem) {
        e.stopPropagation();
        hideTooltip();
        const wsName = wsItem.getAttribute('data-workspace');
        const targetTab = wsItem.getAttribute('data-target-tab');
        const wsLabel = document.querySelector('.workspace-selector .ws-label');
        if (wsName === 'mac-toolbar') {
          closeAllMenus(false);
          switchToMacToolbar();
          return;
        }
        if (wsLabel) wsLabel.textContent = wsName;
        if (targetTab) setActiveTab(targetTab);
        const wsMenu = document.getElementById('menu-workspace');
        if (wsMenu) {
          wsMenu.querySelectorAll('[data-workspace]').forEach(item => {
            const isMatch = item.getAttribute('data-workspace') === wsName;
            item.textContent = (isMatch ? '✓ ' : '') + item.getAttribute('data-workspace');
          });
        }
        closeAllMenus(false);
        return;
      }

      // 2. Dropdown trigger
      const dropdownTrigger = e.target.closest('[data-dropdown]');
      if (dropdownTrigger) {
        e.stopPropagation();
        hideTooltip();
        const menuId = dropdownTrigger.getAttribute('data-dropdown');
        toggleDropdown(dropdownTrigger, menuId);
        return;
      }

      // 3. Panel footer (expand tray if panel has a tray)
      const footer = e.target.closest('.panel-footer');
      if (footer) {
        e.stopPropagation();
        hideTooltip();
        const panel = footer.closest('.panel');
        if (panel && footer.getAttribute('data-has-tray') === 'true') {
          toggleTray(panel, footer);
        }
        return;
      }

      // 4. Native action buttons
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
        closeAllMenus(false);
        return;
      }

      // 5. Command button or menu item
      const cmdBtn = e.target.closest('[data-cmd]');
      if (cmdBtn) {
        hideTooltip();
        const cmd = cmdBtn.getAttribute('data-cmd');
        if (cmdBtn.classList.contains('cad-menu-item')) {
          updateComboOrSplitState(cmdBtn);
        }
        logToAutoCAD('Button clicked: cmd=' + cmd + ', text=' + (cmdBtn.innerText || '').trim());
        runCommand(cmd);
        closeAllMenus(false);
        return;
      }

      // 6. Outside click
      if (!e.target.closest('.cad-menu') && !e.target.closest('.panel-tray') && !e.target.closest('.cad-context-menu')) {
        closeAllMenus(false);
      }
    });

    window.toggleTabVisibility = function (tabId) {
      const tabBtn = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
      if (tabBtn) {
        const isShown = tabBtn.style.display !== 'none';
        tabBtn.style.display = isShown ? 'none' : 'block';
      }
    };

    window.togglePanelVisibility = function (panelId) {
      const panel = document.getElementById(panelId);
      if (panel) {
        const isShown = panel.style.display !== 'none';
        panel.style.display = isShown ? 'none' : 'flex';
        requestAnimationFrame(updateScrollButtons);
      }
    };

    window.toggleMinimizeRibbon = function () {
      toggleMinimize();
    };

    // Tooltip event listeners
    document.addEventListener('mouseover', (e) => {
      const target = e.target.closest('[data-tip-title]');
      if (target && !activeMenu && !activeTray) {
        clearTimeout(tooltipTimer);
        tooltipTimer = setTimeout(() => {
          showTooltip(target);
        }, 350);
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
