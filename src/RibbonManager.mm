#import "RibbonManager.h"
#import "CommandExecutor.h"
#import <CoreGraphics/CoreGraphics.h>
#import <objc/message.h>

extern void LogMacRibbon(NSString *fmt, ...);

@interface RibbonManager () {
    RibbonViewController *_ribbonVC;
    NSWindow *_targetWindow;
    BOOL _isVisible;
    BOOL _hasLoadedOnce;
    CGFloat _baseRibbonHeight;
    NSTimer *_pollTimer;
    NSColor *_lastSampledColor;
    NSDate *_lastHtmlModDate;
    NSDate *_lastStateModDate;
    NSButton *_floatingSwitchButton;
}
@end

@implementation RibbonManager

+ (instancetype)sharedInstance {
    static RibbonManager *s_instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        s_instance = [[RibbonManager alloc] init];
    });
    return s_instance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _isVisible = NO;
        _baseRibbonHeight = 115.0;
        [self locateResourcesAndInitVC];
    }
    return self;
}

- (void)locateResourcesAndInitVC {
    NSBundle *bundle = [NSBundle bundleForClass:[self class]];
    NSURL *resURL = [bundle resourceURL];

    // Candidate resource directories
    NSArray<NSString *> *candidates = @[
        [resURL path] ?: @"",
        @"/Users/Ronci/Documents/AutoCAD/AutoCAD-Mac-Ribbon/ui",
        [NSHomeDirectory() stringByAppendingPathComponent:@"Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle/Contents/Resources"],
        [NSHomeDirectory() stringByAppendingPathComponent:@"Library/Application Support/Autodesk/ApplicationPlugins/MacRibbon.bundle/Contents/Resources"],
        @"/Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle/Contents/Resources",
        @"/Users/Ronci/Desktop/AutoCAD-Mac-Ribbon/ui"
    ];

    for (NSString *candidate in candidates) {
        if (candidate.length == 0) continue;
        NSString *testHtml = [candidate stringByAppendingPathComponent:@"index.html"];
        if ([[NSFileManager defaultManager] fileExistsAtPath:testHtml]) {
            resURL = [NSURL fileURLWithPath:candidate];
            LogMacRibbon(@"Found valid resources path: %@", candidate);
            break;
        }
    }

    _ribbonVC = [[RibbonViewController alloc] initWithResourcesURL:resURL];
    _ribbonVC.delegate = self;
}

- (void)start {
    LogMacRibbon(@"RibbonManager starting...");

    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(onWindowDidBecomeKey:)
                                                 name:NSWindowDidBecomeKeyNotification
                                               object:nil];

    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(onWindowDidResize:)
                                                 name:NSWindowDidResizeNotification
                                               object:nil];

    dispatch_async(dispatch_get_main_queue(), ^{
        [self findAndAttachToTargetWindow];
    });

    if (!_pollTimer) {
        _pollTimer = [NSTimer scheduledTimerWithTimeInterval:1.5
                                                      target:self
                                                    selector:@selector(checkWindowStatus)
                                                    userInfo:nil
                                                     repeats:YES];
    }
}

- (void)stop {
    LogMacRibbon(@"RibbonManager stopping");
    [_pollTimer invalidate];
    _pollTimer = nil;
    [[NSNotificationCenter defaultCenter] removeObserver:self];
    [self hideRibbon];
}

+ (NSView *)findViewWithIdentifier:(NSString *)ident inView:(NSView *)root {
    if (!root) return nil;
    if ([root.identifier isEqualToString:ident]) {
        return root;
    }
    for (NSView *sub in root.subviews) {
        NSView *found = [RibbonManager findViewWithIdentifier:ident inView:sub];
        if (found) return found;
    }
    return nil;
}

