#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-${YADRYSHKO_TARGET:-$(pwd)}}"
REPO="Horosheff/yadryshko-semantic-core-subagent"
BRANCH="main"
ZIP_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.zip"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "Downloading YADryshko Core from ${ZIP_URL}"

if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$ZIP_URL" -o "$TMP_DIR/repo.zip"
elif command -v wget >/dev/null 2>&1; then
  wget -q "$ZIP_URL" -O "$TMP_DIR/repo.zip"
else
  echo "Error: curl or wget is required"
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  echo "Error: unzip is required"
  exit 1
fi

unzip -q "$TMP_DIR/repo.zip" -d "$TMP_DIR/src"
SOURCE="$(find "$TMP_DIR/src" -maxdepth 1 -type d -name "*${BRANCH}" | head -n 1)"

if [ -z "$SOURCE" ]; then
  SOURCE="$(find "$TMP_DIR/src" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
fi

if [ -z "$SOURCE" ]; then
  echo "Error: archive extraction failed"
  exit 1
fi

mkdir -p "$TARGET/.cursor/agents" "$TARGET/docs" "$TARGET/scripts" "$TARGET/templates"

cp "$SOURCE/.cursor/agents/core.md" "$TARGET/.cursor/agents/core.md"
cp "$SOURCE"/docs/*.md "$TARGET/docs/"
cp "$SOURCE/scripts/build_core_html_report.py" "$TARGET/scripts/"
cp "$SOURCE/scripts/build_semantic_core_xlsx.py" "$TARGET/scripts/"
cp "$SOURCE"/templates/*.md "$TARGET/templates/"

echo ""
echo "YADryshko Core installed into: $TARGET"
echo "Restart Cursor or reload the window if /core is not visible immediately."
echo "Run example:"
echo "/core https://example.ru регион Россия, цель заявки"
echo ""
echo "Wordstat setup guide:"
echo "https://mcp-kv.ru/docs/wordstat-mcp-setup"
