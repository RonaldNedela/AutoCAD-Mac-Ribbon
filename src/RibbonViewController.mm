#import "RibbonViewController.h"
#import "CommandExecutor.h"

extern void LogMacRibbon(NSString *fmt, ...);

@interface RibbonWebView : WKWebView
@end

@implementation RibbonWebView
- (NSMenu *)menuForEvent:(NSEvent *)event {
    // Return nil to completely suppress default WebKit Safari context menus (Reload, Inspect, etc.)
    return nil;
}

- (BOOL)acceptsFirstMouse:(NSEvent *)event {
    return YES;
}
@end

@interface RibbonViewController () {
    NSURL *_resourcesURL;
    RibbonWebView *_webView;
}
@end

@implementation RibbonViewController

@synthesize webView = _webView;
@synthesize resourcesURL = _resourcesURL;

- (instancetype)initWithResourcesURL:(NSURL *)resourcesURL {
    self = [super init];
    if (self) {
        _resourcesURL = resourcesURL;
        _currentHeight = 115.0; // Standard AutoCAD Ribbon height
        LogMacRibbon(@"RibbonViewController initialized with URL: %@", [resourcesURL path]);
    }
    return self;
}

- (void)loadView {
    LogMacRibbon(@"RibbonViewController loadView starting...");

    WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
    WKUserContentController *userContent = [[WKUserContentController alloc] init];
    [userContent addScriptMessageHandler:self name:@"autocad"];
    config.userContentController = userContent;

    [config.preferences setValue:@YES forKey:@"allowFileAccessFromFileURLs"];

    NSRect initialRect = NSMakeRect(0, 0, 1200, _currentHeight);
    _webView = [[RibbonWebView alloc] initWithFrame:initialRect configuration:config];
    _webView.navigationDelegate = self;
    _webView.autoresizingMask = NSViewWidthSizable | NSViewHeightSizable;

    _webView.wantsLayer = YES;
    _webView.layer.zPosition = 9999;
    _webView.layer.backgroundColor = [[NSColor clearColor] CGColor];

    if ([_webView respondsToSelector:@selector(setValue:forKey:)]) {
        [_webView setValue:@NO forKey:@"drawsBackground"];
    }

    self.view = _webView;
    LogMacRibbon(@"RibbonViewController loadView complete, view=%p, frame=%@", _webView, NSStringFromRect(initialRect));

    [self loadRibbonContent];
}

- (void)loadRibbonContent {
    if (!_resourcesURL) {
        LogMacRibbon(@"Error: _resourcesURL is nil");
        return;
    }

    NSURL *htmlURL = [_resourcesURL URLByAppendingPathComponent:@"index.html"];
    if ([[NSFileManager defaultManager] fileExistsAtPath:[htmlURL path]]) {
        LogMacRibbon(@"Loading index.html via loadFileURL with read access to: %@", [_resourcesURL path]);
        [_webView loadFileURL:htmlURL allowingReadAccessToURL:_resourcesURL];
    } else {
        LogMacRibbon(@"Error: index.html not found at %@", [htmlURL path]);
    }
}

- (void)reloadRibbonContent {
    _currentHeight = 115.0;
    dispatch_async(dispatch_get_main_queue(), ^{
        [self loadRibbonContent];
    });
}

- (void)evaluateJavaScript:(NSString *)js completionHandler:(void (^)(id result, NSError *error))completionHandler {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (self->_webView) {
            [self->_webView evaluateJavaScript:js completionHandler:completionHandler];
        } else if (completionHandler) {
            completionHandler(nil, [NSError errorWithDomain:@"MacRibbon" code:-1 userInfo:@{NSLocalizedDescriptionKey: @"WebView is nil"}]);
        }
    });
}

- (void)captureSnapshotToFile:(NSString *)filePath {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (!self->_webView) return;
        WKSnapshotConfiguration *config = [[WKSnapshotConfiguration alloc] init];
        [self->_webView takeSnapshotWithConfiguration:config completionHandler:^(NSImage *image, NSError *error) {
            if (error || !image) {
                LogMacRibbon(@"Snapshot failed: %@", error);
                return;
            }
            CGImageRef cgRef = [image CGImageForProposedRect:NULL context:nil hints:nil];
            if (!cgRef) return;
            NSBitmapImageRep *rep = [[NSBitmapImageRep alloc] initWithCGImage:cgRef];
            NSData *pngData = [rep representationUsingType:NSBitmapImageFileTypePNG properties:@{}];
            [pngData writeToFile:filePath atomically:YES];
            LogMacRibbon(@"Ribbon snapshot saved successfully to %@", filePath);
        }];
    });
}

