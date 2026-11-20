#import "CommandExecutor.h"
#import <Cocoa/Cocoa.h>
#import <dlfcn.h>
#import <objc/message.h>
#import <string>

extern void LogMacRibbon(NSString *fmt, ...);

typedef void* (*AcDocManagerPtrFn)();
typedef void* (*StaticCurDocumentFn)();
typedef int (*SendStringToExecuteFn)(void* pMgr, void* pDoc, const wchar_t* pszCmd, bool bActivate, bool bWrapUpInactiveDoc, bool bEchoString);
typedef int (*AcedPostCommandFn)(const wchar_t *);
typedef void* (*GetActiveCmdThroatFn)();
typedef bool (*SendMenuStringToExecuteFn)(void* pThroat, const wchar_t* pszCmd, bool bEcho, bool bWrapUp);
typedef void* (*AcadGetMainAppFn)();
typedef void* (*GetAppServicesFn)(void* pMainApp);
typedef void (*NewDocumentFn)(void* pAppServices);
typedef void (*NewDocumentQuickFn)(void* pAppServices, bool bFlag);
typedef void (*OpenDocFn)();

@interface CommandExecutor () {
    AcDocManagerPtrFn _acDocManagerPtr;
    StaticCurDocumentFn _staticCurDocument;
    SendStringToExecuteFn _sendStringToExecute;
    AcedPostCommandFn _acedPostCommand;
    GetActiveCmdThroatFn _getActiveCmdThroat;
    SendMenuStringToExecuteFn _sendMenuStringToExecute;
    AcadGetMainAppFn _acadGetMainApp;
    GetAppServicesFn _getAppServices;
    NewDocumentFn _newDocument;
    NewDocumentQuickFn _newDocumentQuick;
    OpenDocFn _openDoc;
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
        _getActiveCmdThroat = nullptr;
        _sendMenuStringToExecute = nullptr;
        _acadGetMainApp = nullptr;
        _getAppServices = nullptr;
        _newDocument = nullptr;
        _newDocumentQuick = nullptr;
        _openDoc = nullptr;
        _searchedSymbols = NO;
        [self resolveSymbols];
    }
    return self;
}

- (void)resolveSymbols {
    if (_searchedSymbols) return;
    _searchedSymbols = YES;

    // 1. Resolve CUI Menu Macro Throat (supports ^C^C, \ pauses, ; enters, $M= DIESEL)
    _getActiveCmdThroat = (GetActiveCmdThroatFn)dlsym(RTLD_DEFAULT, "_Z18GetActiveCmdThroatv");
    _sendMenuStringToExecute = (SendMenuStringToExecuteFn)dlsym(RTLD_DEFAULT, "_ZN10CCmdThroat23sendMenuStringToExecuteEPKwbb");

    // 2. Resolve AppServices for zero-document (+ Start tab) New / Open actions
    _acadGetMainApp = (AcadGetMainAppFn)dlsym(RTLD_DEFAULT, "_Z14AcadGetMainAppv");
    _getAppServices = (GetAppServicesFn)dlsym(RTLD_DEFAULT, "_ZN9AcMainApp14getAppServicesEv");
    _newDocument = (NewDocumentFn)dlsym(RTLD_DEFAULT, "_ZN15AcOCAppServices11newDocumentEv");
    _newDocumentQuick = (NewDocumentQuickFn)dlsym(RTLD_DEFAULT, "_ZN15AcOCAppServices16newDocumentQuickEb");
    _openDoc = (OpenDocFn)dlsym(RTLD_DEFAULT, "_Z7openDocv");

    // 3. Resolve Document Manager functions for sendStringToExecute
    _acDocManagerPtr = (AcDocManagerPtrFn)dlsym(RTLD_DEFAULT, "_Z15acDocManagerPtrv");
    _staticCurDocument = (StaticCurDocumentFn)dlsym(RTLD_DEFAULT, "_ZN17AcApDocImpManager17staticCurDocumentEv");
    _sendStringToExecute = (SendStringToExecuteFn)dlsym(RTLD_DEFAULT, "_ZN17AcApDocImpManager19sendStringToExecuteEP12AcApDocumentPKwbbb");

    // 4. Resolve acedPostCommand
    _acedPostCommand = (AcedPostCommandFn)dlsym(RTLD_DEFAULT, "_Z15acedPostCommandPKw");
    if (!_acedPostCommand) {
        _acedPostCommand = (AcedPostCommandFn)dlsym(RTLD_DEFAULT, "acedPostCommand");
    }

    LogMacRibbon(@"Symbol resolution: cmdThroat=%p, sendMenuStr=%p, acDocManagerPtr=%p, curDoc=%p, sendStringToExecute=%p, acedPostCommand=%p",
                 _getActiveCmdThroat, _sendMenuStringToExecute, _acDocManagerPtr, _staticCurDocument, _sendStringToExecute, _acedPostCommand);
}

