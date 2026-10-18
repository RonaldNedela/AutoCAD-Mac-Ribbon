#import "CommandExecutor.h"
#import <dlfcn.h>
#import <string>

extern void LogMacRibbon(NSString *fmt, ...);

typedef void* (*AcDocManagerPtrFn)();
typedef void* (*StaticCurDocumentFn)();
typedef int (*SendStringToExecuteFn)(void* pMgr, void* pDoc, const wchar_t* pszCmd, bool bActivate, bool bWrapUpInactiveDoc, bool bEchoString);
typedef int (*AcedPostCommandFn)(const wchar_t *);

@interface CommandExecutor () {
    AcDocManagerPtrFn _acDocManagerPtr;
    StaticCurDocumentFn _staticCurDocument;
    SendStringToExecuteFn _sendStringToExecute;
    AcedPostCommandFn _acedPostCommand;
    BOOL _searchedSymbols;
}
@end

@implementation CommandExecutor

+ (instancetype)sharedInstance {
    static CommandExecutor *s_instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        s_instance = [[CommandExecutor alloc] init];
    });
    return s_instance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _acDocManagerPtr = nullptr;
        _staticCurDocument = nullptr;
        _sendStringToExecute = nullptr;
        _acedPostCommand = nullptr;
        _searchedSymbols = NO;
        [self resolveSymbols];
    }
    return self;
}

- (void)resolveSymbols {
    if (_searchedSymbols) return;
    _searchedSymbols = YES;

    // 1. Resolve Document Manager functions for sendStringToExecute
    _acDocManagerPtr = (AcDocManagerPtrFn)dlsym(RTLD_DEFAULT, "_Z15acDocManagerPtrv");
    _staticCurDocument = (StaticCurDocumentFn)dlsym(RTLD_DEFAULT, "_ZN17AcApDocImpManager17staticCurDocumentEv");
    _sendStringToExecute = (SendStringToExecuteFn)dlsym(RTLD_DEFAULT, "_ZN17AcApDocImpManager19sendStringToExecuteEP12AcApDocumentPKwbbb");

    // 2. Resolve acedPostCommand
    _acedPostCommand = (AcedPostCommandFn)dlsym(RTLD_DEFAULT, "_Z15acedPostCommandPKw");
    if (!_acedPostCommand) {
        _acedPostCommand = (AcedPostCommandFn)dlsym(RTLD_DEFAULT, "acedPostCommand");
    }

    LogMacRibbon(@"Symbol resolution: acDocManagerPtr=%p, curDoc=%p, sendStringToExecute=%p, acedPostCommand=%p",
                 _acDocManagerPtr, _staticCurDocument, _sendStringToExecute, _acedPostCommand);
}

- (BOOL)isNativeEngineAvailable {
    if (!_searchedSymbols) {
        [self resolveSymbols];
    }
    return (_sendStringToExecute != nullptr || _acedPostCommand != nullptr);
}

- (void)executeCommand:(NSString *)commandString {
    if (!commandString || commandString.length == 0) return;

    if (!_searchedSymbols) {
        [self resolveSymbols];
    }

    // Sanitize macro syntax:
    // Strip ^C^C (Cancel macro in CUI files) and replace with clean command
    NSString *cleanCmd = commandString;
    BOOL cancelActive = NO;
    if ([cleanCmd hasPrefix:@"^C^C"]) {
        cancelActive = YES;
        cleanCmd = [cleanCmd substringFromIndex:4];
    } else if ([cleanCmd hasPrefix:@"^C"]) {
        cancelActive = YES;
        cleanCmd = [cleanCmd substringFromIndex:2];
    }

    // Build the execution string
    NSMutableString *execStr = [NSMutableString string];
    if (cancelActive) {
        // ASCII 27 (ESC) cancels active commands in AutoCAD
        [execStr appendString:@"\x1b\x1b"];
    }
    [execStr appendString:cleanCmd];

    // Ensure it terminates with space or newline
    if (![execStr hasSuffix:@"\n"] && ![execStr hasSuffix:@" "]) {
        [execStr appendString:@"\n"];
    }

    LogMacRibbon(@"Executing CAD command: '%@' (raw: '%@')", cleanCmd, [execStr stringByReplacingOccurrencesOfString:@"\n" withString:@"\\n"]);

    // Convert to wide character string for AutoCAD (wchar_t is UTF-32 on macOS)
    NSUInteger len = [execStr length];
    unichar *buffer = new unichar[len];
    [execStr getCharacters:buffer range:NSMakeRange(0, len)];
    std::wstring wideCmd;
    wideCmd.reserve(len);
    for (NSUInteger i = 0; i < len; ++i) {
        wideCmd.push_back((wchar_t)buffer[i]);
    }
    delete[] buffer;

    // Strategy 1: Canonical sendStringToExecute via AcApDocManager
    if (_sendStringToExecute && _acDocManagerPtr) {
        void *pMgr = _acDocManagerPtr();
        void *pDoc = _staticCurDocument ? _staticCurDocument() : nullptr;
        if (pMgr) {
            int ret = _sendStringToExecute(pMgr, pDoc, wideCmd.c_str(), true, false, true);
            LogMacRibbon(@"sendStringToExecute called with result: %d", ret);
            if (ret == 0) {
                return;
            }
        }
    }

    // Strategy 2: acedPostCommand direct dispatch
    if (_acedPostCommand) {
        int ret = _acedPostCommand(wideCmd.c_str());
        LogMacRibbon(@"acedPostCommand dispatched with result: %d", ret);
        if (ret == 0) {
            return;
        }
    }

    LogMacRibbon(@"Warning: Command dispatch completed without 0 return code");
}

@end