- (NSColor *)sampleAutoCADWindowColor {
    if (!_targetWindow || ![_targetWindow isVisible]) return nil;
    NSView *contentView = _targetWindow.contentView;
    if (!contentView) return nil;

    // Prefer sampling from AutoCAD's native fileTabPane so our Ribbon WebView never samples itself
    NSView *sampleView = [RibbonManager findViewWithIdentifier:@"fileTabPane" inView:contentView];
    if (!sampleView || sampleView.bounds.size.height < 8) {
        sampleView = contentView;
    }

    NSRect bounds = sampleView.bounds;
    CGFloat sampleX = fmax(4.0, bounds.size.width * 0.65);
    CGFloat sampleY = (sampleView == contentView)
        ? fmax(10.0, bounds.size.height - _baseRibbonHeight - 12.0)
        : fmax(2.0, bounds.size.height * 0.5);
    NSRect sampleRect = NSMakeRect(sampleX, sampleY, 4, 4);

    NSBitmapImageRep *rep = [sampleView bitmapImageRepForCachingDisplayInRect:sampleRect];
    if (!rep) return nil;

    [sampleView cacheDisplayInRect:sampleRect toBitmapImageRep:rep];
    NSColor *color = [rep colorAtX:2 y:2];
    return [color colorUsingColorSpace:[NSColorSpace sRGBColorSpace]] ?: color;
}

- (void)updateThemeFromAutoCAD {
    NSColor *color = [self sampleAutoCADWindowColor];
    if (!color) return;

    CGFloat r = [color redComponent];
    CGFloat g = [color greenComponent];
    CGFloat b = [color blueComponent];

    // Check if it changed significantly (avoid redundant JS calls)
    if (_lastSampledColor && 
        fabs([_lastSampledColor redComponent] - r) < 0.015 &&
        fabs([_lastSampledColor greenComponent] - g) < 0.015 &&
        fabs([_lastSampledColor blueComponent] - b) < 0.015) {
        return;
    }
    _lastSampledColor = color;

    // Luminance to determine Dark vs Light mode
    CGFloat lum = 0.299 * r + 0.587 * g + 0.114 * b;
    BOOL isLight = (lum > 0.55);

    // Compute relative palette shades with guaranteed WCAG AA contrast
    CGFloat tabR, tabG, tabB;
    CGFloat tabHovR, tabHovG, tabHovB;
    CGFloat hovR, hovG, hovB;
    CGFloat hovBorR, hovBorG, hovBorB;
    CGFloat actR, actG, actB;
    CGFloat borR, borG, borB;
    CGFloat menuBorR, menuBorG, menuBorB;

    if (isLight) {
        tabR = fmax(0.0, r * 0.94); tabG = fmax(0.0, g * 0.94); tabB = fmax(0.0, b * 0.94);
        tabHovR = fmax(0.0, r * 0.97); tabHovG = fmax(0.0, g * 0.97); tabHovB = fmax(0.0, b * 0.97);
        hovR = fmax(0.0, r * 0.91); hovG = fmax(0.0, g * 0.91); hovB = fmax(0.0, b * 0.91);
        hovBorR = fmax(0.0, r * 0.78); hovBorG = fmax(0.0, g * 0.78); hovBorB = fmax(0.0, b * 0.78);
        actR = fmax(0.0, r * 0.86); actG = fmax(0.0, g * 0.86); actB = fmax(0.0, b * 0.86);
        borR = fmax(0.0, r * 0.82); borG = fmax(0.0, g * 0.82); borB = fmax(0.0, b * 0.82);
        menuBorR = fmax(0.0, r * 0.74); menuBorG = fmax(0.0, g * 0.74); menuBorB = fmax(0.0, b * 0.74);
    } else {
        tabR = fmax(0.0, r * 0.72); tabG = fmax(0.0, g * 0.72); tabB = fmax(0.0, b * 0.72);
        tabHovR = fmax(0.0, r * 0.86); tabHovG = fmax(0.0, g * 0.86); tabHovB = fmax(0.0, b * 0.86);
        hovR = fmin(1.0, r * 1.18); hovG = fmin(1.0, g * 1.18); hovB = fmin(1.0, b * 1.18);
        hovBorR = fmin(1.0, r * 1.38); hovBorG = fmin(1.0, g * 1.38); hovBorB = fmin(1.0, b * 1.38);
        actR = fmax(0.0, r * 0.76); actG = fmax(0.0, g * 0.76); actB = fmax(0.0, b * 0.76);
        borR = fmax(0.0, r * 0.68); borG = fmax(0.0, g * 0.68); borB = fmax(0.0, b * 0.68);
        menuBorR = fmin(1.0, r * 1.24); menuBorG = fmin(1.0, g * 1.24); menuBorB = fmin(1.0, b * 1.24);
    }

    NSString *hexBg = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(r * 255), (int)(g * 255), (int)(b * 255)];
    NSString *hexTabs = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(tabR * 255), (int)(tabG * 255), (int)(tabB * 255)];
    NSString *hexTabHov = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(tabHovR * 255), (int)(tabHovG * 255), (int)(tabHovB * 255)];
    NSString *hexHover = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(hovR * 255), (int)(hovG * 255), (int)(hovB * 255)];
    NSString *hexHovBor = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(hovBorR * 255), (int)(hovBorG * 255), (int)(hovBorB * 255)];
    NSString *hexAct = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(actR * 255), (int)(actG * 255), (int)(actB * 255)];
    NSString *hexBorder = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(borR * 255), (int)(borG * 255), (int)(borB * 255)];
    NSString *hexMenuBor = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(menuBorR * 255), (int)(menuBorG * 255), (int)(menuBorB * 255)];
    NSString *hexMenuBg = isLight ? @"#f5f7fa" : hexTabs;
    NSString *hexPanelTitle = isLight ? @"#3c4654" : @"#dce4ef";
    NSString *hexTextMain = isLight ? @"#1c232b" : @"#f3f6fa";
    NSString *hexTextMuted = isLight ? @"#444f5e" : @"#d3dce8";
    NSString *hexTabText = isLight ? @"#2b3440" : @"#d5dde8";
    NSString *hexTooltipCmd = isLight ? @"#0056a3" : @"#8ad0ff";

    LogMacRibbon(@"AutoCAD Theme synchronized! Sampled: %@, isLight: %d", hexBg, isLight);

    NSString *js = [NSString stringWithFormat:
        @"var r=document.documentElement.style;"
        @"r.setProperty('--cad-ribbon-bg','%@');"
        @"r.setProperty('--cad-tab-bar-bg','%@');"
        @"r.setProperty('--cad-tab-active-bg','%@');"
        @"r.setProperty('--cad-tab-hover-bg','%@');"
        @"r.setProperty('--cad-btn-hover','%@');"
        @"r.setProperty('--cad-btn-border-hover','%@');"
        @"r.setProperty('--cad-btn-active','%@');"
        @"r.setProperty('--cad-panel-border','%@');"
        @"r.setProperty('--cad-menu-bg','%@');"
        @"r.setProperty('--cad-menu-border','%@');"
        @"r.setProperty('--cad-panel-title','%@');"
        @"r.setProperty('--cad-text-main','%@');"
        @"r.setProperty('--cad-text-muted','%@');"
        @"r.setProperty('--cad-tab-text','%@');"
        @"r.setProperty('--cad-tooltip-cmd','%@');"
        @"document.body.classList.toggle('light-theme',%s);",
        hexBg, hexTabs, hexBg, hexTabHov, hexHover, hexHovBor, hexAct,
        hexBorder, hexMenuBg, hexMenuBor, hexPanelTitle, hexTextMain,
        hexTextMuted, hexTabText, hexTooltipCmd, isLight ? "true" : "false"];

    dispatch_async(dispatch_get_main_queue(), ^{
        [_ribbonVC.webView evaluateJavaScript:js completionHandler:nil];
    });
}