#pragma mark - WKScriptMessageHandler

- (void)userContentController:(WKUserContentController *)userContentController
      didReceiveScriptMessage:(WKScriptMessage *)message {
    if (![message.name isEqualToString:@"autocad"]) return;

    NSDictionary *body = nil;
    if ([message.body isKindOfClass:[NSDictionary class]]) {
        body = (NSDictionary *)message.body;
    } else if ([message.body isKindOfClass:[NSString class]]) {
        NSData *data = [((NSString *)message.body) dataUsingEncoding:NSUTF8StringEncoding];
        body = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
    }

    if (!body) return;

    NSString *action = body[@"action"];
    LogMacRibbon(@"Received JS message: action=%@, body=%@", action, body);

    if ([action isEqualToString:@"command"]) {
        NSString *cmd = body[@"command"];
        if (cmd) {
            [[CommandExecutor sharedInstance] executeCommand:cmd];
        }
    } else if ([action isEqualToString:@"log"]) {
        LogMacRibbon(@"[Ribbon JS] %@", body[@"message"]);
    } else if ([action isEqualToString:@"resize"]) {
        NSNumber *heightNum = body[@"height"];
        if (heightNum) {
            _currentHeight = [heightNum doubleValue];
            if ([self.delegate respondsToSelector:@selector(ribbonRequestedHeight:)]) {
                [self.delegate ribbonRequestedHeight:_currentHeight];
            }
        }
    } else if ([action isEqualToString:@"close"]) {
        if ([self.delegate respondsToSelector:@selector(ribbonRequestedClose)]) {
            [self.delegate ribbonRequestedClose];
        }
    } else if ([action isEqualToString:@"switchToMacToolbar"]) {
        if ([self.delegate respondsToSelector:@selector(ribbonRequestedSwitchToMacToolbar)]) {
            [self.delegate ribbonRequestedSwitchToMacToolbar];
        } else if ([self.delegate respondsToSelector:@selector(ribbonRequestedClose)]) {
            [self.delegate ribbonRequestedClose];
        }
    } else if ([action isEqualToString:@"switchToWindowsRibbon"]) {
        if ([self.delegate respondsToSelector:@selector(ribbonRequestedSwitchToWindowsRibbon)]) {
            [self.delegate ribbonRequestedSwitchToWindowsRibbon];
        }
    } else if ([action isEqualToString:@"dockInspectorLeft"]) {
        BOOL left = [body[@"left"] boolValue];
        if ([self.delegate respondsToSelector:@selector(ribbonRequestedDockInspectorLeft:)]) {
            [self.delegate ribbonRequestedDockInspectorLeft:left];
        }
    } else if ([action isEqualToString:@"toggleHidePalettes"]) {
        if ([self.delegate respondsToSelector:@selector(ribbonRequestedToggleHidePalettes)]) {
            [self.delegate ribbonRequestedToggleHidePalettes];
        }
    } else if ([action isEqualToString:@"showNativeContextMenu"]) {
        [self showNativeContextMenuWithData:body];
    }
}