- (BOOL)isNativeEngineAvailable {
    if (!_searchedSymbols) {
        [self resolveSymbols];
    }
    return (_sendMenuStringToExecute != nullptr || _sendStringToExecute != nullptr || _acedPostCommand != nullptr);
}

+ (std::wstring)wideStringFromNSString:(NSString *)str {
    if (!str || str.length == 0) return std::wstring();
    NSData *data = [str dataUsingEncoding:NSUTF32LittleEndianStringEncoding];
    if (!data) return std::wstring();
    const wchar_t *wptr = (const wchar_t *)[data bytes];
    size_t count = [data length] / sizeof(wchar_t);
    return std::wstring(wptr, count);
}

- (void)restoreCanvasFocus {
    dispatch_async(dispatch_get_main_queue(), ^{
        NSWindow *win = [NSApp mainWindow];
        if (win && ![win isKeyWindow]) {
            [win makeKeyAndOrderFront:nil];
        }
    });
}

- (void)executeCommand:(NSString *)commandString {
    if (!commandString || commandString.length == 0) return;

    if (!_searchedSymbols) {
        [self resolveSymbols];
    }

    // Check active document pointer
    void *pDoc = _staticCurDocument ? _staticCurDocument() : nullptr;

    // Handle zero-document state (e.g. when on the "+ Start" tab with no drawing open)
    if (!pDoc) {
        NSString *upper = [commandString uppercaseString];
        if ([upper containsString:@"_QNEW"]) {
            LogMacRibbon(@"Zero-document state: invoking newDocumentQuick");
            if (_acadGetMainApp && _getAppServices && _newDocumentQuick) {
                void *mainApp = _acadGetMainApp();
                void *appServices = mainApp ? _getAppServices(mainApp) : nullptr;
                if (appServices) {
                    _newDocumentQuick(appServices, false);
                    [self restoreCanvasFocus];
                    return;
                }
            }
        } else if ([upper containsString:@"_NEW"]) {
            LogMacRibbon(@"Zero-document state: invoking newDocument");
            if (_acadGetMainApp && _getAppServices && _newDocument) {
                void *mainApp = _acadGetMainApp();
                void *appServices = mainApp ? _getAppServices(mainApp) : nullptr;
                if (appServices) {
                    _newDocument(appServices);
                    [self restoreCanvasFocus];
                    return;
                }
            }
        } else if ([upper containsString:@"_OPEN"]) {
            LogMacRibbon(@"Zero-document state: invoking openDoc");
            if (_openDoc) {
                _openDoc();
                [self restoreCanvasFocus];
                return;
            }
        }
    }

    // Strategy 1: Native CUI Menu Macro Throat (CCmdThroat::sendMenuStringToExecute)
    // Properly interprets ^C^C, \ (pause for user point pick), ; (Enter), and $M= (DIESEL)
    if (pDoc && _getActiveCmdThroat && _sendMenuStringToExecute) {
        void *pThroat = _getActiveCmdThroat();
        if (pThroat) {
            NSMutableString *macroStr = [NSMutableString stringWithString:commandString];
            // CUI macros that do not end with space, semicolon, backslash (user pause), or newline
            // require a trailing space to act as Enter in CCmdThroat.
            if (![macroStr hasSuffix:@" "] &&
                ![macroStr hasSuffix:@";"] &&
                ![macroStr hasSuffix:@"\\"] &&
                ![macroStr hasSuffix:@"\n"] &&
                ![macroStr hasPrefix:@"$M="]) {
                [macroStr appendString:@" "];
            }
            std::wstring wideMacro = [CommandExecutor wideStringFromNSString:macroStr];
            bool ok = _sendMenuStringToExecute(pThroat, wideMacro.c_str(), true, false);
            LogMacRibbon(@"CCmdThroat::sendMenuStringToExecute('%@') -> %d", macroStr, (int)ok);
            if (ok) {
                [self restoreCanvasFocus];
                return;
            }
        }
    }

    // Strategy 2: +[AcOCEditorUtils sendCommandStringToExecute:] Objective-C bridge
    Class editorUtilsCls = NSClassFromString(@"AcOCEditorUtils");
    SEL sendCmdSel = NSSelectorFromString(@"sendCommandStringToExecute:");
    if (pDoc && editorUtilsCls && [editorUtilsCls respondsToSelector:sendCmdSel]) {
        NSMutableString *macroStr = [NSMutableString stringWithString:commandString];
        if (![macroStr hasSuffix:@" "] && ![macroStr hasSuffix:@";"] && ![macroStr hasSuffix:@"\\"] && ![macroStr hasSuffix:@"\n"]) {
            [macroStr appendString:@" "];
        }
        BOOL ok = ((BOOL (*)(id, SEL, NSString *))objc_msgSend)(editorUtilsCls, sendCmdSel, macroStr);
        LogMacRibbon(@"AcOCEditorUtils sendCommandStringToExecute('%@') -> %d", macroStr, (int)ok);
        if (ok) {
            [self restoreCanvasFocus];
            return;
        }
    }

    // Fallback: Sanitize macro syntax for raw sendStringToExecute / acedPostCommand
    NSString *cleanCmd = commandString;
    BOOL cancelActive = NO;
    if ([cleanCmd hasPrefix:@"^C^C"]) {
        cancelActive = YES;
        cleanCmd = [cleanCmd substringFromIndex:4];
    } else if ([cleanCmd hasPrefix:@"^C"]) {
        cancelActive = YES;
        cleanCmd = [cleanCmd substringFromIndex:2];
    }
    // Replace CUI ';' with newline and strip CUI '\' pause tokens for raw fallback
    cleanCmd = [cleanCmd stringByReplacingOccurrencesOfString:@";" withString:@"\n"];
    cleanCmd = [cleanCmd stringByReplacingOccurrencesOfString:@"\\" withString:@""];

    NSMutableString *execStr = [NSMutableString string];
    if (cancelActive) {
        [execStr appendString:@"\x1b\x1b"];
    }
    [execStr appendString:cleanCmd];
    if (![execStr hasSuffix:@"\n"] && ![execStr hasSuffix:@" "]) {
        [execStr appendString:@"\n"];
    }

    LogMacRibbon(@"Fallback executing CAD command: '%@'", [execStr stringByReplacingOccurrencesOfString:@"\n" withString:@"\\n"]);
    std::wstring wideCmd = [CommandExecutor wideStringFromNSString:execStr];

    // Strategy 3: Canonical sendStringToExecute via AcApDocManager
    if (_sendStringToExecute && _acDocManagerPtr) {
        void *pMgr = _acDocManagerPtr();
        if (pMgr && pDoc) {
            int ret = _sendStringToExecute(pMgr, pDoc, wideCmd.c_str(), true, false, true);
            LogMacRibbon(@"sendStringToExecute called with result: %d", ret);
            if (ret == 0) {
                [self restoreCanvasFocus];
                return;
            }
        }
    }

    // Strategy 4: acedPostCommand direct dispatch
    if (_acedPostCommand && pDoc) {
        int ret = _acedPostCommand(wideCmd.c_str());
        LogMacRibbon(@"acedPostCommand dispatched with result: %d", ret);
        if (ret == 0) {
            [self restoreCanvasFocus];
            return;
        }
    }

    LogMacRibbon(@"Warning: Command dispatch completed without success");
}

@end
