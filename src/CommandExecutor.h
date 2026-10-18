#pragma once
#import <Foundation/Foundation.h>

@interface CommandExecutor : NSObject

+ (instancetype)sharedInstance;

/**
 * Executes a command string in the active AutoCAD document.
 * Handles prefixing with cancellation (^C^C) and ensures proper line termination.
 */
- (void)executeCommand:(NSString *)commandString;

/**
 * Returns true if the native AutoCAD command symbol was successfully located.
 */
- (BOOL)isNativeEngineAvailable;

@end
