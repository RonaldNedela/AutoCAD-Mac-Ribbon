#import <Cocoa/Cocoa.h>
#import "RibbonManager.h"
#import <dlfcn.h>

void LogMacRibbon(NSString *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    NSString *msg = [[NSString alloc] initWithFormat:fmt arguments:args];
    va_end(args);
    NSLog(@"[MacRibbon] %@", msg);

    NSString *logLine = [NSString stringWithFormat:@"%@ [MacRibbon] %@\n", [NSDate date], msg];
    NSFileHandle *handle = [NSFileHandle fileHandleForWritingAtPath:@"/tmp/macribbon.log"];
    if (!handle) {
        [[NSFileManager defaultManager] createFileAtPath:@"/tmp/macribbon.log"
                                                contents:[logLine dataUsingEncoding:NSUTF8StringEncoding]
                                              attributes:nil];
    } else {
        [handle seekToEndOfFile];
        [handle writeData:[logLine dataUsingEncoding:NSUTF8StringEncoding]];
        [handle closeFile];
    }
}

enum AcRxAppMsgCode {
    kNullMsg = 0,
    kInitAppMsg = 1,
    kUnloadAppMsg = 2,
    kLoadDwgMsg = 3,
    kUnloadDwgMsg = 4,
    kInvkSubrMsg = 5
};

enum AcRxAppRetCode {
    kRetOK = 0,
    kRetError = 3
};

typedef bool (*AcrxLockApplicationFn)(void*);

extern "C" __attribute__((visibility("default")))
int acrxEntryPoint(int msg, void* pkt) {
    LogMacRibbon(@"acrxEntryPoint called with msg=%d, pkt=%p", msg, pkt);
    switch (msg) {
        case kInitAppMsg: {
            LogMacRibbon(@"kInitAppMsg: Locking application in memory and starting RibbonManager");
            
            // Crucial: lock application in AutoCAD memory so it is NOT immediately unloaded!
            AcrxLockApplicationFn lockFn = (AcrxLockApplicationFn)dlsym(RTLD_DEFAULT, "_Z19acrxLockApplicationPv");
            if (lockFn && pkt) {
                lockFn(pkt);
                LogMacRibbon(@"Application successfully locked in memory via acrxLockApplication");
            } else {
                LogMacRibbon(@"acrxLockApplication symbol not resolved or pkt was null");
            }

            dispatch_async(dispatch_get_main_queue(), ^{
                [[RibbonManager sharedInstance] start];
                [[RibbonManager sharedInstance] switchToWindowsRibbon];
            });
            break;
        }
        case kLoadDwgMsg: {
            LogMacRibbon(@"kLoadDwgMsg received");
            dispatch_async(dispatch_get_main_queue(), ^{
                [[RibbonManager sharedInstance] switchToWindowsRibbon];
            });
            break;
        }
        case kUnloadAppMsg: {
            LogMacRibbon(@"kUnloadAppMsg received - ignoring automatic unload to keep Ribbon persistent");
            // Do NOT stop ribbon on transient unload message unless AutoCAD is terminating
            break;
        }
        default:
            break;
    }
    return kRetOK;
}

__attribute__((constructor))
static void onBundleLoaded() {
    LogMacRibbon(@"MacRibbon constructor triggered! Process: %d (%@)", 
                 [[NSProcessInfo processInfo] processIdentifier], 
                 [[NSProcessInfo processInfo] processName]);

    dispatch_async(dispatch_get_main_queue(), ^{
        [[RibbonManager sharedInstance] start];
        [[RibbonManager sharedInstance] switchToWindowsRibbon];
    });
}

__attribute__((destructor))
static void onBundleUnloaded() {
    LogMacRibbon(@"MacRibbon destructor executed");
}
