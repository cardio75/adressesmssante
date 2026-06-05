#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

APP_NAME="Adresses MSSante"
APP_PATH="dist/$APP_NAME.app"
DMG_PATH="dist/Adresses-MSSante-macOS-arm64.dmg"
STAGING_DIR="dist/dmg-staging"

if [ ! -d "$APP_PATH" ]; then
    echo "$APP_PATH est introuvable."
    echo "Lancez d'abord ./packaging/build_macos.sh"
    exit 1
fi

rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

cp -R "$APP_PATH" "$STAGING_DIR/"
ln -s /Applications "$STAGING_DIR/Applications"

rm -f "$DMG_PATH"
hdiutil create \
    -volname "$APP_NAME" \
    -srcfolder "$STAGING_DIR" \
    -ov \
    -format UDZO \
    "$DMG_PATH"

rm -rf "$STAGING_DIR"

echo ""
echo "DMG cree:"
echo "$DMG_PATH"
