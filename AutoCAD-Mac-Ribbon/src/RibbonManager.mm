#import "RibbonManager.h"
#import "CommandExecutor.h"
#import <CoreGraphics/CoreGraphics.h>

extern void LogMacRibbon(NSString *fmt, ...);

@interface RibbonManager () {
    RibbonViewController *_ribbonVC;
    NSWindow *_targetWindow;
    BOOL _isVisible;
    NSTimer *_pollTimer;
    NSColor *_lastSampledColor;
    NSDate *_lastHtmlModDate;
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
        [NSHomeDirectory() stringByAppendingPathComponent:@"Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle/Contents/Resources"],
        [NSHomeDirectory() stringByAppendingPathComponent:@"Library/Application Support/Autodesk/ApplicationPlugins/MacRibbon.bundle/Contents/Resources"],
        @"/Library/Application Support/Autodesk/ApplicationAddins/MacRibbon.bundle/Contents/Resources",
        @"/Users/Ronci/Desktop/AutoCAD-Mac-Ribbon/ui"
    ];

    for (NSString *candidate in candidates) {
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

- (NSColor *)sampleAutoCADWindowColor {
    if (!_targetWindow || ![_targetWindow isVisible]) return nil;
    NSView *contentView = _targetWindow.contentView;
    if (!contentView) return nil;

    NSRect bounds = contentView.bounds;
    // Sample directly from the toolbar region of contentView (top area)
    CGFloat sampleY = bounds.size.height - 15;
    if (sampleY <= 0) sampleY = 10;
    NSRect sampleRect = NSMakeRect(bounds.size.width * 0.4, sampleY, 4, 4);

    NSBitmapImageRep *rep = [contentView bitmapImageRepForCachingDisplayInRect:sampleRect];
    if (!rep) return nil;

    [contentView cacheDisplayInRect:sampleRect toBitmapImageRep:rep];
    NSColor *color = [rep colorAtX:2 y:2];
    return color;
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

    // Compute relative palette shades
    CGFloat tabR, tabG, tabB;
    CGFloat hovR, hovG, hovB;
    CGFloat borR, borG, borB;

    if (isLight) {
        tabR = fmax(0.0, r * 0.93);
        tabG = fmax(0.0, g * 0.93);
        tabB = fmax(0.0, b * 0.93);

        hovR = fmax(0.0, r * 0.91);
        hovG = fmax(0.0, g * 0.91);
        hovB = fmax(0.0, b * 0.91);

        borR = fmax(0.0, r * 0.84);
        borG = fmax(0.0, g * 0.84);
        borB = fmax(0.0, b * 0.84);
    } else {
        tabR = fmax(0.0, r * 0.70);
        tabG = fmax(0.0, g * 0.70);
        tabB = fmax(0.0, b * 0.70);

        hovR = fmin(1.0, r * 1.25);
        hovG = fmin(1.0, g * 1.25);
        hovB = fmin(1.0, b * 1.25);

        borR = fmax(0.0, r * 0.78);
        borG = fmax(0.0, g * 0.78);
        borB = fmax(0.0, b * 0.78);
    }

    NSString *hexBg = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(r * 255), (int)(g * 255), (int)(b * 255)];
    NSString *hexTabs = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(tabR * 255), (int)(tabG * 255), (int)(tabB * 255)];
    NSString *hexHover = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(hovR * 255), (int)(hovG * 255), (int)(hovB * 255)];
    NSString *hexBorder = [NSString stringWithFormat:@"#%02x%02x%02x", (int)(borR * 255), (int)(borG * 255), (int)(borB * 255)];

    LogMacRibbon(@"AutoCAD Theme synchronized! Sampled: %@, isLight: %d", hexBg, isLight);

    NSString *js = [NSString stringWithFormat:
        @"document.documentElement.style.setProperty('--cad-ribbon-bg', '%@');"
        @"document.documentElement.style.setProperty('--cad-tab-bar-bg', '%@');"
        @"document.documentElement.style.setProperty('--cad-tab-active-bg', '%@');"
        @"document.documentElement.style.setProperty('--cad-btn-hover', '%@');"
        @"document.documentElement.style.setProperty('--cad-panel-border', '%@');"
        @"document.documentElement.style.setProperty('--cad-menu-bg', '%@');"
        @"document.body.classList.toggle('light-theme', %s);",
        hexBg, hexTabs, hexBg, hexHover, hexBorder, hexTabs, isLight ? "true" : "false"];

    dispatch_async(dispatch_get_main_queue(), ^{
        [_ribbonVC.webView evaluateJavaScript:js completionHandler:nil];
    });
}

