param(
  [Parameter(Mandatory=$true)]
  [string]$Target
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Target)) {
  New-Item -ItemType Directory -Path $Target | Out-Null
}

$Root = Split-Path -Parent $PSScriptRoot

New-Item -ItemType Directory -Force -Path (Join-Path $Target ".cursor\agents") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Target "docs") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Target "scripts") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Target "templates") | Out-Null

Copy-Item -Force (Join-Path $Root ".cursor\agents\core.md") (Join-Path $Target ".cursor\agents\core.md")
Copy-Item -Force (Join-Path $Root "docs\*.md") (Join-Path $Target "docs")
Copy-Item -Force (Join-Path $Root "scripts\build_core_html_report.py") (Join-Path $Target "scripts")
Copy-Item -Force (Join-Path $Root "scripts\build_semantic_core_xlsx.py") (Join-Path $Target "scripts")
Copy-Item -Force (Join-Path $Root "templates\*.md") (Join-Path $Target "templates")

Write-Host "Core installed into $Target"
Write-Host "Use in Cursor: /core https://example.ru регион Россия, цель заявки"
