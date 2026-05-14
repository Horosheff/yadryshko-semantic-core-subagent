param(
  [string]$Target = $env:YADRYSHKO_TARGET
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if ([string]::IsNullOrWhiteSpace($Target)) {
  $Target = (Get-Location).Path
}

$Repo = "Horosheff/yadryshko-semantic-core-subagent"
$Branch = "main"
$ZipUrl = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"
$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("yadryshko-" + [System.Guid]::NewGuid().ToString("N"))
$ZipPath = Join-Path $TempRoot "repo.zip"
$ExtractPath = Join-Path $TempRoot "src"

New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
New-Item -ItemType Directory -Force -Path $ExtractPath | Out-Null

try {
  Write-Host "Downloading YADryshko Core from $ZipUrl"
  Invoke-WebRequest -Uri $ZipUrl -OutFile $ZipPath

  Expand-Archive -Path $ZipPath -DestinationPath $ExtractPath -Force
  $Source = Get-ChildItem -Path $ExtractPath -Directory | Select-Object -First 1
  if (-not $Source) {
    throw "Archive extraction failed: source folder not found"
  }

  New-Item -ItemType Directory -Force -Path (Join-Path $Target ".cursor\agents") | Out-Null
  New-Item -ItemType Directory -Force -Path (Join-Path $Target "docs") | Out-Null
  New-Item -ItemType Directory -Force -Path (Join-Path $Target "scripts") | Out-Null
  New-Item -ItemType Directory -Force -Path (Join-Path $Target "templates") | Out-Null

  Copy-Item -Force (Join-Path $Source.FullName ".cursor\agents\core.md") (Join-Path $Target ".cursor\agents\core.md")
  Copy-Item -Force (Join-Path $Source.FullName "docs\*.md") (Join-Path $Target "docs")
  Copy-Item -Force (Join-Path $Source.FullName "scripts\build_core_html_report.py") (Join-Path $Target "scripts")
  Copy-Item -Force (Join-Path $Source.FullName "scripts\build_semantic_core_xlsx.py") (Join-Path $Target "scripts")
  Copy-Item -Force (Join-Path $Source.FullName "templates\*.md") (Join-Path $Target "templates")

  Write-Host ""
  Write-Host "YADryshko Core installed into: $Target"
  Write-Host "Restart Cursor or reload the window if /core is not visible immediately."
  Write-Host "Run example:"
  Write-Host "/core https://example.ru region Russia, goal leads"
  Write-Host ""
  Write-Host "Wordstat setup guide:"
  Write-Host "https://mcp-kv.ru/docs/wordstat-mcp-setup"
}
finally {
  if (Test-Path $TempRoot) {
    Remove-Item -Recurse -Force $TempRoot
  }
}