- (void)checkHtmlUpdate {
    if (!_ribbonVC || !_ribbonVC.resourcesURL) return;
    NSArray<NSString *> *watched = @[@"index.html", @"style.css", @"ribbon.js"];
    NSDate *latestDate = nil;
    for (NSString *fname in watched) {
        NSURL *fileURL = [_ribbonVC.resourcesURL URLByAppendingPathComponent:fname];
        NSDictionary *attrs = [[NSFileManager defaultManager] attributesOfItemAtPath:[fileURL path] error:nil];
        NSDate *d = attrs[NSFileModificationDate];
        if (d && (!latestDate || [d compare:latestDate] == NSOrderedDescending)) {
            latestDate = d;
        }
    }
    if (latestDate) {
        if (_lastHtmlModDate && [latestDate timeIntervalSinceDate:_lastHtmlModDate] > 0.5) {
            _lastHtmlModDate = latestDate;
            LogMacRibbon(@"Ribbon UI assets modified on disk - automatically reloading Ribbon WebView!");
            dispatch_async(dispatch_get_main_queue(), ^{
                [self reloadRibbon];
            });
        } else if (!_lastHtmlModDate) {
            _lastHtmlModDate = latestDate;
        }
    }
}

- (void)checkAutoCADStateSync {
    NSString *statePath = @"/tmp/macribbon_state.json";
    NSDictionary *attrs = [[NSFileManager defaultManager] attributesOfItemAtPath:statePath error:nil];
    NSDate *modDate = attrs[NSFileModificationDate];
    if (!modDate) return;
    if (_lastStateModDate && [modDate timeIntervalSinceDate:_lastStateModDate] < 0.1) {
        return;
    }
    _lastStateModDate = modDate;
    NSString *jsonStr = [NSString stringWithContentsOfFile:statePath encoding:NSUTF8StringEncoding error:nil];
    if (!jsonStr || jsonStr.length == 0) return;
    NSString *js = [NSString stringWithFormat:@"if (window.syncAutoCADState) window.syncAutoCADState(%@);", jsonStr];
    [_ribbonVC evaluateJavaScript:js completionHandler:nil];
}