- (void)checkHtmlUpdate {
    if (!_ribbonVC || !_ribbonVC.resourcesURL) return;
    NSURL *htmlURL = [_ribbonVC.resourcesURL URLByAppendingPathComponent:@"index.html"];
    if (!htmlURL) return;

    NSDictionary *attrs = [[NSFileManager defaultManager] attributesOfItemAtPath:[htmlURL path] error:nil];
    NSDate *modDate = attrs[NSFileModificationDate];
    if (modDate) {
        if (_lastHtmlModDate && [modDate timeIntervalSinceDate:_lastHtmlModDate] > 0.5) {
            _lastHtmlModDate = modDate;
            LogMacRibbon(@"index.html modified on disk - automatically reloading Ribbon WebView!");
            dispatch_async(dispatch_get_main_queue(), ^{
                [self reloadRibbon];
            });
        } else if (!_lastHtmlModDate) {
            _lastHtmlModDate = modDate;
        }
    }
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
        } else if ([cmd isEqualToString:@"toggleRibbon"]) {
            [self toggleRibbon];
        }
    }
}

- (void)checkWindowStatus {
    [self checkExternalCommands];
    if (!_targetWindow || ![_targetWindow isVisible]) {
        [self findAndAttachToTargetWindow];
    } else {
        [self updateThemeFromAutoCAD];
        [self checkHtmlUpdate];
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

    NSString *clsName = NSStringFromClass([win class]);
    NSString *title = win.title ?: @"";

    // AcMainWindow is AutoCAD's main window class
    if ([clsName containsString:@"AcMainWindow"]) {
        return YES;
    }

    // Check by window title
    if ([title containsString:@"AutoCAD"] || [title containsString:@".dwg"]) {
        return YES;
    }

    // General fallback: main size window
    NSRect frame = win.frame;
    if (frame.size.width >= 600 && frame.size.height >= 450) {
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
    [[CommandExecutor sharedInstance] executeCommand:@"_TOOLSETSCLOSE\n"];
    [self ensurePalettesHidden:YES];
    [self updateRibbonFrame];
}

static void dumpViewHierarchy(NSView *v, int depth) {
    if (depth > 10) return;
    NSString *indent = [@"" stringByPaddingToLength:depth*2 withString:@" " startingAtIndex:0];
    LogMacRibbon(@"%@|-- %@ frame=%@ flipped=%d", indent, NSStringFromClass([v class]), NSStringFromRect(v.frame), (int)v.isFlipped);
    for (NSView *sub in v.subviews) {
        dumpViewHierarchy(sub, depth + 1);
    }
}

- (CGFloat)detectRightSidebarWidth {
    if (!_targetWindow || !_targetWindow.contentView) return 0.0;

    // Check Window menu: if "Show Palettes" is present, palettes are hidden -> 0.0
    NSMenu *mainMenu = [NSApp mainMenu];
    if (mainMenu) {
        for (NSMenuItem *top in mainMenu.itemArray) {
            if ([top.title isEqualToString:@"Window"] && top.hasSubmenu) {
                [top.submenu update];
                for (NSMenuItem *sub in top.submenu.itemArray) {
                    if ([sub.title isEqualToString:@"Show Palettes"]) {
                        return 0.0;
                    }
                }
            }
        }
    }

    // Palettes are visible. Detect inspector width on the right:
    NSView *contentView = _targetWindow.contentView;
    CGFloat winWidth = contentView.bounds.size.width;
    CGFloat rightWidth = 0.0;

    for (NSView *sub in contentView.subviews) {
        if (sub != _ribbonVC.view && [NSStringFromClass([sub class]) containsString:@"PaneLayout"]) {
            for (NSView *split in sub.subviews) {
                if ([NSStringFromClass([split class]) containsString:@"SplitView"]) {
                    for (NSView *pane in split.subviews) {
                        for (NSView *inner in pane.subviews) {
                            if ([NSStringFromClass([inner class]) containsString:@"SplitView"]) {
                                for (NSView *innerPane in inner.subviews) {
                                    NSRect f = innerPane.frame;
                                    if (fabs((f.origin.x + f.size.width) - winWidth) < 2.0 && f.size.width > 50 && f.size.width < 500) {
                                        rightWidth = f.size.width;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if (rightWidth <= 0.0) {
        rightWidth = 236.0;
    }
    return rightWidth;
}

- (void)updateRibbonFrame {
    if (!_targetWindow || !_ribbonVC.view.superview) return;

    NSView *contentView = _targetWindow.contentView;
    NSRect bounds = contentView.bounds;
    CGFloat h = _ribbonVC.currentHeight;

    // Top Quick Access toolbar height in AutoCAD Mac is 24.0 (y=0 to 24 from top)
    CGFloat topToolbarH = 24.0;

    // Dynamically detect right sidebar width so Ribbon never covers the Inspector palette header
    CGFloat rightSidebarW = [self detectRightSidebarWidth];
    CGFloat ribbonWidth = bounds.size.width - rightSidebarW;

    // Pin Ribbon directly beneath the top Quick Access toolbar
    NSRect newFrame = NSMakeRect(0, bounds.size.height - topToolbarH - h, ribbonWidth, h);
    _ribbonVC.view.frame = newFrame;
    _ribbonVC.view.autoresizingMask = NSViewWidthSizable | NSViewMinYMargin;
    LogMacRibbon(@"Ribbon frame updated to %@ (rightSidebarW=%.1f)", NSStringFromRect(newFrame), rightSidebarW);
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
    LogMacRibbon(@"switchToMacToolbar: Hiding Ribbon, showing native Mac Tool Sets palette and palettes");
    [self hideRibbon];
    [[CommandExecutor sharedInstance] executeCommand:@"_TOOLSETS\n"];
    [self ensurePalettesHidden:NO];
    [self showFloatingSwitchButton];
}

- (void)switchToWindowsRibbon {
    LogMacRibbon(@"switchToWindowsRibbon: Showing Ribbon, closing native Mac Tool Sets palette, hiding sidebar palettes");
    [self hideFloatingSwitchButton];
    [[CommandExecutor sharedInstance] executeCommand:@"_TOOLSETSCLOSE\n"];
    [self ensurePalettesHidden:YES];
    if (_ribbonVC) {
        _ribbonVC.currentHeight = 115.0;
        [_ribbonVC reloadRibbonContent];
    }
    [self showRibbon];
    [self updateRibbonFrame];
}

- (void)ensurePalettesHidden:(BOOL)hidden {
    dispatch_async(dispatch_get_main_queue(), ^{
        NSString *targetTitle = hidden ? @"Hide Palettes" : @"Show Palettes";
        NSString *procName = [[NSProcessInfo processInfo] processName];
        NSString *script = [NSString stringWithFormat:
            @"tell application \"System Events\" to tell process \"%@\" to "
            @"if exists (menu item \"%@\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1) then "
            @"click menu item \"%@\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1",
            procName, targetTitle, targetTitle];
        NSAppleScript *as = [[NSAppleScript alloc] initWithSource:script];
        [as executeAndReturnError:nil];
        LogMacRibbon(@"ensurePalettesHidden(%d): Processed '%@' via AppleScript", hidden, targetTitle);
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.15 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            [self updateRibbonFrame];
        });
    });
}

- (void)showFloatingSwitchButton {
    if (!_targetWindow || !_targetWindow.contentView) return;
    NSView *contentView = _targetWindow.contentView;
    NSRect bounds = contentView.bounds;

    CGFloat btnW = 145;
    CGFloat btnH = 21;
    // Position cleanly in the top bar empty zone between Quick Access and User profile
    CGFloat btnX = bounds.size.width - 320;
    CGFloat btnY = bounds.size.height - 23;

    if (!_floatingSwitchButton) {
        _floatingSwitchButton = [[NSButton alloc] initWithFrame:NSMakeRect(btnX, btnY, btnW, btnH)];
        _floatingSwitchButton.title = @"⚡️ Windows Ribbon";
        _floatingSwitchButton.bezelStyle = NSBezelStyleInline;
        _floatingSwitchButton.target = self;
        _floatingSwitchButton.action = @selector(onFloatingSwitchClicked:);
        _floatingSwitchButton.toolTip = @"Click to switch to Windows Ribbon";
        _floatingSwitchButton.autoresizingMask = NSViewMinXMargin | NSViewMinYMargin;
        _floatingSwitchButton.wantsLayer = YES;
        _floatingSwitchButton.layer.cornerRadius = 4.0;
        _floatingSwitchButton.layer.borderWidth = 1.0;
        _floatingSwitchButton.layer.borderColor = [[NSColor colorWithCalibratedRed:0.0 green:0.64 blue:1.0 alpha:0.8] CGColor];
        _floatingSwitchButton.layer.backgroundColor = [[NSColor colorWithCalibratedRed:0.15 green:0.20 blue:0.26 alpha:0.95] CGColor];
        _floatingSwitchButton.contentTintColor = [NSColor whiteColor];
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
    // Left-docking by swapping ACSplitView subviews corrupts AutoCAD's Metal rendering viewport.
    // Windows parity is achieved cleanly by ensurePalettesHidden:YES (full-width canvas with ViewCube top-right).
    [self ensurePalettesHidden:YES];
}

- (void)ribbonRequestedToggleHidePalettes {
    LogMacRibbon(@"ribbonRequestedToggleHidePalettes triggered");
    dispatch_async(dispatch_get_main_queue(), ^{
        NSString *procName = [[NSProcessInfo processInfo] processName];
        NSString *script = [NSString stringWithFormat:
            @"tell application \"System Events\" to tell process \"%@\" to "
            @"if exists (menu item \"Hide Palettes\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1) then\n"
            @"    click menu item \"Hide Palettes\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1\n"
            @"else if exists (menu item \"Show Palettes\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1) then\n"
            @"    click menu item \"Show Palettes\" of menu \"Window\" of menu bar item \"Window\" of menu bar 1\n"
            @"end if",
            procName];
        NSAppleScript *as = [[NSAppleScript alloc] initWithSource:script];
        [as executeAndReturnError:nil];
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.15 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            [self updateRibbonFrame];
        });
    });
}

@end
