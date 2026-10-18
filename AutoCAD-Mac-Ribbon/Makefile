CC = clang++
CFLAGS = -O2 -std=c++17 -fobjc-arc -arch arm64 -arch x86_64 -bundle -undefined dynamic_lookup
DYLIB_FLAGS = -O2 -std=c++17 -fobjc-arc -arch arm64 -arch x86_64 -dynamiclib -undefined dynamic_lookup
FRAMEWORKS = -framework Cocoa -framework WebKit -framework Foundation -framework AppKit

SRC = src/main.mm src/CommandExecutor.mm src/RibbonViewController.mm src/RibbonManager.mm
BUILD_DIR = build
PKG_NAME = MacRibbon.bundle
PKG_DIR = $(BUILD_DIR)/$(PKG_NAME)
INNER_BUNDLE = $(PKG_DIR)/Contents/MacOS/MacRibbon.bundle

DEST_ADDINS = $(HOME)/Library/Application Support/Autodesk/ApplicationAddins/$(PKG_NAME)
DEST_PLUGINS = $(HOME)/Library/Application Support/Autodesk/ApplicationPlugins/$(PKG_NAME)

all: $(PKG_DIR)

$(PKG_DIR): $(SRC) ui/style.css ui/ribbon.js scripts/generate_ribbon.py
	@mkdir -p $(PKG_DIR)/Contents/MacOS
	@mkdir -p $(INNER_BUNDLE)/Contents/MacOS
	@mkdir -p $(PKG_DIR)/Contents/Resources
	@echo "Generating full 7-tab Windows Ribbon HTML..."
	@python3 scripts/generate_ribbon.py
	@echo "Bundling self-contained HTML assets..."
	@python3 scripts/bundle_html.py
	@echo "Compiling Universal Binary (arm64 + x86_64) bundle..."
	$(CC) $(CFLAGS) $(FRAMEWORKS) $(SRC) -o $(INNER_BUNDLE)/Contents/MacOS/MacRibbon
	@cp $(INNER_BUNDLE)/Contents/MacOS/MacRibbon $(PKG_DIR)/Contents/MacOS/MacRibbon
	@echo "Compiling Universal Binary dylib fallback..."
	$(CC) $(DYLIB_FLAGS) $(FRAMEWORKS) $(SRC) -o $(PKG_DIR)/Contents/MacOS/MacRibbon.dylib
	@echo "Copying Info.plist..."
	@cp Info.plist $(INNER_BUNDLE)/Contents/
	@cp Info.plist $(PKG_DIR)/Contents/
	@echo "Ad-hoc signing binaries..."
	@codesign -s - --force $(PKG_DIR)/Contents/MacOS/MacRibbon.dylib
	@codesign -s - --force $(INNER_BUNDLE)
	@codesign -s - --force $(PKG_DIR)/Contents/MacOS/MacRibbon
	@echo "Copying manifests and resources..."
	@cp PackageContents.xml $(PKG_DIR)/
	@cp ui/index.html $(PKG_DIR)/Contents/Resources/
	@cp ui/style.css $(PKG_DIR)/Contents/Resources/
	@cp ui/ribbon.js $(PKG_DIR)/Contents/Resources/
	@cp ui/macribbon.lsp $(PKG_DIR)/Contents/Resources/
	@echo "Build complete at $(PKG_DIR)"
	@lipo -info $(INNER_BUNDLE)/Contents/MacOS/MacRibbon

install: all
	@echo "Installing to ApplicationAddins & ApplicationPlugins..."
	@mkdir -p "$(HOME)/Library/Application Support/Autodesk/ApplicationAddins"
	@mkdir -p "$(HOME)/Library/Application Support/Autodesk/ApplicationPlugins"
	@rm -rf "$(DEST_ADDINS)"
	@rm -rf "$(DEST_PLUGINS)"
	@cp -R $(PKG_DIR) "$(DEST_ADDINS)"
	@cp -R $(PKG_DIR) "$(DEST_PLUGINS)"
	@echo "Installed to:"
	@echo "  1) $(DEST_ADDINS)"
	@echo "  2) $(DEST_PLUGINS)"
	@python3 scripts/setup_acad_lsp.py

uninstall:
	@rm -rf "$(DEST_ADDINS)"
	@rm -rf "$(DEST_PLUGINS)"
	@echo "Uninstalled from both locations."

clean:
	@rm -rf $(BUILD_DIR)
	@echo "Cleaned build directory."

.PHONY: all install uninstall clean