- (void)checkExternalCommands {
    NSString *cmdPath = @"/tmp/ribbon_cmd.txt";
    if ([[NSFileManager defaultManager] fileExistsAtPath:cmdPath]) {
        NSString *cmd = [[NSString stringWithContentsOfFile:cmdPath encoding:NSUTF8StringEncoding error:nil] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
        [[NSFileManager defaultManager] removeItemAtPath:cmdPath error:nil];
        LogMacRibbon(@"checkExternalCommands received: '%@'", cmd);
        if ([cmd isEqualToString:@"dockInspectorLeft"]) {
            [self ribbonRequestedDockInspectorLeft:YES];
        } else if ([cmd isEqualToString:@"dockInspectorRight"]) {
            [self ribbonRequestedDockInspectorLeft:NO];
        } else if ([cmd isEqualToString:@"toggleHidePalettes"]) {
            [self ribbonRequestedToggleHidePalettes];
        } else if ([cmd isEqualToString:@"switchToMacToolbar"] || [cmd isEqualToString:@"ribbonclose"] || [cmd isEqualToString:@"hideRibbon"]) {
            [self switchToMacToolbar];
        } else if ([cmd isEqualToString:@"switchToWindowsRibbon"] || [cmd isEqualToString:@"ribbon"] || [cmd isEqualToString:@"mr"] || [cmd isEqualToString:@"showRibbon"]) {
            [self switchToWindowsRibbon];
        } else if ([cmd isEqualToString:@"ensureRibbonVisible"]) {
            [self ensureRibbonVisible];
        } else if ([cmd isEqualToString:@"toggleRibbon"]) {
            [self toggleRibbon];
        } else if ([cmd hasPrefix:@"evalJs:"]) {
            NSString *js = [cmd substringFromIndex:7];
            LogMacRibbon(@"Executing evalJs: %@", js);
            [_ribbonVC evaluateJavaScript:js completionHandler:^(id result, NSError *error) {
                if (error) {
                    LogMacRibbon(@"evalJs error: %@", error.localizedDescription);
                } else {
                    LogMacRibbon(@"evalJs result: %@", result);
                }
            }];
        } else if ([cmd hasPrefix:@"snapshot:"]) {
            NSString *path = [cmd substringFromIndex:9];
            [_ribbonVC captureSnapshotToFile:path];
        } else if ([cmd hasPrefix:@"winSnapshot:"]) {
            NSString *path = [cmd substringFromIndex:12];
            [self captureWindowSnapshotToFile:path];
        }
    }
}

- (void)captureWindowSnapshotToFile:(NSString *)filePath {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (!self->_targetWindow || !self->_targetWindow.contentView) {
            LogMacRibbon(@"captureWindowSnapshotToFile failed: targetWindow or contentView is nil");
            return;
        }
        NSView *view = self->_targetWindow.contentView;
        NSRect bounds = view.bounds;
        NSBitmapImageRep *rep = [view bitmapImageRepForCachingDisplayInRect:bounds];
        if (!rep) {
            LogMacRibbon(@"captureWindowSnapshotToFile failed: bitmapImageRep is nil");
            return;
        }
        [view cacheDisplayInRect:bounds toBitmapImageRep:rep];
        NSData *pngData = [rep representationUsingType:NSBitmapImageFileTypePNG properties:@{}];
        [pngData writeToFile:filePath atomically:YES];
        LogMacRibbon(@"Window snapshot successfully saved to: %@", filePath);
    });
}

