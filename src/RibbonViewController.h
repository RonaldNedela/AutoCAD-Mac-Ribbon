#pragma once
#import <Cocoa/Cocoa.h>
#import <WebKit/WebKit.h>

@protocol RibbonViewDelegate <NSObject>
@optional
- (void)ribbonRequestedHeight:(CGFloat)height;
- (void)ribbonRequestedClose;
- (void)ribbonRequestedSwitchToMacToolbar;
- (void)ribbonRequestedSwitchToWindowsRibbon;
- (void)ribbonRequestedDockInspectorLeft:(BOOL)dockLeft;
- (void)ribbonRequestedToggleHidePalettes;
@end

@interface RibbonViewController : NSViewController <WKScriptMessageHandler, WKNavigationDelegate>

@property (nonatomic, weak) id<RibbonViewDelegate> delegate;
@property (nonatomic, strong, readonly) WKWebView *webView;
@property (nonatomic, strong, readonly) NSURL *resourcesURL;
@property (nonatomic, assign) CGFloat currentHeight;

- (instancetype)initWithResourcesURL:(NSURL *)resourcesURL;
- (void)sendThemeUpdate:(BOOL)isDark;
- (void)reloadRibbonContent;
- (void)evaluateJavaScript:(NSString *)js completionHandler:(void (^)(id result, NSError *error))completionHandler;
- (void)captureSnapshotToFile:(NSString *)filePath;

@end