- (void)showNativeContextMenuWithData:(NSDictionary *)data {
    NSMenu *menu = [[NSMenu alloc] initWithTitle:@"Ribbon Context"];

    NSMenuItem *switchItem = [[NSMenuItem alloc] initWithTitle:@"Switch to Mac Toolbar"
                                                        action:@selector(onContextSwitchToToolbar:)
                                                 keyEquivalent:@""];
    switchItem.target = self;
    [menu addItem:switchItem];

    [menu addItem:[NSMenuItem separatorItem]];

    NSArray *tabs = data[@"tabs"];
    if (tabs && [tabs count] > 0) {
        NSMenuItem *tabsItem = [[NSMenuItem alloc] initWithTitle:@"Show Tabs" action:nil keyEquivalent:@""];
        NSMenu *tabsSubmenu = [[NSMenu alloc] initWithTitle:@"Show Tabs"];
        for (NSDictionary *t in tabs) {
            NSString *tId = t[@"id"];
            NSString *name = t[@"name"] ?: tId;
            BOOL visible = [t[@"visible"] boolValue];
            NSMenuItem *subItem = [[NSMenuItem alloc] initWithTitle:name
                                                             action:@selector(onContextToggleTab:)
                                                      keyEquivalent:@""];
            subItem.target = self;
            subItem.representedObject = tId;
            subItem.state = visible ? NSControlStateValueOn : NSControlStateValueOff;
            [tabsSubmenu addItem:subItem];
        }
        [tabsItem setSubmenu:tabsSubmenu];
        [menu addItem:tabsItem];
    }

    NSArray *panels = data[@"panels"];
    if (panels && [panels count] > 0) {
        NSMenuItem *panelsItem = [[NSMenuItem alloc] initWithTitle:@"Show Panels" action:nil keyEquivalent:@""];
        NSMenu *panelsSubmenu = [[NSMenu alloc] initWithTitle:@"Show Panels"];
        for (NSDictionary *p in panels) {
            NSString *pId = p[@"id"];
            NSString *name = p[@"name"] ?: pId;
            BOOL visible = [p[@"visible"] boolValue];
            NSMenuItem *subItem = [[NSMenuItem alloc] initWithTitle:name
                                                             action:@selector(onContextTogglePanel:)
                                                      keyEquivalent:@""];
            subItem.target = self;
            subItem.representedObject = pId;
            subItem.state = visible ? NSControlStateValueOn : NSControlStateValueOff;
            [panelsSubmenu addItem:subItem];
        }
        [panelsItem setSubmenu:panelsSubmenu];
        [menu addItem:panelsItem];
    }

    [menu addItem:[NSMenuItem separatorItem]];

    BOOL isMin = [data[@"isMinimized"] boolValue];
    NSMenuItem *minItem = [[NSMenuItem alloc] initWithTitle:@"Minimize the Ribbon"
                                                    action:@selector(onContextToggleMinimize:)
                                             keyEquivalent:@""];
    minItem.target = self;
    minItem.state = isMin ? NSControlStateValueOn : NSControlStateValueOff;
    [menu addItem:minItem];

    double clientX = [data[@"clientX"] doubleValue];
    double clientY = [data[@"clientY"] doubleValue];
    NSPoint loc = NSMakePoint(clientX, _webView.isFlipped ? clientY : (_webView.bounds.size.height - clientY));

    [menu popUpMenuPositioningItem:nil atLocation:loc inView:_webView];
}

- (void)onContextSwitchToToolbar:(id)sender {
    if ([self.delegate respondsToSelector:@selector(ribbonRequestedSwitchToMacToolbar)]) {
        [self.delegate ribbonRequestedSwitchToMacToolbar];
    }
}

- (void)onContextToggleTab:(NSMenuItem *)sender {
    NSString *tabId = sender.representedObject;
    if (tabId) {
        NSString *js = [NSString stringWithFormat:@"if (window.toggleTabVisibility) window.toggleTabVisibility('%@');", tabId];
        [_webView evaluateJavaScript:js completionHandler:nil];
    }
}

- (void)onContextTogglePanel:(NSMenuItem *)sender {
    NSString *panelId = sender.representedObject;
    if (panelId) {
        NSString *js = [NSString stringWithFormat:@"if (window.togglePanelVisibility) window.togglePanelVisibility('%@');", panelId];
        [_webView evaluateJavaScript:js completionHandler:nil];
    }
}

- (void)onContextToggleMinimize:(id)sender {
    [_webView evaluateJavaScript:@"if (window.toggleMinimizeRibbon) window.toggleMinimizeRibbon();" completionHandler:nil];
}

- (void)sendThemeUpdate:(BOOL)isDark {
    NSString *js = [NSString stringWithFormat:@"if (window.setTheme) window.setTheme('%@');", isDark ? @"dark" : @"light"];
    [_webView evaluateJavaScript:js completionHandler:nil];
}

#pragma mark - WKNavigationDelegate

- (void)webView:(WKWebView *)webView didFinishNavigation:(WKNavigation *)navigation {
    LogMacRibbon(@"Ribbon HTML navigation finished successfully!");
}

- (void)webView:(WKWebView *)webView didFailNavigation:(WKNavigation *)navigation withError:(NSError *)error {
    LogMacRibbon(@"Ribbon HTML navigation failed: %@", error);
}

- (void)webView:(WKWebView *)webView didFailProvisionalNavigation:(WKNavigation *)navigation withError:(NSError *)error {
    LogMacRibbon(@"Ribbon HTML provisional navigation failed: %@", error);
}

@end