- (void)checkWindowStatus {
    [self checkExternalCommands];
    if (!_targetWindow || ![_targetWindow isVisible]) {
        [self findAndAttachToTargetWindow];
    } else {
        [self updateThemeFromAutoCAD];
        [self checkHtmlUpdate];
        [self checkAutoCADStateSync];
    }
}

- (void)onWindowDidBecomeKey:(NSNotification *)note {
    NSWindow *win = note.object;
    LogMacRibbon(@"Window became key: title='%@', class='%@'", win.title, NSStringFromClass([win class]));
    if ([self isCandidateWindow:win]) {
        if (_targetWindow != win) {
            [self attachToWindow:win];
        }
    }
}

- (void)onWindowDidResize:(NSNotification *)note {
    if (note.object == _targetWindow && _isVisible) {
        [self updateRibbonFrame];
    }
}

- (BOOL)isCandidateWindow:(NSWindow *)win {
    if (!win) return NO;
    if (!win.isVisible) return NO;
    if ([win isKindOfClass:[NSPanel class]]) return NO;
    if (win.sheetParent != nil) return NO;

    NSString *clsName = NSStringFromClass([win class]);

    // Explicitly reject modal dialogs, sheets, splash screens, flyouts, and auxiliary windows
    if ([clsName containsString:@"Modal"] ||
        [clsName containsString:@"Dialog"] ||
        [clsName containsString:@"Splash"] ||
        [clsName containsString:@"Panel"] ||
        [clsName containsString:@"Flyout"] ||
        [clsName containsString:@"Visor"] ||
        [clsName containsString:@"TUI"] ||
        [clsName containsString:@"Sheet"] ||
        [clsName containsString:@"Alert"]) {
        return NO;
    }

    // AcMainWindow is AutoCAD's sole primary document window class
    if ([clsName containsString:@"AcMainWindow"]) {
        return YES;
    }

    return NO;
}

- (void)findAndAttachToTargetWindow {
    NSArray<NSWindow *> *windows = [NSApp windows];
    LogMacRibbon(@"Scanning %lu windows in NSApp...", (unsigned long)[windows count]);

    NSWindow *bestCandidate = nil;

    for (NSWindow *win in windows) {
        LogMacRibbon(@"Found window: title='%@', class='%@', visible=%d, frame=%@",
                     win.title, NSStringFromClass([win class]), win.isVisible, NSStringFromRect(win.frame));

        if ([self isCandidateWindow:win]) {
            if ([win isKeyWindow] || [win isMainWindow]) {
                bestCandidate = win;
                break;
            } else if (!bestCandidate) {
                bestCandidate = win;
            }
        }
    }

    if (bestCandidate && bestCandidate != _targetWindow) {
        [self attachToWindow:bestCandidate];
    }
}

- (id)paneLayoutViewController {
    if (!_targetWindow) return nil;
    id wc = [_targetWindow windowController];
    SEL sel = NSSelectorFromString(@"paneLayoutViewController");
    if (wc && [wc respondsToSelector:sel]) {
        return ((id (*)(id, SEL))objc_msgSend)(wc, sel);
    }
    return nil;
}

- (void)setLeftToolSetsPaneHidden:(BOOL)hidden {
    id paneVC = [self paneLayoutViewController];
    if (paneVC) {
        SEL actionSel = NSSelectorFromString(hidden ? @"hidePane:" : @"unhidePane:");
        if ([paneVC respondsToSelector:actionSel]) {
            ((void (*)(id, SEL, NSUInteger))objc_msgSend)(paneVC, actionSel, 0); // 0 = leftPane (Tool Sets)
            LogMacRibbon(@"setLeftToolSetsPaneHidden(%d) via ACPaneLayoutViewController", hidden);
            return;
        }
    }
    [[CommandExecutor sharedInstance] executeCommand:hidden ? @"_TOOLSETSCLOSE\n" : @"_TOOLSETS\n"];
}

