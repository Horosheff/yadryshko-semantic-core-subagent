#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: ./scripts/install.sh /path/to/target/project"
  exit 1
fi

TARGET="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET/.cursor/agents" "$TARGET/docs" "$TARGET/scripts" "$TARGET/templates"

cp "$ROOT/.cursor/agents/core.md" "$TARGET/.cursor/agents/core.md"
cp "$ROOT"/docs/*.md "$TARGET/docs/"
cp "$ROOT/scripts/build_core_html_report.py" "$TARGET/scripts/"
cp "$ROOT/scripts/build_semantic_core_xlsx.py" "$TARGET/scripts/"
cp "$ROOT"/templates/*.md "$TARGET/templates/"

echo "Core installed into $TARGET"
echo "Use in Cursor: /core https://example.ru регион Россия, цель заявки"
