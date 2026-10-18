#pragma once
#import <Cocoa/Cocoa.h>
#import "RibbonViewController.h"

@interface RibbonManager : NSObject <RibbonViewDelegate>

+ (instancetype)sharedInstance;

- (void)start;
- (void)stop;

- (void)showRibbon;
- (void)hideRibbon;
- (void)toggleRibbon;
- (void)reloadRibbon;
- (void)switchToMacToolbar;
- (void)switchToWindowsRibbon;

@property (nonatomic, assign, readonly) BOOL isVisible;

@end