- (BOOL)updateTopSpacerConstraint:(CGFloat)targetHeight {
    if (!_targetWindow || !_targetWindow.contentView) return NO;
    NSView *sepView = [RibbonManager findViewWithIdentifier:@"separatorView" inView:_targetWindow.contentView];
    if (!sepView) return NO;

    NSArray<NSView *> *constraintHolders = sepView.superview ? @[sepView, sepView.superview] : @[sepView];
    for (NSView *holder in constraintHolders) {
        for (NSLayoutConstraint *c in holder.constraints) {
            if (c.firstItem == sepView &&
                c.firstAttribute == NSLayoutAttributeHeight &&
                c.secondItem == nil) {
                if (fabs(c.constant - targetHeight) > 0.5) {
                    c.constant = targetHeight;
                    [sepView setNeedsLayout:YES];
                    [sepView.superview setNeedsLayout:YES];
                    [sepView.superview.superview setNeedsLayout:YES];
                    [_targetWindow.contentView layoutSubtreeIfNeeded];
                    LogMacRibbon(@"Updated separatorView top spacer constraint to %.1f", targetHeight);
                }
                return YES;
            }
        }
    }
    return NO;
}

- (void)attachToWindow:(NSWindow *)window {
    if (!window || !window.contentView) return;

    if (_targetWindow && _ribbonVC.view.superview) {
        [_ribbonVC.view removeFromSuperview];
    }

    _targetWindow = window;
    LogMacRibbon(@"ATTACHING Ribbon to window: '%@' (%@)", window.title, NSStringFromClass([window class]));

    NSView *contentView = window.contentView;
    [contentView addSubview:_ribbonVC.view positioned:NSWindowAbove relativeTo:nil];

    _isVisible = YES;
    _hasLoadedOnce = YES;
    _baseRibbonHeight = (_ribbonVC.currentHeight > 0 && _ribbonVC.currentHeight <= 125.0) ? _ribbonVC.currentHeight : 115.0;
    [self setLeftToolSetsPaneHidden:YES];
    [self updateRibbonFrame];
}

- (void)updateRibbonFrame {
    if (!_targetWindow || !_ribbonVC.view.superview) return;

    NSView *contentView = _targetWindow.contentView;
    NSRect bounds = contentView.bounds;
    CGFloat h = _ribbonVC.currentHeight;

    if (_isVisible && !_ribbonVC.view.hidden && h > 0.0 && h <= 125.0) {
        _baseRibbonHeight = h;
    }

    // Reserve space at the very top of AutoCAD's ACPaneLayoutView (above fileTabPane and centerPane)
    // so the Ribbon never overlaps the Drawing Canvas, ViewCube, Viewport Controls, Start Tab, or Right Inspector!
    CGFloat reservedTopH = (_isVisible && !_ribbonVC.view.hidden) ? _baseRibbonHeight : 1.0;
    BOOL hasSpacerConstraint = [self updateTopSpacerConstraint:reservedTopH];

    // If top spacer constraint is active, Ribbon sits at y = bounds.size.height - h (above fileTabPane, matching Windows AutoCAD).
    // Otherwise fallback to sitting below the 24px fileTabPane.
    CGFloat topOffset = hasSpacerConstraint ? 0.0 : 24.0;
    CGFloat ribbonWidth = bounds.size.width;

    NSRect newFrame = NSMakeRect(0, bounds.size.height - topOffset - h, ribbonWidth, h);
    _ribbonVC.view.frame = newFrame;
    _ribbonVC.view.autoresizingMask = NSViewWidthSizable | NSViewMinYMargin;
    LogMacRibbon(@"Ribbon frame updated to %@ (baseH=%.1f, spacer=%d)", NSStringFromRect(newFrame), _baseRibbonHeight, hasSpacerConstraint);
}

- (void)showRibbon {
    if (!_targetWindow) {
        [self findAndAttachToTargetWindow];
    }

    if (_ribbonVC.view.superview == nil && _targetWindow) {
        [_targetWindow.contentView addSubview:_ribbonVC.view positioned:NSWindowAbove relativeTo:nil];
    }

    _ribbonVC.view.hidden = NO;
    _isVisible = YES;
    [self hideFloatingSwitchButton];
    [self updateRibbonFrame];
    LogMacRibbon(@"Ribbon shown explicitly");
}

- (void)hideRibbon {
    _ribbonVC.view.hidden = YES;
    _isVisible = NO;
    [self updateRibbonFrame];
    LogMacRibbon(@"Ribbon hidden explicitly");
}

- (void)toggleRibbon {
    if (_isVisible && !_ribbonVC.view.hidden) {
        [self switchToMacToolbar];
    } else {
        [self switchToWindowsRibbon];
    }
}

- (void)switchToMacToolbar {
    LogMacRibbon(@"switchToMacToolbar: Hiding Ribbon, showing native Mac Tool Sets palette");
    [self hideRibbon];
    [self setLeftToolSetsPaneHidden:NO];
    [self showFloatingSwitchButton];
}

- (void)switchToWindowsRibbon {
    LogMacRibbon(@"switchToWindowsRibbon: Showing Ribbon, closing native Mac Tool Sets palette");
    [self hideFloatingSwitchButton];
    [self setLeftToolSetsPaneHidden:YES];
    _baseRibbonHeight = 115.0;
    if (_ribbonVC) {
        _ribbonVC.currentHeight = 115.0;
        if (!_hasLoadedOnce) {
            _hasLoadedOnce = YES;
            [_ribbonVC reloadRibbonContent];
        }
    }
    [self showRibbon];
    [self updateRibbonFrame];
}

- (void)ensureRibbonVisible {
    if (_isVisible && _targetWindow && _ribbonVC.view.superview == _targetWindow.contentView && !_ribbonVC.view.hidden) {
        [self setLeftToolSetsPaneHidden:YES];
        [self updateRibbonFrame];
        [self checkAutoCADStateSync];
        return;
    }
    [self switchToWindowsRibbon];
}

- (void)ensurePalettesHidden:(BOOL)hidden {
    dispatch_async(dispatch_get_main_queue(), ^{
        id paneVC = [self paneLayoutViewController];
        if (paneVC) {
            SEL actionSel = NSSelectorFromString(hidden ? @"hidePane:" : @"unhidePane:");
            if ([paneVC respondsToSelector:actionSel]) {
                ((void (*)(id, SEL, NSUInteger))objc_msgSend)(paneVC, actionSel, 1); // 1 = rightPane (Layers/Properties Inspector)
                LogMacRibbon(@"ensurePalettesHidden(%d) via ACPaneLayoutViewController", hidden);
                [self updateRibbonFrame];
                return;
            }
        }
        [[CommandExecutor sharedInstance] executeCommand:hidden ? @"^C^C_HIDEPALETTES " : @"^C^C_SHOWPALETTES "];
        [self updateRibbonFrame];
    });
}

- (void)showFloatingSwitchButton {
    if (!_targetWindow || !_targetWindow.contentView) return;
    NSView *contentView = _targetWindow.contentView;
    NSRect bounds = contentView.bounds;

    CGFloat btnW = 145;
    CGFloat btnH = 21;
    // Position cleanly in the top bar empty zone between File Tabs and right edge
    CGFloat btnX = bounds.size.width - 320;
    CGFloat btnY = bounds.size.height - 23;

    if (!_floatingSwitchButton) {
        _floatingSwitchButton = [[NSButton alloc] initWithFrame:NSMakeRect(btnX, btnY, btnW, btnH)];
        _floatingSwitchButton.bordered = NO;
        NSMutableParagraphStyle *para = [[NSMutableParagraphStyle alloc] init];
        para.alignment = NSTextAlignmentCenter;
        NSDictionary *attrs = @{
            NSForegroundColorAttributeName: [NSColor colorWithCalibratedRed:0.93 green:0.95 blue:0.98 alpha:1.0],
            NSFontAttributeName: [NSFont systemFontOfSize:11.0 weight:NSFontWeightMedium],
            NSParagraphStyleAttributeName: para
        };
        _floatingSwitchButton.attributedTitle = [[NSAttributedString alloc] initWithString:@"Windows Ribbon" attributes:attrs];
        _floatingSwitchButton.target = self;
        _floatingSwitchButton.action = @selector(onFloatingSwitchClicked:);
        _floatingSwitchButton.toolTip = @"Switch to Windows Ribbon (command: RIBBON)";
        _floatingSwitchButton.autoresizingMask = NSViewMinXMargin | NSViewMinYMargin;
        _floatingSwitchButton.wantsLayer = YES;
        _floatingSwitchButton.layer.cornerRadius = 2.0;
        _floatingSwitchButton.layer.borderWidth = 1.0;
        _floatingSwitchButton.layer.borderColor = [[NSColor colorWithCalibratedRed:0.38 green:0.45 blue:0.54 alpha:0.95] CGColor];
        _floatingSwitchButton.layer.backgroundColor = [[NSColor colorWithCalibratedRed:0.17 green:0.21 blue:0.26 alpha:0.98] CGColor];
        _floatingSwitchButton.layer.zPosition = 99999;
    } else {
        _floatingSwitchButton.frame = NSMakeRect(btnX, btnY, btnW, btnH);
    }

    if (_floatingSwitchButton.superview != contentView) {
        [contentView addSubview:_floatingSwitchButton positioned:NSWindowAbove relativeTo:nil];
    }
    _floatingSwitchButton.hidden = NO;
    LogMacRibbon(@"Floating switch button displayed at %@", NSStringFromRect(_floatingSwitchButton.frame));
}

- (void)hideFloatingSwitchButton {
    if (_floatingSwitchButton) {
        _floatingSwitchButton.hidden = YES;
        [_floatingSwitchButton removeFromSuperview];
        LogMacRibbon(@"Floating switch button hidden");
    }
}

- (void)onFloatingSwitchClicked:(id)sender {
    [self switchToWindowsRibbon];
}

- (void)reloadRibbon {
    LogMacRibbon(@"Reloading Ribbon content explicitly...");
    [_ribbonVC reloadRibbonContent];
    [self updateRibbonFrame];
}

#pragma mark - RibbonViewDelegate

- (void)ribbonRequestedHeight:(CGFloat)height {
    LogMacRibbon(@"Ribbon height requested: %.1f", height);
    if (height > 0.0 && height <= 125.0) {
        _baseRibbonHeight = height;
    }
    [self updateRibbonFrame];
}

- (void)ribbonRequestedClose {
    [self switchToMacToolbar];
}

- (void)ribbonRequestedSwitchToMacToolbar {
    [self switchToMacToolbar];
}

- (void)ribbonRequestedSwitchToWindowsRibbon {
    [self switchToWindowsRibbon];
}

- (void)ribbonRequestedDockInspectorLeft:(BOOL)dockLeft {
    [self ensurePalettesHidden:dockLeft];
}

- (void)ribbonRequestedToggleHidePalettes {
    LogMacRibbon(@"ribbonRequestedToggleHidePalettes triggered");
    dispatch_async(dispatch_get_main_queue(), ^{
        id paneVC = [self paneLayoutViewController];
        NSView *paneView = _targetWindow ? [RibbonManager findViewWithIdentifier:@"rightPane" inView:_targetWindow.contentView] : nil;
        NSView *layoutView = paneView ? paneView.superview.superview.superview : nil;
        SEL isHiddenSel = NSSelectorFromString(@"isPaneHidden:");
        if (paneVC && layoutView && [layoutView respondsToSelector:isHiddenSel]) {
            BOOL currentlyHidden = ((BOOL (*)(id, SEL, NSUInteger))objc_msgSend)(layoutView, isHiddenSel, 1);
            SEL toggleSel = NSSelectorFromString(currentlyHidden ? @"unhidePane:" : @"hidePane:");
            if ([paneVC respondsToSelector:toggleSel]) {
                ((void (*)(id, SEL, NSUInteger))objc_msgSend)(paneVC, toggleSel, 1);
                LogMacRibbon(@"Toggled rightPane (Inspector Palettes) -> hidden=%d", !currentlyHidden);
                [self updateRibbonFrame];
                return;
            }
        }
        // Fallback: check rightPane frame width
        if (paneVC && paneView) {
            BOOL currentlyHidden = (paneView.frame.size.width < 10.0 || paneView.isHidden);
            SEL toggleSel = NSSelectorFromString(currentlyHidden ? @"unhidePane:" : @"hidePane:");
            if ([paneVC respondsToSelector:toggleSel]) {
                ((void (*)(id, SEL, NSUInteger))objc_msgSend)(paneVC, toggleSel, 1);
                [self updateRibbonFrame];
                return;
            }
        }
    });
}

@end
